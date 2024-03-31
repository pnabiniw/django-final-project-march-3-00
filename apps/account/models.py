import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.commons.models import BaseModel


class User(AbstractUser):
    username = models.CharField(default=uuid.uuid4, max_length=100, blank=True)
    email = models.EmailField(unique=True)
    middle_name = models.CharField(null=True, blank=True, max_length=50)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.email


class EmailVerificationKey(BaseModel):
    key = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_activation_key')


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(null=True, blank=True, upload_to="profile_pictures/")
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=14)
    bio = models.TextField(max_length=500)
    resume = models.FileField(null=True, blank=True, upload_to="resumes/")

    def __str__(self):
        return f"Profile of {self.user.email}"
