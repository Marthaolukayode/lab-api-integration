import requests

from config import NEWS_API_KEY, REQUEST_TIMEOUT

def fetch_tech_news(limit=3):
    """Fetch technology news articles from NewsAPI."""

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "category": "technology",
        "language": "en",
        "pageSize": limit,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(
        url,
        params=params,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    data = response.json()

    return data.get("articles", [])


if __name__ == "__main__":
    articles = fetch_tech_news(3)

    print(f"Fetched {len(articles)} articles:\n")

    for i, article in enumerate(articles, start=1):
        print(f"{i}. {article['title']}")