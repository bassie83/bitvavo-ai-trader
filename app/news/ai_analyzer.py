import json

from app.ai.prompts import build_news_analysis_prompt
from app.ai.provider import chat
from app.news.models import NewsArticle, NewsAnalysis


def analyze_news_article(article: NewsArticle) -> NewsAnalysis:
    """
    Analyze a news article using the configured AI provider.
    """

    prompt = build_news_analysis_prompt(article)
    response = chat(prompt)

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        return NewsAnalysis(
            summary=response,
            sentiment="neutral",
            impact="LOW",
            confidence=0,
            affected_assets=[],
            reasoning=[
                "AI response was not valid JSON.",
                "Atlas used a safe neutral fallback.",
            ],
        )

    return NewsAnalysis(
        summary=data.get("summary", ""),
        sentiment=data.get("sentiment", "neutral"),
        impact=data.get("impact", "LOW"),
        confidence=data.get("confidence", 0),
        affected_assets=data.get("affected_assets", []),
        reasoning=data.get("reasoning", []),
    )
