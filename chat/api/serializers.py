from rest_framework import serializers
from chat.models import Message
from accounts.models import CustomUser
from accounts.api.serializers import ShortUserSerializer
from events.models import Event


class MessageSerializer(serializers.ModelSerializer):

    user = ShortUserSerializer()


    class Meta:
        model = Message
        fields = ('event', 'user', 'text', 'date', 'is_read')


