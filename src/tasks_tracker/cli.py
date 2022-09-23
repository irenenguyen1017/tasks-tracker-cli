from datetime import datetime
from typing import Optional

from typer import Exit, Option, Typer, confirm, echo

from tasks_tracker.configs import (
    ADDING_TASK_ERROR,
    ADDING_TASK_SUCCESS,
    DB_DATE_FORMAT,
    DELETE_ALL_TASKS_ERROR,
    DELETE_ALL_TASKS_SUCCESS,
    DELETE_TASK_ERROR,
    DELETE_TASK_SUCCESS,
    DISPLAYING_DATE_FORMAT,
    NO_TASK_FOUND_ERROR,
    UPDATE_TASK_ERROR,
    UPDATE_TASK_SUCCESS,
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
    print_tasks_list_table,
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
        help="Set the start date. E.g 22/02/2022",
        is_eager=True,
        show_default=False,
        formats=[DISPLAYING_DATE_FORMAT],
    ),
    end_date: Optional[datetime] = Option(
        None,
        "--end-date",
        "-ed",
        help="Set the end date. E.g 22/02/2022",
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


@cli_controller.command()
def list(
    status: Optional[Status] = Option(
        None,
        "--status",
        "-s",
        help="Filter by status.",
        is_eager=True,
        show_default=False,
    ),
    priority: Optional[Priority] = Option(
        None,
        "--priority",
        "-p",
        help="Filter by priority.",
        is_eager=True,
        show_default=False,
    ),
    start_date: Optional[datetime] = Option(
        None,
        "--start-date",
        "-sd",
        help="Filter by the date from the start date. E.g 22/02/2022",
        is_eager=True,
        show_default=False,
        formats=[DISPLAYING_DATE_FORMAT],
    ),
    end_date: Optional[datetime] = Option(
        None,
        "--end-date",
        "-ed",
        help="Filter by the date before the end date. E.g 22/02/2022",
        is_eager=True,
        show_default=False,
        formats=[DISPLAYING_DATE_FORMAT],
    ),
) -> None:
    tasks = app_data.get_tasks_list(status, priority, start_date, end_date)
    print_tasks_list_table(tasks)


@cli_controller.command()
def update(
    id: str,
    is_forced_update: bool = Option(False, "--force", "-f", help="Force update tasks"),
    title: Optional[str] = Option(
        None,
        "--title",
        "-t",
        help="Update task's title",
        is_eager=True,
        show_default=False,
    ),
    priority: Optional[Priority] = Option(
        None,
        "--priority",
        "-p",
        help="Update task's priority.",
        is_eager=True,
        show_default=False,
    ),
    status: Optional[Status] = Option(
        None,
        "--status",
        "-s",
        help="Update task's status.",
        is_eager=True,
        show_default=False,
    ),
    description: Optional[str] = Option(
        None,
        "--description",
        "-d",
        help="Update task's description.",
        is_eager=True,
        show_default=False,
    ),
    start_date: Optional[datetime] = Option(
        None,
        "--start-date",
        "-sd",
        help="Update the start date. E.g 22/02/2022",
        is_eager=True,
        show_default=False,
        formats=[DISPLAYING_DATE_FORMAT],
    ),
    end_date: Optional[datetime] = Option(
        None,
        "--end-date",
        "-ed",
        help="Update the end date. E.g 22/02/2022",
        is_eager=True,
        show_default=False,
        formats=[DISPLAYING_DATE_FORMAT],
    ),
) -> None:
    input_data_validation(
        id=id, title=title, description=description, start_date=start_date, end_date=end_date
    )

    can_update = confirm("Update this task with provided data?") if not is_forced_update else True

    if can_update:
        current_task = app_data.find_task_by_id(id)

        if current_task:
            updated_task = Task(
                id=id,
                title=title or current_task.title,
                status=get_task_status_value(status) or current_task.status,
                priority=get_task_priority_value(priority) or current_task.priority,
                description=description or current_task.description,
                start_date=format_db_date_str(start_date) or current_task.start_date,
                end_date=format_db_date_str(end_date) or current_task.end_date,
            )

            is_task_updated_successfully = app_data.update_task(updated_task)

            if is_task_updated_successfully:
                print_success_message(UPDATE_TASK_SUCCESS)
                print_task_detail(updated_task)
            else:
                print_error(UPDATE_TASK_ERROR)
        else:
            print_error(error_message=NO_TASK_FOUND_ERROR)

    else:
        raise Exit()


@cli_controller.command()
def delete(
    id: str,
    is_forced_delete: bool = Option(
        False,
        "--force",
        "-f",
        help="Force deleting task",
    ),
):
    input_data_validation(id=id)

    can_delete = confirm("Surely you want to delete this task?") if not is_forced_delete else True

    if can_delete:
        current_task = app_data.find_task_by_id(id)

        if current_task:
            is_task_deleted = app_data.delete_task(id)

            if is_task_deleted:
                print_success_message(DELETE_TASK_SUCCESS)
            else:
                print_error(DELETE_TASK_ERROR)
        else:
            print_error(error_message=NO_TASK_FOUND_ERROR)
    else:
        raise Exit()


@cli_controller.command()
def delete_all(
    is_forced_delete_all: bool = Option(
        False,
        "--force",
        "-f",
        help="Force removing all tasks",
    ),
):
    can_delete_all = (
        confirm("Surely you want to delete all your tasks?") if not is_forced_delete_all else True
    )

    if can_delete_all:
        all_tasks_deleted = app_data.delete_all_tasks()

        if all_tasks_deleted:
            print_success_message(DELETE_ALL_TASKS_SUCCESS)
        else:
            print_error(DELETE_ALL_TASKS_ERROR)
    else:
        raise Exit()
