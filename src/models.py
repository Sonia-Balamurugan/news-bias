"""Data models for News Bias Detector"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Article:
    """Represents a news article"""
    source_name: str
    title: str
    url: str
    content: str
    published_at: datetime
    author: Optional[str] = None
    image_url: Optional[str] = None
    
    def __str__(self):
        return f"{self.source_name}: {self.title}"


@dataclass
class BiasAnalysis:
    """Represents the bias analysis of a single article"""
    article: Article
    tone: str  # "optimistic", "cautious", "skeptical"
    perspective_balance: float  # 0-1 scale, 0=risk-focused, 1=benefit-focused
    perspective_diversity: List[str]  # ["researchers", "companies", etc.]
    source_quality: str  # "research-backed", "mixed", "speculative"
    language_tone: str  # "measured", "emotionally-loaded"
    analysis_text: str
    
    def __str__(self):
        return f"{self.article.source_name} - Tone: {self.tone}"


@dataclass
class ComparisonReport:
    """Represents a comparison across multiple articles"""
    topic: str
    articles_analyzed: int
    analyses: List[BiasAnalysis]
    consensus: List[str]
    disagreements: List[str]
    missing_perspectives: List[str]
    summary: str