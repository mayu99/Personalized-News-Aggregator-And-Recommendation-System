import requests
import openai
from django.conf import settings
from news.models import Article
from django.utils.dateparse import parse_datetime

def fetch_and_store_news():
    url = (
        f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={settings.NEWS_API_KEY}"
    )
    response = requests.get(url)
    articles = response.json().get("articles", [])

    for item in articles:
        title = item.get("title")
        content = item.get("content") or item.get("description")
        url = item.get("url")
        published = parse_datetime(item.get("publishedAt"))
        author = item.get("author") or "Unknown"

        if not content:
            continue

        # Check if already exists
        if Article.objects.filter(title=title).exists():
            continue

        # Summarize using OpenAI
        openai.api_key = settings.OPENAI_API_KEY
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Summarize the following news article:\n\n{content}",
                max_tokens=150,
                temperature=0.5,
            )
            summary = response.choices[0].text.strip()
        except Exception as e:
            summary = "Summary unavailable due to API error."

        Article.objects.create(
            title=title,
            author=author,
            content=content,
            summary=summary,
            url=url,
            published_at=published,
        )
