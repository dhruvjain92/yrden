import typer

assistant = typer.Typer()


def style(text, severity=""):
    if severity == "info":
        formatted_text = typer.style(text, fg=typer.colors.GREEN, bold=True)
    elif severity == "warning":
        formatted_text = typer.style(text, fg=typer.colors.YELLOW, bold=True)
    elif severity == "error":
        formatted_text = typer.style(text, fg=typer.colors.RED, bold=True)
    elif severity == "casual":
        formatted_text = typer.style(text, fg=typer.colors.ORANGE, bold=True)
    else:
        formatted_text = text
    return formatted_text


def speak(text, severity=""):
    typer.echo(style(text, severity))


def ask(text, severity=""):
    return typer.prompt(style(text, severity))


def run(exception):
    speak(exception, "error")


def confirm(text, severity=""):
    return typer.confirm(style(text, severity))
