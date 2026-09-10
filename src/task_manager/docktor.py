import sys
from pathlib import Path

from rich.console import Console

console = Console()


def check_enveronment() -> bool:
    """ Проверяет окружения """
    console.print("\n[bold]Проверка окружения:[/bold]")

    is_ok = True

    console.print(f"✓ Python {sys.version.split()[0]}")

    try:
        import sqlite3
        console.print(f"✓ SQLite3 {sqlite3.sqlite_version}")
    except ImportError:
        console.print("[red]✗ sqlite3 не установлен.[/red]")
        console.print("→ sudo apt install python3-sqlite3")
        is_ok = False

    try:
        import typer
        import rich
        import dotenv
        console.print(f"✓ Пакеты [bold]typer, rich, dotenv[/bold] установлены")
    except ImportError as e:
        console.print(f"[red]✗ Отсутствие: {e}[/red]")
        console.print("→ uv sync")
        is_ok = False

    console.print()
    return is_ok
