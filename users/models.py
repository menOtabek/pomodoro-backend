from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    coins = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=20, default='en')
    first_name = models.CharField(max_length=55, verbose_name='first name')
    last_name = models.CharField(max_length=55, verbose_name='last name')
    username = models.CharField(max_length=55, unique=True, verbose_name='username')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
