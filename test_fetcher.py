"""Test the news fetcher"""

from src.news_fetcher import NewsFetcher

if __name__ == "__main__":
    print("Testing News Fetcher...\n")
    
    fetcher = NewsFetcher()
    
    # Fetch articles about a recent AI topic
    articles = fetcher.fetch_articles(
        query="AI safety governance",
        num_articles=8,
        days_back=7
    )
    
    if articles:
        print(f"Found {len(articles)} articles:\n")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article}")
            print(f"   URL: {article.url}")
            print(f"   Published: {article.published_at}")
            print()
    else:
        print("No articles found!")