import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from task_manager.docktor import check_enveronment
from task_manager.manager import TaskManager
from task_manager.models import Priority, Status
from task_manager.storage import TaskStorage

app: typer.Typer = typer.Typer(help="Мощный CLI менеджер задач")
console: Console = Console()

load_dotenv()

manager = TaskManager(TaskStorage())

@app.command()
def add(
    title: str,
    priority: Priority = Priority.MEDIUM
) -> None:
    """Добавить новую задачу."""
    task = manager.add_task(title, priority)
    console.print(f"[green]Задача добавлена:[/green] {task}")

@app.command(name="list")
def list_tasks() -> None:
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
        status_style = "green" if task.status == Status.DONE else "red"

        table.add_row(
            task.id,
            f"[{status_style}]{task.status.value}[/{status_style}]",
            task.priority.name,
            task.title,
            style=status_style,
        )

    console.print(table)

@app.command()
def done(query: str) -> None:
    """Отметить задачу как выполненную по ID или названию."""

    success, matches = manager.complete_task_by_query(query)

    if not matches:
        console.print(f"[red]Задача по запросу '{query}' не найдена.[/red]")
    elif len(matches) > 1:
        console.print(
            f"[yellow]Найдено несколько задач ({len(matches)}). Уточните запрос:[/yellow]"
        )
        for task in matches:
            console.print(f"  - [cyan]{task.id}[/cyan]: {task.title}")
    elif success:
        console.print(f"[green]Задача '{matches[0].title}' выполнена![/green]")
        return

@app.command()
def remove(query: str) -> None:
    """Удалить задачу по ID или названию."""

    success, matches = manager.remove_task_by_query(query)

    if not matches:
        console.print(f"[red]Задача по запросу '{query}' не найдена.[/red]")
    elif len(matches) > 1:
        console.print(
            f"[yellow]Найдено несколько задач ({len(matches)}). Уточните запрос:[/yellow]"
        )
        for task in matches:
            console.print(f"  - [cyan]{task.id}[/cyan]: {task.title}")
    elif success:
        console.print(f"[red]Задача '{matches[0].title}' удалена.[/red]")

@app.command()
def clear(flag: bool = typer.Option(
    False,
    "--yes", "-y",
    help="Не запрашивать подтверждение"
)) -> None:
    """ Удалить все задачи (необротимо) """

    if not manager.tasks:
        console.print("[yellow]Список задач пуст.[/yellow]")
        return

    count = len(manager.tasks)

    if not flag:
        confirm = typer.confirm(
            f"Вы уверены, что хотите удалить все задачи ({count})?"
        )

        if not confirm:
            console.print("[yellow]Отменено.[/yellow]")
            return

    removed = manager.remove_all_tasks()
    console.print(f"[red]Удалено задач: {removed}.[/red]")

@app.command()
def doctor() -> None:
    """ Проверить окружение """
    if check_enveronment():
        console.print("[green]✓ Всё готово![/green]")
        raise typer.Exit(0)

    console.print("[red bold]✗ Есть проблемы![/red bold]\n")
    raise typer.Exit(1)


if __name__ == "__main__":
    app()
