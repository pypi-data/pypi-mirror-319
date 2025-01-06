"""Configuration management for Reposaurus."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigurationError(Exception):
    """Raised when there are configuration-related errors."""
    pass


class ConfigManager:
    """Manages Reposaurus configuration loading and validation."""

    DEFAULT_CONFIG_FILE = ".reposaurus.yml"

    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_file = config_file or self.DEFAULT_CONFIG_FILE
        self.config = self._load_default_config()

        if Path(self.config_file).exists():
            self._load_config()

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            'patterns': {
                'use_default_ignores': True,
                'ignore_file_path': '.reposaurusignore'
            },
            'output': {
                'filename_template': '{repo_name}_repository_contents',
                'directory': '.',
                'use_versioning': True
            },
            'git': {
                'auto_update_gitignore': True
            }
        }

    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self._merge_config(user_config)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing config file: {str(e)}")
        except Exception as e:
            raise ConfigurationError(f"Error loading config file: {str(e)}")

    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """Merge user configuration with defaults."""
        for section, values in user_config.items():
            if section in self.config:
                if isinstance(values, dict):
                    self.config[section].update(values)
                else:
                    self.config[section] = values

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        try:
            return self.config[section][key]
        except KeyError:
            return default

    def validate(self) -> None:
        """Validate configuration values."""
        # Add validation logic here
        pass