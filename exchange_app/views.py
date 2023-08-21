from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers

from .models import *
from .serializers import BookSerializer, BookAllSerializer, ExchangeCreateSerializer, \
    ExchangeRatingSerializer, ExchangeSerializer, GenreSerializer
from users.serializers import RatingSerializer


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


@swagger_auto_schema(request_body=GenreSerializer)
class GenreListView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@swagger_auto_schema(request_body=GenreSerializer)
class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # You can customize the response data here if needed
        response_data = {
            'message': 'List of all books retrieved successfully',
            'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # You can customize the response data here if needed
        response_data = {
            'message': 'Book created successfully',
            'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserBookListView(generics.ListAPIView):
    serializer_class = BookAllSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']  # Получаем user_id из URL
        return Book.objects.filter(user_id=user_id)


class BookListView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['author', 'title', 'genre__name']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # You can customize the response data here if needed
        response_data = {
            'message': 'Book details retrieved successfully',
            'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


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


class BookGenreListView(ListAPIView):
    serializer_class = BookAllSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 12
    pagination_class.page_query_param = 'page'
    pagination_class.page_size_query_param = 'page_size'

    def get_queryset(self):
        genre_id = self.kwargs['genre_id']
        return Book.objects.filter(genre_id=genre_id)

from rest_framework.pagination import PageNumberPagination

class BooksByGenreView(APIView):
    def get(self, request, genre):
        books = Book.objects.filter(genre=genre)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class ExchangeCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user_sender'] = request.user.id  # Set the authenticated user as the sender

        serializer = ExchangeCreateSerializer(data=data)
        if serializer.is_valid():
            exchange = serializer.save()

            # Set initial status when creating the exchange
            initial_status = Status.objects.get(name="Request sent")
            exchange.status = initial_status
            exchange.save()

            # Send email to user_receiver
            user_receiver = exchange.user_receiver  # Adjust this according to your serializer fields
            subject = 'Exchange Offer Received'
            message = f'Hello {user_receiver.username}, you have received an exchange offer.'
            from_email = 'exchange.innovat@example.com'  # Set your sender email address
            recipient_list = [user_receiver.email]

            send_mail(subject, message, from_email, recipient_list)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        exchange_id = request.data.get('exchange_id')  # Assuming you send the exchange ID in the request data
        status_completed = Status.objects.get(name="Exchange completed")

        try:
            exchange = Exchange.objects.get(id=exchange_id)

            if exchange.status == status_completed:
                serializer = ExchangeRatingSerializer(instance=exchange, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Ratings updated successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                exchange.status = status_completed
                exchange.save()
                return Response({"message": "Exchange status changed to 'Exchange completed'."},
                                status=status.HTTP_200_OK)

        except Exchange.DoesNotExist:
            return Response({"error": "Exchange not found."}, status=status.HTTP_404_NOT_FOUND)


class ExchangeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.status == 'Запрос принят':
            self.send_notification(instance.sender.email, "Ваш запрос на обмен был принят.")

        if instance.status == 'Детали обмена согласованы':
            self.send_notification(instance.sender.email, "Детали обмена были успешно согласованы.")
            self.send_notification(instance.receiver.email, "Детали обмена были успешно согласованы.")

        if instance.status == 'Отклонен':
            self.send_notification(instance.receiver.email, "Отклонен")
            self.send_notification(instance.sender.email, "Отклонен")

        if instance.status == 'Отменен':
            self.send_notification(instance.sender.email, "Отменен")
            self.send_notification(instance.receiver.email, "Отменен")

        if instance.status == 'Обмен завершен':
            # Создайте объект рейтинга и свяжите его с запросом на обмен
            rating_data = {
                'from_user': instance.sender,
                'to_user': instance.receiver,
                'rating': 5,  # Здесь вы можете использовать любую оценку, которую хотите
                'exchange_request': instance,
            }
            rating_serializer = RatingSerializer(data=rating_data)
            if rating_serializer.is_valid():
                rating_serializer.save()
                self.send_notification(instance.sender.email,
                                       "Обмен книгами успешно завершен. Не забудьте оставить рейтинг пользователю")
                self.send_notification(instance.receiver.email,
                                       "Обмен книгами успешно завершен. Не забудьте оставить рейтинг пользователю")
            else:
                return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_notification(self, recipient_email, message):
        subject = 'Уведомление о запросе на обмен'
        from_email = 'mybook.innovat@gmail.com'
        recipient_list = [recipient_email]
        send_mail(subject, message, from_email, recipient_list)


class ExchangeListView(ListAPIView):
    serializer_class = ExchangeSerializer

    def get_queryset(self):
        user = self.request.user
        return Exchange.objects.filter(sender=user) | Exchange.objects.filter(receiver=user)
