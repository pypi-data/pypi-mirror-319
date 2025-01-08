"""Utility modules for the Virtual Consultant CLI."""

from .dependencies import check_dependencies
from .project import create_project, setup_project

__all__ = ['check_dependencies', 'create_project', 'setup_project'] 