import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from blog.models import CustomUser
from .models import Message, Chat


class ChatConsumer(WebsocketConsumer):

    def message_to_json(self, message: Message):
        return {
            "owner": message.owner.username,
            "text": message.text,
            "chat": message.chat,
            "timestamp": f'{message.timestamp.hour}:{message.timestamp.minute}',
        }

    def messages_to_json(self, messages):
        msg = []
        for message in messages:
            msg.append(self.message_to_json(message))
        return msg

    def fetch_messages(self, data):
        chat = Chat.objects.get(pk=int(data))
        messages = Message.objects.filter(chat=chat)
        content = self.messages_to_json(messages)

        self.send_chat_messages(content)

    def new_message(self, data):
        chat = Chat.objects.get(pk=int(data['room_name']))
        owner = CustomUser.objects.get(username=data['owner'])
        Message.objects.create(
            owner=owner,
            chat=chat,
            text=data['message'],
        )

    commands = {
        "new_message": new_message,
        "fetch_messages": fetch_messages,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        self.fetch_messages(self.room_name)

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.new_message(data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data['message'],
                'owner': data['owner'],
            }
        )

    def send_chat_messages(self, messages):
        for message in messages:
            msg = message["text"]
            owner = message["owner"]
            timestamp = f'{message["timestamp"]}'
            self.send(text_data=json.dumps({
                "message":msg,
                "owner":owner,
                "timestamp":timestamp,
            }))

    # Receive message from room group

    def chat_message(self, event):
        message = event["message"]
        owner = event['owner']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "owner": owner,
            "timestamp": f'{timezone.datetime.now().hour}:{timezone.datetime.now().minute}',

        }))
