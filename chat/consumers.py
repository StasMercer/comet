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
        errors = []

        try:
            message = text_data_json.get('message', '')
            username = text_data_json.get('username', '')
            event = Event.objects.get(pk=self.scope['url_route']['kwargs']['event_id'])
            user = CustomUser.objects.get(username=username)

        except CustomUser.DoesNotExist:
                errors.append('user_does_not_exist')
        except Event.DoesNotExist:
                errors.append('event_does_not_exist')

        if not errors and message:

            Message.objects.create(user=user, event=event, text=message, is_read=False)

            # Send message to room group
            await self.channel_layer.group_send(
                self.event_group_id,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username,
                    'avatar': str(user.avatar),
                }
            )
        else:
            await self.channel_layer.group_send(
                self.event_group_id,
                {
                    'type': 'chat_error',
                    'error': errors,

                }

            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        avatar = event['avatar']
        # Send message to WebSocket

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'avatar': avatar,

        }))

    async def chat_error(self, event):
        error = event['error']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'error': error
        }))
