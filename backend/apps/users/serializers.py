from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # type: ignore
from rest_framework import serializers  # type: ignore
from django.contrib.auth.password_validation import validate_password  # type: ignore
from .models import CustomUser

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds role, user_id, and login_id to the JWT token payload."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['user_id'] = user.id
        token['login_id'] = user.login_id
        token['email'] = user.email
        return token


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['login_id', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_login_id(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Login ID must be at least 6 characters.")
        if len(value) > 12:
            raise serializers.ValidationError("Login ID cannot exceed 12 characters.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'login_id', 'email', 'role', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
