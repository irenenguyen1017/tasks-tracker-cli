from datetime import datetime
from typing import Optional

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typer import BadParameter

from tasks_tracker.configs import DB_DATE_FORMAT, DISPLAYING_DATE_FORMAT
from tasks_tracker.model import Task
from tasks_tracker.typing import Priority, Status

console = Console()


def enum_value_to_str(enum_value: Optional[str]) -> str:
    return enum_value.replace("_", " ").strip().upper() if enum_value else "-"


def task_id_validation(id: Optional[str] = None) -> None:
    if id and len(id) != 10:
        raise BadParameter("ID must have a length of 10 alphabet mixed with number characters.")
    else:
        pass


def task_title_validation(title: Optional[str] = None) -> None:
    if title and len(title) > 30:
        raise BadParameter("Title must not be longer than 30 characters.")
    else:
        pass


def task_description_validation(description: Optional[str] = None) -> None:
    if description and len(description) > 150:
        raise BadParameter("Description must not be longer than 150 characters.")
    else:
        pass


def date_validation(
    start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
) -> None:
    if start_date and start_date < datetime.now():
        raise BadParameter("Start date cannot be past date.")
    elif end_date and end_date < datetime.now():
        raise BadParameter("End date cannot be past date.")
    elif end_date and start_date and end_date < start_date:
        raise BadParameter("End date must be after start date.")
    else:
        pass


def db_to_displaying_date(date_str: str) -> str:
    return datetime.strptime(date_str, DB_DATE_FORMAT).strftime(DISPLAYING_DATE_FORMAT)


def print_date(date: Optional[str], default_date: Optional[str] = None) -> str:
    return db_to_displaying_date(date) if date else default_date if default_date else "Not setting"


def input_data_validation(
    id: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> None:
    task_id_validation(id)
    task_title_validation(title)
    task_description_validation(description)
    date_validation(start_date, end_date)


def print_error(error_message: str, with_trace: Optional[bool] = False) -> None:
    if with_trace:
        console.print_exception()

    console.print(
        Panel(
            error_message,
            title="Error",
            title_align="left",
            border_style="bright_red",
        )
    )


def print_success_message(message: str) -> None:
    console.print(
        Panel(
            message,
            border_style="bright_green",
        )
    )


def get_task_status_value(status: Optional[Status] = None) -> Optional[str]:
    return status.value if status else None


def get_task_priority_value(priority: Optional[Priority] = None) -> Optional[str]:
    return priority.value if priority else None


def format_db_date_str(date: Optional[datetime]) -> Optional[str]:
    return date.strftime(DB_DATE_FORMAT) if date else None


def print_task_detail(task: Task) -> None:
    console.print()
    table = Table(show_header=False, show_lines=True, box=box.ROUNDED)
    table.add_column(style="bold green_yellow", min_width=10)
    table.add_column(style="blink magenta", no_wrap=False, min_width=50)
    table.add_row("Id", task.id)
    table.add_row("Title", task.title.capitalize() if task.title else "-")
    table.add_row(
        "Description",
        task.description if task.description else "Not provided",
    )
    table.add_row(
        "Priority",
        enum_value_to_str(task.priority),
    )
    table.add_row(
        "Status",
        enum_value_to_str(task.status),
    )
    table.add_row("Start date", print_date(task.start_date))
    table.add_row("End date", print_date(task.end_date))
    console.print(table)
