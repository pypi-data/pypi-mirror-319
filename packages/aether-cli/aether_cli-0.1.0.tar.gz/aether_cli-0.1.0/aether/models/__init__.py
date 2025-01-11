from .gpt import GPT4Model, GPT35TurboModel, GPT4MiniModel
from .gemini import (
    GeminiProModel, 
    GeminiProVisionModel, 
    GeminiUltraModel,
    Gemini2FlashModel
)
from .kimi import KimiModel
from .qwen import QwenModel
from .spark import SparkModel

MODEL_REGISTRY = {
    # OpenAI Models
    'gpt-4': GPT4Model,
    'gpt-4-turbo': GPT4Model,  # 使用最新的GPT-4 Turbo
    'gpt-4-mini': GPT4MiniModel,
    'gpt-3.5': GPT35TurboModel,
    
    # Google Models
    'gemini-pro': GeminiProModel,
    'gemini-pro-vision': GeminiProVisionModel,
    'gemini-ultra': GeminiUltraModel,
    'gemini-2-flash': Gemini2FlashModel,
    
    # Other Models
    'kimi': KimiModel,
    'qwen': QwenModel,
    'spark': SparkModel
}

def get_model_class(model_name):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model_name}. Available models: {', '.join(MODEL_REGISTRY.keys())}")
    return MODEL_REGISTRY[model_name] 