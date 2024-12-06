# ArhWords

ArhWords — это веб-API для генерации тематических облаков слов на основе переданного текста. Облака слов позволяют визуализировать важность и частоту слов в тексте, что может быть полезно для анализа данных, маркетинговых целей и многого другого.

## Команда разработчиков

- [@SH4R1K](https://github.com/SH4R1K) - Разработчик
- [@Pluhenciya](https://github.com/Pluhenciya) - Разработчик
- [@Morokenec](https://github.com/Morokenec) - Менеджер
- [@Meresk](https://www.github.com/Meresk) - Разработчик
- [@hhallva](https://github.com/hhallva) - Дизайнер

## Стек технологий

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Natasha](https://img.shields.io/badge/Natasha-FF6347?style=for-the-badge&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-FFD700?style=for-the-badge&logo=python&logoColor=black)
![WordCloud](https://img.shields.io/badge/WordCloud-FFB300?style=for-the-badge&logo=python&logoColor=black)
![NLTK](https://img.shields.io/badge/NLTK-3E5B9A?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![GigaChat](https://img.shields.io/badge/GigaChat-016c3e?style=for-the-badge&logo=chat&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)



## Установка

Для использования ArhWords вам потребуется Python, установка зависимостей, получение API ключа GigaChat для работы модуля с интеграцией GPT. Следуйте этим шагам:

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/sh4r1k/ArhWords.git
   ```
2. Перейдите в директорию с проектом:
   ```bash
   cd ArhWords
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Получить API ключ [GigaChat](https://developers.sber.ru/portal/products/gigachat-api)
5. Создайте файл окружения `dev.env` на основе [dev.env.example](dev.env.example) и запишите туда свой ключ
6. Запустите API:
   ```bash
   python main.py
   ```



## Использование
Вы можете воспользоваться уже готовой реализацией веб-сайта с интеграцией нашего API. Откройте [index.html](./ArhWordsWeb/index.html) в [ArhWordsWeb](./ArhWordsWeb/). 

## Эндпоинты

### 1. `/wordCloudGpt`

**Метод:** `POST`

**--- Работает только при наличии API ключа GigaChat ---**

**Описание:** Этот эндпоинт принимает текст и генерирует облако слов, используя ключевые слова, полученные через GigaChat API. Он позволяет настраивать параметры облака слов, такие как размер шрифта, цветовая схема и маска. 

**Запрос:**

- **Тело запроса (JSON):**
  ```json
  {
    "text": "Ваш текст здесь",
    "min_font_size": 4,
    "max_font_size": null,
    "max_words": 100,
    "theme": "black",
    "contour": false,
    "colormap": null,
    "font_family": null,
    "mask_type": "mask_type1"
  }

**Параметры:**

| Параметр       | Тип          | Описание                                                                 |
|----------------|--------------|--------------------------------------------------------------------------|
| `text`         | *обязательный* | Текст для анализа.                                                      |
| `min_font_size`| *необязательный* | Минимальный размер шрифта (по умолчанию 4).                            |
| `max_font_size`| *необязательный* | Максимальный размер шрифта (по умолчанию `null`).                     |
| `max_words`    | *необязательный* | Максимальное количество слов в облаке (по умолчанию 100).              |
| `theme`        | *необязательный* | Цветовая схема облака слов (`black` или `white`, по умолчанию `black`).|
| `contour`      | *необязательный* | Флаг для отображения контура (по умолчанию `false`).                  |
| `colormap`     | *необязательный* | Цветовая карта для облака слов (по умолчанию `null`).                 |
| `font_family`  | *необязательный* | Шрифт для облака слов (по умолчанию `null`).                          |
| `mask_type`    | *необязательный* | Тип маски для облака слов (по умолчанию `mask_type1`).                |

### 2. `/wordCloud`

**Метод:** `POST`

**Описание:** Этот эндпоинт принимает текст и генерирует облако слов, используя TF-IDF для определения весов слов и словосочетаний. Он также позволяет настраивать параметры облака слов.

**Запрос:**

- **Тело запроса (JSON):**
  ```json
  {
    "text": "Ваш текст здесь",
    "min_font_size": 4,
    "max_font_size": null,
    "max_words": 100,
    "theme": "black",
    "contour": false,
    "colormap": null,
    "font_family": null,
    "mask_type": "mask_type1"
  }

**Параметры:**

| Параметр       | Тип          | Описание                                                                 |
|----------------|--------------|--------------------------------------------------------------------------|
| `text`         | *обязательный* | Текст для анализа.                                                      |
| `min_font_size`| *необязательный* | Минимальный размер шрифта (по умолчанию 4).                            |
| `max_font_size`| *необязательный* | Максимальный размер шрифта (по умолчанию `null`).                     |
| `max_words`    | *необязательный* | Максимальное количество слов в облаке (по умолчанию 100).              |
| `theme`        | *необязательный* | Цветовая схема облака слов (`black` или `white`, по умолчанию `black`).|
| `contour`      | *необязательный* | Флаг для отображения контура (по умолчанию `false`).                  |
| `colormap`     | *необязательный* | Цветовая карта для облака слов (по умолчанию `null`).                 |
| `font_family`  | *необязательный* | Шрифт для облака слов (по умолчанию `null`).                          |
| `mask_type`    | *необязательный* | Тип маски для облака слов (по умолчанию `mask_type1`).                |

## Доступные цветовые палитры

Ниже представлен список доступных цветовых палитр, которые можно использовать:

- **Reds**
- **afmhot**
- **Purples**
- **RdPu**
- **gnuplot**
- **PRGn**
- **Greens**
- **Blues**
- **RdBu**
- **Greys**
- **cool**
- **Dark2**
- **brg**
- **winter**
- **spring**
- **plasma**
- **magma**
- **hot**
