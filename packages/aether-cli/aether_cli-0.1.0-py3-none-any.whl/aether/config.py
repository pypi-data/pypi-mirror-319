import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / '.aether'
        self.config_file = self.config_dir / 'config.json'
        self.ensure_config_exists()
        self.load_config()
        self.migrate_config()
        
    def ensure_config_exists(self):
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.save_config({
                'version': '1.0.0',
                'current_model': None,
                'api_keys': {},
                'proxy': None
            })
    
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
                if self.config.get('proxy'):
                    os.environ['http_proxy'] = self.config['proxy']
                    os.environ['https_proxy'] = self.config['proxy']
        except json.JSONDecodeError:
            print("Warning: Config file corrupted, creating new one")
            self.ensure_config_exists()
    
    def migrate_config(self):
        """迁移旧版本配置"""
        if 'version' not in self.config:
            # 迁移旧配置
            new_config = {
                'version': '1.0.0',
                'current_model': None,
                'api_keys': {},
                'proxy': self.config.get('proxy')
            }
            
            # 迁移API密钥，更新模型名称
            old_keys = self.config.get('api_keys', {})
            if 'gemini' in old_keys:
                new_config['api_keys']['gemini-pro'] = old_keys['gemini']
            if 'gpt-4o' in old_keys:
                new_config['api_keys']['gpt-4'] = old_keys['gpt-4o']
            
            # 迁移当前模型
            old_model = self.config.get('current_model')
            if old_model == 'gemini':
                new_config['current_model'] = 'gemini-pro'
            elif old_model == 'gpt-4o':
                new_config['current_model'] = 'gpt-4'
            
            self.config = new_config
            self.save_config()
    
    def save_config(self, config=None):
        if config is not None:
            self.config = config
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set_api_key(self, model, key):
        self.config['api_keys'][model] = key
        self.save_config()
    
    def get_api_key(self, model):
        return self.config['api_keys'].get(model)
    
    def set_current_model(self, model):
        self.config['current_model'] = model
        self.save_config()
    
    def get_current_model(self):
        return self.config['current_model']
        
    def set_proxy(self, proxy):
        self.config['proxy'] = proxy
        if proxy is None:
            os.environ.pop('http_proxy', None)
            os.environ.pop('https_proxy', None)
        else:
            os.environ['http_proxy'] = proxy
            os.environ['https_proxy'] = proxy
        self.save_config()
        
    def get_proxy(self):
        return self.config.get('proxy') 