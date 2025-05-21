from django.core.management.base import BaseCommand
from news.utils.news_fetcher import fetch_and_store_news

class Command(BaseCommand):
    help = "Fetch news articles and summarize them"

    def handle(self, *args, **kwargs):
        fetch_and_store_news()
        self.stdout.write(self.style.SUCCESS("News fetched and stored successfully!"))
