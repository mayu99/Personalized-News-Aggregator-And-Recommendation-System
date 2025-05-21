from django.core.management.base import BaseCommand
from news.models import Article
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates slugs for existing articles'

    def handle(self, *args, **kwargs):
        articles = Article.objects.filter(slug__isnull=True)
        count = 0
        
        for article in articles:
            base_slug = slugify(article.title)
            slug = base_slug
            counter = 1
            
            # Ensure unique slug
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            article.slug = slug
            article.save()
            count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated slugs for {count} articles')
        ) 