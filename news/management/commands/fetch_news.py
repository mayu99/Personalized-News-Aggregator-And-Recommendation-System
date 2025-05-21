from django.core.management.base import BaseCommand
from news.utils.news_fetcher import fetch_and_store_news
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Fetch news articles and summarize them"

    def handle(self, *args, **options):
        """Handle the command."""
        self.stdout.write("Starting news fetch...")
        success = fetch_and_store_news()
        
        if success:
            self.stdout.write(self.style.SUCCESS("News articles processed successfully!"))
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch or process news articles. Check the logs for details."))
