"""Implementation of the init-config command."""

import argparse
from pathlib import Path
from ...config.config_template import CONFIG_TEMPLATE
from ..commands.base import Command, register_command


@register_command
class InitConfigCommand(Command):
    """Command for initializing a Reposaurus configuration file."""

    name = "init-config"
    help = "Create a default Reposaurus configuration file"
    description = "Initialize a new .reposaurus.yml file with default configuration"

    @classmethod
    def configure_parser(cls, parser: argparse.ArgumentParser) -> None:
        """Configure init-config command arguments."""
        parser.add_argument('--force', '-f',
                            action='store_true',
                            help='Overwrite existing config file if it exists')
        parser.add_argument('--output', '-o',
                            default='.reposaurus.yml',
                            help='Output file path (default: .reposaurus.yml)')

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the init-config command."""
        try:
            output_path = Path(args.output)

            # Check if file already exists
            if output_path.exists() and not args.force:
                raise FileExistsError(
                    f"Error: {output_path} already exists. Use --force to overwrite."
                )

            # Create parent directories if they don't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the config file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(CONFIG_TEMPLATE)

            print(f"Created Reposaurus configuration file at {output_path}")

        except Exception as e:
            raise RuntimeError(f"Failed to create config file: {str(e)}")