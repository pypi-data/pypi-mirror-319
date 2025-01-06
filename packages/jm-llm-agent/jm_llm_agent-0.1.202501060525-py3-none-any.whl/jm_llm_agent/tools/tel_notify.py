import requests


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    response = requests.get(url, params=params)
    return response.json()


def send_trade_notification(msg: str):
    # 设置你的 Telegram bot token 和 chat ID
    bot_token = "7391784238:AAHB8nkTWqCWs5uJJxM25ZW-TRwR6fLPYZI"
    chat_id = "5627190886"
    send_telegram_message(bot_token, chat_id, msg)
