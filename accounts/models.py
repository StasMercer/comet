from datetime import date

from django import forms
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf.global_settings import MEDIA_ROOT

class CustomUser(AbstractUser):

    username = models.CharField(max_length=30, unique=True)

    first_name = models.CharField(max_length=30)

    last_name = models.CharField(max_length=30)

    password = models.CharField(max_length=100)

    email = models.CharField(max_length=100, unique=True)

    date_of_birth = models.DateField(default='2000-01-03')

    avatar = models.ImageField(upload_to='users/', name='avatar', default=MEDIA_ROOT+'/users/a.jpg')

    phone_number = models.CharField(max_length=30, unique=True, null=True)

    friends = models.ManyToManyField('CustomUser', related_name='user_friend', blank=True)

    tags = models.ManyToManyField('events.Tag')

    def get_username(self):
        return str(self.username)

class Rate(models.Model):

    value = models.PositiveSmallIntegerField(default=0)

    date = models.DateField(auto_now_add=True)

    from_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='rate_from', default='')

    to_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='user_rate', default='')


class UserPhoto(models.Model):

    photo_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, default='', related_name='user_photos')

    img_value = models.ImageField(upload_to='users/', default='_')

    def __str__(self):
        return self.img_value





