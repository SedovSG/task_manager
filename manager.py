from typing import final

from models import Priority, Status, Task
from storage import TaskStorage


@final
class TaskManager:
    def __init__(self, storage: TaskStorage):
        self._storage = storage
        self.tasks: list[Task] = self._storage.load()

    def add_task(self, title: str, priority: Priority) -> Task:
        new_task = Task(title, priority)
        self.tasks.append(new_task)
        self.save()

        return new_task

    def complete_task(self, task_id: str) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.status = Status.DONE
                self.save()
                return True
        return False

    def remove_task(self, task_id: str) -> bool:
        lenth = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if lenth != len(self.tasks):
            self.save()
            return True
        return False

    def get_sorted_tasks(self) -> list[Task]:
        return sorted(self.tasks)

    def save(self) -> None:
        self._storage.save(self.tasks)
