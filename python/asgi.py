# HomeLab/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from consola import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/consola/", consumers.ConsolaConsumer.as_asgi()),  # Ruta WebSocket
        ])
    ),
})
