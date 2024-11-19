from os import path
from tasks.comsumers import UploadProgressConsumer
websocket_urlpatterns = [
    path("ws/progress/", UploadProgressConsumer.as_asgi()),
]