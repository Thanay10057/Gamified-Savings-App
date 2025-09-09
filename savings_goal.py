import uuid
from datetime import datetime, timedelta
from typing import Dict

class SavingsGoal:
    def __init__(self, user_id: str, title: str, target_amount: float, 
                 deadline_days: int, goal_id: str = None):
        self.goal_id = goal_id or str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.target_amount = target_amount
        self.current_amount = 0.0
        self.created_at = datetime.now()
        self.deadline = self.created_at + timedelta(days=deadline_days)
        self.is_completed = False
        self.completion_date = None
    
    def add_progress(self, amount: float) -> bool:
        """Add progress towards the goal"""
        if amount > 0:
            self.current_amount += amount
            if self.current_amount >= self.target_amount and not self.is_completed:
                self.is_completed = True
                self.completion_date = datetime.now()
                return True  # Goal completed
            return False  # Progress added but not completed
        return False
    
    def get_progress_percentage(self) -> float:
        """Get completion percentage"""
        return min((self.current_amount / self.target_amount) * 100, 100.0)
    
    def days_remaining(self) -> int:
        """Get days remaining to deadline"""
        return max(0, (self.deadline - datetime.now()).days)
    
    def calculate_reward_points(self) -> int:
        """Calculate reward points based on goal completion"""
        base_points = int(self.target_amount / 10)  # 1 point per $10
        if self.is_completed:
            if self.completion_date <= self.deadline:
                return base_points * 2  # Double points for on-time completion
            else:
                return base_points  # Regular points for late completion
        return 0
    
    def to_dict(self) -> Dict:
        return {
            'goal_id': self.goal_id,
            'user_id': self.user_id,
            'title': self.title,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'created_at': self.created_at.isoformat(),
            'deadline': self.deadline.isoformat(),
            'is_completed': self.is_completed,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        goal = cls(
            data['user_id'], 
            data['title'], 
            data['target_amount'], 
            0,  # deadline_days not needed for reconstruction
            data['goal_id']
        )
        goal.current_amount = data['current_amount']
        goal.created_at = datetime.fromisoformat(data['created_at'])
        goal.deadline = datetime.fromisoformat(data['deadline'])
        goal.is_completed = data['is_completed']
        goal.completion_date = datetime.fromisoformat(data['completion_date']) if data['completion_date'] else None
        return goal
