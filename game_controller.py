from typing import List, Tuple
from models.user import User
from models.achievement import AchievementManager, Achievement
from utils.database import Database

class GameController:
    def __init__(self, db: Database):
        self.db = db
        self.achievement_manager = AchievementManager()
    
    def award_points(self, user_id: str, points: int, reason: str = "") -> Tuple[bool, bool]:
        """Award points to user and check for level up"""
        user = self.db.get_user(user_id)
        if user:
            level_up = user.add_points(points)
            self.db.save_user(user)
            return True, level_up
        return False, False
    
    def check_and_award_achievements(self, user_id: str) -> List[Achievement]:
        """Check for new achievements and award them"""
        user = self.db.get_user(user_id)
        if not user:
            return []
        
        goals = self.db.get_user_goals(user_id)
        earned_achievement_ids = self.achievement_manager.check_achievements(user, goals)
        
        awarded_achievements = []
        for achievement_id in earned_achievement_ids:
            achievement = self.achievement_manager.get_achievement(achievement_id)
            if achievement and user.add_achievement(achievement_id):
                user.add_points(achievement.points_reward)
                awarded_achievements.append(achievement)
        
        if awarded_achievements:
            self.db.save_user(user)
        
        return awarded_achievements
    
    def get_user_achievements(self, user_id: str) -> List[Achievement]:
        """Get all achievements earned by user"""
        user = self.db.get_user(user_id)
        if not user:
            return []
        
        achievements = []
        for achievement_id in user.achievements:
            achievement = self.achievement_manager.get_achievement(achievement_id)
            if achievement:
                achievements.append(achievement)
        
        return achievements
    
    def get_available_achievements(self, user_id: str) -> List[Achievement]:
        """Get achievements not yet earned by user"""
        user = self.db.get_user(user_id)
        if not user:
            return self.achievement_manager.achievements
        
        return [a for a in self.achievement_manager.achievements 
                if a.achievement_id not in user.achievements]
