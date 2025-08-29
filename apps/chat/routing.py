from django.urls import path
from .consumers import ChatConsumer


ASGI_urlpatterns = [
    path("websocket/<int:person_id>/", ChatConsumer.as_asgi()),
]