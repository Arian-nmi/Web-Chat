from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Message, UserChannel
import datetime, json


User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        print("==== DEBUG USER IN WEBSOCKET CONNECT ====", self.user, "Authenticated?", self.user.is_authenticated)

        if not self.user.is_authenticated:
            self.close()
            return

        self.person_id = self.scope["url_route"]["kwargs"]["person_id"]
        self.group_name = f"user_{self.user.id}"

        UserChannel.objects.update_or_create(
            user_id=self.user.id,
            defaults={"channel_name": self.channel_name}
        )

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        UserChannel.objects.filter(user_id=self.user.id).update(channel_name=None)

    def receive(self, text_data):
        data = json.loads(text_data)
        other_user = User.objects.get(id=self.person_id)

        if data.get("type") == "new_message":
            now = datetime.datetime.now()

            Message.objects.create(
                from_who_id=self.user.id,
                to_who_id=other_user.id,
                message=data["message"],
                date=now.date(),
                time=now.time()
            )

            async_to_sync(self.channel_layer.group_send)(
                f"user_{other_user.id}",
                {
                    "type": "receiver_function",
                    "type_of_data": "new_message",
                    "data": data.get("message"),
                    "from_user": self.user.username,
                    "date": str(now.date()),
                    "time": now.strftime("%H:%M:%S"),                }
            )

        elif data.get("type") == "i_have_seen":
            Message.objects.filter(
                from_who_id=other_user.id, to_who_id=self.user.id
            ).update(has_been_seen=True)

            async_to_sync(self.channel_layer.group_send)(
                f"user_{other_user.id}",
                {
                    "type": "receiver_function",
                    "type_of_data": "have_been_seen",
                }
            )

    def receiver_function(self, event):
        self.send(text_data=json.dumps(event))