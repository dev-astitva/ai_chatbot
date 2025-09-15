import requests
from gemini import chat_gemini
from config import load_conf

conf = load_conf()
NEWS_API_KEY = conf["news_api_key"]

def fetch_news(topic, max_articles=3):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&language=en&pageSize={max_articles}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles

def summarize_article(title, desc, pref):
    prompt = f"Summarize for a user interested in {pref}: Title: {title}. {desc}"
    return chat_gemini(prompt)

def get_news(preferences):
    summary_list = []
    topics = [t.strip() for t in preferences.split(",")]
    for topic in topics:
        articles = fetch_news(topic)
        for article in articles:
            summary = summarize_article(article["title"], article.get("description", ""), topic)
            summary_list.append(
                f"Topic: {topic}\nTitle: {article['title']}\n{summary}\nLink: {article['url']}"
            )
    return "\n\n".join(summary_list)
