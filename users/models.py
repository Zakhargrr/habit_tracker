from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    chat_id = models.CharField(verbose_name='id чата')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
