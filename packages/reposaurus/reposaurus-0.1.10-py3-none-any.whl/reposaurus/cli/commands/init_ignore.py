"""Implementation of the init-ignore command for creating default ignore files."""

import argparse
import os
from pathlib import Path

from .base import Command, register_command
from ...config.ignore_template import IGNORE_TEMPLATE


@register_command
class InitIgnoreCommand(Command):
    """Command for initializing a Reposaurus ignore file."""

    name = "init-ignore"
    help = "Create a default Reposaurus ignore file"
    description = "Initialize a new .reposaurusignore file with default exclusion patterns"

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        """Configure init-ignore command arguments."""
        parser.add_argument('--force', '-f',
                          action='store_true',
                          help='Overwrite existing ignore file if it exists')
        parser.add_argument('--output', '-o',
                          default='.reposaurusignore',
                          help='Output file path (default: .reposaurusignore)')

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the init-ignore command."""
        try:
            output_path = Path(args.output)

            # Check if file already exists
            if output_path.exists() and not args.force:
                raise FileExistsError(
                    f"Error: {output_path} already exists. Use --force to overwrite."
                )

            # Create parent directories if they don't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Check directory permissions
            if not os.access(output_path.parent, os.W_OK):
                raise PermissionError(
                    f"Error: No write permission for directory {output_path.parent}"
                )

            # Write the ignore file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(IGNORE_TEMPLATE)

            print(f"Created Reposaurus ignore file at {output_path}")

        except (FileExistsError, PermissionError) as e:
            # Re-raise expected errors with their messages
            raise
        except Exception as e:
            # Wrap unexpected errors
            raise RuntimeError(f"An unexpected error occurred: {str(e)}")