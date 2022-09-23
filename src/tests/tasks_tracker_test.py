from unittest.mock import Mock

from typer.testing import CliRunner

from tasks_tracker.cli import cli_controller
from tasks_tracker.configs import (
    ADDING_TASK_ERROR,
    ADDING_TASK_SUCCESS,
    DELETE_ALL_TASKS_ERROR,
    DELETE_ALL_TASKS_SUCCESS,
    DELETE_TASK_ERROR,
    DELETE_TASK_SUCCESS,
    NO_TASK_FOUND,
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

runner = CliRunner()

mock_task_data = (
    (
        "1",
        "title_1",
        Status.IN_PROGRESS.value,
        Priority.HIGH.value,
        "task 1 description",
        "2022-02-02",
        None,
    ),
    (
        "2",
        "title_2",
        Status.DONE.value,
        Priority.MEDIUM.value,
        "task 2 description",
        "2022-01-01",
        "2022-11-11",
    ),
)


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


# List command tests


def test_list_command_with_help_option():
    result = runner.invoke(cli_controller, ["list", "--help"])
    assert result.exit_code == 0
    # It should show --priority option
    assert "--priority" in result.stdout
    # It should show --status option
    assert "--status" in result.stdout
    # It should show --start-date option
    assert "--start-date" in result.stdout
    # It should show --start-date option
    assert "--end-date" in result.stdout


def test_list_command_with_empty_list():
    TasksTrackerData.get_tasks_list = Mock(return_value=[])
    result = runner.invoke(cli_controller, ["list"])
    assert result.exit_code == 0
    assert NO_TASK_FOUND in result.stdout


def test_list_command_with_data_exist():
    TasksTrackerData.get_tasks_list = Mock(return_value=[Task(*i) for i in mock_task_data])
    result = runner.invoke(cli_controller, ["list"])
    assert result.exit_code == 0
    assert "Title_1" in result.stdout
    assert "Task 1 description" in result.stdout


# Update command tests


def test_update_command_with_help_option():
    result = runner.invoke(cli_controller, ["update", "--help"])
    assert result.exit_code == 0
    # It should show --title option
    assert "--title" in result.stdout
    # It should show --description option
    assert "--description" in result.stdout
    # It should show --priority option
    assert "--priority" in result.stdout
    # It should show --status option
    assert "--status" in result.stdout
    # It should show --start-date option
    assert "--start-date" in result.stdout
    # It should show --start-date option
    assert "--end-date" in result.stdout
    # It should show --force option
    assert "--force" in result.stdout


def test_update_command_with_prompt():
    TasksTrackerData.find_task_by_id = Mock(return_value=None)
    TasksTrackerData.update_task = Mock(return_value=False)
    result = runner.invoke(cli_controller, ["update", "1234567890"])
    assert result.exit_code == 0
    assert "Update this task with provided data?" in result.stdout


def test_update_command_with_no_task_id_error():
    TasksTrackerData.find_task_by_id = Mock(return_value=None)
    TasksTrackerData.update_task = Mock(return_value=False)
    result = runner.invoke(cli_controller, ["update", "1234567890", "-f"])
    assert result.exit_code == 0
    assert NO_TASK_FOUND_ERROR in result.stdout


def test_update_command_without_prompt_and_success():
    TasksTrackerData.find_task_by_id = Mock(return_value=Task(*mock_task_data[0]))
    TasksTrackerData.update_task = Mock(return_value=True)
    result = runner.invoke(cli_controller, ["update", "1234567890", "-f"])
    assert result.exit_code == 0
    assert UPDATE_TASK_SUCCESS in result.stdout


def test_update_command_without_prompt_and_fail():
    TasksTrackerData.find_task_by_id = Mock(return_value=Task(*mock_task_data[0]))
    TasksTrackerData.update_task = Mock(return_value=False)
    result = runner.invoke(cli_controller, ["update", "1234567890", "-f"])
    assert result.exit_code == 0
    assert UPDATE_TASK_ERROR in result.stdout


# Delete command test


def test_detete_command_with_help_option():
    result = runner.invoke(cli_controller, ["delete", "--help"])
    assert result.exit_code == 0
    # It should show --force option
    assert "--force" in result.stdout


def test_delete_command_with_no_task_id_error():
    TasksTrackerData.find_task_by_id = Mock(return_value=None)
    TasksTrackerData.delete_task = Mock(return_value=False)
    result = runner.invoke(cli_controller, ["delete", "1234567890", "-f"])
    assert result.exit_code == 0
    assert NO_TASK_FOUND_ERROR in result.stdout


def test_delete_command_with_prompt():
    TasksTrackerData.delete_task = Mock(return_value=True)
    result = runner.invoke(cli_controller, ["delete", "1234567890"])
    assert result.exit_code == 0
    assert "Surely you want to delete this task?" in result.stdout


def test_delete_command_without_prompt_and_success():
    TasksTrackerData.find_task_by_id = Mock(return_value=Task(*mock_task_data[0]))
    TasksTrackerData.delete_task = Mock(return_value=True)
    result = runner.invoke(cli_controller, ["delete", "1234567890", "-f"])
    assert result.exit_code == 0
    assert DELETE_TASK_SUCCESS in result.stdout


def test_delete_command_without_prompt_and_fail():
    TasksTrackerData.find_task_by_id = Mock(return_value=Task(*mock_task_data[0]))
    TasksTrackerData.delete_task = Mock(return_value=False)
    result = runner.invoke(cli_controller, ["delete", "1234567890", "-f"])
    assert result.exit_code == 0
    assert DELETE_TASK_ERROR in result.stdout


# Delete all command test


def test_detete_all_command_with_help_option():
    result = runner.invoke(cli_controller, ["delete-all", "--help"])
    assert result.exit_code == 0
    # It should show --force option
    assert "--force" in result.stdout


def test_delete_all_command_with_prompt():
    TasksTrackerData.delete_all_tasks = Mock(return_value=True)
    result = runner.invoke(cli_controller, ["delete-all"])
    assert result.exit_code == 0
    assert "Surely you want to delete all your tasks?" in result.stdout


def test_delete_all_command_without_prompt_and_success():
    TasksTrackerData.delete_all_tasks = Mock(return_value=True)
    result = runner.invoke(cli_controller, ["delete-all", "-f"])
    assert result.exit_code == 0
    assert DELETE_ALL_TASKS_SUCCESS in result.stdout


def test_delete_all_command_without_prompt_and_fail():
    TasksTrackerData.delete_all_tasks = Mock(return_value=False)
    result = runner.invoke(cli_controller, ["delete-all", "-f"])
    assert result.exit_code == 0
    assert DELETE_ALL_TASKS_ERROR in result.stdout
