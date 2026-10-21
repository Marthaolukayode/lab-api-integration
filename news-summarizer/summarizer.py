from news_api import fetch_tech_news
from llm_providers import (
    ask_openai,
    ask_cohere
)

class NewsSummarizer:
    """Coordinates news fetching, summarization, and sentiment analysis."""

    def __init__(self):
        self.total_processed = 0

    def process_news(self, limit=2):
        """Fetch and process multiple news articles."""

        articles = fetch_tech_news(limit)        
        results = []

        for i, article in enumerate(articles, start=1):
            print(article['title'])
            result = self.process_article_and_review(text)
            results.append(result)

        return results

    def process_article_and_review(self, topic):
        """
        Use OpenAI to generate content, then Anthropic to review it.
        Tracks token usage from both API calls.
    
        Args:
            topic: Topic to write about
        
        Returns:
            Dictionary with content, review, and usage data
        """
        # Step 1: Generate content with OpenAI
        print(f"Step 1: Generating content about '{topic}' with OpenAI...")
        content_prompt = f"Write a short paragraph about {topic}"
        openai_result = ask_openai(content_prompt)
        content = openai_result['response']
        print(f"Content: {content}")
        print(f"OpenAI Usage: {openai_result['usage']}\n")
        
        # Step 2: Review with Anthropic
        print("Step 2: Reviewing with Anthropic...")
        review_prompt = f"""Analyze the sentiment of the following news text:

    {content}
    
    Provide:
    1. What's good about it
    2. What could be improved
    3. A rating out of 10"""
    
        cohere_result = ask_cohere(review_prompt)
        review = cohere_result['response']
        print(f"Review: {review}")
        print(f"Anthropic Usage: {cohere_result['usage']}\n")
    
        return {
            "topic": topic,
            "content": content,
            "review": review,
            "usage": {
                "openai": openai_result['usage'],
                "cohere": cohere_result['usage']
            }
        }

    
    

    

    # Test (commented out to avoid API calls)
    # result = generate_and_review("artificial intelligence")
    # print("✅ Generate and review complete!")   

if __name__ == "__main__":

    summarizer = NewsSummarizer()

    print("Fetching and processing news...\n")

    results = summarizer.process_news(limit=2)

    for i, result in enumerate(results, start=1):
        print(f"Article {i}")
        print(f"Title: {result['title']}")
        print(f"Summary: {result['summary']}")
        print(f"Sentiment: {result['sentiment']}")
        print("-" * 50)

    print(f"\nTotal processed: {summarizer.total_processed}")
