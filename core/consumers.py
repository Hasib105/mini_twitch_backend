# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stream_slug = self.scope['url_route']['kwargs']['slug']
        self.room_group_name = f'chat_{self.stream_slug}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        # Save chat message to the database
        chat_message = ChatMessage(stream_slug=self.stream_slug, user=user, message=message)
        chat_message.save()

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'user': user
        })

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))