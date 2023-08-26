# your_project/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from user_1.consumer import YourConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/<str:user_id>/', YourConsumer.as_asgi()),
    ]),
})
