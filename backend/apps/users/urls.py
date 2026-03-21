from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, SignupView, UserListView

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/users/', UserListView.as_view(), name='user_list'),
]
