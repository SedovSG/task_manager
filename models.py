from datetime import datetime
from enum import Enum
import uuid

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH= 3
class Status(Enum):
    TODO = "TODO"
    DONE = "DONE"

class Task:
    def __init__(self,title:str, priority:Priority = Priority.MEDIUM) -> None:
        self._id = str(uuid.uuid4())[:8]
        self.title = title
        self.priority = priority
        self._status = Status.TODO
        self._created_at = datetime.now()

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self,value:Status) -> None:
        if not isinstance(value, Status):
            raise ValueError("Неверный статус задачи!")
        self._status = value

    @property
    def id(self) -> str:
        return self._id

    def __str__(self) -> str:
        icon =  "✅" if self.status == Status.DONE else "⬜️"
        return f"{icon} [{self.priority.name}] {self.title} (ID: {self.id})"
    def __report__(self) -> str:
        return f"TASK(id='{self.id}',title = '{self.title}',piority = '{self.priority}')"
    def __eq__(self, other) -> bool:
        if not isinstance(other,Task):
            return NotImplemented
        return self._id == other._id
    def __lt__(self, other) -> bool:
        if self.status != other.status:
            return self.status == Status.TODO
        return bool(self.priority.value > other.priority.value)
