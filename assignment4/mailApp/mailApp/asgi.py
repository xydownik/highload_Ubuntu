"""
ASGI config for mailApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from tasks.consumers import UploadProgressConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailApp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Add WebSocket URL patterns
            os.path("ws/progress/", UploadProgressConsumer.as_asgi()),
        ])
    ),
})