from django.contrib.auth.models import User
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, UserChannel
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        try:
            user_channel = UserChannel.objects.get(user=self.scope.get('user'))
            user_channel.channel_name = self.channel_name
            user_channel.save()
        except:
            user_channel = UserChannel()
            user_channel.user = self.scope.get('user')
            user_channel.channel_name = self.channel_name
            user_channel.save()

        self.person_id = self.scope.get("url_route").get("kwargs").get("id")

    def receive(self, text_data):
        text_data = json.loads(text_data)

        other_user = User.objects.get(id=self.person_id)

        new_message = Message()
        new_message.from_who = self.scope.get("user")
        new_message.to_who = User.objects.get(id=self.person_id)
        new_message.message = text_data.get("message")
        new_message.date = "2025-9-23"
        new_message.time = "10:10:10"
        new_message.has_been_seen = False
        new_message.save()

        try:
            user_channel_name = UserChannel.objects.get(user=other_user)

            data = {
                "type": "receiver_function",
                "type_of_data": "new_message",
                "data": text_data.get("message")
            }
        except:
            pass

        async_to_sync(self.channel_layer.send)(user_channel_name.channel_name, data)

    def receiver_function(self, event):
        data = json.dumps(event)
        self.send(data)