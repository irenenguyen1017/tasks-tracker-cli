from datetime import datetime
from typing import List, Optional

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typer import BadParameter

from tasks_tracker.configs import DB_DATE_FORMAT, DISPLAYING_DATE_FORMAT, NO_TASK_FOUND
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


def print_text_with_panel(
    title: Optional[str] = None,
    content: Optional[str] = None,
    border_style: Optional[str] = "bright_green",
) -> None:
    console.print(
        Panel(
            content,
            title=title,
            title_align="left",
            border_style=border_style,
        )
    )


def print_error(error_message: str, with_trace: Optional[bool] = False) -> None:
    if with_trace:
        console.print_exception()
    print_text_with_panel(title="Error", content=error_message, border_style="bright_red")


def print_success_message(message: str) -> None:
    print_text_with_panel(content=message, border_style="bright_green")


def get_task_status_value(status: Optional[Status] = None) -> Optional[str]:
    return status.value if status else None


def get_task_priority_value(priority: Optional[Priority] = None) -> Optional[str]:
    return priority.value if priority else None


def format_db_date_str(date: Optional[datetime]) -> Optional[str]:
    return date.strftime(DB_DATE_FORMAT) if date else None


def styling_status(status: Optional[str]) -> str:
    if status == Status.DONE.value:
        return f"[bold spring_green2]{enum_value_to_str(status)}[/bold spring_green2]"
    elif status == Status.ON_HOLD.value:
        return f"[bold orange_red1]{enum_value_to_str(status)}[/bold orange_red1]"
    elif status == Status.IN_PROGRESS.value:
        return f"[bold turquoise2]{enum_value_to_str(status)}[/bold turquoise2]"
    else:
        return enum_value_to_str(status)


def styling_priority(priority: Optional[str]) -> str:
    if priority == Priority.HIGH.value:
        return f"[bold orange_red1]{enum_value_to_str(priority)}[/bold orange_red1]"
    elif priority == Priority.MEDIUM.value:
        return f"[bold bright_cyan]{enum_value_to_str(priority)}[/bold bright_cyan]"
    else:
        return f"[bold]{enum_value_to_str(priority)}[/bold]"


def print_date_end_with_warning(date_end: Optional[str]) -> Optional[str]:
    display_date_end = print_date(date_end)

    if date_end is None:
        return display_date_end

    days_left = (datetime.strptime(date_end, DB_DATE_FORMAT) - datetime.now()).days

    if days_left == 0:
        return f"[orange1]{display_date_end}[/orange1] \n[orange1 bold]Expired soon[/orange1 bold]"
    elif days_left < 0:
        return f"[bright_red]{display_date_end}[/bright_red] \n[bright_red bold]Expired[/bright_red bold]"
    else:
        return display_date_end


def print_task_detail(task: Task) -> None:
    console.print()
    table = Table(show_header=False, show_lines=True, box=box.ROUNDED)
    table.add_column(style="bold", min_width=10)
    table.add_column(style="blink", no_wrap=False, min_width=50)
    table.add_row("[light_green]ID[/light_green]", f"[magenta]{task.id}[/magenta]")
    table.add_row(
        "[light_green]Title[/light_green]",
        f"[magenta]{task.title.capitalize() if task.title else '-'}[/magenta]",
    )
    table.add_row(
        "[light_green]Description[/light_green]",
        f"[magenta]{task.description if task.description else 'Not provided'}[/magenta]",
    )
    table.add_row("[light_green]Priority[/light_green]", styling_priority(task.priority))
    table.add_row(
        "[light_green]Status[/light_green]",
        styling_status(task.status),
    )
    table.add_row(
        "[light_green]Start date[/light_green]", f"[magenta]{print_date(task.start_date)}[/magenta]"
    )
    table.add_row(
        "[light_green]End date[/light_green]", f"[magenta]{print_date(task.end_date)}[/magenta]"
    )
    console.print(table)


def print_tasks_list_table(tasks: List[Task]) -> None:
    console.print()
    if len(tasks) == 0:
        print_success_message(NO_TASK_FOUND)
    else:
        console.print("[bold turquoise2]TASKS LIST[/bold turquoise2]")
        console.print()
        table = Table(show_header=True, show_lines=True, box=box.ROUNDED)
        table.add_column("[bold magenta2]Id[/bold magenta2]", width=10)
        table.add_column("[bold magenta2]Title[/bold magenta2]", min_width=10, max_width=20)
        table.add_column(
            "[bold magenta2]Description[/bold magenta2]",
            min_width=30,
            max_width=50,
            justify="left",
            no_wrap=False,
        )
        table.add_column("[bold magenta2]Priority[/bold magenta2]", width=10, no_wrap=False)
        table.add_column("[bold magenta2]Status[/bold magenta2]", width=12, no_wrap=False)
        table.add_column("[bold magenta2]Start date[/bold magenta2]", width=12)
        table.add_column("[bold magenta2]End date[/bold magenta2]", width=14, no_wrap=False)
        for task in tasks:
            table.add_row(
                task.id,
                task.title.capitalize() if task.title else "-",
                f"[left]{task.description.capitalize() if task.description else 'Not provided'}[/left]",
                styling_priority(task.priority),
                styling_status(task.status),
                print_date(task.start_date),
                print_date_end_with_warning(task.end_date),
            )
        console.print(table)
