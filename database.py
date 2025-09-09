# utils/database.py
import json
import os
from typing import Dict, List, Optional

class Database:
    def __init__(self, data_file: str = "data/savings_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        
        return {"users": {}, "goals": {}}
    
    def _save_data(self):
        """Save data to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    # Add your database methods here...
