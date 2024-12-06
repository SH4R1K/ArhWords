import requests
from bs4 import BeautifulSoup

# URL страницы, которую вы хотите парсить
url = 'https://xn--b1afb8babli.xn--p1ai/tur/newgodarh2025'  # Замените на нужный URL

# Получаем HTML-код страницы
response = requests.get(url)

# Проверяем, что запрос успешен
if response.status_code == 200:
    # Парсим HTML-код с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все блоки <p> с нужными атрибутами
    paragraphs = soup.find_all('p')

    # Извлекаем текст из найденных блоков
    for p in paragraphs:
        text = p.get_text()
        print(text)
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")
