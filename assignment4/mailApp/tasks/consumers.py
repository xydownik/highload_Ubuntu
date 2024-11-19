from channels.generic.websocket import AsyncWebsocketConsumer
import json

class UploadProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"user_{self.user.id}_progress"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_progress(self, event):
        await self.send(text_data=json.dumps({
            "progress": event["progress"],
        }))
