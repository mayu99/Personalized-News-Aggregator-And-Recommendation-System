from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Article
from django.utils.html import strip_tags
from django.utils.text import Truncator
from accounts.models import UserPreference
from .utils.recommendations import log_article_click, get_recommended_articles, get_related_articles

def article_list(request):
    """View for the article list page with recommendations."""
    # Get user preferences if authenticated
    if request.user.is_authenticated:
        preferences = request.user.preferences
        if preferences and preferences.categories:
            articles = Article.objects.filter(category__in=preferences.categories)
        else:
            articles = Article.objects.all()
    else:
        articles = Article.objects.all()

    # Get recommended articles
    recommended_articles = get_recommended_articles(request.user)

    # Sort options
    sort = request.GET.get('sort', '-published_at')
    valid_sorts = {
        '-published_at': 'Latest',
        'published_at': 'Oldest',
        '-sentiment': 'Most Positive',
        'sentiment': 'Most Negative',
    }
    
    if sort in valid_sorts:
        articles = articles.order_by(sort)
    
    # Process articles for display
    for article in articles:
        if not article.summary:
            # Create a simple summary from content if none exists
            content = article.content or ''
            article.display_summary = ' '.join(content.split()[:50]) + '...'
        else:
            article.display_summary = article.summary
    
    context = {
        'articles': articles,
        'recommended_articles': recommended_articles,
        'sort_options': valid_sorts.items(),
        'current_sort': sort,
    }
    return render(request, 'news/index.html', context)

def article_detail(request, article_id):
    """View for individual article pages with click tracking."""
    article = get_object_or_404(Article, id=article_id)
    
    # Log the click if user is authenticated
    if request.user.is_authenticated:
        log_article_click(request.user, article)
    
    # Get related articles using NLP similarity
    related_articles = get_related_articles(article, limit=5)
    
    # Process content for display
    if not article.summary:
        content = article.content or ''
        article.display_summary = ' '.join(content.split()[:50]) + '...'
    else:
        article.display_summary = article.summary
    
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'news/article_detail.html', context)
