from app.news.models import NewsArticle


def build_news_analysis_prompt(article: NewsArticle) -> str:
    """
    Build a prompt for AI news analysis.
    """

    return f"""
Analyze this crypto news article.

Return JSON with:
- summary
- sentiment: bullish, bearish, or neutral
- impact: LOW, MEDIUM, or HIGH
- confidence: 0-100
- affected_assets
- reasoning

Title:
{article.title}

Summary:
{article.summary}

Source:
{article.source}
"""
