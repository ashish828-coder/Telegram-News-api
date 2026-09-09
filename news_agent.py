

import os
import requests

# ---- CONFIG ----
NEWS_API_KEY = ""
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

COUNTRY = os.environ.get("COUNTRY", "us")           # 'in' = India
CATEGORY = os.environ.get("CATEGORY", "general")    # business, tech, sports, etc.
# ----------------

def get_top_headlines():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": COUNTRY,
        "category": CATEGORY,
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    articles = data.get("articles", [])
    if not articles:
        return "📰 No news found today."

    lines = ["📰 *Today's Top Headlines*\n"]
    for i, article in enumerate(articles, start=1):
        title = article["title"]
        link = article["url"]
        lines.append(f"{i}. [{title}]({link})")

    return "\n".join(lines)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    response = requests.post(url, data=payload, timeout=10)
    response.raise_for_status()
    return response.json()

def main():
    try:
        news_message = get_top_headlines()
        send_telegram_message(news_message)
        print("News message sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()