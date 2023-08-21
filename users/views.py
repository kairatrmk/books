from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.views import APIView
from drf_yasg import openapi
from users.serializers import *
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from django.contrib.auth import login
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


from rest_framework import generics
from .models import *
from exchange_app.models import Exchange



class RegisterApiView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вы успешно зарегестрировались! Вам отправлено сообщение на почту.', status=201)


User = get_user_model()


class ActivationApiView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'успешно'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'msg': 'неверный код'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # Этот шаг авторизует пользователя на сервере

            response_data = serializer.create(serializer.validated_data)  # Получаем токены

            return Response(response_data, status=status.HTTP_200_OK)  # Отправляем токены в ответе
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'

    @swagger_auto_schema(request_body=UserProfileSerializer)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data.get('access')
            return Response({'access_token': str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ссылка для сброса пароля отправлена на ваш email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
                'uidb64': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['token', 'uidb64', 'new_password']
        ),
        responses={status.HTTP_200_OK: 'Success', status.HTTP_400_BAD_REQUEST: 'Bad Request'}
    )
    def post(self, request):
        token = request.data.get('token')
        uidb64 = request.data.get('uidb64')
        new_password = request.data.get('new_password')

        if token and uidb64 and new_password:
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Пароль успешно изменен.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': 'Пользователь не найден.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Необходимо предоставить токен, uidb64 и новый пароль.'},
                            status=status.HTTP_400_BAD_REQUEST)


class RatingCreateView(APIView):
    def post(self, request, *args, **kwargs):
        exchange_request_id = request.data.get("exchange_request")
        try:
            exchange_request = Exchange.objects.get(pk=exchange_request_id)
        except Exchange.DoesNotExist:
            return Response({"detail": "Запрос на обмен не найден"}, status=status.HTTP_400_BAD_REQUEST)

        if exchange_request.status != 'Обмен завершен':
            return Response({"detail": "Рейтинг можно выставлять только после успешного завершения обмена"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.request.user.id == self.kwargs['pk']:
            return CustomUserProfileSerializer  # Используйте CustomUserProfileSerializer для текущего пользователя
        return CustomAnotherUserSerializer  # Используйте CustomUserDetailSerializer для других пользователей

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = self.kwargs['pk']
        queryset = queryset.annotate(average_rating=Avg('received_ratings__rating'))
        obj = queryset.get(id=user_id)
        return obj


class UserRatingView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        received_ratings = user.received_ratings.all()

        if received_ratings.exists():
            average_rating = received_ratings.aggregate(Avg('rating'))['rating__avg']
        else:
            average_rating = 0.0

        return Response({"average_rating": average_rating})


@swagger_auto_schema(request_body=CitySerializer)
class CityListView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer