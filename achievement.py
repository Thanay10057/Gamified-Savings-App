from typing import Dict, List
from enum import Enum

class AchievementType(Enum):
    FIRST_DEPOSIT = "first_deposit"
    SAVINGS_MILESTONE = "savings_milestone"
    GOAL_COMPLETION = "goal_completion"
    CONSISTENCY = "consistency"
    LEVEL_UP = "level_up"

class Achievement:
    def __init__(self, achievement_id: str, title: str, description: str, 
                 points_reward: int, achievement_type: AchievementType, 
                 requirements: Dict = None):
        self.achievement_id = achievement_id
        self.title = title
        self.description = description
        self.points_reward = points_reward
        self.achievement_type = achievement_type
        self.requirements = requirements or {}
    
    def to_dict(self) -> Dict:
        return {
            'achievement_id': self.achievement_id,
            'title': self.title,
            'description': self.description,
            'points_reward': self.points_reward,
            'achievement_type': self.achievement_type.value,
            'requirements': self.requirements
        }

class AchievementManager:
    def __init__(self):
        self.achievements = self._create_default_achievements()
    
    def _create_default_achievements(self) -> List[Achievement]:
        """Create default achievements"""
        return [
            Achievement(
                "first_deposit", "First Step", 
                "Make your first deposit", 50, 
                AchievementType.FIRST_DEPOSIT
            ),
            Achievement(
                "saver_100", "Century Saver", 
                "Save $100", 100, 
                AchievementType.SAVINGS_MILESTONE,
                {"amount": 100}
            ),
            Achievement(
                "saver_500", "Half Grand", 
                "Save $500", 250, 
                AchievementType.SAVINGS_MILESTONE,
                {"amount": 500}
            ),
            Achievement(
                "saver_1000", "Grand Saver", 
                "Save $1,000", 500, 
                AchievementType.SAVINGS_MILESTONE,
                {"amount": 1000}
            ),
            Achievement(
                "first_goal", "Goal Crusher", 
                "Complete your first savings goal", 200, 
                AchievementType.GOAL_COMPLETION
            ),
            Achievement(
                "level_5", "Rising Star", 
                "Reach Level 5", 300, 
                AchievementType.LEVEL_UP,
                {"level": 5}
            ),
            Achievement(
                "level_10", "Savings Master", 
                "Reach Level 10", 500, 
                AchievementType.LEVEL_UP,
                {"level": 10}
            )
        ]
    
    def get_achievement(self, achievement_id: str) -> Achievement:
        """Get achievement by ID"""
        for achievement in self.achievements:
            if achievement.achievement_id == achievement_id:
                return achievement
        return None
    
    def check_achievements(self, user, goals: List) -> List[str]:
        """Check which achievements user has earned"""
        earned_achievements = []
        
        for achievement in self.achievements:
            if achievement.achievement_id in user.achievements:
                continue  # Already earned
            
            if self._check_achievement_condition(user, goals, achievement):
                earned_achievements.append(achievement.achievement_id)
        
        return earned_achievements
    
    def _check_achievement_condition(self, user, goals, achievement: Achievement) -> bool:
        """Check if user meets achievement requirements"""
        if achievement.achievement_type == AchievementType.FIRST_DEPOSIT:
            return user.balance > 0
        
        elif achievement.achievement_type == AchievementType.SAVINGS_MILESTONE:
            required_amount = achievement.requirements.get("amount", 0)
            return user.balance >= required_amount
        
        elif achievement.achievement_type == AchievementType.GOAL_COMPLETION:
            completed_goals = [g for g in goals if g.user_id == user.user_id and g.is_completed]
            return len(completed_goals) > 0
        
        elif achievement.achievement_type == AchievementType.LEVEL_UP:
            required_level = achievement.requirements.get("level", 0)
            return user.level >= required_level
        
        return False
