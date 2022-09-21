from unittest.mock import Mock

from typer.testing import CliRunner

from tasks_tracker.cli import cli_controller
from tasks_tracker.configs import (
    ADDING_TASK_ERROR,
    ADDING_TASK_SUCCESS,
    __app_name__,
    __author__,
    __version__,
)
from tasks_tracker.database import TasksTrackerData

runner = CliRunner()


def test_show_app_version():
    result = runner.invoke(cli_controller, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} - version: {__version__}\n" in result.stdout


def test_show_app_author():
    result = runner.invoke(cli_controller, ["--author"])
    assert result.exit_code == 0
    assert f"Tasks Tracker CLI is made by {__author__}\n" in result.stdout


# Add command tests


def test_add_command_with_help_option():
    result = runner.invoke(cli_controller, ["add", "--help"])
    assert result.exit_code == 0
    # It should show --priority option
    assert "--priority" in result.stdout
    # It should show --status option
    assert "--status" in result.stdout
    # It should show --description option
    assert "--description" in result.stdout
    # It should show --start-date option
    assert "--start-date" in result.stdout
    # It should show --start-date option
    assert "--end-date" in result.stdout


def test_add_command_with_failure():
    TasksTrackerData.add_new_task = Mock(return_value=False)
    result = runner.invoke(cli_controller, ["add", "task-title"])
    assert result.exit_code == 0
    assert ADDING_TASK_ERROR in result.stdout


def test_add_command_with_success():
    TasksTrackerData.add_new_task = Mock(return_value=True)
    result = runner.invoke(cli_controller, ["add", "task-title"])
    assert result.exit_code == 0
    assert ADDING_TASK_SUCCESS in result.stdout
