from abc import ABC, abstractmethod
import ssl
import certifi
import aiohttp

class BaseModel(ABC):
    def __init__(self, api_key):
        self.api_key = api_key
        # 创建SSL上下文
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        
    async def get_client_session(self):
        """获取配置好的aiohttp会话"""
        return aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                ssl=False  # 禁用SSL验证，使用代理时需要
            )
        )
    
    @abstractmethod
    async def chat(self, message):
        pass
    
    @property
    @abstractmethod
    def name(self):
        pass 