from datetime import datetime
from typing import Optional

from typer import Exit, Option, Typer, echo

from tasks_tracker.configs import (
    DISPLAYING_DATE_FORMAT,
    __app_name__,
    __author__,
    __version__,
)
from tasks_tracker.database import TasksTrackerData
from tasks_tracker.typing import Priority, Status

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
    print(title)
