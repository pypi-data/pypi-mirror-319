"""Modern styling for CLIDB."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich.box import ROUNDED
from rich.layout import Layout
from rich.console import Group

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
    table = Table(show_header=False, box=ROUNDED, expand=True, padding=(0, 1))
    table.add_column("Key", style="cyan bold")
    table.add_column("Value", style="white")
    
    for key, value in info_dict.items():
        # Special styling for sensitive info
        if key in ["Password"]:
            value_style = "yellow bold"
        elif key in ["Host", "Port"]:
            value_style = "green"
        elif key in ["Type", "Version"]:
            value_style = "magenta"
        else:
            value_style = "white"
        table.add_row(f"{key}:", f"[{value_style}]{value}[/{value_style}]")

    # Create sections
    sections = [table]
    
    if connection_string:
        sections.append("")  # Add spacing
        sections.append(Text("Connection String:", style="cyan bold"))
        sections.append(Syntax(connection_string, "uri", theme="monokai", word_wrap=True))
    
    if cli_command:
        sections.append("")  # Add spacing
        sections.append(Text("CLI Command:", style="cyan bold"))
        sections.append(Syntax(cli_command, "bash", theme="monokai"))
    
    # Combine all sections in a main panel
    console.print(Panel(
        Group(*sections),
        title=f"[bold blue]{title}[/bold blue]",
        box=ROUNDED,
        padding=(1, 2)
    ))

def print_db_list(containers: list):
    """Print a list of databases in a styled table."""
    if not containers:
        print_warning("No databases found")
        return
    
    table = Table(
        title="[bold blue]Databases[/bold blue]",
        box=ROUNDED,
        show_lines=True,
        padding=(0, 1)
    )
    
    table.add_column("Name", style="cyan bold")
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
    # Convert the plain text to rich text with proper styling
    lines = db_info.split('\n')
    styled_lines = []
    
    for line in lines:
        if line.strip():
            if ':' in line:
                # Database header line
                if '(' in line:
                    name, rest = line.split('(', 1)
                    styled_lines.append(f"[cyan bold]{name}[magenta]({rest}")
                else:
                    key, value = line.split(':', 1)
                    styled_lines.append(f"[cyan bold]{key}:[white]{value}")
            else:
                # Description or version line
                styled_lines.append(f"[white]{line}")
        else:
            styled_lines.append("")
    
    console.print(Panel(
        "\n".join(styled_lines),
        title="[bold blue]Supported Databases[/bold blue]",
        box=ROUNDED,
        padding=(1, 2)
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