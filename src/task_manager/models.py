import uuid
from datetime import datetime
from enum import Enum
from typing import final, override
from zoneinfo import ZoneInfo


class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Status(Enum):
    TODO = "TODO"
    DONE = "DONE"

@final
class Task:
    def __init__(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        task_id: str | None = None,
        status: Status = Status.TODO,
        created_at: str | None = None,
    ) -> None:
        self._id = task_id if task_id else str(uuid.uuid4())[:8]
        self.title = title
        self.priority = priority
        self._status = status
        self._created_at = created_at or datetime.now(tz=ZoneInfo("Asia/Yekaterinburg"))

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, value: Status) -> None:
        self._status = value

    @property
    def created_at(self) -> str:
        return str(self._created_at)

    @created_at.setter
    def created_at(self, value: str) -> None:
        self._created_at = value


    @property
    def id(self) -> str:
        return self._id

    @override
    def __str__(self) -> str:
        icon = "✅" if self.status == Status.DONE else "⬜️"
        return f"{icon} [{self.priority.name}] {self.title} (ID: {self.id})"

    @override
    def __repr__(self) -> str:
        return f"Task(id='{self.id}', title='{self.title}', priority={self.priority})"

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self._id == other._id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        if self.status != other.status:
            return self.status == Status.TODO
        return bool(self.priority.value > other.priority.value)
