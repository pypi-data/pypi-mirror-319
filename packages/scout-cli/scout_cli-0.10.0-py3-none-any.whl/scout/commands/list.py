from rich.console import Console
from rich.table import Table
from pathlib import Path
from datetime import datetime
import typer

console = Console()

def get_file_info(path: Path):
    stats = path.stat()
    return {
        "name": path.name,
        "size": stats.st_size,
        "modified": datetime.fromtimestamp(stats.st_mtime),
        "is_dir": path.is_dir()
    }

def list_command(
    path: str = typer.Argument(".", help="Directory path to list"),
    all: bool = typer.Option(False, "--all", "-a", help="Show hidden files"),
    sort: str = typer.Option("name", "--sort", "-s", help="Sort by: name, size, modified")
):
    """Scout through directory contents with a modern UI"""
    try:
        directory = Path(path)
        if not directory.exists():
            console.print(f"[red]Error: Path '{path}' does not exist[/red]")
            raise typer.Exit(1)

        files = []
        for item in directory.iterdir():
            if not all and item.name.startswith('.'):
                continue
            files.append(get_file_info(item))

        # Sort files
        sort_key = lambda x: x["name"].lower()
        if sort == "size":
            sort_key = lambda x: x["size"]
        elif sort == "modified":
            sort_key = lambda x: x["modified"]
        
        files.sort(key=sort_key)

        # Create and populate table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name")
        table.add_column("Size", justify="right")
        table.add_column("Modified")
        table.add_column("Type")

        for file in files:
            name_color = "blue" if file["is_dir"] else "green"
            name = f"[{name_color}]{file['name']}[/{name_color}]"
            size = f"{file['size']:,} B" if not file["is_dir"] else "DIR"
            modified = file["modified"].strftime("%Y-%m-%d %H:%M")
            file_type = "Directory" if file["is_dir"] else "File"
            
            table.add_row(name, size, modified, file_type)

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1) 