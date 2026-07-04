from dataclasses import dataclass


@dataclass
class NewsArticle:
    title: str
    summary: str
    source: str
    published: str
    url: str
