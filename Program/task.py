from datetime import datetime
from dataclasses import dataclass

@dataclass
# Task data structure #

class task_data:
    title: str
    priority: int
   # deadline: datetime
    completed: bool = False
    reward_claimed: bool = False

