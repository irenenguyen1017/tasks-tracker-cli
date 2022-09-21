from . import cli, configs


def main():
    cli.cli_controller(prog_name=configs.__app_name__)
