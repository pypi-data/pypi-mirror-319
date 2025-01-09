from pathlib import Path
import typer
from rich.console import Console
from rich import print
from rich.prompt import Prompt
import os
from typing import Optional, List
from thefuzz import fuzz
from datetime import datetime
from ..functions.smart_predict import SmartPredictor

console = Console()
predictor = SmartPredictor()

def find_matching_directories(search_term: str, max_depth: int = 3) -> List[str]:
    """Find directories that match the search term using fuzzy matching"""
    matches = []
    current = os.getcwd()
    
    # Search in current directory and subdirectories
    for root, dirs, _ in os.walk(current):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # Check depth
        depth = root[len(current):].count(os.sep)
        if depth > max_depth:
            continue

        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            # Calculate fuzzy match ratio
            ratio = fuzz.ratio(search_term.lower(), dir_name.lower())
            if ratio > 50:  # Match threshold
                matches.append((ratio, full_path))
    
    # Search in parent directories
    parent = Path(current).parent
    while parent != parent.parent:  # Stop at root
        if parent.name:
            ratio = fuzz.ratio(search_term.lower(), parent.name.lower())
            if ratio > 50:
                matches.append((ratio, str(parent)))
        parent = parent.parent

    # Search common directories
    home = str(Path.home())
    common_dirs = [
        home,
        os.path.join(home, "Documents"),
        os.path.join(home, "Downloads"),
        os.path.join(home, "Desktop"),
        os.path.join(home, "Projects"),
        "/etc",
        "/usr/local",
    ]

    for dir_path in common_dirs:
        if os.path.exists(dir_path):
            dir_name = os.path.basename(dir_path)
            ratio = fuzz.ratio(search_term.lower(), dir_name.lower())
            if ratio > 50:
                matches.append((ratio, dir_path))

    # Sort by match ratio
    matches.sort(reverse=True, key=lambda x: x[0])
    paths = [path for ratio, path in matches]

    # Use smart predictor to rerank results
    current_hour = datetime.now().hour
    smart_predictions = predictor.predict_directories(search_term, current_hour, paths)
    
    if smart_predictions:
        # Combine fuzzy matches with smart predictions
        smart_paths = [path for path, score in smart_predictions]
        # Keep the order of fuzzy matches but prioritize smart predictions
        return list(dict.fromkeys(smart_paths + paths))
    
    return paths

