from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Event(models.Model):

    description = models.TextField()

    date_created = models.DateField(auto_now_add=True)

    date_expire = models.DateField()

    author = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='event_author')

    members = models.ManyToManyField(CustomUser, related_name='event_member')

    views = models.IntegerField(default=0)

    #photos

    #tags


class Tag(models.Model):

    name = models.CharField(unique=True, max_length=50)