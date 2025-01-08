"""Project creation and setup utilities."""
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class ProjectError(Exception):
    """Raised when a project operation fails."""

def run_command(cmd: str, cwd: Optional[Path] = None) -> subprocess.CompletedProcess[str]:
    """Run a shell command safely.
    
    Args:
        cmd: Command to run
        cwd: Working directory for the command
        
    Returns:
        CompletedProcess instance with command output
        
    Raises:
        ProjectError: If command execution fails
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=str(cwd) if cwd else None
        )
        return result
    except subprocess.CalledProcessError as e:
        raise ProjectError(f"Command failed: {cmd}\nError: {e.stderr}")

def create_pyproject_toml(path: Path, name: str) -> None:
    """Create a minimal pyproject.toml file.
    
    Args:
        path: Project path
        name: Project name
        
    Raises:
        ProjectError: If file creation fails
    """
    try:
        content = f'''[tool.poetry]
name = "{name}"
version = "0.1.0"
description = "A Virtual Consultant project"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{{"include" = "{name}"}}]

[tool.poetry.dependencies]
python = "^3.9"
click = "^8.1.8"
rich = "^13.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
'''
        (path / "pyproject.toml").write_text(content)
    except Exception as e:
        raise ProjectError(f"Failed to create pyproject.toml: {str(e)}")

def create_mkdocs_config(path: Path, name: str) -> None:
    """Create MkDocs configuration file.
    
    Args:
        path: Project path
        name: Project name
        
    Raises:
        ProjectError: If file creation fails
    """
    try:
        config = f"""site_name: {name}
theme:
  name: material
  palette:
    scheme: default
    primary: indigo
    accent: indigo
plugins:
  - search
  - mkdocstrings
nav:
  - Home: index.md
  - API: api.md
  - Usage: usage.md
"""
        (path / "mkdocs.yml").write_text(config)
        
        # Create docs directory and initial files
        docs_dir = path / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        index_content = f"""# {name}

Welcome to the {name} documentation.

## Overview

This project was created using the Virtual Consultant CLI.

## Getting Started

See the [Usage](usage.md) guide to get started.
"""
        (docs_dir / "index.md").write_text(index_content)
        
        usage_content = """# Usage Guide

## Installation

```bash
pip install package-name
```

## Basic Usage

Describe how to use your package here.
"""
        (docs_dir / "usage.md").write_text(usage_content)
        
        api_content = """# API Reference

## Functions

Document your API functions here.
"""
        (docs_dir / "api.md").write_text(api_content)
    except Exception as e:
        raise ProjectError(f"Failed to create documentation: {str(e)}")

def create_project(name: str, path: Path, auto_setup: bool = False, skip_deps: bool = False) -> None:
    """Create a new project with the given name at the specified path.
    
    Args:
        name: Name of the project
        path: Path where project should be created
        auto_setup: Whether to run setup after creation
        skip_deps: Whether to skip dependency checks
        
    Raises:
        ProjectError: If project creation fails
    """
    try:
        project_path = path / name
        if project_path.exists():
            raise ProjectError(f"Directory {project_path} already exists")
            
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create project structure
        directories: List[Path] = [
            project_path / "src",
            project_path / "src" / "components",
            project_path / "src" / "pages",
            project_path / "src" / "operations",
            project_path / "src" / "utils",
            project_path / "tests",
            project_path / "docs",
            project_path / "scripts"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # Create initial files
        (project_path / "README.md").write_text(f"# {name}\n\nA Virtual Consultant project.")
        (project_path / ".gitignore").write_text("node_modules/\n__pycache__/\n.env\nsite/\n")
        
        # Create configuration files - do this BEFORE git init
        create_pyproject_toml(project_path, name)
        create_mkdocs_config(project_path, name)
        
        # Initialize git repository
        run_command("git init", cwd=project_path)
        run_command("git add .", cwd=project_path)
        run_command('git commit -m "Initial commit"', cwd=project_path)
        
        # Run setup after git initialization if requested
        if auto_setup:
            setup_project(project_path, skip_deps)
    except ProjectError:
        raise
    except Exception as e:
        raise ProjectError(f"Failed to create project: {str(e)}")

def setup_project(path: Path, skip_deps: bool = False) -> None:
    """Set up an existing project at the specified path.
    
    Args:
        path: Path to the project
        skip_deps: Whether to skip dependency checks
        
    Raises:
        ProjectError: If project setup fails
    """
    try:
        if not path.exists():
            raise ProjectError(f"Directory {path} does not exist")
            
        if not (path / "pyproject.toml").exists():
            raise ProjectError("No project configuration found in current directory")
        
        # Install dependencies if not skipped
        if not skip_deps:
            if (path / "package.json").exists():
                run_command("npm install", cwd=path)
            
            if (path / "poetry.lock").exists():
                run_command("poetry install", cwd=path)
        
        # Initialize git if not already initialized
        if not (path / ".git").exists():
            run_command("git init", cwd=path)
            run_command("git add .", cwd=path)
            run_command('git commit -m "Initial commit"', cwd=path)
            
        # Build documentation if mkdocs.yml exists
        if (path / "mkdocs.yml").exists():
            run_command("mkdocs build", cwd=path)
    except ProjectError:
        raise
    except Exception as e:
        raise ProjectError(f"Failed to set up project: {str(e)}") 