from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from exchange_app.views import *
from exchange_app import views
from swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('users.urls')),

    # path('api/login/', views.custom_login, name='api-login'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Эндпоинт для обновления токена доступа
    # path('api/books/', views.BookListCreateView.as_view(), name='book-list-create'),
    # path('api/books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('api/book_exchanges/', BookExchangeListCreateView.as_view(), name='book-exchange-create'),
    path('api/book_exchanges/<int:pk>/', BookExchangeDetailView.as_view(), name='book-exchange-detail'),
    path('api/books/search/', BookListView.as_view(), name='search-books'),

    path('swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
