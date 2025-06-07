import time
import requests
import telegram
from datetime import datetime
from flask import Flask
import threading
import pytz

# === CONFIGURAÇÕES ===
API_KEY = "c95f42c34f934f91938f91e5cc8604a6"
TELEGRAM_TOKEN = "7239698274:AAFyg7HWLPvXceJYDope17DkfJpxtU4IU2Y"
TELEGRAM_ID = "6821521589"
INTERVALO = "1min"

bot = telegram.Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de sinais ativo!"

def obter_ativo():
    try:
        with open("ativo.txt", "r") as f:
            ativo = f.read().strip()
            print(f"[INFO] Ativo lido: {ativo}")
            return ativo
    except Exception as e:
        print(f"[ERRO] Falha ao ler ativo.txt: {e}")
        return "CAD/CHF"

def enviar_sinal(texto):
    try:
        bot.send_message(chat_id=TELEGRAM_ID, text=texto)
        print(f"[ENVIADO] {texto}")
    except Exception as e:
        print(f"[ERRO TELEGRAM] {e}")

def obter_candles(ativo):
    url = f"https://api.twelvedata.com/time_series?symbol={ativo}&interval={INTERVALO}&apikey={API_KEY}&outputsize=5"
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        print(f"[API] Resposta: {dados}")
        if "values" in dados:
            return dados["values"]
        else:
            erro = dados.get("message", "Erro desconhecido")
            enviar_sinal(f"❌ Erro na API para {ativo}: {erro}")
            return None
    except Exception as e:
        print(f"[ERRO API] {e}")
        return None

def calcular_sinal():
    ativo = obter_ativo()
    candles = obter_candles(ativo)

    if not candles or len(candles) < 3:
        msg = f"[AVISO] Dados insuficientes para {ativo}. Nenhum sinal gerado."
        print(msg)
        enviar_sinal(msg)
        return

    c1 = float(candles[2]['close'])  # 3 velas atrás
    c2 = float(candles[1]['close'])  # 2 velas atrás
    c3 = float(candles[0]['close'])  # última vela

    # Análise de tendência com 3 velas
    if c1 < c2 < c3:
        direcao = "📈 COMPRA"
        forca = abs((c3 - c1) / c1)
    elif c1 > c2 > c3:
        direcao = "📉 VENDA"
        forca = abs((c3 - c1) / c1)
    else:
        direcao = "⏸️ LATERAL"
        forca = 0

    # Filtro: só envia se a força for relevante (> 0.02%, ou seja, 0.0002)
    if forca < 0.0002:
        print(f"[FILTRO] Variação fraca: {forca:.5f}. Nenhum sinal enviado.")
        return

    horario_brasilia = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime('%H:%M:%S')

    mensagem = (
        f"SINAL DE ENTRADA 🔔\n"
        f"Ativo: {ativo}\n"
        f"Direção: {direcao}\n"
        f"Fechamentos: {c1:.5f} ➡ {c2:.5f} ➡ {c3:.5f}\n"
        f"Força: {forca:.5%}\n"
        f"Horário: {horario_brasilia}"
    )

    enviar_sinal(mensagem)

def iniciar_bot():
    enviar_sinal("✅ Bot de sinais iniciado com sucesso!")
    while True:
        print("[LOOP] Executando nova análise...")
        calcular_sinal()
        time.sleep(60)

threading.Thread(target=iniciar_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
