import requests
import logging

logger = logging.getLogger(__name__)

class EvolutionAPI:
    def __init__(self):
        self.base_url = 'https://n8n-ai-evolution-api.pueq1b.easypanel.host'
        self.api_key = '2E6580F17EF3-4EB4-88D5-AF858D782DA8' # Global Key ou instanciável

    def send_text(self, instance: str, number: str, text: str):
        # Na v2, o endpoint é fixo e a instância vai no header ou path conforme config
        url = f"{self.base_url}/message/sendText/{instance}"
        
        headers = {
            'apikey': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # Payload simplificado conforme doc v2
        payload = {
            "number": number,
            "text": text,
            "delay": 1200, # Recomendado para evitar ban
            "linkPreview": True
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao enviar mensagem Evolution API: {e}")
            return None

#https://n8n-ai-evolution-api.pueq1b.easypanel.host/message/sendText/Alexandre

'''
{"key":{"remoteJid":"554896444643@s.whatsapp.net",
        "fromMe":true,
        "id":"3EB024A05252AF10B4DAA6"},
        "pushName":"Você",
        "status":"PENDING",
        "message":{"conversation":"Oi Python 02"},
        "contextInfo":{"mentionedJid":[],
                        "groupMentions":[],
                        "ephemeralSettingTimestamp":{"low":1778425452,"high":0,"unsigned":false},
                        "disappearingMode":{"initiator":0}
                        },
        "messageType":"conversation",
        "messageTimestamp":1778598252,
        "instanceId":"92007157-43d2-4485-87ff-217b6f5c78df","source":"web"}  
'''