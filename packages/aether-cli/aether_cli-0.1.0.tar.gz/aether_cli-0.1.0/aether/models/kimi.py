import aiohttp
from .base import BaseModel

class KimiModel(BaseModel):
    name = "kimi"
    
    def __init__(self, api_key):
        super().__init__(api_key)
        self.api_url = "https://api.moonshot.cn/v1/chat/completions"
        
    async def chat(self, message):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "moonshot-v1-8k",
            "messages": [{"role": "user", "content": message}]
        }
        
        try:
            async with await self.get_client_session() as session:
                async with session.post(self.api_url, headers=headers, json=data) as response:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}" 