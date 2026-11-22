import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client
from models.task import Task

load_dotenv()

LOCAL_DB_FILE = "local_data.json"


class SupabaseService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")

        if url.startswith("http") and key:
            self.client: Client = create_client(url, key)
            self.is_connected = True
        else:
            self.client = None
            self.is_connected = False
            self._load_local_data()

    def _load_local_data(self):
        """Încarcă datele salvate pe disc sau creează datele inițiale dacă nu există fișierul."""
        if os.path.exists(LOCAL_DB_FILE):
            try:
                with open(LOCAL_DB_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._mock_tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
                self._mock_users = data.get("users", [])
                return
            except Exception:
                pass

        # Date inițiale la prima pornire
        self._mock_tasks = [
            Task(id=1, title="Set up Git repositories for each project", description="Create GitHub repo for Desktop app", assignee="Evghenia Roman", priority="P1", status="In Progress", due_date="2026-11-23"),
            Task(id=2, title="Make topological architecture diagram", description="Prepare system architecture & UML class diagrams", assignee="Evghenia Roman", priority="P1", status="Ready", due_date="2026-11-24"),
            Task(id=3, title="Set up database (Supabase PostgreSQL)", description="Shared database schema for Web, Mobile, Desktop", assignee="Alexandra Gradinaru", priority="P1", status="In Review", due_date="2026-11-23"),
            Task(id=4, title="Build Mobile UI task list screen", description="Connect mobile app to Supabase API", assignee="Ivo Dubšík", priority="P2", status="Backlog", due_date="2026-11-26"),
            Task(id=5, title="Initialize PyQt6 MVC project structure", description="Setup models, views, controllers, services", assignee="Evghenia Roman", priority="P1", status="Done", due_date="2026-11-22"),
        ]
        self._mock_users = [
            {"id": 1, "name": "Ivo Dubšík", "role": "Mobile Developer", "platform": "Mobile Application"},
            {"id": 2, "name": "Evghenia Roman", "role": "Desktop Admin Developer", "platform": "Desktop Application"},
            {"id": 3, "name": "Alexandra Gradinaru", "role": "Backend & Web Lead", "platform": "Web Application"},
        ]
        self._save_local_data()

    def _save_local_data(self):
        """Salvează toate task-urile și membrii în fișierul local_data.json."""
        if self.is_connected:
            return
        tasks_data = []
        for t in self._mock_tasks:
            d = t.to_dict()
            d["id"] = t.id
            tasks_data.append(d)

        with open(LOCAL_DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"tasks": tasks_data, "users": self._mock_users}, f, indent=2, ensure_ascii=False)

    def get_all_tasks(self) -> list[Task]:
        if self.is_connected:
            response = self.client.table("tasks").select("*").order("id").execute()
            return [Task.from_dict(item) for item in response.data]
        return self._mock_tasks

    def add_task(self, task: Task) -> Task:
        if self.is_connected:
            response = self.client.table("tasks").insert(task.to_dict()).execute()
            return Task.from_dict(response.data[0])

        new_id = max([t.id for t in self._mock_tasks], default=0) + 1
        task.id = new_id
        self._mock_tasks.append(task)
        self._save_local_data()
        return task

    def update_task(self, task: Task):
        if self.is_connected:
            self.client.table("tasks").update(task.to_dict()).eq("id", task.id).execute()
        else:
            for idx, t in enumerate(self._mock_tasks):
                if t.id == task.id:
                    self._mock_tasks[idx] = task
                    break
            self._save_local_data()

    def delete_task(self, task_id: int):
        if self.is_connected:
            self.client.table("tasks").delete().eq("id", task_id).execute()
        else:
            self._mock_tasks = [t for t in self._mock_tasks if t.id != task_id]
            self._save_local_data()

    def auto_reschedule_uncompleted(self) -> int:
        tasks = self.get_all_tasks()
        priority_map = {"P3": "P2", "P2": "P1", "P1": "P1", "Low": "Medium", "Medium": "High", "High": "High"}
        updated_count = 0

        for task in tasks:
            if task.status != "Done":
                task.priority = priority_map.get(task.priority, "P1")
                try:
                    dt = datetime.strptime(task.due_date, "%Y-%m-%d")
                    task.due_date = (dt + timedelta(days=1)).strftime("%Y-%m-%d")
                except ValueError:
                    pass
                self.update_task(task)
                updated_count += 1
        return updated_count

    def get_team_members(self) -> list[dict]:
        return self._mock_users

    def add_team_member(self, name: str, role: str, platform: str):
        new_id = max([u["id"] for u in self._mock_users], default=0) + 1
        self._mock_users.append({"id": new_id, "name": name, "role": role, "platform": platform})
        self._save_local_data()

    def update_team_member(self, user_id: int, name: str, role: str, platform: str):
        for u in self._mock_users:
            if u["id"] == user_id:
                u["name"] = name
                u["role"] = role
                u["platform"] = platform
                break
        self._save_local_data()

    def delete_team_member(self, user_id: int):
        self._mock_users = [u for u in self._mock_users if u["id"] != user_id]
        self._save_local_data()