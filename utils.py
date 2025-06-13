import os
import requests

def send_telegram(message):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"
    data = {
        "chat_id": str(os.getenv("TELEGRAM_ID")),
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

def predict_next_candle(candles):
    ups = sum(1 for c in candles if c.get("close", 0) > c.get("open", 0))
    downs = sum(1 for c in candles if c.get("close", 0) < c.get("open", 0))
    if ups > downs: return "put"
    if downs > ups: return "call"
    return "doji"
