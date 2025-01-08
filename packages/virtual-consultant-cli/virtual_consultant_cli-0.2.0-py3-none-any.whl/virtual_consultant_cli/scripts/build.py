import os
import subprocess
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Confirm

console = Console()

def run_command(cmd: str, cwd: Optional[Path] = None) -> bool:
    """Run a shell command and return whether it succeeded."""
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError:
        return False

def build_wasp_app(project_path: Path) -> bool:
    """Build the WASP application."""
    console.print("[bold]Building WASP application...[/bold]")
    
    # Check if wasp is installed
    if not run_command("wasp -v"):
        console.print("[red]Error: WASP is not installed. Installing now...[/red]")
        if not run_command("curl -sSL https://get.wasp-lang.dev/installer.sh | sh"):
            console.print("[red]Failed to install WASP[/red]")
            return False
    
    # Build WASP app
    if not run_command("wasp build", cwd=project_path):
        console.print("[red]Failed to build WASP application[/red]")
        return False
    
    console.print("[green]✓ WASP application built successfully[/green]")
    return True

def build_python_package(project_path: Path) -> bool:
    """Build the Python package."""
    console.print("[bold]Building Python package...[/bold]")
    
    # Clean previous builds
    dist_dir = project_path / "dist"
    if dist_dir.exists():
        for file in dist_dir.glob("*"):
            file.unlink()
    
    # Build package
    if not run_command("poetry build", cwd=project_path):
        console.print("[red]Failed to build Python package[/red]")
        return False
    
    console.print("[green]✓ Python package built successfully[/green]")
    return True

def main(project_path: Path) -> None:
    """Main build function."""
    # Ensure project path exists
    if not project_path.exists():
        console.print(f"[red]Error: Project path {project_path} does not exist[/red]")
        return
    
    # Build Python package
    if not build_python_package(project_path):
        return
    
    # Check if this is a WASP project
    wasp_file = project_path / "main.wasp"
    if wasp_file.exists():
        if Confirm.ask("WASP project detected. Would you like to build the WASP application?"):
            build_wasp_app(project_path)

if __name__ == "__main__":
    main(Path.cwd()) 