from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    title: str
    description: str = ""
    assignee: str = "Unassigned"
    priority: str = "Medium"  # Low, Medium, High
    status: str = "Todo"      # Todo, In Progress, Done
    due_date: str = "2026-11-30"
    id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            assignee=data.get("assignee", "Unassigned"),
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Todo"),
            due_date=data.get("due_date", "2026-11-30")
        )

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date
        }