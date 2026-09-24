"""Fetch articles from NewsAPI"""

import os
import requests
from datetime import datetime, timedelta
from typing import List
from dotenv import load_dotenv
from src.models import Article

load_dotenv()


class NewsFetcher:
    """Fetches articles from NewsAPI"""
    
    def __init__(self):
        self.api_key = os.getenv("NEWSAPI_KEY")
        if not self.api_key:
            raise ValueError("NEWSAPI_KEY not found in .env file")
        self.base_url = "https://newsapi.org/v2"
    
    def fetch_articles(
        self,
        query: str,
        num_articles: int = 10,
        days_back: int = 7,
        sources: Optional[List[str]] = None
    ) -> List[Article]:
        """
        Fetch articles about a topic from multiple sources.
        
        Args:
            query: Search topic (e.g., "AI safety")
            num_articles: Number of articles to fetch
            days_back: How many days back to search
            sources: Specific sources to search (optional)
        
        Returns:
            List of Article objects
        """
        
        # Default sources for AI news coverage
        if sources is None:
            sources = [
                "bbc-news",
                "cnn",
                "techcrunch",
                "the-verge",
                "wired",
                "the-washington-post",
                "the-new-york-times"
            ]
        
        articles = []
        
        # Calculate date range
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        try:
            # Fetch from each source
            for source in sources:
                print(f"Fetching from {source}...")
                
                params = {
                    "apiKey": self.api_key,
                    "sources": source,
                    "q": query,
                    "sortBy": "publishedAt",
                    "language": "en",
                    "pageSize": max(3, num_articles // len(sources))
                }
                
                response = requests.get(
                    f"{self.base_url}/everything",
                    params=params,
                    timeout=10
                )
                
                if response.status_code != 200:
                    print(f"  ⚠️  Error fetching from {source}: {response.status_code}")
                    continue
                
                data = response.json()
                
                if data.get("articles"):
                    for article_data in data["articles"]:
                        # Skip articles with missing content
                        if not article_data.get("content"):
                            continue
                        
                        article = Article(
                            source_name=article_data.get("source", {}).get("name", "Unknown"),
                            title=article_data.get("title", "No title"),
                            url=article_data.get("url", ""),
                            content=article_data.get("content", ""),
                            published_at=datetime.fromisoformat(
                                article_data.get("publishedAt", "").replace("Z", "+00:00")
                            ),
                            author=article_data.get("author"),
                            image_url=article_data.get("urlToImage")
                        )
                        articles.append(article)
            
            print(f"\n✅ Fetched {len(articles)} articles total\n")
            return articles[:num_articles]
        
        except Exception as e:
            print(f"❌ Error fetching articles: {e}")
            return []


# Optional type hint import
from typing import Optional