from app.news.models import NewsArticle


def analyze_news_article(article: NewsArticle) -> dict:
    """
    Analyze a news article and return normalized AI news intelligence.

    This is a placeholder implementation.
    A real LLM provider will be connected in the next sprint.
    """

    return {
        "title": article.title,
        "source": article.source,
        "url": article.url,
        "summary": article.summary,
        "sentiment": "neutral",
        "impact": "LOW",
        "confidence": 50,
        "affected_assets": [],
        "reasoning": [
            "AI provider not connected yet.",
            "Default neutral analysis returned.",
        ],
    }
