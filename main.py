import os
from os import path
import flask
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import nltk
from nltk.corpus import stopwords
from flask import Flask, send_file, request
import io


app = Flask(__name__)

@app.route('/wordCloud', methods=['POST'])
def wordCloud():
    # Загрузка стоп-слов NLTK
    nltk.download('stopwords')

    data = request.get_json()

    if not data or 'text' not in data:
        return {"error": "no text found in request"}, 400

    text = data['text']
    min_font_size = data.get('min_font_size', 4)
    max_font_size = data.get('max_font_size', None)
    max_words = data.get('max_words', 100)
    theme = data.get('theme', "black")

    if theme not in ["black", "white"]:
        return {"error": "theme must be 'black' or 'white'"}, 400

    # get data directory
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    try:
        mask_image = np.array(Image.open(path.join(d, 'mask.png')))
    except Exception as e:
        return {"error": f"Error loading mask image: {str(e)}"}, 500

    # Получение стоп-слов на русском языке
    russian_stopwords = set(stopwords.words('russian'))

    # Определение пользовательских стоп-слов (опционально)
    custom_stopwords = set(STOPWORDS).union(russian_stopwords).union(
        {"и", "в", "на", "с", "что", "как", "это", "по", "к", "для", "из", "но", "так", "же", "от", "то", "все",
         "также"})

    try:
        # Generate a word cloud image with the mask and stop words
        wordcloud = WordCloud(
            mask=mask_image,
            contour_color=theme,
            contour_width=1,
            stopwords=custom_stopwords,
            max_words=max_words,
            min_font_size=min_font_size,
            max_font_size=max_font_size,
        ).generate(text)
    except Exception as e:
        return {"error": f"Error generating word cloud: {str(e)}"}, 500

    img = wordcloud.to_image()

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)

    return flask.send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
