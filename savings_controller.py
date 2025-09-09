from typing import List, Optional
from models.user import User
from models.savings_goal import SavingsGoal
from utils.database import Database


class SavingsController:
    def __init__(self, db: Database):
        self.db = db
    
    def create_user(self, name: str, email: str) -> User:
        """Create a new user"""
        if not name or not email:
            raise ValueError("Name and email are required")
        
        user = User(name, email)
        self.db.save_user(user)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        if not user_id:
            return None
        return self.db.get_user(user_id)
    
    def deposit_money(self, user_id: str, amount: float) -> bool:
        """Make a deposit"""
        if amount <= 0:
            return False
            
        user = self.db.get_user(user_id)
        if user and user.add_money(amount):
            self.db.save_user(user)
            return True
        return False
    
    def withdraw_money(self, user_id: str, amount: float) -> bool:
        """Make a withdrawal"""
        if amount <= 0:
            return False
            
        user = self.db.get_user(user_id)
        if user and user.withdraw_money(amount):
            self.db.save_user(user)
            return True
        return False
    
    def create_savings_goal(self, user_id: str, title: str, 
                          target_amount: float, deadline_days: int) -> Optional[SavingsGoal]:
        """Create a new savings goal"""
        if not user_id or not title or target_amount <= 0 or deadline_days <= 0:
            return None
            
        # Verify user exists
        user = self.db.get_user(user_id)
        if not user:
            return None
            
        goal = SavingsGoal(user_id, title, target_amount, deadline_days)
        self.db.save_goal(goal)
        return goal
    
    def add_progress_to_goal(self, goal_id: str, amount: float) -> bool:
        """Add progress to a savings goal"""
        if not goal_id or amount <= 0:
            return False
            
        goal = self.db.get_goal(goal_id)
        if goal:
            completed = goal.add_progress(amount)
            self.db.save_goal(goal)
            return completed
        return False
    
    def get_user_goals(self, user_id: str) -> List[SavingsGoal]:
        """Get all goals for a user"""
        if not user_id:
            return []
        return self.db.get_user_goals(user_id)
