from models.task import Task
from services.supabase_service import SupabaseService

class TaskController:
    def __init__(self):
        self.service = SupabaseService()

    def get_connection_status(self) -> str:
        if self.service.is_connected:
            return "Connected to Supabase (PostgreSQL)"
        return "Local Workspace Mode (Ready for Supabase Sync)"

    def load_tasks(self, search_query: str = "", status_filter: str = "All") -> list[Task]:
        tasks = self.service.get_all_tasks()
        filtered = []
        for t in tasks:
            matches_search = search_query.lower() in t.title.lower() or search_query.lower() in t.assignee.lower()
            matches_status = (status_filter == "All") or (t.status == status_filter)
            if matches_search and matches_status:
                filtered.append(t)
        return filtered

    def get_stats(self) -> dict:
        tasks = self.service.get_all_tasks()
        return {
            "total": len(tasks),
            "in_progress": sum(1 for t in tasks if t.status == "In Progress"),
            "done": sum(1 for t in tasks if t.status == "Done"),
            "high_priority": sum(1 for t in tasks if t.priority == "High" and t.status != "Done")
        }

    def create_task(self, title: str, description: str, assignee: str, priority: str, status: str, due_date: str) -> Task:
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        new_task = Task(
            title=title.strip(),
            description=description.strip(),
            assignee=assignee.strip() or "Unassigned",
            priority=priority,
            status=status,
            due_date=due_date.strip() or "2026-11-30"
        )
        return self.service.add_task(new_task)

    def edit_task(self, task_id: int, title: str, description: str, assignee: str, priority: str, status: str, due_date: str):
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        updated_task = Task(
            id=task_id,
            title=title.strip(),
            description=description.strip(),
            assignee=assignee.strip() or "Unassigned",
            priority=priority,
            status=status,
            due_date=due_date.strip() or "2026-11-30"
        )
        self.service.update_task(updated_task)

    def remove_task(self, task_id: int):
        self.service.delete_task(task_id)

    def run_end_of_day_scheduler(self) -> int:
        return self.service.auto_reschedule_uncompleted()

    def get_users(self) -> list[dict]:
        return self.service.get_team_members()

    def create_user(self, name: str, role: str, platform: str):
        if not name.strip():
            raise ValueError("Member name cannot be empty.")
        self.service.add_team_member(name.strip(), role.strip() or "Developer", platform.strip() or "General")

    def edit_user(self, user_id: int, name: str, role: str, platform: str):
        if not name.strip():
            raise ValueError("Member name cannot be empty.")
        self.service.update_team_member(user_id, name.strip(), role.strip() or "Developer", platform.strip() or "General")

    def remove_user(self, user_id: int):
        self.service.delete_team_member(user_id)