import os

import requests
from dotenv import load_dotenv

def get_access_token(env_path):
    dotenv_path = env_path
    load_dotenv(dotenv_path=dotenv_path)
    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"Файл .env не найден по пути: {dotenv_path}")

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '57372e62-86c7-4a21-962d-7b0e3376751b',
        'Authorization': f"Basic {os.getenv('API_KEY')}"  # Замените 'key' на ваш реальный ключ
    }

    # Отключение проверки SSL
    response = requests.post(url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None