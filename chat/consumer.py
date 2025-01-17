import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        loginUser = self.scope['user']
        user_list = [int(self.scope['url_route']['kwargs']['id']), int(loginUser.id)]
        self.room_name = f"{max(user_list)}-{min(user_list)}"
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.send(text_data=json.dumps({
            'type': 'join',
            'room': self.room_name
        }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.send(text_data=json.dumps({
            'type': 'leave',
            'room': self.room_name
        }))
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']
        receiver = await self.get_user(id=self.scope['url_route']['kwargs']['id'])
        saved_message = await self.save_message_to_db(sender, receiver, message)
        print(message, sender.id, receiver.id)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': saved_message,
            }
        )

    async def chat_message(self , event) : 
        print(event)
        message = event["message"]
        sender = str(message.sender.id)
        receiver = str(message.receiver.id)
        time = message.timestamp.strftime("%I:%M %p")
        data = {"message":message.content, "sender": sender, "receiver": receiver, "time":time}
        await self.send(text_data = json.dumps(data))

    @database_sync_to_async
    def get_user(self, id):
        return get_user_model().objects.filter(id=id).first()
    @database_sync_to_async
    def save_message_to_db(self, sender, receiver, message):
        chat_id = f"{max(sender.id, receiver.id)}-{min(sender.id, receiver.id)}"
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=message,
            chat_id=chat_id,
        )
        return message
