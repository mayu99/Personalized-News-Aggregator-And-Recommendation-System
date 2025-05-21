from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('TECH', 'Technology'),
        ('BUSINESS', 'Business'),
        ('SCIENCE', 'Science'),
        ('HEALTH', 'Health'),
        ('SPORTS', 'Sports'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('POLITICS', 'Politics'),
        ('WORLD', 'World News'),
    ]

    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)  # ✅ This must exist
    url = models.URLField(max_length=500, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)  # optional
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='WORLD')
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, default='neutral')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class UserClickLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='click_logs')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='click_logs')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['article', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} clicked {self.article.title} at {self.timestamp}"
