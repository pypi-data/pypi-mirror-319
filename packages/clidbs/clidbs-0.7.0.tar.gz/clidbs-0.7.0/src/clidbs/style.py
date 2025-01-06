"""Modern styling for CLIDB."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich.box import ROUNDED

# Initialize console
console = Console()

def print_success(message: str):
    """Print a success message in a green panel."""
    console.print(Panel(message, style="green", box=ROUNDED))

def print_error(message: str):
    """Print an error message in a red panel."""
    console.print(Panel(f"[red bold]Error:[/red bold] {message}", style="red", box=ROUNDED))

def print_warning(message: str):
    """Print a warning message in a yellow panel."""
    console.print(Panel(f"[yellow bold]Warning:[/yellow bold] {message}", style="yellow", box=ROUNDED))

def print_db_info(title: str, info_dict: dict, connection_string: str = None, cli_command: str = None):
    """Print database information in a styled panel."""
    # Create the main table
    table = Table(show_header=False, box=ROUNDED, expand=True)
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")
    
    for key, value in info_dict.items():
        table.add_row(f"{key}:", str(value))
    
    # Add connection information if provided
    sections = [table]
    
    if connection_string:
        conn_panel = Panel(
            Syntax(connection_string, "uri", theme="monokai", word_wrap=True),
            title="[bold cyan]Connection String[/bold cyan]",
            box=ROUNDED
        )
        sections.append(conn_panel)
    
    if cli_command:
        cmd_panel = Panel(
            Syntax(cli_command, "bash", theme="monokai"),
            title="[bold cyan]CLI Command[/bold cyan]",
            box=ROUNDED
        )
        sections.append(cmd_panel)
    
    # Combine all sections in a main panel
    console.print(Panel(
        "\n".join(str(section) for section in sections),
        title=f"[bold blue]{title}[/bold blue]",
        box=ROUNDED
    ))

def print_db_list(containers: list):
    """Print a list of databases in a styled table."""
    if not containers:
        print_warning("No databases found")
        return
    
    table = Table(
        title="[bold blue]Databases[/bold blue]",
        box=ROUNDED,
        show_lines=True
    )
    
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Status", style="green")
    
    for name, db_type, status in sorted(containers):
        # Style the status
        if status == "running":
            status_style = "[green]⚡ running[/green]"
        elif status == "exited":
            status_style = "[red]⏹ stopped[/red]"
        else:
            status_style = f"[yellow]{status}[/yellow]"
            
        table.add_row(name, db_type, status_style)
    
    console.print(table)

def print_supported_dbs(db_info: str):
    """Print supported databases in a styled panel."""
    console.print(Panel(
        Text(db_info, style="cyan"),
        title="[bold blue]Supported Databases[/bold blue]",
        box=ROUNDED
    ))

def print_action(action: str, db_name: str, success: bool = True):
    """Print an action result with an emoji."""
    if success:
        emoji = "✅"
        color = "green"
    else:
        emoji = "❌"
        color = "red"
    
    console.print(f"[{color}]{emoji} {action} '{db_name}' {success and 'successful' or 'failed'}[/{color}]") 