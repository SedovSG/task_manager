import json
from pathlib import Path
from models import Task, Priority, Status

class TaskStorage:
    def __init__(self, file_path: str = "tasks.json") -> None:
        self._file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if not self._file_path.exists():
            self._file_path.write_text("[]")

    def save(self, tasks: list[Task]) -> None:
        data = []
        for task in tasks:
            data.append({
                "id": task.id,
                "title": task.title,
                "priority": task.priority.name,
                "status": task.status.name,
            })
        self._file_path.write_text(json.dumps(data, indent=4, ensure_ascii=False))

    def load(self) -> list[Task]:
        data = json.loads(self._file_path.read_text())
        tasks = []
        for item in data:
            task = Task(item["title"], Priority[item["priority"]])
            task.status = Status[item["status"]]
            task._id = item["id"]
            tasks.append(task)
        return tasks
