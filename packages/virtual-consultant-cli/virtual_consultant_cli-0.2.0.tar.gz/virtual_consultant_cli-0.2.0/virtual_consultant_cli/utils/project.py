"""Project creation and setup utilities."""
import os
import shutil
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Confirm

from .dependencies import check_dependencies

console = Console()

class ProjectError(Exception):
    """Custom exception for project-related errors."""
    pass

def create_project(name: str, path: Path, auto_setup: bool = False, skip_deps: bool = False) -> None:
    """Create a new Virtual Consultant project."""
    project_path = path / name
    
    # Check if project directory already exists
    if project_path.exists():
        raise ProjectError(f"Directory {project_path} already exists")
    
    try:
        # Create project directory
        project_path.mkdir(parents=True)
        
        # Copy template files
        template_dir = Path(__file__).parent.parent / 'templates'
        if not template_dir.exists():
            raise ProjectError("Template directory not found")
        
        # Copy base project structure
        for item in template_dir.glob('*'):
            if item.is_file():
                shutil.copy2(item, project_path)
            else:
                shutil.copytree(item, project_path / item.name)
        
        # Create Eliza directory
        eliza_dir = project_path / 'eliza'
        eliza_dir.mkdir(exist_ok=True)
        
        # Copy Eliza template
        eliza_template = template_dir / 'eliza'
        if eliza_template.exists():
            for item in eliza_template.glob('*'):
                if item.is_file():
                    shutil.copy2(item, eliza_dir)
                else:
                    shutil.copytree(item, eliza_dir / item.name)
        
        # Create tests directory for Eliza
        tests_dir = eliza_dir / 'tests'
        tests_dir.mkdir(exist_ok=True)
        
        # Create pyproject.toml for Eliza
        create_eliza_pyproject(eliza_dir, name)
        
        # Set up CI/CD if requested
        if auto_setup or Confirm.ask("Would you like to set up CI/CD?"):
            setup_cicd(project_path)
        
        # Set up Cursor automation if requested
        if auto_setup or Confirm.ask("Would you like to set up Cursor automation?"):
            setup_cursor_automation(project_path)
        
        console.print(f"[green]✓ Project {name} created successfully[/green]")
        
    except Exception as e:
        # Clean up on failure
        if project_path.exists():
            shutil.rmtree(project_path)
        raise ProjectError(f"Failed to create project: {str(e)}")

def create_eliza_pyproject(eliza_dir: Path, project_name: str) -> None:
    """Create pyproject.toml for Eliza."""
    content = f'''[tool.poetry]
name = "{project_name}-eliza"
version = "0.1.0"
description = "Eliza chatbot for {project_name}"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-cov = "^4.1.0"
black = "^24.1.1"
mypy = "^1.8.0"
ruff = "^0.2.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=eliza --cov-report=term-missing"

[tool.black]
line-length = 100
target-version = ["py39"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.ruff]
select = ["E", "F", "B", "I"]
ignore = []
line-length = 100
target-version = "py39"
'''
    
    with open(eliza_dir / 'pyproject.toml', 'w') as f:
        f.write(content)

def setup_cicd(project_path: Path) -> None:
    """Set up CI/CD configuration."""
    github_dir = project_path / '.github' / 'workflows'
    github_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy CI/CD templates
    template_dir = Path(__file__).parent.parent / 'templates' / '.github' / 'workflows'
    if template_dir.exists():
        for template_file in template_dir.glob('*.yml'):
            target_path = github_dir / template_file.name
            shutil.copy2(template_file, target_path)
    
    console.print("[green]✓ CI/CD configuration added[/green]")

def setup_cursor_automation(project_path: Path) -> None:
    """Set up Cursor automation."""
    cursor_dir = project_path / '.cursor'
    cursor_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy Cursor automation templates
    template_dir = Path(__file__).parent.parent / 'templates' / '.cursor'
    if template_dir.exists():
        for item in template_dir.glob('**/*'):
            if item.is_file():
                relative_path = item.relative_to(template_dir)
                target_path = cursor_dir / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_path)
    
    console.print("[green]✓ Cursor automation added[/green]")

def setup_project(project_path: Path, skip_deps: bool = False) -> None:
    """Set up an existing Virtual Consultant project."""
    if not skip_deps:
        check_dependencies()
    
    try:
        # Initialize git if not already initialized
        if not (project_path / '.git').exists():
            os.system('git init')
        
        # Install dependencies
        os.system('poetry install')
        
        # Set up pre-commit hooks
        os.system('poetry run pre-commit install')
        
        console.print("[green]✓ Project setup complete[/green]")
        
    except Exception as e:
        raise ProjectError(f"Failed to set up project: {str(e)}") 