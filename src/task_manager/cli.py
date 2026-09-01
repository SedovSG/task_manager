import typer
from rich.console import Console
from rich.table import Table

from task_manager.manager import TaskManager
from task_manager.models import Priority, Status
from task_manager.storage import TaskStorage

app: typer.Typer = typer.Typer(help="Мощный CLI менеджер задач")
console: Console = Console()

manager = TaskManager(TaskStorage())

@app.command()
def add(title: str, priority: Priority = Priority.MEDIUM):
    """Добавить новую задачу."""
    task = manager.add_task(title, priority)
    console.print(f"[green]Задача добавлена:[/green] {task}")

@app.command(name="list")
def list_tasks():
    """Показать все задачи (отсортированные)."""
    tasks = manager.get_sorted_tasks()

    if not tasks:
        console.print("[yellow]Список задач пуст.[/yellow]")
        return

    table = Table(title="Мои задачи", show_lines=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Статус", justify="center")
    table.add_column("Приоритет", justify="center")
    table.add_column("Название", style="white")

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
def done(query: str) -> None:
    """Отметить задачу как выполненную по ID или названию."""

    success, matches = manager.complete_task_by_query(query)

    if not matches:
        console.print(f"[red]Задача с ID {query} не найдена.[/red]")
    elif len(matches) > 1:
        console.print(f"[red]Найдено несколько задач с ID {query}. Укажите конкретный ID.[/red]")
        for task in matches:
            console.print(f"  - [cyan]{task.id}[/cyan]: {task.title}")
    else:
        task = matches[0]

        if success:
            console.print(f"[green]Задача {task.id} выполнена![/green]")
        else:
            console.print(f"[red]Задача с ID {task.id} не найдена.[/red]")

@app.command()
def remove(query: str) -> None:
    """Удалить задачу по ID или названию."""

    success, matches = manager.remove_task_by_query(query)

    if not matches:
        console.print(f"[red]Задача с ID {query} не найдена.[/red]")
    elif len(matches) > 1:
        console.print(f"[red]Найдено несколько задач с ID {query}. Укажите конкретный ID.[/red]")
        for task in matches:
            console.print(f"  - [cyan]{task.id}[/cyan]: {task.title}")
    else:
        task = matches[0]

        if success:
            console.print(f"[red]Задача {task.id} удалена.[/red]")
        else:
            console.print(f"[red]Задача {task.id} не найдена.[/red]")

if __name__ == "__main__":
    app()
