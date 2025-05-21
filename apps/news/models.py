# news/models.py

from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)  # ✅ This must exist
    url = models.URLField(max_length=500, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)  # optional

    def __str__(self):
        return self.title
