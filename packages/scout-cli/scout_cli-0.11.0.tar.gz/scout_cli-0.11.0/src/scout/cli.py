import typer
import os
from .commands import list_command, jump_command, help_command

app = typer.Typer(help="Scout - A modern alternative to ls and cd commands")

# Register the list command as the default command
app.command()(list_command)

# Register the jump command
app.command(name="jump")(jump_command)

# Register the help command
app.command(name="help")(help_command)

def main():
    """Main entry point that handles shell integration"""
    # Run the CLI
    app()
    
    # Check if we need to change directory in the parent shell
    if "SCOUT_NEW_PWD" in os.environ:
        new_pwd = os.environ["SCOUT_NEW_PWD"]
        # Print special sequence that shell can detect
        print(f"\x1b]9;9;{new_pwd}\x1b\\")

if __name__ == "__main__":
    main() 