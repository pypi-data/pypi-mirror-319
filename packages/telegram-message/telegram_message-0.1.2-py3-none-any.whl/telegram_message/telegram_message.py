import requests

def send(bot_token: str, chat_id: str, message: str = "no notification") -> None:
    """
    Відправляє повідомлення в Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
        }
    requests.post(url, json=payload, timeout=10)