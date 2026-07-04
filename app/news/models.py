from dataclasses import dataclass, field


@dataclass
class NewsAnalysis:
    summary: str
    sentiment: str
    impact: str
    confidence: int
    affected_assets: list[str] = field(default_factory=list)
    reasoning: list[str] = field(default_factory=list)


@dataclass
class NewsArticle:
    title: str
    summary: str
    source: str
    published: str
    url: str
