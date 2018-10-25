from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    username = models.CharField(max_length=30, unique=True)

    first_name = models.CharField(max_length=30)

    last_name = models.CharField(max_length=30)

    password = models.TextField()

    email = models.CharField(max_length=100, unique=True)

    date_of_birth = models.CharField(max_length=20)

    phone_number = models.CharField(max_length=30, unique=True, null=True)

