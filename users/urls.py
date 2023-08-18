from django.urls import path
from users import views

urlpatterns = [

    path('api/ratings/create/', views.RatingCreateView.as_view(), name='create-rating'),
    path('api/user/<int:pk>/', views.CustomUserDetailView.as_view(), name='user-detail'),
    path('api/user/<int:pk>/rating/', views.UserRatingView.as_view(), name='user-rating'),


    path('register/', views.RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationApiView.as_view()),


    path('login/', views.UserLoginView.as_view(), name='token_obtain_pair'),  # Вход и получение токена доступа
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),


    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),


    path('update/<int:id>/', views.UpdateUserProfileView.as_view(), name='update-profile'),
]



