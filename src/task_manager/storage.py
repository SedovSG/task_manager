import json
from pathlib import Path
from typing import cast, final

from task_manager.models import Priority, Status, Task


@final
class TaskStorage:
    def __init__(self, file_path: str = "tasks.json") -> None:
        self._file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if not self._file_path.exists():
            _ = self._file_path.write_text("[]")

    def save(self, tasks: list[Task]) -> None:
        data: list[dict[str, str]] = []
        for task in tasks:
            data.append({
                "id": task.id,
                "title": task.title,
                "priority": task.priority.name,
                "status": task.status.name,
            })
        _ = self._file_path.write_text(json.dumps(data, indent=4, ensure_ascii=False))

    def load(self) -> list[Task]:
        data = cast(list[dict[str, str]], json.loads(self._file_path.read_text()))
        tasks: list[Task] = []

        for item in data:
            task = Task(item["title"], Priority[item["priority"]], item["id"])
            task.status = Status[item["status"]]
            tasks.append(task)
        return tasks
