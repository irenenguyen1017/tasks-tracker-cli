from typing import Optional

from typer import Exit, Option, Typer, echo

from tasks_tracker.configs import __app_name__, __author__, __version__

cli_controller = Typer(add_completion=False)


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
