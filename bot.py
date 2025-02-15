import requests

token = '7226776764:AAE2SKaTIn2hjS8ZegIVr4inzuOmHYmJkT8'
chat_id = '6122087405'
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()


