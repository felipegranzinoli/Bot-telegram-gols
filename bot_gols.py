import os
import requests
import time
import logging
from datetime import datetime

# Configurações (usará variáveis de ambiente)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class BotGols:
    def __init__(self):
        self.alertas_enviados = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def enviar_telegram(self, mensagem):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
        try:
            resposta = self.session.post(url, json=payload, timeout=10)
            return resposta.status_code == 200
        except:
            return False

    def obter_jogos(self):
        try:
            url = "https://api.sofascore.com/api/v1/sport/football/events/live"
            headers = {
                'Origin': 'https://www.sofascore.com',
                'Referer': 'https://www.sofascore.com/',
            }
            resposta = self.session.get(url, headers=headers, timeout=15)
            if resposta.status_code == 200:
                return resposta.json().get('events', [])
        except Exception as e:
            logging.error(f"Erro: {e}")
        return []

    def monitorar(self):
        logging.info("🤖 Bot Iniciado no Railway!")
        self.enviar_telegram("🚀 Bot implantado no Railway! Monitorando 24/7")
        
        while True:
            try:
                jogos = self.obter_jogos()
                if jogos:
                    logging.info(f"📊 {len(jogos)} jogos encontrados")
                    # Sua lógica de análise aqui
                
                time.sleep(60)
            except Exception as e:
                logging.error(f"Erro geral: {e}")
                time.sleep(30)

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not CHAT_ID:
        logging.error("❌ Configure as variáveis de ambiente!")
    else:
        bot = BotGols()
        bot.monitorar()
