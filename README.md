# Exnova Telegram Bot

Bot que envia sinais automáticos para Telegram com base nas últimas 3 velas da Exnova.

## Como rodar na Render

1. Clone este repositório
2. Configure as variáveis de ambiente:
   - API_KEY
   - TELEGRAM_TOKEN
   - TELEGRAM_ID
3. Tipo de serviço: Background Worker
4. Start command:
   ```
   python main.py
   ```

## Intervalo

- Coleta velas a cada 2 minutos
- Envia sinais de 1 minuto (CALL ou PUT)
