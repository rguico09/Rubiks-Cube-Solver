# Provides visual and textual output formatting
# Prints the move sequence nicely in the terminal (using `rich`)
#   - and renders step-by-step directions/visual indicators

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from solver import get_move_description

console = Console()

def print_welcome() -> None:
    # prints a header panel to welcome user
    welcome_text = Text()
    welcome_text.append("RUBIK'S CUBE CAMERA SOLVER\n", style="bold cyan")
    welcome_text.append("\nAlign each face of your cube to the on-screen camera grid in order.", style="italic white")
    welcome_text.append("\nThe middle cell of each face indicates its identity colour.", style="italic white")

    panel = Panel(welcome_text, title="Rubik's Cube Solver", border_style="green", expand=False)
    console.print(panel)

def print_validation_status(is_valid: bool, msg: str) -> None:
    # prints result of cube state validation
    if is_valid:
        console.print(f"[bold green]Success[/bold green] [white]{msg}[/white]\n")
    else:
        panel = Panel(
            f"[bold red]Validation Failure:[/bold red]\n{msg}\n\nPlease scan again.",
            title="Scan Error",
            border_style="red",
            expand=False
        )
        console.print(panel)

def print_solution(moves: list[str]) -> None:
    # prints moves required to solve the cube
    if not moves:
        console.print(Panel("[bold green]The cube is already solved! No moves needed.[/bold green]", border_style="green"))
        return
    
    raw_moves_str = " ".join(moves)
    console.print(Panel(
        f"[bold yellow]{raw_moves_str}[/bold yellow]",
        title="Raw WCA Move Notation Sequence",
        border_style="yellow",
        expand=False
    ))

    table = Table(title="Step-by-Step Solving Instructions", show_header=True, header_style="bold magenta")
    table.add_column("Step", style="dim", width=6, justify="center")
    table.add_column("Move", style="bold cyan", width=10, justify="center")
    table.add_column("Instructions", style="white")

    for i, move in enumerate(moves, 1):
        desc = get_move_description(move)
        table.add_row(str(i), move, desc)

    console.print(table)
    console.print("\n[bold green]Done![/bold green] Follow the steps in order starting from the orientation you scanned the front face.\n")
