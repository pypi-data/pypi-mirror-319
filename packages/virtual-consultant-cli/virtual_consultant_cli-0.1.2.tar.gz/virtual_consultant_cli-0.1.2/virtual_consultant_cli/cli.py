#!/usr/bin/env python3
"""Command-line interface for Virtual Consultant CLI."""

from pathlib import Path
from typing import NoReturn

import click
from rich.box import DOUBLE, DOUBLE_EDGE
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.style import Style
from rich.table import Table
from rich.theme import Theme

from .utils.dependencies import check_dependencies
from .utils.project import create_project, setup_project, ProjectError

# Custom theme with cyberpunk aesthetics for internal UI only
theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "danger": "red",
    "success": "green",
    "title": Style(color="magenta", bold=True),
    "subtitle": Style(color="cyan", bold=True),
    "path": Style(color="yellow"),
    "command": Style(color="green"),
})

console = Console(theme=theme)

def print_banner() -> None:
    """Print the CLI banner."""
    banner = (
        "[title]╔═══════════════════════════════════════╗[/title]\n"
        "[title]║     VIRTUAL CONSULTANT CLI v0.1.0     ║[/title]\n"
        "[title]╚═══════════════════════════════════════╝[/title]\n\n"
        "[subtitle]> Initializing environment...[/subtitle]\n"
        "[subtitle]> Checking dependencies...[/subtitle]\n"
        "[subtitle]> Ready to proceed...[/subtitle]"
    )
    console.print(Panel(banner, box=DOUBLE, style="blue"))

def create_progress() -> Progress:
    """Create a styled progress bar."""
    return Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[progress.description]{task.description}", style="cyan"),
        BarColumn(complete_style="green", finished_style="green"),
        TaskProgressColumn(),
        console=console,
    )

@click.group()
def main() -> None:
    """Virtual Consultant CLI - Create and manage Virtual Consultant projects."""
    try:
        print_banner()
    except Exception as e:
        raise click.ClickException(f"Failed to initialize CLI: {str(e)}")

@main.command()
@click.argument('name')
@click.option('--path', '-p', default='.', help='Path where the project should be created')
@click.option('--skip-deps', is_flag=True, help='Skip dependency checks')
@click.option('--auto-setup', is_flag=True, help='Automatically run all setup steps')
def create(name: str, path: str = '.', skip_deps: bool = False, auto_setup: bool = False) -> None:
    """Create a new Virtual Consultant project."""
    try:
        with create_progress() as progress:
            if not skip_deps:
                task = progress.add_task("[cyan]> Checking system dependencies...[/cyan]", total=None)
                check_dependencies()
                progress.remove_task(task)

            task = progress.add_task("[cyan]> Generating project structure...[/cyan]", total=None)
            create_project(name, Path(path), auto_setup=auto_setup, skip_deps=skip_deps)
            progress.remove_task(task)

        click.echo(f"\n✓ Project {name} successfully created!")
        if not auto_setup:
            click.echo("\nTo complete setup, run:")
            click.echo(f"  cd {name}")
            click.echo("  vconsult setup")
    except ProjectError as e:
        raise click.ClickException(str(e))
    except Exception as e:
        raise click.ClickException(f"An unexpected error occurred: {str(e)}")

@main.command()
@click.option('--skip-deps', is_flag=True, help='Skip dependency checks')
def setup(skip_deps: bool = False) -> None:
    """Set up an existing Virtual Consultant project."""
    try:
        if not Path('pyproject.toml').exists():
            raise ProjectError("No project configuration found in current directory")

        with create_progress() as progress:
            if not skip_deps:
                task = progress.add_task("[cyan]> Checking system dependencies...[/cyan]", total=None)
                check_dependencies()
                progress.remove_task(task)

            task = progress.add_task("[cyan]> Setting up project...[/cyan]", total=None)
            setup_project(Path.cwd(), skip_deps=skip_deps)
            progress.remove_task(task)

        click.echo("\n✓ Project setup complete!")
        click.echo("\nTo start the development server:")
        click.echo("  wasp start")
    except ProjectError as e:
        raise click.ClickException(str(e))
    except Exception as e:
        raise click.ClickException(f"An unexpected error occurred: {str(e)}")

@main.command()
def doctor() -> None:
    """Run system diagnostics."""
    try:
        table = Table(title="System Diagnostics", box=DOUBLE_EDGE)
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Version", style="yellow")

        with create_progress() as progress:
            task = progress.add_task("[cyan]> Running diagnostics...[/cyan]", total=None)
            results = check_dependencies(table=table)
            progress.remove_task(task)

        console.print(table)
        
        # Check if any dependencies are missing or have errors
        has_issues = any(status == "✗" for _, (_, status) in results.items())
        if has_issues:
            raise click.ClickException("Some system dependencies are missing or have issues")
            
        click.echo("\n✓ System diagnostics complete - all dependencies are available!")
    except ProjectError as e:
        raise click.ClickException(str(e))
    except Exception as e:
        raise click.ClickException(f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    main() 