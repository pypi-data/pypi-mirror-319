"""Pattern matching and file exclusion management."""

from pathlib import Path
from typing import Optional, List
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

from ..config.ignore_template import IGNORE_TEMPLATE


class ExclusionManager:
    """Manages file exclusion patterns and matching."""

    def __init__(self, repo_path: Optional[Path] = None, exclude_file: Optional[str] = None,
                 additional_excludes: Optional[List[str]] = None):
        """
        Initialize the exclusion manager.

        Args:
            repo_path: Root path of the repository (defaults to current directory)
            exclude_file: Optional path to a custom exclusion file
            additional_excludes: Optional list of additional patterns to exclude
        """
        self.repo_path = repo_path.resolve() if repo_path else Path.cwd().resolve()
        self.exclude_file = exclude_file
        self.additional_excludes = additional_excludes or []

        # If no exclude file specified, look for .reposaurusignore in repo root
        if not exclude_file:
            repo_ignore = self.repo_path / '.reposaurusignore'
            if repo_ignore.exists():
                self.exclude_file = str(repo_ignore)

        self.spec = self._create_path_spec()

    def _create_path_spec(self) -> PathSpec:
        """Create a PathSpec object with all patterns."""
        patterns = []

        # First add default patterns from template
        for line in IGNORE_TEMPLATE.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                pattern = line.split('#')[0].strip()
                if pattern:  # Extra check for empty patterns
                    patterns.append(pattern)

        # Add additional exclude patterns
        if self.additional_excludes:
            patterns.extend(pat.strip() for pat in self.additional_excludes if pat.strip())

        # Then add custom patterns from exclude file
        if self.exclude_file and Path(self.exclude_file).exists():
            try:
                with open(self.exclude_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            pattern = line.split('#')[0].strip()
                            if pattern:  # Extra check for empty patterns
                                patterns.append(pattern)
            except Exception as e:
                print(f"Warning: Could not read exclusion patterns from {self.exclude_file}: {str(e)}")

        # Debug log of patterns
        # print("Active exclusion patterns:", patterns)
        return PathSpec.from_lines(GitWildMatchPattern, patterns)

    def should_exclude(self, path: Path) -> bool:
        """
        Check if a path should be excluded based on patterns.

        Args:
            path: Path to check

        Returns:
            True if the path should be excluded
        """
        try:
            # Always use path relative to repository root
            rel_path = str(path.resolve().relative_to(self.repo_path))
            # Normalize path separators for consistent matching
            normalized_path = rel_path.replace('\\', '/')

            # Check if the path matches any pattern
            is_excluded = self.spec.match_file(normalized_path)

            # Debug logging
            # if is_excluded:
            #     print(f"Excluding: {normalized_path}")

            return is_excluded

        except Exception as e:
            # If we can't get a relative path, use the full path
            return self.spec.match_file(str(path))