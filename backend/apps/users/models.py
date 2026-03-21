from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, login_id, email, password=None, role='engineering', **extra_fields):
        if not login_id:
            raise ValueError('Login ID is required')
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(login_id=login_id, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return self.create_user(login_id, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    ROLE_CHOICES = [
        ('engineering', 'Engineering'),
        ('approver', 'Approver'),
        ('operations', 'Operations'),
        ('admin', 'Admin'),
    ]

    login_id   = models.CharField(max_length=12, unique=True)
    email      = models.EmailField(unique=True)
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default='engineering')
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.login_id} ({self.role})'

    def has_perm(self, perm, obj=None):
        return self.role == 'admin'

    def has_module_perms(self, app_label):
        return self.role == 'admin'
