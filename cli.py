from enum import show_flag_values

import storage
import typer
from rich.console import Console
from rich.table import Table
from models import Priority, Status
from manager import TaskManager
from storage import TaskStorage

app = typer.Typer(help="Мощный CLI менеджер задач")
console = Console()

manager = TaskManager(TaskStorage())


@app.command()
def add(title: str, priority: Priority = Priority.MEDIUM):
    task = manager.add_task(title, priority)
    console.print(f"[green]Задача добавлена:[/green] {task}")

@app.command(name="list")
def list_tasks():
    tasks = manager.get_sorted_tasks()

    if not tasks:
        console.print("[yellow]Нет задач[/yellow]")
        return

    table = Table(title="Мои задачи", show_lines=True)
    table.add_column("ID", style="cyan", justify="center", no_wrap=True)
    table.add_column("Статус", justify="center")
    table.add_column("Приоритет", justify="center")
    table.add_column("Название", justify="center")

    for task in tasks:
        status_slyle = "green" if task.status == Status.DONE else "red"

        table.add_row(
            task.id,
            f"[{status_slyle}]{task.status.value}[/{status_slyle}]",
            task.priority.name,
            task.title,
            style=status_slyle
        )
    console.print(table)

@app.command()
def done(task_id: str):
    if manager.complete_task(task_id):
        console.print(f"[green]Задача завершена:[/green] {task_id}")
    else:
        console.print(f"[yellow]Задача не найдена:[/yellow] {task_id}")

@app.command()
def remove(task_id: str):
    if manager.remove_task(task_id):
        console.print(f"[green]Задача удалена:[/green] {task_id}")
    else:
        console.print(f"[red]Задача не найдена:[/red] {task_id}")

if __name__ == "__main__":
    app()
