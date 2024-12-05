import os
from os import path
import flask
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import nltk
from flask import Flask, send_file, request
import io
import requests  # Импортируем библиотеку requests

app = Flask(__name__)

# URL для обращения к GigaChat API
GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
@app.route('/wordCloud', methods=['POST'])
def wordCloud():
    # Загрузка стоп-слов NLTK
    nltk.download('stopwords', quiet=True)

    data = request.get_json()

    if not data or 'text' not in data:
        return {"error": "no text found in request"}, 400
    
    # Чтение текста
    text = data['text']
    print(f"Received text: {text}")  # Логируем полученный текст

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

    min_font_size = data.get('min_font_size', 4)
    max_font_size = data.get('max_font_size', None)
    max_words = data.get('max_words', 100)
    theme = data.get('theme', "black")

    if theme not in ["black", "white"]:
        return {"error": "theme must be 'black' or 'white'"}, 400

    # Получение директории данных
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    try:
        mask_image = np.array(Image.open(path.join(d, 'mask.png')))
    except Exception as e:
        return {"error": f"Error loading mask image: {str(e)}"}, 500

    try:
        # Генерация изображения облака слов с маской и стоп-словами
        wordcloud = WordCloud(
            mask=mask_image,
            contour_color=theme,
            contour_width=1,
            stopwords=STOPWORDS,
            max_words=max_words,
            min_font_size=min_font_size,
            max_font_size=max_font_size,
            relative_scaling=0,
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
        'Authorization': 'Bearer key'  # Замените на ваш токен
    }
    
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
        
        # Логируем текст запроса и ответа
        print("Request payload:", payload)
        print("Response text:", response.text)  # Логируем текст ответа
        
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
