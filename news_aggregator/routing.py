from django.urls import re_path
from news.consumers import NewsConsumer

websocket_urlpatterns = [
    re_path(r'ws/news/$', NewsConsumer.as_asgi()),
] 