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
    path('api/books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('api/books/search/', BookListView.as_view(), name='search-books'),



    path('api/books/favorite/<int:book_id>/', views.AddToFavoriteView.as_view(), name='add-to-favorite'),
    path('api/books/favorite/', views.FavoriteBooksListView.as_view(), name='favorite-books-list'),
    path('api/books/favorite/remove/<int:book_id>/', views.RemoveFromFavoriteView.as_view(),


         name='remove-from-favorite'),

    path('exchange/', views.ExchangeListView.as_view(), name='exchange-request-list'),
    path('exchange/create/', ExchangeCreateView.as_view(), name='exchange-create'),
    path('api/exchange-requests/<int:pk>/', views.ExchangeDetailView.as_view(), name='exchange-request-detail'),

    path('swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-re2doc'),
]
