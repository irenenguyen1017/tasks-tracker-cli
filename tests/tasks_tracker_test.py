from ast import Eq

from typer.testing import CliRunner

from tasks_tracker import cli, configs

runner = CliRunner()


def test_show_app_version():
    result = runner.invoke(cli.cli_controller, ["--version"])
    assert result.exit_code == 0
    assert f"{configs.__app_name__} - version: {configs.__version__}\n" in result.stdout


def test_show_app_author():
    result = runner.invoke(cli.cli_controller, ["--author"])
    assert result.exit_code == 0
    assert f"Tasks Tracker CLI is made by {configs.__author__}\n" in result.stdout
