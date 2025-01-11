import google.generativeai as genai
from .base import BaseModel

class GeminiBaseModel(BaseModel):
    def __init__(self, api_key):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        
    async def chat(self, message):
        try:
            model = genai.GenerativeModel(self.model_name)
            response = await model.generate_content_async(message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

class GeminiProModel(GeminiBaseModel):
    name = "gemini-pro"
    model_name = "gemini-pro"

class GeminiProVisionModel(GeminiBaseModel):
    name = "gemini-pro-vision"
    model_name = "gemini-pro-vision"
    
    async def chat(self, message):
        # TODO: 添加图像处理支持
        return "Image processing not implemented yet"

class GeminiUltraModel(GeminiBaseModel):
    name = "gemini-ultra"
    model_name = "gemini-1.5-pro-latest"

class Gemini2FlashModel(GeminiBaseModel):
    name = "gemini-2-flash"
    model_name = "gemini-2.0-flash-exp" 