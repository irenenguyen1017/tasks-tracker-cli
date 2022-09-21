from typing import Optional

from rich.console import Console

console = Console()


def print_error(error_message: str, with_trace: Optional[bool] = False) -> None:
    if with_trace:
        console.print_exception()
    console.print(f"[bold bright_red]{error_message}[/bold bright_red]")
