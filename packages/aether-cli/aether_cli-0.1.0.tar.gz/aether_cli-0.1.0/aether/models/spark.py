import time
import hashlib
import hmac
import base64
import json
import aiohttp
from urllib.parse import urlencode
from .base import BaseModel

class SparkModel(BaseModel):
    name = "spark"
    
    def __init__(self, api_key):
        super().__init__(api_key)
        self.app_id, self.api_key, self.api_secret = api_key.split(':')
        self.host = "spark-api.xf-yun.com"
        self.path = "/v2.1/chat"
        
    def create_url(self):
        date = time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.gmtime())
        signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), 
                               signature_origin.encode('utf-8'),
                               digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(signature_sha).decode()
        
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()
        
        params = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        return f"wss://{self.host}{self.path}?{urlencode(params)}"
    
    async def chat(self, message):
        try:
            url = self.create_url()
            data = {
                "header": {
                    "app_id": self.app_id
                },
                "parameter": {
                    "chat": {
                        "domain": "general",
                        "temperature": 0.7,
                        "max_tokens": 2048
                    }
                },
                "payload": {
                    "message": {
                        "text": [{"role": "user", "content": message}]
                    }
                }
            }
            
            async with await self.get_client_session() as session:
                async with session.ws_connect(url) as ws:
                    await ws.send_str(json.dumps(data))
                    response = await ws.receive_str()
                    result = json.loads(response)
                    return result['payload']['choices']['text'][0]['content']
        except Exception as e:
            return f"Error: {str(e)}" 