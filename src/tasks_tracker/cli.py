from datetime import datetime
from typing import Optional

from typer import Exit, Option, Typer, echo

from tasks_tracker.configs import (
    ADDING_TASK_ERROR,
    ADDING_TASK_SUCCESS,
    DB_DATE_FORMAT,
    DISPLAYING_DATE_FORMAT,
    __app_name__,
    __author__,
    __version__,
)
from tasks_tracker.database import TasksTrackerData
from tasks_tracker.model import Task
from tasks_tracker.typing import Priority, Status
from tasks_tracker.utils import (
    format_db_date_str,
    get_task_priority_value,
    get_task_status_value,
    input_data_validation,
    print_error,
    print_success_message,
    print_task_detail,
)

cli_controller = Typer(add_completion=False)

app_data = TasksTrackerData()


def _show_version_callback(value: bool) -> None:
    if value:
        echo(f"{__app_name__} - version: {__version__}")
        raise Exit()


# Author check callback
def _show_author_callback(value: bool) -> None:
    if value:
        echo(f"Tasks Tracker CLI is made by {__author__}")
        raise Exit()


@cli_controller.callback()
def main(
    author: Optional[bool] = Option(
        None,
        "--author",
        "-a",
        help="Show author of Tasks Tracker CLI and exit.",
        callback=_show_author_callback,
        is_eager=True,
    ),
    version: Optional[bool] = Option(
        None,
        "--version",
        "-v",
        help="Show version of Tasks Tracker CLI and exit.",
        callback=_show_version_callback,
        is_eager=True,
    ),
) -> None:
    return


@cli_controller.command()
def add(
    title: str,
    priority: Optional[Priority] = Option(
        None,
        "--priority",
        "-p",
        help="Set task's priority.",
        is_eager=True,
        show_default=False,
    ),
    status: Optional[Status] = Option(
        None,
        "--status",
        "-s",
        help="Set task's status.",
        is_eager=True,
        show_default=False,
    ),
    description: Optional[str] = Option(
        None,
        "--description",
        "-d",
        help="Set task's description.",
        is_eager=True,
        show_default=False,
    ),
    start_date: Optional[datetime] = Option(
        None,
        "--start-date",
        "-sd",
        help="Set the start date. E.g 11/11/2011",
        is_eager=True,
        show_default=False,
        formats=[DISPLAYING_DATE_FORMAT],
    ),
    end_date: Optional[datetime] = Option(
        None,
        "--end-date",
        "-ed",
        help="Set the end date. E.g 11/11/2011",
        is_eager=True,
        show_default=False,
        formats=[DISPLAYING_DATE_FORMAT],
    ),
) -> None:
    input_data_validation(
        title=title, description=description, start_date=start_date, end_date=end_date
    )

    task = Task(
        None,
        title=title,
        status=get_task_status_value(status) or Status.NOT_STARTED.value,
        priority=get_task_priority_value(priority) or Priority.LOW.value,
        description=description,
        start_date=format_db_date_str(start_date) or datetime.now().strftime(DB_DATE_FORMAT),
        end_date=format_db_date_str(end_date),
    )

    adding_new_task_success = app_data.add_new_task(task)

    if adding_new_task_success:
        print_success_message(ADDING_TASK_SUCCESS)
        print_task_detail(task)
    else:
        print_error(ADDING_TASK_ERROR)
