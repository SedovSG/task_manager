from typing import final

from task_manager.models import Priority, Status, Task
from task_manager.storage import TaskStorage


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
        return False, matches

    def find_tasks_by_query(self, query: str) -> list[Task]:
        query_lower = query.lower()
        return [
            task for task in self.tasks
            if query_lower in task.id.lower() or query_lower in task.title.lower()
        ]

    def remove_task_by_query(self, query: str) -> tuple[bool, list[Task]]:
        matches: list[Task] = self.find_tasks_by_query(query)
        if len(matches) == 1:
            self.tasks.remove(matches[0])
            self.save()
            return True, matches
        return False, matches

    def remove_all_tasks(self) -> int:
        """ Удаляет все задачи. Возвращает кол-во удалённых. """
        count = len(self.tasks)
        self.tasks.clear()
        self._storage.remove_all()
        return count


    def get_sorted_tasks(self) -> list[Task]:
        return sorted(self.tasks)

    def save(self) -> None:
        self._storage.save(self.tasks)
