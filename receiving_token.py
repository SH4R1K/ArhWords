import requests

def get_access_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '57372e62-86c7-4a21-962d-7b0e3376751b',
        'Authorization': 'Basic key'  # Замените 'key' на ваш реальный ключ
    }

    # Отключение проверки SSL
    response = requests.post(url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None