import requests
import logging
import json
from django.conf import settings
from news.models import Article
from django.utils.dateparse import parse_datetime
from requests.exceptions import RequestException
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from transformers import pipeline

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Hugging Face summarizer (local model)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def analyze_sentiment(text):
    """Analyze sentiment of text using VADER."""
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    
    # Determine sentiment based on compound score
    if scores['compound'] >= 0.05:
        return 'positive'
    elif scores['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def determine_category(title, content):
    """Determine article category based on keywords in title and content."""
    keywords = {
        'TECH': ['technology', 'tech', 'ai', 'software', 'digital', 'cyber', 'robot', 'computer', 'internet'],
        'BUSINESS': ['business', 'economy', 'market', 'stock', 'trade', 'finance', 'company', 'startup'],
        'SCIENCE': ['science', 'research', 'study', 'discovery', 'space', 'physics', 'biology', 'chemistry'],
        'HEALTH': ['health', 'medical', 'medicine', 'disease', 'treatment', 'doctor', 'patient', 'hospital'],
        'SPORTS': ['sports', 'game', 'player', 'team', 'tournament', 'championship', 'athlete', 'football', 'basketball'],
        'ENTERTAINMENT': ['entertainment', 'movie', 'music', 'celebrity', 'film', 'tv', 'show', 'actor', 'actress'],
        'POLITICS': ['politics', 'government', 'election', 'president', 'congress', 'senate', 'democrat', 'republican'],
        'WORLD': ['world', 'international', 'global', 'foreign', 'country', 'nation', 'diplomatic', 'embassy']
    }
    
    text = (title + ' ' + (content or '')).lower()
    
    # Count keyword matches for each category
    category_scores = {cat: sum(1 for kw in kws if kw in text) for cat, kws in keywords.items()}
    
    # Return the category with the most matches, or 'WORLD' if no matches
    max_score = max(category_scores.values())
    if max_score > 0:
        for cat, score in category_scores.items():
            if score == max_score:
                return cat
    return 'WORLD'

def notify_new_article(article):
    """Send WebSocket notification for new article."""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "news_updates",
        {
            "type": "news_update",
            "data": {
                "type": "new_article",
                "article": {
                    "id": article.id,
                    "title": article.title,
                    "author": article.author,
                    "summary": article.summary,
                    "url": article.url,
                    "published_at": article.published_at.isoformat(),
                    "source": article.source,
                    "category": article.category,
                    "sentiment": article.sentiment,
                    "slug": article.slug
                }
            }
        }
    )

def fetch_and_store_news():
    """Fetch news from NewsAPI and store in database with local Hugging Face summaries."""
    try:
        # Check if API key is configured
        if not hasattr(settings, 'NEWS_API_KEY') or not settings.NEWS_API_KEY:
            logger.error("NEWS_API_KEY not configured in settings")
            return False

        # Fetch news from API
        url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"country=us&"
            f"pageSize=20&"
            f"apiKey={settings.NEWS_API_KEY}"
        )
        logger.info(f"Fetching news from NewsAPI...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'status' in data and data['status'] != 'ok':
                logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return False
            articles = data.get("articles", [])
            logger.info(f"Fetched {len(articles)} articles from NewsAPI")
        except RequestException as e:
            logger.error(f"Error fetching news: {str(e)}")
            return False
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            return False

        articles_created = 0
        articles_skipped = 0
        articles_exist = 0

        for item in articles:
            try:
                title = item.get("title")
                content = item.get("content") or item.get("description")
                url = item.get("url")
                published_str = item.get("publishedAt")
                source = item.get("source", {}).get("name")
                if not all([title, content, url, published_str]):
                    missing_fields = [field for field, value in {'title': title, 'content': content, 'url': url, 'published_at': published_str}.items() if not value]
                    logger.warning(f"Skipping article due to missing fields ({', '.join(missing_fields)}): {title}")
                    articles_skipped += 1
                    continue
                published = parse_datetime(published_str)
                if not published:
                    logger.warning(f"Invalid publication date format: {published_str}")
                    articles_skipped += 1
                    continue
                author = item.get("author") or "Unknown"
                if Article.objects.filter(title=title).exists():
                    logger.info(f"Article already exists: {title}")
                    articles_exist += 1
                    continue
                category = determine_category(title, content)
                sentiment = analyze_sentiment(f"{title} {content}")
                # Generate summary with local model or fallback
                if content and len(content) > 50:
                    try:
                        summary = summarizer(content, min_length=20, max_length=80, do_sample=False)[0]['summary_text']
                    except Exception as e:
                        logger.warning(f"Local summarization failed: {str(e)}")
                        summary = content[:250] + "..."
                else:
                    summary = content if content else "No summary available."
                article = Article.objects.create(
                    title=title,
                    author=author,
                    content=content,
                    summary=summary,
                    url=url,
                    published_at=published,
                    source=source,
                    category=category,
                    sentiment=sentiment
                )
                articles_created += 1
                logger.info(f"Created article: {title} (Category: {category}, Sentiment: {sentiment})")
                notify_new_article(article)
            except Exception as e:
                logger.error(f"Error processing article: {str(e)}")
                continue
        logger.info(f"Articles processed - Created: {articles_created}, Skipped: {articles_skipped}, Already exist: {articles_exist}")
        return True
    except Exception as e:
        logger.error(f"Unexpected error in fetch_and_store_news: {str(e)}")
        return False
