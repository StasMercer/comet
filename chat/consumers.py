# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.conf import settings
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser
from .api.serializers import MessageSerializer
from .models import Message
from events.models import Event
from accounts.api.serializers import ShortUserSerializer


class ChatConsumer(AsyncWebsocketConsumer):

    user = None
    event = None
    errors = []

    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.event_group_id = 'chat_%s' % self.event_id

        # Join room group
        await self.channel_layer.group_add(
            self.event_group_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.event_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        try:
            message = text_data_json.get('message', '')
            username = text_data_json.get('username', '')
            self.event = Event.objects.get(pk=self.scope['url_route']['kwargs']['event_id'])
            self.user = CustomUser.objects.get(username=username)

        except CustomUser.DoesNotExist:
             self.errors.append('user_does_not_exist')
        except Event.DoesNotExist:
                self.errors.append('event_does_not_exist')

        if not self.errors and message:

            Message.objects.create(user=self.user, event=self.event, text=message, is_read=False)

            # Send message to room group
            await self.channel_layer.group_send(
                self.event_group_id,
                {
                    'type': 'chat_message',
                    'message': message,

                }
            )
        else:
            await self.channel_layer.group_send(
                self.event_group_id,
                {
                    'type': 'chat_error',
                    'error': self.errors,

                }

            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': self.user.username,
            'avatar': str(self.user.avatar),

        }))

    async def chat_error(self, event):
        error = event['error']
        self.errors = []
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'error': error
        }))
