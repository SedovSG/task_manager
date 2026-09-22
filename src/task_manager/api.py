from tokenize import String
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.task_manager import storage

app = FastAPI(title="Task Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")

class TaskCreate(BaseModel):
    title: str
    priority: str = "MEDIUM"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

storage = storage.TaskStorage()

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
async def create_task(task_data: BaseModel):
    pass
