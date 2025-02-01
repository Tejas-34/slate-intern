from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        """Create and return a regular user with the given email and password."""
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ("school", "School"),
        ("parent", "Parent"),
        ("student", "Student"),
    ]

    username = None  # Remove the default username field
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    linked_student_id = models.IntegerField(null=True, blank=True)

    objects = CustomUserManager()  # Use the custom UserManager

    USERNAME_FIELD = "email"  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # Remove username requirement

    class Meta:
        swappable = "AUTH_USER_MODEL"


class StudentAchievement(models.Model):
    student_id = models.IntegerField()
    name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    achievements = models.TextField()