def jump_command(
    path: str = typer.Argument(
        None,
        help="Directory to jump to. Use '-' to go back to previous directory"
    ),
    create: bool = typer.Option(
        False,
        "--create", "-c",
        help="Create directory if it doesn't exist"
    ),
    bookmarks: bool = typer.Option(
        False,
        "--bookmarks", "-b",
        help="Show bookmarked directories"
    ),
    save: bool = typer.Option(
        False,
        "--save", "-s",
        help="Save current directory as a bookmark"
    ),
    name: Optional[str] = typer.Option(
        None,
        "--name", "-n",
        help="Name for the bookmarked directory"
    ),
    interactive: bool = typer.Option(
        True,
        "--no-interactive",
        help="Disable interactive directory selection",
        is_flag=True,
        flag_value=False
    )
):
    """
    Enhanced directory navigation with fuzzy matching and bookmarks
    """
    try:
        # Handle bookmarks
        bookmark_file = Path.home() / ".scout_bookmarks"
        bookmarks_dict = {}
        
        if bookmark_file.exists():
            with open(bookmark_file) as f:
                for line in f:
                    if ":" in line:
                        k, v = line.strip().split(":", 1)
                        bookmarks_dict[k] = v

        # Show bookmarks if requested
        if bookmarks:
            if not bookmarks_dict:
                print("[yellow]No bookmarks saved yet[/yellow]")
                return
            
            print("[bold blue]Saved Bookmarks:[/bold blue]")
            for k, v in bookmarks_dict.items():
                print(f"  [green]{k}[/green] -> {v}")
            return

        # Save current directory as bookmark
        if save:
            current_dir = os.getcwd()
            bookmark_name = name or Path(current_dir).name
            
            bookmarks_dict[bookmark_name] = current_dir
            with open(bookmark_file, "w") as f:
                for k, v in bookmarks_dict.items():
                    f.write(f"{k}:{v}\n")
            
            print(f"[green]Saved bookmark:[/green] {bookmark_name} -> {current_dir}")
            return

        # If no path provided, show current directory
        if path is None:
            console.print(f"[blue]Current directory:[/blue] {os.getcwd()}")
            return

        # Handle directory navigation
        target_path = path
        
        # Check if it's a bookmark
        if path in bookmarks_dict:
            target_path = bookmarks_dict[path]
        
        # Handle special case for previous directory
        if path == "-":
            if "OLDPWD" not in os.environ:
                console.print("[red]No previous directory available[/red]")
                raise typer.Exit(1)
            target_path = os.environ["OLDPWD"]
        
        # Expand user path (~/something) and make absolute
        target = Path(target_path).expanduser().resolve()
        
        # If create flag is set, create directory immediately without fuzzy matching
        if create:
            if not target.exists():
                try:
                    target.mkdir(parents=True)
                    console.print(f"[green]Created directory:[/green] {target}")
                except Exception as e:
                    console.print(f"[red]Error creating directory:[/red] {str(e)}")
                    raise typer.Exit(1)
            elif not target.is_dir():
                console.print(f"[red]Path exists but is not a directory:[/red] {target}")
                raise typer.Exit(1)
        # If path doesn't exist and no create flag, try fuzzy matching
        elif not target.exists() and interactive:
            matches = find_matching_directories(target_path)
            current_dir = os.getcwd()
            current_time = datetime.now().hour
            
            # Get contextual suggestions
            context = predictor.get_contextual_suggestions(current_dir, current_time)
            
            if context['helpful_tips']:
                console.print("\n[blue]Smart Tips:[/blue]")
                for tip in context['helpful_tips']:
                    console.print(f"  [cyan]•[/cyan] {tip}")
            
            if matches:
                console.print("\n[yellow]Directory not found. Did you mean one of these?[/yellow]")
                for idx, match in enumerate(matches, 1):
                    # Add indicators for special directories
                    indicators = []
                    
                    # Star for frequently used
                    if any(h['path'] == match and h['success'] 
                          for h in predictor.history[-50:]):
                        indicators.append("[yellow]★[/yellow]")
                    
                    # Project root indicator
                    if match in predictor.patterns['project_roots']:
                        indicators.append("[blue]⌂[/blue]")  # House for project root
                    
                    # Next likely destination
                    if match == context.get('next_likely'):
                        indicators.append("[green]→[/green]")  # Arrow for likely next
                    
                    # Time-based suggestion
                    if match == context.get('time_based'):
                        indicators.append("[magenta]⏰[/magenta]")  # Clock for time-based
                    
                    # Format indicators
                    indicator_str = " ".join(indicators) + " " if indicators else "  "
                    
                    console.print(f"{indicator_str}{idx}. {match}")
                
                if context['project_root']:
                    console.print("\n[blue]Legend:[/blue]")
                    console.print("  [yellow]★[/yellow] Frequently used")
                    console.print("  [blue]⌂[/blue] Project root")
                    console.print("  [green]→[/green] Likely next destination")
                    console.print("  [magenta]⏰[/magenta] Common at this time")
                
                choice = Prompt.ask(
                    "\nSelect a directory",
                    choices=[str(i) for i in range(1, len(matches) + 1)] + ["n"],
                    default="1"
                )
                
                if choice != "n":
                    target_path = matches[int(choice) - 1]

        # Store current directory before changing
        os.environ["OLDPWD"] = os.getcwd()
        
        # Change directory
        os.chdir(target)
        console.print(f"[green]Jumped to:[/green] {target}")
        
        # Record successful navigation
        predictor.add_to_history(str(target), datetime.now().hour, success=True)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1) 