from rest_framework import serializers
from chat.models import Message
from accounts.models import CustomUser
from events.models import Event


class MessageSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        many=False,
        queryset=CustomUser.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Message
        fields = "__all__"

