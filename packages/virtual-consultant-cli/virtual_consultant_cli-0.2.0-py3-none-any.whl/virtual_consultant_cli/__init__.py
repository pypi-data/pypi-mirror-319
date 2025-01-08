"""Virtual Consultant CLI - Create and manage Virtual Consultant projects."""

from .cli import main
from .utils.dependencies import check_dependencies
from .utils.project import create_project, setup_project

__version__ = "0.1.0"
__all__ = ["main", "check_dependencies", "create_project", "setup_project"] 