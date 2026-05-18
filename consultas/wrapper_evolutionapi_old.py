import requests
from urllib.parse import urlencode, urljoin

class BaseEVolutionAPI:

    def __init__(self):
        self._BASE_URL = 'https://n8n-ai-evolution-api.pueq1b.easypanel.host'
        self._API_KEY = {
            'Alexandre': '2E6580F17EF3-4EB4-88D5-AF858D782DA8'
        }
    
    def _send_request(
        self,
        path,
        method='GET',
        body=None,
        headers={},
        params_url={}
    ):
        method = method.upper()
        url = self._mount_url(path, params_url)
        
        if not isinstance(headers, dict):
            headers = {}

        headers.setdefault('Content-Type', 'application/json')
        instance = self._get_instance(path)
        headers['apikey'] = self._API_KEY.get(instance)

        request = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }.get(method)

        return request(url, headers=headers, json=body)
        
    def _mount_url(self, path, params_url):
        if isinstance(params_url, dict):
            parameters = urlencode(params_url)
        
        url = urljoin(self._BASE_URL, path)

        if parameters:
            url = url + '?' + parameters

        print(url)
        return url
        
    def _get_instance(self, path):
        return path.strip('/').split('/')[-1]


class SendMessage(BaseEVolutionAPI):

    def send_message(self, instance, body):
        path = f'/message/sendText/{instance}'
        
        print(f'URL: {path}')
        print(f'instance: {instance}')
        print(f'body: {body}-------------------------------------')
        print(f'send_xxxx: {self._send_request(path, method='POST', body=body)}')

        return self._send_request(path, method='POST', body=body)




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

