from django.contrib.auth.models import User

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .serializers import UserSerializer, BookSerializer, BookExchangeSerializer
from .models import *


# class BookListCreateView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user (unauthenticated users) to access this view
def custom_obtain_token(request):
    # Your custom logic to obtain the token, if needed
    # For example, you can perform additional checks or validations here
    token_obtain_view = TokenObtainPairView.as_view()
    return token_obtain_view(request)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user (unauthenticated users) to access this view
def custom_refresh_token(request):
    # Your custom logic to refresh the token, if needed
    # For example, you can perform additional checks or validations here
    token_refresh_view = TokenRefreshView.as_view()
    return token_refresh_view(request)


@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    # Вручную передаем request в сериализатор, чтобы избежать ошибки
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    # Ваша дополнительная логика для обработки успешного входа пользователя, если нужно
    return Response({
        'user_id': user.pk,
        'email': user.email,
        'access_token': serializer.validated_data['access'],
    })


class CustomTokenObtainPairView(TokenObtainPairView):
    @permission_classes([AllowAny])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Customize the response data if needed
            data = {
                'access_token': response.data['access'],
                'refresh_token': response.data['refresh'],
            }
            return Response(data, status=status.HTTP_200_OK)
        return response


class BookExchangeListCreateView(ListCreateAPIView):
    serializer_class = BookExchangeSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Exchange.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class BookExchangeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Exchange.objects.all()
    serializer_class = BookExchangeSerializer


class BookListView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['author', 'title', 'genr__name']

