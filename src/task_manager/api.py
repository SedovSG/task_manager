from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from task_manager.models import Priority, Status, Task
from task_manager.storage import TaskStorage

app = FastAPI(title="Task Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Название задачи")
    priority: str = Field(default="MEDIUM", description="Приоритет")

class TaskUpdate(BaseModel):
    title: str | None = None
    priority: str | None = None
    status: str | None = None

storage: TaskStorage = TaskStorage()

@app.get("/")
async def root():
    """ Главная страница """
    return FileResponse("static/index.html")

@app.get("/api/tasks")
async def get_tasks():
    """ Получает список задач """
    tasks = storage.load()
    return {
        "count": len(tasks),
        "tasks": [
            {
               "id": task.id,
               "title": task.title,
               "priority": task.priority.value,
               "status": task.status.value,
            }
            for task in tasks
        ]
    }

@app.post("/api/tasks", status_code=201)
async def create_task(task_data: TaskCreate) -> object:
    """ Добавление задачи """

try:
    priority = Priority[task_data.priority.upper()]
except KeyError:
    raise HTTPException(
        status_code=400,
        detail=f"Неверный приоритет '{task_data.priority}'. "
            f"Допустимые значения: LOW, MEDIUM, HIGH"
    )

tasks = storage.load()

new_task = Task(title=task_data.title, priority=task_data.priority)

tasks.append(new_task)
storage.save(tasks)

return {
    "id": new_task.id,
    "title": new_task.title,
    "priority": new_task.priority.value,
    "status": new_task.status.value,
    "created_at": new_task.created_at.isoformat(),
}
