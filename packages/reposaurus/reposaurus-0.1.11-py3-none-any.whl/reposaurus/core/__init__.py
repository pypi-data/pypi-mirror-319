"""Core functionality for Reposaurus."""

from .processor import RepositoryProcessor
from .output import OutputHandler
from .exclusions import ExclusionManager

__all__ = ['RepositoryProcessor', 'OutputHandler', 'ExclusionManager']