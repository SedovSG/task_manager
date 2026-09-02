import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import final

from task_manager.models import Priority, Status, Task


@final
class TaskStorage:
    def __init__(self, db_path: str = "data/tasks.db") -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """ Коннектор к БД SQLite3 """

        connect = sqlite3.connect(self._db_path)
        try:
            yield connect
            connect.commit()
        except Exception:
            connect.rollback()
            raise
        finally:
            connect.close()

    def _init_db(self) -> None:
        """Создаёт таблицу taks, если её нет """

        with self._get_connection() as connect:
            _ = connect.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'TODO',
                    created_at TEXT NOT NULL
                )
            """)

    def save(self, tasks: list[Task]) -> None:
        """ Сохряняет список задач в БД (перезапись) """

        with self._get_connection() as connect:
            _ = connect.execute("delete from tasks")
            for task in tasks:
                _ = connect.execute("""
                    INSERT INTO tasks (id, title, priority, status, created_at)
                        VALUES (?, ?, ?, ?, ?)
                """,
                (
                    task.id,
                    task.title,
                    task.priority.name,
                    task.status.value,
                    task.created_at,
                )
            )

    def load(self) -> list[Task]:
        """ Выгружает задачи из БД """

        with self._get_connection() as connect:
            cursor = connect.execute(
                "SELECT id, title, priority, status, created_at FROM tasks"
            )
            rows = cursor.fetchall()

        tasks: list[Task] = []
        for row in rows:
            task_id, title, priority_name, status_name, created_at = row

            task = Task(
                title=title,
                priority=Priority[priority_name],
            )
            task.status = Status[status_name]
            tasks.append(task)

        return tasks
