import os
import shutil
import configparser
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.user_home = str(Path.home())
        self.app_config_dir = os.path.join(self.user_home, '.zoomzoom')
        self.user_config_path = os.path.join(self.app_config_dir, 'config.ini')
        self.default_config_path = os.path.join(os.path.dirname(__file__), 'config', 'default_config.ini')
        
        # 确保配置目录存在
        os.makedirs(self.app_config_dir, exist_ok=True)
        
        # 如果用户配置不存在，复制默认配置
        if not os.path.exists(self.user_config_path):
            self.copy_default_config()
        
        # 加载配置
        self.config = configparser.ConfigParser()
        self.config.read(self.user_config_path, encoding='utf-8')
    
    def copy_default_config(self):
        """复制默认配置文件到用户目录"""
        shutil.copy2(self.default_config_path, self.user_config_path)
    
    def get_config(self):
        """获取配置对象"""
        return self.config
    
    def save_config(self):
        """保存配置到文件"""
        with open(self.user_config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_config_path(self):
        """获取当前使用的配置文件路径"""
        return self.user_config_path 