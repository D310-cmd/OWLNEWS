from flask import Flask, render_template, request
import requests
from deep_translator import GoogleTranslator

app = Flask(__name__)

API_KEY = "24a1ef3f46d11aaf11c3405670a30c20"  
GNEWS_BASE = "https://gnews.io/api/v4/search"

# Available language options
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German"
}

# News segments and corresponding GNews queries
SEGMENT_QUERIES = {
    "headlines": "top news",
    "finance": "finance OR stock OR economy",
    "jobs": "jobs OR hiring OR career",
    "notices": "school OR exam OR notice OR education"
}


@app.route('/')
def home():
    segment = request.args.get('segment', 'headlines')
    lang = request.args.get('lang', 'en')
    query = SEGMENT_QUERIES.get(segment, 'top news')

    params = {
        'q': query,
        'token': API_KEY,
        'lang': 'en',  # Always fetch in English, then translate
        'max': 10
    }

    response = requests.get(GNEWS_BASE, params=params)
    data = response.json()
    articles = data.get("articles", [])

    if lang != 'en':
        for article in articles:
            try:
                article['title'] = GoogleTranslator(source='auto', target=lang).translate(article['title'])
                article['description'] = GoogleTranslator(source='auto', target=lang).translate(article['description'])
            except Exception as e:
                print("Translation failed:", e)

    return render_template(
        "index.html",
        articles=articles,
        current_segment=segment,
        current_language=lang,
        languages=LANGUAGES
    )


if __name__ == '__main__':
    app.run(debug=True)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Use the PORT environment variable or default to 10000
    app.run(host="0.0.0.0", port=port)
