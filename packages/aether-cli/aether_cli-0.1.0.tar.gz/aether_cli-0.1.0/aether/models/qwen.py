import aiohttp
from .base import BaseModel

class QwenModel(BaseModel):
    name = "qwen"
    
    def __init__(self, api_key):
        super().__init__(api_key)
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
    async def chat(self, message):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": [{"role": "user", "content": message}]
            }
        }
        
        try:
            async with await self.get_client_session() as session:
                async with session.post(self.api_url, headers=headers, json=data) as response:
                    result = await response.json()
                    return result['output']['text']
        except Exception as e:
            return f"Error: {str(e)}" 