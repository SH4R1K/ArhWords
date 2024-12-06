import requests
from bs4 import BeautifulSoup

url = 'http://news.hahatun.fun/'  

# Получаем HTML-код страницы
def ParseSite():
    response = requests.get(url)

    # Проверяем, что запрос успешен
    if response.status_code == 200:
        # Устанавливаем кодировку вручную, если это необходимо
        response.encoding = response.apparent_encoding  # Устанавливаем кодировку на основе анализа содержимого

        # Парсим HTML-код с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все блоки <p> с нужными атрибутами
        paragraphs = soup.find_all('p', {"class": "news"})
        text = ""
        # Извлекаем текст из найденных блоков
        for p in paragraphs:
            text = text + p.get_text()
        return text
    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")
