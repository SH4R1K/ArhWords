from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Настройка драйвера (например, Chrome)
driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver

# Открываем страницу
url = 'https://pomorland.travel/what-to-see/?TYPES=attractions'
driver.get(url)

# Ждем, пока кнопка "Загрузить еще" станет доступной
try:
    while True:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'load-more'))
        )
        load_more_button.click()  # Нажимаем на кнопку
        time.sleep(2)  # Ждем, пока данные загрузятся
except Exception as e:
    print("Больше нет кнопки 'Загрузить еще' или произошла ошибка:", e)

# Получаем HTML-код страницы после загрузки всех данных
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Находим все блоки с нужными данными
paragraphs = soup.find_all('div', {'class': 'tiles-list__info__title'})

# Извлекаем текст из найденных блоков
for p in paragraphs:
    text = p.get_text()
    print(text)

# Закрываем драйвер
driver.quit()
