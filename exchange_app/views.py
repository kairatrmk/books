from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics
from .serializers import UserSerializer, BookSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.views import obtain_auth_token
from .models import Book

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]






class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



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