from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers

from .models import *
from .serializers import BookSerializer, BookExchangeSerializer, BookAllSerializer, ExchangeCreateSerializer
from users.models import CustomUser


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
    search_fields = ['author', 'title', 'genre__name']


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]  # Добавляем проверку аутентификации

    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            request.user.favorite_books.add(book)
            return Response({'message': 'Книга добавлена в избранное'}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'message': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)


class FavoriteBooksListView(ListAPIView):
    serializer_class = BookAllSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.favorite_books.all()


class RemoveFromFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Удаление книги из избранного",
        responses={
            204: 'Book removed from favorites',
            404: 'Book not found'
        }
    )
    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            request.user.favorite_books.remove(book)
            return Response({'message': 'Книга удалена из избранного'}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({'message': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)


class ExchangeCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user_sender'] = request.user.id  # Set the authenticated user as the sender

        serializer = ExchangeCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)