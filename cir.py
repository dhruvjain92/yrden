from core.assistant import *
from core.handler import Handler
import typer


def main(
    mode: str = typer.Option("ir", "--mode"),
    plugin_name: str = typer.Option("", "--name"),
    format: str = typer.Option("json", "--format"),
):

    Handler(mode, plugin_name, format)


def start():
    typer.run(main)


start()
