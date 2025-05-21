from django.db.models import Q
from django.db.models import Count, F, ExpressionWrapper, FloatField
from django.utils import timezone
from datetime import timedelta
from ..models import Article, UserClickLog
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def log_article_click(user, article):
    """Log a user's click on an article."""
    UserClickLog.objects.create(user=user, article=article)

def get_user_category_preferences(user, days=30):
    """Get user's category preferences based on recent clicks."""
    cutoff_date = timezone.now() - timedelta(days=days)
    
    # Get click counts by category with time decay
    category_clicks = (
        UserClickLog.objects
        .filter(user=user, timestamp__gte=cutoff_date)
        .values('article__category')
        .annotate(
            click_count=Count('id'),
            # Apply time decay: recent clicks have higher weight
            weighted_count=ExpressionWrapper(
                Count('id') * (1.0 / (1.0 + F('timestamp__day') / days)),
                output_field=FloatField()
            )
        )
        .order_by('-weighted_count')
    )
    
    return {item['article__category']: item['weighted_count'] for item in category_clicks}

def get_user_content_preferences(user, days=30):
    """Get user's content preferences based on clicked articles."""
    cutoff_date = timezone.now() - timedelta(days=days)
    
    # Get recently clicked articles
    clicked_articles = (
        UserClickLog.objects
        .filter(user=user, timestamp__gte=cutoff_date)
        .select_related('article')
        .order_by('-timestamp')
    )
    
    if not clicked_articles:
        return None
    
    # Combine article content for analysis
    clicked_content = [
        f"{log.article.title} {log.article.content or ''} {log.article.summary or ''}"
        for log in clicked_articles
    ]
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=1000,
        ngram_range=(1, 2)
    )
    
    try:
        # Fit and transform clicked content
        clicked_vectors = vectorizer.fit_transform(clicked_content)
        
        # Get feature names (keywords)
        feature_names = vectorizer.get_feature_names_out()
        
        # Calculate average TF-IDF scores for each feature
        avg_scores = clicked_vectors.mean(axis=0).A1
        
        # Get top keywords
        top_indices = avg_scores.argsort()[-20:][::-1]  # Get top 20 keywords
        top_keywords = [feature_names[i] for i in top_indices]
        
        return top_keywords
    except Exception as e:
        print(f"Error in content analysis: {str(e)}")
        return None

def get_recommended_articles(user, limit=5):
    """Get recommended articles based on user's click history and content preferences."""
    if not user.is_authenticated:
        return Article.objects.all().order_by('-published_at')[:limit]
    
    # Get user's category preferences
    category_preferences = get_user_category_preferences(user)
    
    # Get user's content preferences
    content_keywords = get_user_content_preferences(user)
    
    # Base queryset
    articles = Article.objects.all()
    
    if category_preferences:
        # Filter by preferred categories
        articles = articles.filter(category__in=category_preferences.keys())
    
    if content_keywords:
        # Create content-based query
        content_query = Q()
        for keyword in content_keywords:
            content_query |= Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(summary__icontains=keyword)
        
        # Apply content filter
        articles = articles.filter(content_query)
    
    # Get articles and prepare for content similarity scoring
    articles = articles.order_by('-published_at')[:limit * 2]  # Get more articles for better selection
    
    if not articles:
        return Article.objects.all().order_by('-published_at')[:limit]
    
    # Prepare content for similarity analysis
    article_contents = [
        f"{article.title} {article.content or ''} {article.summary or ''}"
        for article in articles
    ]
    
    # Calculate content similarity
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        content_vectors = vectorizer.fit_transform(article_contents)
        similarity_matrix = cosine_similarity(content_vectors)
        
        # Calculate average similarity scores
        avg_similarities = similarity_matrix.mean(axis=0)
        
        # Get indices of top similar articles
        top_indices = avg_similarities.argsort()[-limit:][::-1]
        
        # Return top similar articles
        return [articles[i] for i in top_indices]
    except Exception as e:
        print(f"Error in similarity calculation: {str(e)}")
        return articles[:limit]

def get_related_articles(article, limit=5):
    """Return the most similar articles to the given article using TF-IDF + cosine similarity."""
    # Exclude the current article
    all_articles = Article.objects.exclude(id=article.id)
    if not all_articles.exists():
        return []
    # Prepare corpus: first item is the target article, rest are candidates
    corpus = [f"{article.title} {article.content or ''}"] + [f"{a.title} {a.content or ''}" for a in all_articles]
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        # Get indices of top similar articles
        top_indices = similarities.argsort()[-limit:][::-1]
        related_articles = [all_articles[i] for i in top_indices]
        return related_articles
    except Exception as e:
        print(f"Error in related article similarity calculation: {str(e)}")
        return all_articles[:limit] 