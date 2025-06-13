import os
import time
import requests
from dotenv import load_dotenv
from utils import predict_next_candle, send_telegram

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.exnova.com/v1"

def get_candles():
    try:
        response = requests.get(
            f"{BASE_URL}/quotes/history",
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={
                "asset": "EURUSD",
                "interval": 60,
                "limit": 3
            }
        )
        candles = response.json().get("data", [])
        return candles
    except Exception as e:
        print(f"Erro ao obter velas: {e}")
        return []

def main_loop():
    while True:
        candles = get_candles()
        if len(candles) == 3:
            signal = predict_next_candle(candles)
            if signal != "doji":
                send_telegram(f"SINAL ENVIADO: *{signal.upper()}* ⏱️ 1 minuto")
            else:
                print("Doji detectado, sinal ignorado.")
        else:
            print("Velas insuficientes para prever.")
        time.sleep(120)  # Espera 2 minutos

if __name__ == "__main__":
    main_loop()
    
