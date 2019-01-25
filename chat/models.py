import uuid

from django.db import models
from events.models import Event
from accounts.models import CustomUser


# Create your models here.

class Message(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='message_event', null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='message_user')

    text = models.CharField(max_length=300)

    date = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.text
