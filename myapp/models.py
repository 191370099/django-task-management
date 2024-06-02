from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('developer', 'Developer'),
        ('qa', 'QA'),
        ('manager', 'Manager'),
    )
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'role']


class Task(models.Model):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned_by')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned_to')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
