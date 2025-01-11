from .base import BaseModel

class GPTBaseModel(BaseModel):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
    async def chat(self, message):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": message}]
        }
        
        try:
            async with await self.get_client_session() as session:
                async with session.post(self.api_url, headers=headers, json=data) as response:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"

class GPT4Model(GPTBaseModel):
    name = "gpt-4"
    model_name = "gpt-4-turbo-preview"

class GPT4MiniModel(GPTBaseModel):
    name = "gpt-4-mini"
    model_name = "gpt-4-0125-preview"  # 使用较小的上下文窗口版本

class GPT35TurboModel(GPTBaseModel):
    name = "gpt-3.5"
    model_name = "gpt-3.5-turbo" 