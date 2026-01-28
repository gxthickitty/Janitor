import json
import discord
from pathlib import Path
from typing import Optional

class Config:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.data = self._load_config()
    
    def _load_config(self) -> dict:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def save(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    @property
    def token(self) -> str:
        return self.data.get('token', '')
    
    @property
    def genius_token(self) -> str:
        return self.data.get('genius_token', '')
    
    @property
    def bot_info(self) -> dict:
        return self.data.get('bot_info', {})
    
    @property
    def embed_color(self) -> discord.Color:
        color_hex = self.data.get('colors', {}).get('primary', 'a84141')
        return discord.Color(int(color_hex, 16))
    
    @property
    def birthday_role_id(self) -> int:
        return self.data.get('roles', {}).get('birthday_role_id', 0)
    
    @property
    def duel_cooldown(self) -> int:
        return self.data.get('cooldowns', {}).get('duel_seconds', 30)
    
    @property
    def fork_cooldown_minutes(self) -> int:
        return self.data.get('cooldowns', {}).get('fork_minutes', 10)
    
    @property
    def fork_timeout_minutes(self) -> int:
        return self.data.get('cooldowns', {}).get('fork_timeout_minutes', 5)
    
    @property
    def purge_max(self) -> int:
        return self.data.get('limits', {}).get('purge_max', 350)
    
    @property
    def quote_scan_limit(self) -> int:
        return self.data.get('limits', {}).get('quote_scan_limit', 2000)
    
    @property
    def quote_min_length(self) -> int:
        return self.data.get('limits', {}).get('quote_min_length', 20)
    
    @property
    def database_path(self) -> str:
        return self.data.get('database', {}).get('path', 'data/bot.db')
    
    @property
    def log_channel_id(self) -> Optional[int]:
        return self.data.get('logging', {}).get('log_channel_id')
    
    def set_log_channel(self, channel_id: Optional[int]):
        if 'logging' not in self.data:
            self.data['logging'] = {}
        self.data['logging']['log_channel_id'] = channel_id
        self.save()
