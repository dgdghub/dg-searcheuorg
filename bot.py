import requests
from config import Config

token = Config.TG_TOKEN
chat_id = Config.TG_CHAT_ID

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

