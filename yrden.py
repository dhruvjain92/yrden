from core.handler import Handler
import typer
import datetime


def main(
    mode: str = typer.Option("ir", "--mode"),
    plugin_name: str = typer.Option("", "--name"),
    format: str = typer.Option("json", "--format"),
    output_file: str = typer.Option(
        datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"), "--output-file"
    ),
):
    Handler(mode, plugin_name, format, output_file)


def start():
    typer.run(main)


start()
