from django.contrib import admin
from .models import Article, UserClickLog

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'source', 'category', 'sentiment', 'published_at')
    list_filter = ('category', 'sentiment', 'source')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'published_at'

@admin.register(UserClickLog)
class UserClickLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'article__title')
    date_hierarchy = 'timestamp' 