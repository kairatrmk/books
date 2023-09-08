from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
    path('api/books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('api/books/search/', BookListView.as_view(), name='search-books'),
    path('api/books/user/<int:user_id>/', views.UserBookListView.as_view(), name='user-book-list'),

    path('api/genres/', views.GenreListView.as_view(), name='genre-list'),
    path('api/genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),

    path('api/books/favorite/<int:book_id>/', views.AddToFavoriteView.as_view(), name='add-to-favorite'),
    path('api/books/favorite/', views.FavoriteBooksListView.as_view(), name='favorite-books-list'),
    path('api/books/favorite/remove/<int:book_id>/', views.RemoveFromFavoriteView.as_view(),
         name='remove-from-favorite'),

    path('api/books/genre/<int:genre_id>/', views.BookGenreListView.as_view(), name='genre-book-list'),

    path('conditions/', ConditionListCreateView.as_view(), name='condition-list-create'),

    path('exchange/', views.ExchangeListView.as_view(), name='exchange-request-list'),
    path('exchange/create/', ExchangeCreateView.as_view(), name='exchange-create'),
    path('api/exchange-requests/<int:pk>/', views.ExchangeDetailView.as_view(), name='exchange-request-detail'),

    path('api/exchanges/received/', views.ExchangeReceivedListView.as_view(), name='exchange-received-list'),
    path('api/exchanges/sent/', views.ExchangeSentListView.as_view(), name='exchange-sent-list'),
    path('api/exchanges/completed/', views.CompletedExchangeListView.as_view(), name='completed-exchange-list'),

    path('swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-re2doc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
