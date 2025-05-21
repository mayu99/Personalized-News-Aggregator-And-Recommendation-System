import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Article
from accounts.models import UserPreference

class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("news_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("news_updates", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'get_preferences':
            user_id = text_data_json.get('user_id')
            if user_id:
                preferences = await self.get_user_preferences(user_id)
                await self.send(text_data=json.dumps({
                    'type': 'preferences',
                    'preferences': preferences
                }))

    async def news_update(self, event):
        """Send news update to WebSocket"""
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def get_user_preferences(self, user_id):
        """Get user preferences from database"""
        try:
            preferences = UserPreference.objects.get(user_id=user_id)
            return {
                'categories': preferences.categories,
                'keywords': preferences.keywords,
                'excluded_sources': preferences.excluded_sources
            }
        except UserPreference.DoesNotExist:
            return None 