from django.urls import path  # type: ignore
from rest_framework_simplejwt.views import TokenRefreshView  # type: ignore
from .views import (
    CustomTokenObtainPairView, SignupView, UserListView, UserDetailView,
    PasswordResetRequestView, PasswordResetVerifyOTPView, PasswordResetConfirmView
)

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/users/', UserListView.as_view(), name='user_list'),
    path('auth/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('auth/password-reset-verify/', PasswordResetVerifyOTPView.as_view(), name='password_reset_verify'),
    path('auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
