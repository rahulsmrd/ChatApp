from django.urls import path
from chat.consumer import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:id>/', ChatConsumer.as_asgi()),
]