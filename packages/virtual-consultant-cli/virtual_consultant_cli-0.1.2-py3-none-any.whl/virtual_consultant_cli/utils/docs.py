import os
import tempfile
from pathlib import Path
from typing import List, Optional

import requests
from markdowner import Markdowner
from rich.console import Console
from rich.prompt import Confirm

console = Console()

def extract_links_from_markdown(content: str) -> List[str]:
    """Extract all URLs from markdown content."""
    # Simple regex for URLs
    import re
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    return urls

def process_url(url: str, docs_dir: Path) -> None:
    """Process a URL and save its content to the docs directory."""
    try:
        md = Markdowner()
        content = md.url_to_markdown(url)
        
        # Create a filename from the URL
        filename = url.split('/')[-1].replace('.html', '.md')
        if not filename.endswith('.md'):
            filename += '.md'
        
        # Save the content
        output_path = docs_dir / filename
        with open(output_path, 'w') as f:
            f.write(content)
        
        console.print(f"[green]✓ Processed {url} -> {filename}[/green]")
        
        # Extract and process nested links
        nested_urls = extract_links_from_markdown(content)
        for nested_url in nested_urls:
            if Confirm.ask(f"Process nested link: {nested_url}?"):
                process_url(nested_url, docs_dir)
                
    except Exception as e:
        console.print(f"[red]Error processing {url}: {str(e)}[/red]")

def setup_documentation(project_path: Path) -> None:
    """Set up project documentation."""
    docs_dir = project_path / 'docs'
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy template files
    template_dir = Path(__file__).parent.parent / 'templates' / 'docs'
    if template_dir.exists():
        for template_file in template_dir.glob('**/*'):
            if template_file.is_file():
                relative_path = template_file.relative_to(template_dir)
                target_path = docs_dir / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(template_file, 'r') as src, open(target_path, 'w') as dst:
                    dst.write(src.read())
    
    while True:
        if not Confirm.ask("Would you like to add documentation from a URL?"):
            break
            
        url = console.input("Enter URL to process: ")
        process_url(url, docs_dir)
    
    # Ask about CI/CD setup
    if Confirm.ask("Would you like to set up CI/CD?"):
        setup_cicd(project_path)
    
    # Ask about Cursor actions
    if Confirm.ask("Would you like to include Cursor actions?"):
        setup_cursor_actions(project_path)

def setup_cicd(project_path: Path) -> None:
    """Set up CI/CD configuration."""
    github_dir = project_path / '.github' / 'workflows'
    github_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy CI/CD templates
    template_dir = Path(__file__).parent.parent / 'templates' / '.github' / 'workflows'
    if template_dir.exists():
        for template_file in template_dir.glob('*.yml'):
            target_path = github_dir / template_file.name
            with open(template_file, 'r') as src, open(target_path, 'w') as dst:
                dst.write(src.read())
    
    console.print("[green]✓ CI/CD configuration added[/green]")

def setup_cursor_actions(project_path: Path) -> None:
    """Set up Cursor actions."""
    cursor_dir = project_path / '.cursor'
    cursor_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy Cursor action templates
    template_dir = Path(__file__).parent.parent / 'templates' / '.cursor'
    if template_dir.exists():
        for template_file in template_dir.glob('**/*'):
            if template_file.is_file():
                relative_path = template_file.relative_to(template_dir)
                target_path = cursor_dir / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(template_file, 'r') as src, open(target_path, 'w') as dst:
                    dst.write(src.read())
    
    console.print("[green]✓ Cursor actions added[/green]") 