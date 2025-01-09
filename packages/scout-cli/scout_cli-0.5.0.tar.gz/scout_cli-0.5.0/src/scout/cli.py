import typer
from .commands import list_command, jump_command

app = typer.Typer(help="Scout - A modern alternative to ls and cd commands")

# Register the list command as the default command
app.command()(list_command)

# Register the jump command
app.command(name="jump")(jump_command)

if __name__ == "__main__":
    app() 