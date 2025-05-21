from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Add additional fields that you want to include for users.
    """
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # Required for custom user model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserPreference(models.Model):
    """
    Model to store user's news preferences
    """
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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    categories = models.JSONField(default=list, blank=True, help_text="List of preferred news categories")
    keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords of interest")
    excluded_sources = models.CharField(max_length=255, blank=True, help_text="Comma-separated news sources to exclude")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"

    def get_categories_list(self):
        return self.categories if self.categories else []

    def get_keywords_list(self):
        return [k.strip() for k in self.keywords.split(',')] if self.keywords else []

    def get_excluded_sources_list(self):
        return [s.strip() for s in self.excluded_sources.split(',')] if self.excluded_sources else []
