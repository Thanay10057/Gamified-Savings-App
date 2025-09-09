import json
import uuid
from datetime import datetime
from typing import Dict, List

class User:
    def __init__(self, name: str, email: str, user_id: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.balance = 0.0
        self.total_points = 0
        self.level = 1
        self.achievements = []
        self.created_at = datetime.now().isoformat()
        
    def add_money(self, amount: float) -> bool:
        """Add money to user's savings"""
        if amount > 0:
            self.balance += amount
            return True
        return False
    
    def withdraw_money(self, amount: float) -> bool:
        """Withdraw money from savings"""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    def add_points(self, points: int):
        """Add points and check for level up"""
        self.total_points += points
        new_level = self.calculate_level()
        if new_level > self.level:
            self.level = new_level
            return True  # Level up occurred
        return False
    
    def calculate_level(self) -> int:
        """Calculate user level based on points"""
        return (self.total_points // 100) + 1
    
    def add_achievement(self, achievement_id: str):
        """Add achievement to user's collection"""
        if achievement_id not in self.achievements:
            self.achievements.append(achievement_id)
            return True
        return False
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'balance': self.balance,
            'total_points': self.total_points,
            'level': self.level,
            'achievements': self.achievements,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        user = cls(data['name'], data['email'], data['user_id'])
        user.balance = data['balance']
        user.total_points = data['total_points']
        user.level = data['level']
        user.achievements = data['achievements']
        user.created_at = data['created_at']
        return user
