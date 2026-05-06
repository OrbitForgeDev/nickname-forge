"""
CLI entry point for Nickname Forge.
Initial comments in Russian, translated to English via AI tools for global accessibility.
"""

import typer
from rich.console import Console
from rich.table import Table

from .engine import NicknameForge, StyleNotFoundError

app = typer.Typer(
    name="forge",
    help="Forge unique nicknames in various styles. A tool by OrbitForgeDev.",
    add_completion=False,
)
console = Console()


@app.command()
def main(
    style: str = typer.Option(
        "cyberpunk",
        "--style",
        "-s",
        help="Style of nickname (cyberpunk, fantasy, space, steampunk)",
    ),
    count: int = typer.Option(
        10, "--count", "-c", min=1, max=50, help="Number of nicknames to generate"
    ),
    separator: str = typer.Option(
        "", "--sep", help="Separator between parts: '-', '_', or ''"
    ),
    show_score: bool = typer.Option(
        True, "--score/--no-score", help="Show readability score"
    ),
    list_styles: bool = typer.Option(
        False, "--list-styles", "-l", help="List all available styles and exit"
    ),
    save: str = typer.Option(
        None, "--save", help="Save nicknames to a file"
    ),
):
    """
    Forge unique nicknames in various styles.

    Examples:
        forge --style cyberpunk --count 10
        forge -s space --sep "-"
        forge --list-styles
        forge -s fantasy --count 20 --save nicknames.txt
    """
    # Show available styles if requested
    if list_styles:
        _list_styles_handler()
        return

    forge_engine = NicknameForge()

    try:
        nicknames = forge_engine.generate_batch(
            style=style,
            count=count,
            separator=separator,
            unique=True,
        )
    except StyleNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    # Save to file if --save is provided
    if save:
        try:
            written = forge_engine.export_to_file(
                style=style,
                filepath=save,
                count=count,
                separator=separator,
            )
            console.print(
                f"[bold green]Saved {written} nicknames to '{save}'[/bold green]"
            )
        except IOError as e:
            console.print(f"[bold red]Error writing file:[/bold red] {e}")
            raise typer.Exit(code=1)

    _display_results(nicknames, show_score=show_score)


def _list_styles_handler() -> None:
    """Display available styles with examples."""
    forge_engine = NicknameForge()

    console.print("\n[bold cyan]Available Styles[/bold cyan]\n")

    table = Table(title="Styles & Examples")
    table.add_column("Style", style="cyan", no_wrap=True)
    table.add_column("Example", style="green")

    for style_name in forge_engine.available_styles:
        example = forge_engine.generate(style_name)
        table.add_row(style_name, example.name)

    console.print(table)
    console.print("\n[dim]Usage: forge --style <style> --count 10[/dim]")


def _display_results(nicknames, show_score: bool = True) -> None:
    """Display generated nicknames in a table."""
    console.print("\n[bold cyan]Forged Nicknames[/bold cyan]\n")

    if show_score:
        table = Table(title="Results")
        table.add_column("#", style="dim", no_wrap=True)
        table.add_column("Nickname", style="bold green")
        table.add_column("Score", style="yellow", justify="center")
        table.add_column("Verdict", style="dim")

        for i, n in enumerate(nicknames, 1):
            if n.score >= 80:
                verdict = "Legendary"
            elif n.score >= 60:
                verdict = "Solid"
            else:
                verdict = "Meh"
            table.add_row(str(i), n.name, str(n.score), verdict)

        console.print(table)
    else:
        for n in nicknames:
            console.print(f"  [bold green]{n.name}[/bold green]")

    console.print("\n[dim]Forge complete.[/dim]")


def main_entry():
    """Entry point for console_scripts."""
    app()