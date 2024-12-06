import requests

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload = {
    'scope': 'GIGACHAT_API_PERS'
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': '57372e62-86c7-4a21-962d-7b0e3376751b',
    'Authorization': 'Basic ZGQxYjgzNzktZjQ5OC00ZWNkLWExYTEtMmQyMzVhMzlkN2Q0OjgyMjM2OTA0LTQ4NjUtNDA5NC04YWMxLWE5ZjA4MmViZWEzNQ=='
}

# Отключение проверки SSL
response = requests.post(url, headers=headers, data=payload, verify=False)

print(response.text)
