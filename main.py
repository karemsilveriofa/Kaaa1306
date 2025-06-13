import os
import time
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_ID = os.getenv("TELEGRAM_ID")

# Configurar log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_double_max_signal():
    agora = datetime.now()
    rodada = f"Rodada {agora.strftime('%H:%M')}"
    sugestao = "🎯 Sinal: Apostar em Branco ou Vermelho 🔴⚪️"
    return f"{rodada}\n{sugestao}"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.ok

def run_bot():
    logging.info("Bot iniciado...")
    while True:
        try:
            sinal = get_double_max_signal()
            sucesso = send_telegram_message(sinal)
            if sucesso:
                logging.info("Sinal enviado com sucesso.")
            else:
                logging.error("Erro ao enviar sinal.")
            time.sleep(120)  # Espera 2 minutos
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()