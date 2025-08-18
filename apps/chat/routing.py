from django.urls import path
from .consumers import anything


ASGI_urlpatterns = [
    path("websocket", anything.as_asgi()),
]