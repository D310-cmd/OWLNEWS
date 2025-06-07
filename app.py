from flask import Flask, render_template, request
import requests
from deep_translator import GoogleTranslator
import datetime
import os

app = Flask(__name__)

API_KEY = os.getenv("NEWSAPI_KEY", "649e90417a664d8e895c4a9ca06fdd12")  
CATEGORIES = {
    'headlines': 'general',
    'finance': 'business',
    'jobs': 'technology',  # NewsAPI doesn't have 'jobs'; using 'technology' as a placeholder
    'notices': 'general'
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
        url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"category={CATEGORIES.get(category, 'general')}&"
            f"language=en&"  # Always fetch in English, then translate if needed
            f"pageSize=20&"
            f"apiKey={API_KEY}"
        )
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        articles = data.get("articles", [])
        for article in articles:
            article['source'] = {'name': article.get('source', {}).get('name', 'Unknown')}
            if lang != 'en':
                try:
                    article['title'] = GoogleTranslator(source='auto', target=lang).translate(article['title'])
                    if article.get('description'):
                        article['description'] = GoogleTranslator(source='auto', target=lang).translate(article['description'])
                except Exception as e:
                    print(f"Translation error: {e}")
        return articles

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

@app.route("/")
def home():
    segment = request.args.get("segment", "headlines")
    selected_lang = request.args.get("lang", "en")
    news_articles = fetch_news(category=segment, lang=selected_lang)

    return render_template(
        "index.html",
        news=news_articles,
        languages=LANGUAGES,
        current_language=selected_lang,
        current_segment=segment,
        time=datetime.datetime.now()
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
