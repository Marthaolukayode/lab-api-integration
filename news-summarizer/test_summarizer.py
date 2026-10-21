
from news_api import fetch_tech_news
from summarizer import NewsSummarizer

# Test (commented out to avoid API calls)

news_summarizer = NewsSummarizer()

print("Fetching and processing news...\n")

results = news_summarizer.process_news(limit=2)

for i, result in enumerate(results, start=1):
    print(f"Article {i}")
    print(f"Title: {result['topic']}")
    print(f"Summary: {result['content']}")
    print(f"Sentiment: {result['review']}")
    print("-" * 50)

print(f"\nTotal processed: {news_summarizer.total_processed}")

# result = generate_and_review("artificial intelligence")
# print("✅ Generate and review complete!")