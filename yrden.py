from core.assistant import *
from core.handler import Handler
import typer


def main(
    mode: str = typer.Option("ir", "--mode"),
    plugin_name: str = typer.Option("", "--name"),
    format: str = typer.Option("json", "--format"),
    output_file: str = typer.Option("temp_file", "--output-file"),
):

    Handler(mode, plugin_name, format, output_file)


def start():
    typer.run(main)


start()
