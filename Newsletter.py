from flask import Flask, render_template, request
import requests
from deep_translator import GoogleTranslator
import datetime
import os

app = Flask(__name__)

API_KEY = "24a1ef3f46d11aaf11c3405670a30c20"

CATEGORIES = {
    'headlines': 'general',
    'finance': 'business',
    'jobs': 'general',    # fallback to 'general' if not supported
    'notices': 'general'  # fallback to 'general' if not supported
}

LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German'
}

def fetch_news(category='headlines', lang='en'):
    try:
        endpoint = f"https://gnews.io/api/v4/top-headlines?category={CATEGORIES.get(category, 'general')}&lang={lang}&token={API_KEY}"
        print(f"Fetching: {endpoint}")

        res = requests.get(endpoint)
        res.raise_for_status()
        data = res.json()
        articles = data.get("articles", [])
        print(f"Got {len(articles)} articles")

        # Translate titles only if lang is not English
        if lang != 'en':
            for article in articles:
                try:
                    translated = GoogleTranslator(source='auto', target=lang).translate(article['title'])
                    article['title'] = translated
                except Exception as e:
                    print(f"Translation failed: {e}")

        return articles

    except Exception as e:
        print(f"Failed to fetch news: {e}")
        return []

@app.route("/")
def home():
    category = request.args.get("segment", "headlines")  # match frontend param name
    selected_lang = request.args.get("lang", "en")
    news_articles = fetch_news(category=category, lang=selected_lang)

    return render_template(
        "index.html",
        news=news_articles,
        languages=LANGUAGES,
        current_language=selected_lang,  # match your HTML template vars
        current_segment=category,
        time=datetime.datetime.now()
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
