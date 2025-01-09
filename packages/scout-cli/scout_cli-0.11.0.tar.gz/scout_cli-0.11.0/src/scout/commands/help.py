from rich.console import Console

console = Console()

def help_command():
    """Show detailed help and usage tips"""
    console.print("\n[bold blue]Scout CLI - Modern Directory Navigation[/bold blue]")
    console.print("\n[yellow]Basic Commands:[/yellow]")
    
    # List files (ls replacement)
    console.print("\n[green]List Files (replaces ls):[/green]")
    console.print("  scout                    List files in current directory")
    console.print("  scout -a                 Show hidden files")
    console.print("  scout --sort size        Sort by file size")
    console.print("  scout --sort modified    Sort by modification time")
    console.print("  scout --sort name        Sort by name (default)")
    
    # Directory navigation (cd replacement)
    console.print("\n[green]Directory Navigation (replaces cd):[/green]")
    console.print("  scout jump <dir>         Smart jump to directory")
    console.print("  scout jump -             Go back to previous directory")
    console.print("  scout jump docs -c       Create 'docs' directory and jump to it")
    console.print("  scout jump path/to/dir -c  Create nested directories")
    console.print("  scout jump old-dir -d    Delete directory (with confirmation)")
    console.print("  scout jump old-dir -d -f Force delete without confirmation")
    
    # Bookmarks
    console.print("\n[green]Bookmark Management:[/green]")
    console.print("  scout jump --save        Save current directory as bookmark")
    console.print("  scout jump --bookmarks   List saved bookmarks")
    console.print("  scout jump <bookmark>    Jump to bookmarked directory")
    
    # Smart Features
    console.print("\n[yellow]Smart Features:[/yellow]")
    console.print("• [cyan]Fuzzy Matching:[/cyan] Type partial names, scout finds matches")
    console.print("• [cyan]AI Suggestions:[/cyan] Scout learns from your navigation patterns")
    console.print("• [cyan]Context Aware:[/cyan] Suggests based on time and location")
    console.print("• [cyan]Project Detection:[/cyan] Recognizes project directories")
    
    # Icons Legend
    console.print("\n[yellow]Icons Legend:[/yellow]")
    console.print("  [yellow]★[/yellow]  Frequently used directory")
    console.print("  [blue]⌂[/blue]  Project root")
    console.print("  [green]→[/green]  Likely next destination")
    console.print("  [magenta]⏰[/magenta]  Common at this time")
    
    # Tips
    console.print("\n[yellow]Pro Tips:[/yellow]")
    console.print("• Use tab completion for paths")
    console.print("• Type partial names for fuzzy matching")
    console.print("• Save frequently used directories as bookmarks")
    console.print("• Watch for icons that suggest smart matches")
    console.print("• The more you use scout, the smarter it gets!") 