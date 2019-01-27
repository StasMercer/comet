# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json


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
        await async_to_sync(self.channel_layer.group_discard)(
            self.event_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.event_group_id,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
