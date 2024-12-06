import os
import string
from os import path

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import nltk
from flask import Flask, send_file, request
import text_module as tm
import io
import requests  # Импортируем библиотеку requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# URL для обращения к GigaChat API
GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
AVAILABLE_COLORMAPS = [
    "Wisteria", "Reds", "afmhot", "Purples", "RdPu",
    "gnuplot", "PRGn", "Greens", "Blues", "RdBu",
    "Greys", "cool", "Dark2", "brg", "winter",
    "spring", "plasma", "magma", "hot"
]

AVAILABLE_FONTS = {
    "HachiMaruPop", "Pacifico", "Lobster", "Comfortaa", "Overpass"
}

# Чтение списка матерных слов из файла
def load_bad_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        bad_words = file.read().splitlines()
    return bad_words

# Функция для предварительной обработки текста
def preprocess_text(text):
    bad_words = load_bad_words('bad_words.txt')

    # Приведение к нижнему регистру
    text = text.lower()
    # Удаление пунктуации
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', string.ascii_letters))

    words = text.split()
    words = [word for word in words if word not in bad_words]
    return ' '.join(words)

@app.route('/wordCloudGpt', methods=['POST'])
def wordCloudGpt():
    # Загрузка стоп-слов NLTK
    nltk.download('stopwords', quiet=True)

    data = request.get_json()

    if not data or 'text' not in data:
        return {"error": "no text found in request"}, 400

    # parameters for wordCloud
    min_font_size = data.get('min_font_size', 4)
    max_font_size = data.get('max_font_size', None)
    max_words = data.get('max_words', 100)
    theme = data.get('theme', "black")
    colormap = data.get('colormap', None)
    font_family = data.get('font_family', None)

    if colormap not in AVAILABLE_COLORMAPS and colormap is not None:
        return {"error": f"Invalid colormap. Choose one of {AVAILABLE_COLORMAPS}"}, 400

    if theme not in ["black", "white"]:
        return {"error": "theme must be 'black' or 'white'"}, 400

    # Чтение текста
    text = data['text']

    text = preprocess_text(text)
    # Получение ключевых слов и весов с помощью GigaChat API
    keywords_with_weights = get_keywords(text)

    # Проверка, если keywords_with_weights пуст
    if not keywords_with_weights:
        return {"error": "No keywords returned from API"}, 500

    # Преобразование результата в словарь
    weights = {}
    for line in keywords_with_weights.splitlines():
        line = line.strip()
        if ':' in line:
            try:
                word, weight = line.split(':', 1)
                weights[word.strip()] = float(weight.strip())
            except ValueError:
                continue  # Игнорируем строки с неправильным форматом

    # Проверка, если weights пуст
    if not weights:
        return {"error": "No valid keywords found"}, 500

    # Получение директории данных
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    try:
        mask_image = np.array(Image.open(path.join(d, 'mask.png')))
    except Exception as e:
        return {"error": f"Error loading mask image: {str(e)}"}, 500

    try:
        # Генерация изображения облака слов с маской и стоп-словами
        wordcloud = WordCloud(
            font_path="./fonts/" + font_family + ".ttf" if font_family is not None else None,
            mask=mask_image,
            background_color=theme,
            contour_width=1,
            stopwords=STOPWORDS,
            max_words=max_words,
            min_font_size=min_font_size,
            max_font_size=max_font_size,
            relative_scaling=0,
            colormap=colormap,
            contour_color="white" if theme == "white" else "black",
        ).generate_from_frequencies(weights)
    except Exception as e:
        return {"error": f"Error generating word cloud: {str(e)}"}, 500

    img_io = io.BytesIO()
    wordcloud.to_image().save(img_io, format='PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


def get_keywords(text):
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '}

    payload = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": "Ты лингвист и эксперт в области туризма."
            },
            {
                "role": "user",
                "content": f"Пожалуйста, выпиши ключевые слова и словосочетания, связанные с темой 'Новогодний туризм в Архангельской области'. Формат: слово(словосочетание):вес из вот этого текста: {text}."
            }
        ],
        "stream": False,
        "update_interval": 0
    }

    try:
        response = requests.post(GIGACHAT_API_URL, headers=headers, json=payload, verify='russian_trusted_root_ca.cer')
        response.raise_for_status()  # Проверяем на ошибки HTTP

        # Логируем текст ответа
        print("Response text:", response.text)

        keywords_data = response.json()
        print(keywords_data)  # Для отладки

        # Проверяем, есть ли ключевые слова в ответе
        if 'choices' in keywords_data and len(keywords_data['choices']) > 0:
            keywords = keywords_data['choices'][0]['message']['content'].split(', ')
            # Присваиваем каждому слову вес 1.0
            return '\n'.join([f"{keyword}:1.0" for keyword in keywords])  # Форматируем в нужный вид
        else:
            print("No 'choices' field in the response.")
            return ""
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return ""
    except Exception as err:
        print(f"An error occurred: {err}")
        return ""

@app.route('/wordCloud', methods=['POST'])
def wordCloud():
    # Загрузка стоп-слов NLTK
    nltk.download('stopwords', quiet=True)

    data = request.get_json()

    if not data or 'text' not in data:
        return {"error": "no text found in request"}, 400

    # parameters for wordCloud
    min_font_size = data.get('min_font_size', 4)
    max_font_size = data.get('max_font_size', None)
    max_words = data.get('max_words', 100)
    theme = data.get('theme', "black")
    colormap = data.get('colormap', None)
    font_family = data.get('font_family', None)

    if colormap not in AVAILABLE_COLORMAPS and colormap is not None:
        return {"error": f"Invalid colormap. Choose one of {AVAILABLE_COLORMAPS}"}, 400

    if font_family not in AVAILABLE_FONTS and font_family is not None:
        return {"error": f"Invalid font_family. Choose one of {AVAILABLE_FONTS}"}, 400

    if theme not in ["black", "white"]:
        return {"error": "theme must be 'black' or 'white'"}, 400

    # Чтение текста
    text = data['text']
    slovosochetaniya = " ".join(tm.get_slovosochetaniya(text))
    normal_text = tm.get_text_in_normal_form(text)
    text = slovosochetaniya + f" {normal_text}"
    text = preprocess_text(text)  # Предварительная обработка текста
    # Получение стоп-слов на русском языке
    russian_stopwords = set(stopwords.words('russian'))
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

    # Получение директории данных
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    try:
        mask_image = np.array(Image.open(path.join(d, 'mask.png')))
    except Exception as e:
        return {"error": f"Error loading mask image: {str(e)}"}, 500

    try:
        # Генерация изображения облака слов с маской и стоп-словами
        wordcloud = WordCloud(
            font_path="./fonts/" + font_family + ".ttf" if font_family is not None else None,
            mask=mask_image,
            background_color=theme,
            contour_width=1,
            stopwords=STOPWORDS,
            max_words=max_words,
            min_font_size=min_font_size,
            max_font_size=max_font_size,
            relative_scaling=0,
            colormap=colormap,
            contour_color="white" if theme == "white" else "black",
        ).generate_from_frequencies(weights)
    except Exception as e:
        return {"error": f"Error generating word cloud: {str(e)}"}, 500

    img_io = io.BytesIO()
    wordcloud.to_image().save(img_io, format='PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
