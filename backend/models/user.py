from .base import TimeStampedModel
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser, TimeStampedModel):
    abha_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    preferred_language = models.CharField(max_length=10, default='en')
    is_verified = models.BooleanField(default=False)