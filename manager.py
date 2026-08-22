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

    def complete_task_by_query(self, query: str) -> tuple[bool, list[Task]]:
        matches: list[Task] = self.find_tasks_by_query(query)
        if len(matches) == 1:
            matches[0].status = Status.DONE
            self.save()
            return True, matches
        return False, []

    def find_tasks_by_query(self, query: str) -> list[Task]:
        query_lower = query.lower()
        return [
            task for task in self.tasks
            if query_lower in task.id.lower() or query_lower in task.title.lower()
        ]

    def remove_task_by_query(self, query: str) -> tuple[bool, list[Task]]:
        matches: list[Task] = self.find_tasks_by_query(query)
        if matches:
            self.tasks.remove(matches[0])
            self.save()
            return True, matches
        return False, []

    def get_sorted_tasks(self) -> list[Task]:
        return sorted(self.tasks)

    def save(self) -> None:
        self._storage.save(self.tasks)
