import typer
from .commands import list_command

app = typer.Typer(help="Scout - A modern alternative to ls command")

app.command()(list_command)

if __name__ == "__main__":
    app() 