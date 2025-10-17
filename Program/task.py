from datetime import datetime, date
from dataclasses import dataclass

@dataclass
# Task data structure #

class task_data:
    def __init__(self,title, priority, has_deadline_bool, deadline, completed, has_description_bool, description=False):
        self.title = title
        self.priority = priority
        self.has_description_bool = has_deadline_bool
        self.deadline = deadline
        self.completed = completed
        self.has_description_bool = has_description_bool
        self.description = description

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "has_deadline_bool": self.has_description_bool,
            "deadline": self.deadline.isoformat() if isinstance(self.deadline, date) else self.deadline,
            "completed": self.completed,
            "is_task_description": self.has_description_bool,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, d):
        from datetime import datetime
        deadline = datetime.strptime(d["deadline"], "%Y-%m-%d").date() if d["deadline"] else None
        return cls(
        d["title"],
        d["priority"],
        d.get("has_deadline_bool", False),
        deadline,
        d.get("completed", False),
        d.get("is_task_description", False),
        d.get("description", "")
    )