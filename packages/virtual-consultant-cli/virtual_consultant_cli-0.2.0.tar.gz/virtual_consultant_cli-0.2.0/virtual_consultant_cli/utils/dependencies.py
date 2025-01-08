"""Dependency management utilities."""
import shutil
import subprocess
from typing import Dict, Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from rich.table import Table

def run_command(cmd: str) -> Tuple[str, bool]:
    """Run a command and return its output and status.
    
    Args:
        cmd: Command to run
        
    Returns:
        Tuple of (output, success)
    """
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip(), True
    except subprocess.CalledProcessError:
        return "Error", False

def check_dependencies(table: Optional["Table"] = None) -> Dict[str, Tuple[str, str]]:
    """Check if required system dependencies are installed.
    
    Args:
        table: Optional Rich table for displaying results
        
    Returns:
        Dictionary of dependency results {name: (version, status)}
    """
    dependencies = {
        "git": "git --version",
        "node": "node --version",
        "npm": "npm --version",
        "python": "python --version",
        "poetry": "poetry --version",
        "wasp": "wasp --version",
        "mkdocs": "mkdocs --version"
    }

    results: Dict[str, Tuple[str, str]] = {}

    for name, command in dependencies.items():
        path = shutil.which(name)
        if path:
            version, success = run_command(command)
            status = "✓" if success else "✗"
        else:
            version = "Not Found"
            status = "✗"

        results[name] = (version, status)
        if table is not None:
            table.add_row(name, status, version)

    return results 