#!/usr/bin/env python
"""
Word Cloud with Custom Shape and TF-IDF Weights (Including N-grams)
========================================================

Generating a word cloud from the US constitution using a custom shape and TF-IDF weights, including n-grams.
"""
import os
from os import path

import flask
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from flask import Flask, send_file, request
import io

app = Flask(__name__)

# Функция для предварительной обработки текста
def preprocess_text(text):
    # Приведение к нижнему регистру
    text = text.lower()
    # Удаление пунктуации
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

@app.route('/wordCloud', methods=['POST'])
def wordCloud():
    # Загрузка стоп-слов NLTK
    nltk.download('stopwords')

# Чтение текста
    text = open(path.join(d, 'constitution.txt'), encoding="utf8").read()
    text = preprocess_text(text)  # Предварительная обработка текста

# Загрузка маски
    mask_image = np.array(Image.open(path.join(d, 'black.png')))  # Замените 'black.png' на имя вашего файла маски
    data = request.get_json()

    if not data or 'text' not in data:
        return {"error": "no text found in request"}, 400

    # Определение пользовательских стоп-слов
    custom_stopwords = set(STOPWORDS).union(russian_stopwords)

    # Преобразование пользовательских стоп-слов в список
    custom_stopwords_list = list(custom_stopwords)

    # Применение TF-IDF с учетом биграмм
    vectorizer = TfidfVectorizer(stop_words=custom_stopwords_list, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()

    # Получение весов слов и словосочетаний
    weights = dict(zip(feature_names, tfidf_matrix.toarray()[0]))

    # Генерация облака слов с учетом весов
    wordcloud = WordCloud(mask=mask_image, contour_color='black', contour_width=1,
                        max_words=100, relative_scaling=0, normalize_plurals=False,
                        colormap='viridis').generate_from_frequencies(weights)  # Использование цветовой схемы

    # Отображение сгенерированного изображения
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    # Сохранение изображения облака слов в файл
    output_file = path.join(d, 'wordcloud_shape.png')
    wordcloud.to_file(output_file)

    print(f"Облако слов сохранено в файл: {output_file}")
    text = data['text']


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
        wordcloud = WordCloud(mask=mask_image, contour_color='black', contour_width=1,
                              stopwords=custom_stopwords, max_words=100).generate(text)
    except Exception as e:
        return {"error": f"Error generating word cloud: {str(e)}"}, 500

    img = wordcloud.to_image()

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)

    return flask.send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
