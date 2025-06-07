from flask import Flask, render_template, request
import requests
from deep_translator import GoogleTranslator
import datetime
import os

app = Flask(__name__)

API_KEY = "24a1ef3f46d11aaf11c3405670a30c20"

CATEGORIES = {
    'headlines': 'top-headlines',
    'finance': 'business',
    'jobs': 'jobs',
    'notices': 'nation'
}

LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German'
}

def fetch_news(category='headlines', lang='en'):
    endpoint = f"https://gnews.io/api/v4/top-headlines?category={CATEGORIES.get(category, 'general')}&lang={lang}&token={API_KEY}"
    res = requests.get(endpoint)
    articles = res.json().get("articles", [])

    # Translate only title if language is not English
    if lang != 'en':
        for article in articles:
            try:
                translated = GoogleTranslator(source='auto', target=lang).translate(article['title'])
                article['title'] = translated
            except:
                continue
    return articles

@app.route("/")
def home():
    category = request.args.get("category", "headlines")
    selected_lang = request.args.get("lang", "en")
    news_articles = fetch_news(category=category, lang=selected_lang)

    return render_template(
        "index.html",
        news=news_articles,
        languages=LANGUAGES,
        selected=selected_lang,
        category=category,
        time=datetime.datetime.now()
    )

# 👇 Required for Render hosting
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # For Render or local
    app.run(host="0.0.0.0", port=port)
