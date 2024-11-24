from django.urls import re_path
from .consumers import ProgressConsumer

websocket_urlpatterns = [
    re_path(r"ws/progress/(?P<user_id>\d+)/$", ProgressConsumer.as_asgi()),
]