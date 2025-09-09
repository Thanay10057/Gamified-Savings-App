import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'controllers'))

# Now your imports should work
from utils.database import Database
from models.user import User
import os
import sys
from colorama import init, Fore, Style
from controllers.savings_controller import SavingsController
from controllers.game_controller import GameController
from utils.database import Database

# Initialize colorama for colored console output
init()

class SavingsGameApp:
    def __init__(self):
        self.db = Database()
        self.savings_controller = SavingsController(self.db)
        self.game_controller = GameController(self.db)
        self.current_user = None
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print colored header"""
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"{title:^50}")
        print(f"{'=' * 50}{Style.RESET_ALL}\n")
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"{Fore.YELLOW}ℹ {message}{Style.RESET_ALL}")
    
    def main_menu(self):
        """Display main menu"""
        while True:
            self.clear_screen()
            self.print_header("💰 GAMIFIED SAVINGS APP 💰")
            
            if self.current_user:
                print(f"{Fore.GREEN}Welcome back, {self.current_user.name}!{Style.RESET_ALL}")
                print(f"Balance: ${self.current_user.balance:.2f} | Level: {self.current_user.level} | Points: {self.current_user.total_points}")
                print()
            
            print("1. 👤 Login/Register")
            print("2. 💵 Make Deposit")
            print("3. 💸 Withdraw Money")
            print("4. 🎯 Create Savings Goal")
            print("5. 📊 View Goals")
            print("6. 🎮 View Game Stats")
            print("7. 🏆 View Achievements")
            print("8. 📈 View Progress")
            print("9. 🚪 Exit")
            
            choice = input(f"\n{Fore.YELLOW}Select an option (1-9): {Style.RESET_ALL}")
            
            if choice == "1":
                self.login_register()
            elif choice == "2":
                self.make_deposit()
            elif choice == "3":
                self.withdraw_money()
            elif choice == "4":
                self.create_goal()
            elif choice == "5":
                self.view_goals()
            elif choice == "6":
                self.view_game_stats()
            elif choice == "7":
                self.view_achievements()
            elif choice == "8":
                self.view_progress()
            elif choice == "9":
                print(f"\n{Fore.CYAN}Thanks for using Gamified Savings App! 👋{Style.RESET_ALL}")
                sys.exit()
            else:
                self.print_error("Invalid option. Please try again.")
                input("Press Enter to continue...")
    
    def login_register(self):
        """Handle login/registration"""
        self.clear_screen()
        self.print_header("LOGIN / REGISTER")
        
        print("1. Register New User")
        print("2. Login Existing User")
        
        choice = input(f"\n{Fore.YELLOW}Select option (1-2): {Style.RESET_ALL}")
        
        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            
            self.current_user = self.savings_controller.create_user(name, email)
            self.print_success(f"Welcome {name}! Your account has been created.")
            
            # Check for first achievements
            achievements = self.game_controller.check_and_award_achievements(self.current_user.user_id)
            if achievements:
                self.print_success(f"You earned {len(achievements)} achievement(s)!")
        
        elif choice == "2":
            users = self.db.get_all_users()
            if not users:
                self.print_error("No users found. Please register first.")
                input("Press Enter to continue...")
                return
            
            print("\nExisting users:")
            for i, user in enumerate(users, 1):
                print(f"{i}. {user.name} ({user.email})")
            
            try:
                user_choice = int(input("Select user number: ")) - 1
                if 0 <= user_choice < len(users):
                    self.current_user = users[user_choice]
                    self.print_success(f"Welcome back, {self.current_user.name}!")
                else:
                    self.print_error("Invalid user selection.")
            except ValueError:
                self.print_error("Please enter a valid number.")
        
        input("Press Enter to continue...")
    
    def make_deposit(self):
        """Handle money deposit"""
        if not self.current_user:
            self.print_error("Please login first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("MAKE DEPOSIT")
        
        try:
            amount = float(input("Enter deposit amount: $"))
            if amount <= 0:
                self.print_error("Amount must be positive.")
                input("Press Enter to continue...")
                return
            
            # Make deposit
            if self.savings_controller.deposit_money(self.current_user.user_id, amount):
                self.current_user = self.savings_controller.get_user(self.current_user.user_id)
                self.print_success(f"Deposited ${amount:.2f}! New balance: ${self.current_user.balance:.2f}")
                
                # Award points for deposit
                points = int(amount * 2)  # 2 points per dollar
                success, level_up = self.game_controller.award_points(self.current_user.user_id, points, "Deposit")
                if success:
                    self.print_success(f"You earned {points} points!")
                    if level_up:
                        self.print_success("🎉 LEVEL UP! 🎉")
                
                # Check for achievements
                achievements = self.game_controller.check_and_award_achievements(self.current_user.user_id)
                if achievements:
                    self.print_success(f"🏆 You earned {len(achievements)} new achievement(s)!")
                    for achievement in achievements:
                        print(f"   • {achievement.title}: {achievement.description}")
                
                # Update current user data
                self.current_user = self.savings_controller.get_user(self.current_user.user_id)
            else:
                self.print_error("Deposit failed.")
        
        except ValueError:
            self.print_error("Please enter a valid amount.")
        
        input("Press Enter to continue...")
    
    def withdraw_money(self):
        """Handle money withdrawal"""
        if not self.current_user:
            self.print_error("Please login first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("WITHDRAW MONEY")
        print(f"Current balance: ${self.current_user.balance:.2f}")
        
        try:
            amount = float(input("Enter withdrawal amount: $"))
            if amount <= 0:
                self.print_error("Amount must be positive.")
                input("Press Enter to continue...")
                return
            
            if self.savings_controller.withdraw_money(self.current_user.user_id, amount):
                self.current_user = self.savings_controller.get_user(self.current_user.user_id)
                self.print_success(f"Withdrew ${amount:.2f}! New balance: ${self.current_user.balance:.2f}")
            else:
                self.print_error("Insufficient funds or withdrawal failed.")
        
        except ValueError:
            self.print_error("Please enter a valid amount.")
        
        input("Press Enter to continue...")
    
    def create_goal(self):
        """Create a new savings goal"""
        if not self.current_user:
            self.print_error("Please login first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("CREATE SAVINGS GOAL")
        
        title = input("Goal title: ")
        
        try:
            target_amount = float(input("Target amount: $"))
            deadline_days = int(input("Deadline (days from now): "))
            
            if target_amount <= 0 or deadline_days <= 0:
                self.print_error("Target amount and deadline must be positive.")
                input("Press Enter to continue...")
                return
            
            goal = self.savings_controller.create_savings_goal(
                self.current_user.user_id, title, target_amount, deadline_days
            )
            
            self.print_success(f"Goal '{title}' created successfully!")
            self.print_info(f"Target: ${target_amount:.2f} | Deadline: {deadline_days} days")
            
            # Award points for creating goal
            points = 25
            self.game_controller.award_points(self.current_user.user_id, points, "Goal Creation")
            self.print_success(f"You earned {points} points for creating a goal!")
        
        except ValueError:
            self.print_error("Please enter valid numbers.")
        
        input("Press Enter to continue...")
    
    def view_goals(self):
        """View all user goals"""
        if not self.current_user:
            self.print_error("Please login first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("YOUR SAVINGS GOALS")
        
        goals = self.savings_controller.get_user_goals(self.current_user.user_id)
        
        if not goals:
            self.print_info("No goals created yet. Create your first goal to get started!")
        else:
            for i, goal in enumerate(goals, 1):
                status = "✅ COMPLETED" if goal.is_completed else "🔄 IN PROGRESS"
                progress = goal.get_progress_percentage()
                days_left = goal.days_remaining()
                
                print(f"\n{Fore.CYAN}{i}. {goal.title}{Style.RESET_ALL}")
                print(f"   Status: {status}")
                print(f"   Progress: ${goal.current_amount:.2f} / ${goal.target_amount:.2f} ({progress:.1f}%)")
                print(f"   Days remaining: {days_left}")
                
                # Progress bar
                bar_length = 30
                filled_length = int(bar_length * progress // 100)
                bar = "█" * filled_length + "░" * (bar_length - filled_length)
                print(f"   [{bar}] {progress:.1f}%")
            
            # Option to add progress to a goal
            print(f"\n{Fore.YELLOW}Would you like to add progress to a goal? (y/n): {Style.RESET_ALL}", end="")
            if input().lower() == 'y':
                self.add_goal_progress(goals)
        
        input("Press Enter to continue...")
    
    def add_goal_progress(self, goals):
        """Add progress to a specific goal"""
        try:
            goal_num = int(input("Enter goal number: ")) - 1
            if 0 <= goal_num < len(goals):
                goal = goals[goal_num]
                if goal.is_completed:
                    self.print_info("This goal is already completed!")
                    return
                
                amount = float(input(f"Add progress amount for '{goal.title}': $"))
                if amount <= 0:
                    self.print_error("Amount must be positive.")
                    return
                
                # Check if user has enough balance
                if amount > self.current_user.balance:
                    self.print_error("Insufficient balance!")
                    return
                
                # Transfer money from balance to goal
                if self.savings_controller.withdraw_money(self.current_user.user_id, amount):
                    completed = self.savings_controller.add_progress_to_goal(goal.goal_id, amount)
                    
                    self.print_success(f"Added ${amount:.2f} to '{goal.title}'!")
                    
                    # Award points for progress
                    points = int(amount * 3)  # 3 points per dollar for goal progress
                    self.game_controller.award_points(self.current_user.user_id, points, "Goal Progress")
                    self.print_success(f"You earned {points} points!")
                    
                    if completed:
                        self.print_success("🎉 GOAL COMPLETED! 🎉")
                        # Award bonus points for completion
                        bonus_points = 100
                        self.game_controller.award_points(self.current_user.user_id, bonus_points, "Goal Completion")
                        self.print_success(f"Bonus: {bonus_points} points for completing the goal!")
                    
                    # Check for achievements
                    achievements = self.game_controller.check_and_award_achievements(self.current_user.user_id)
                    if achievements:
                        self.print_success(f"🏆 You earned {len(achievements)} new achievement(s)!")
                        for achievement in achievements:
                            print(f"   • {achievement.title}")
                    
                    # Update current user
                    self.current_user = self.savings_controller.get_user(self.current_user.user_id)
            else:
                self.print_error("Invalid goal number.")
        
        except ValueError:
            self.print_error("Please enter valid numbers.")
    
    def view_game_stats(self):
        """View game statistics"""
        if not self.current_user:
            self.print_error("Please login first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("GAME STATISTICS")
        
        print(f"{Fore.GREEN}👤 Player: {self.current_user.name}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🎮 Level: {self.current_user.level}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⭐ Points: {self.current_user.total_points}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}💰 Balance: ${self.current_user.balance:.2f}{Style.RESET_ALL}")
        
        # Points to next level
        points_to_next = (self.current_user.level * 100) - self.current_user.total_points
        if points_to_next > 0:
            print(f"{Fore.MAGENTA}🚀 Points to next level: {points_to_next}{Style.RESET_ALL}")
        
        # Goal statistics
        goals = self.savings_controller.get_user_goals(self.current_user.user_id)
        completed_goals = [g for g in goals if g.is_completed]
        
        print(f"\n{Fore.CYAN}🎯 Goals Statistics:{Style.RESET_ALL}")
        print(f"   Total Goals: {len(goals)}")
        print(f"   Completed: {len(completed_goals)}")
        print(f"   In Progress: {len(goals) - len(completed_goals)}")
        
        # Achievement count
        achievements = self.game_controller.get_user_achievements(self.current_user.user_id)
        available = self.game_controller.get_available_achievements(self.current_user.user_id)
        
        print(f"\n{Fore.YELLOW}🏆 Achievements:{Style.RESET_ALL}")
        print(f"   Earned: {len(achievements)}")
        print(f"   Available: {len(available)}")
        
        input("Press Enter to continue...")
    
    def view_achievements(self):
        """View achievements"""
        if not self.current_user:
            self.print_error("Please login first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("ACHIEVEMENTS")
        
        earned = self.game_controller.get_user_achievements(self.current_user.user_id)
        available = self.game_controller.get_available_achievements(self.current_user.user_id)
        
        if earned:
            print(f"{Fore.GREEN}🏆 EARNED ACHIEVEMENTS:{Style.RESET_ALL}\n")
            for achievement in earned:
                print(f"✅ {achievement.title} (+{achievement.points_reward} points)")
                print(f"   {achievement.description}\n")
        
        if available:
            print(f"{Fore.YELLOW}🎯 AVAILABLE ACHIEVEMENTS:{Style.RESET_ALL}\n")
            for achievement in available:
                print(f"🔲 {achievement.title} (+{achievement.points_reward} points)")
                print(f"   {achievement.description}\n")
        
        if not earned and not available:
            self.print_info("No achievements found.")
        
        input("Press Enter to continue...")
    
    def view_progress(self):
        """View overall progress"""
        if not self.current_user:
            self.print_error("Please login first.")
            input("Press Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header("PROGRESS OVERVIEW")
        
        goals = self.savings_controller.get_user_goals(self.current_user.user_id)
        
        # Overall savings rate
        total_saved = sum(goal.current_amount for goal in goals)
        total_targets = sum(goal.target_amount for goal in goals)
        
        print(f"{Fore.GREEN}💰 Total Saved: ${total_saved:.2f}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🎯 Total Targets: ${total_targets:.2f}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💼 Available Balance: ${self.current_user.balance:.2f}{Style.RESET_ALL}")
        
        if total_targets > 0:
            overall_progress = (total_saved / total_targets) * 100
            print(f"{Fore.MAGENTA}📊 Overall Goal Progress: {overall_progress:.1f}%{Style.RESET_ALL}")
        
        # Recent activity summary
        completed_goals = [g for g in goals if g.is_completed]
        active_goals = [g for g in goals if not g.is_completed]
        
        print(f"\n{Fore.CYAN}📈 Quick Stats:{Style.RESET_ALL}")
        print(f"   • Level {self.current_user.level} ({self.current_user.total_points} points)")
        print(f"   • {len(completed_goals)} goals completed")
        print(f"   • {len(active_goals)} goals in progress")
        print(f"   • {len(self.current_user.achievements)} achievements earned")
        
        # Motivation message
        if self.current_user.level >= 5:
            print(f"\n{Fore.GREEN}🌟 You're doing amazing! Keep up the great work!{Style.RESET_ALL}")
        elif self.current_user.total_points > 0:
            print(f"\n{Fore.YELLOW}🚀 You're making progress! Keep saving to level up!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}💪 Start your savings journey today!{Style.RESET_ALL}")
        
        input("Press Enter to continue...")

if __name__ == "__main__":
    app = SavingsGameApp()
    app.main_menu()
