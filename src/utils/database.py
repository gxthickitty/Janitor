import sqlite3
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "data/bot.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_tables()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _init_tables(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS duel_stats (
                user_id INTEGER PRIMARY KEY,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                last_duel INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_roles (
                user_id INTEGER,
                role_id INTEGER,
                created_at INTEGER,
                PRIMARY KEY (user_id, role_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_duel_stats(self, user_id: int) -> Dict[str, int]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT wins, losses, last_duel FROM duel_stats WHERE user_id=?",
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'wins': result[0],
                'losses': result[1],
                'last_duel': result[2]
            }
        return {'wins': 0, 'losses': 0, 'last_duel': 0}
    
    def update_duel_stats(self, user_id: int, won: bool = False):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT OR IGNORE INTO duel_stats (user_id) VALUES (?)",
            (user_id,)
        )
        
        timestamp = int(datetime.now().timestamp())
        
        if won:
            cursor.execute(
                "UPDATE duel_stats SET wins = wins + 1, last_duel = ? WHERE user_id=?",
                (timestamp, user_id)
            )
        else:
            cursor.execute(
                "UPDATE duel_stats SET losses = losses + 1, last_duel = ? WHERE user_id=?",
                (timestamp, user_id)
            )
        
        conn.commit()
        conn.close()
    
    def get_duel_leaderboard(self, limit: int = 5):
        """Get top players by win ratio"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, wins, losses 
            FROM duel_stats 
            WHERE wins + losses > 0 
            ORDER BY CAST(wins AS FLOAT) / NULLIF(wins + losses, 0) DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
                
        return results

    def get_user_custom_roles(self, user_id: int):
        """Get all custom roles for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role_id, created_at FROM custom_roles WHERE user_id=?",
            (user_id,)
        )
        results = cursor.fetchall()
        conn.close()
        
        return [(r[0], r[1]) for r in results]
    
    def add_custom_role(self, user_id: int, role_id: int):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        timestamp = int(datetime.now().timestamp())
        
        cursor.execute(
            "INSERT OR REPLACE INTO custom_roles (user_id, role_id, created_at) VALUES (?, ?, ?)",
            (user_id, role_id, timestamp)
        )
        
        conn.commit()
        conn.close()
    
    def remove_custom_role(self, user_id: int, role_id: int):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM custom_roles WHERE user_id=? AND role_id=?",
            (user_id, role_id)
        )
        
        conn.commit()
        conn.close()
    
    def count_user_custom_roles(self, user_id: int) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT COUNT(*) FROM custom_roles WHERE user_id=?",
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 0
