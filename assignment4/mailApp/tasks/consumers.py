import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"user_{self.user_id}_progress"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"WebSocket connected for user: {self.user_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"WebSocket disconnected for user: {self.user_id}")

    async def send_progress(self, event):
        await self.send(text_data=json.dumps({
            "progress": event["progress"],
            "message": event["message"],
        }))
