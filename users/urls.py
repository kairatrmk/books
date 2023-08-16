from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationApiView.as_view()),

    path('login/', views.UserLoginView.as_view(), name='token_obtain_pair'),  # Вход и получение токена доступа
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path('update/<int:id>/', views.UpdateUserProfileView.as_view(), name='update-profile'),
]