from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.permissions import AllowAny, IsAuthenticated  # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore
from django.core.mail import send_mail  # type: ignore
from django.core.cache import cache  # type: ignore
import random

from .serializers import (
    CustomTokenObtainPairSerializer, SignupSerializer, UserSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from .models import CustomUser


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    """Returns list of all active users (for approver dropdowns etc.)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.filter(is_active=True).order_by('login_id')
        return Response(UserSerializer(users, many=True).data)

class UserDetailView(APIView):
    """Allows Admin to modify a specific user (role assignment)."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied. Admins only.'}, status=status.HTTP_403_FORBIDDEN)
        
        user = CustomUser.objects.filter(pk=pk, is_active=True).first()
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        role = request.data.get('role')
        if role:
            # Validate role
            valid_roles = [r[0] for r in CustomUser.ROLE_CHOICES]
            if role not in valid_roles:
                return Response({'error': 'Invalid role provided.'}, status=status.HTTP_400_BAD_REQUEST)
            user.role = role
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({'error': 'No role provided.'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email, is_active=True).first()
            if not user:
                return Response({'error': 'This email is not registered in the system.'}, status=status.HTTP_404_NOT_FOUND)
            
            # Generate 6-digit OTP
            otp = f"{random.randint(100000, 999999)}"
            cache_key = f"pwd_reset_otp_{email}"
            cache.set(cache_key, otp, timeout=600)  # Valid for 10 minutes
            
            send_mail(
                'PLM System - Password Reset OTP',
                f'Hello {user.login_id},\n\nYour 6-digit One Time Password (OTP) for resetting your account is:\n\n{otp}\n\nThis OTP will expire in 10 minutes.\nIf you did not request this, please ignore this email.',
                None,  # uses DEFAULT_FROM_EMAIL
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent successfully to the registered email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetVerifyOTPView(APIView):
    """Midpoint verification to allow frontend to unlock 2-step UI"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if not email or not otp:
            return Response({'error': 'Email and OTP are strictly required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        cache_key = f"pwd_reset_otp_{email}"
        stored_otp = cache.get(cache_key)
        
        if stored_otp is None or stored_otp != str(otp):
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'message': 'OTP validated. Proceed to password swap.'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_entered = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            
            cache_key = f"pwd_reset_otp_{email}"
            stored_otp = cache.get(cache_key)

            if stored_otp is None or stored_otp != otp_entered:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = CustomUser.objects.filter(email=email, is_active=True).first()
            if user:
                user.set_password(new_password)
                user.save()
                cache.delete(cache_key)  # Ensure OTP can't be reused
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

