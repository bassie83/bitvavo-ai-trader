import feedparser
from app.news.models import NewsArticle

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
]


def get_latest_news(limit: int = 10) -> list[dict]:
    """
    Collect the latest crypto news from configured RSS feeds.
    """

    articles = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:limit]:
            articles.append(
                NewsArticle(
                    title=entry.get("title", ""),
                    summary=entry.get("summary", ""),
                    source=feed.feed.get("title", "Unknown"),
                    published=entry.get("published", ""),
                    url=entry.get("link", ""),
                )
            )

    articles.sort(
        key=lambda article: article.published,
        reverse=True,
    )

    return articles[:limit]
