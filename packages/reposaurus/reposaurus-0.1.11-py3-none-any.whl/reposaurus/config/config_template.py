"""Default template for Reposaurus configuration file."""

CONFIG_TEMPLATE = """# Reposaurus Configuration File
# Configure how Reposaurus processes and outputs repository content

patterns:
  # Use built-in default ignore patterns
  use_default_ignores: true

  # Path to custom ignore file (relative to repository root)
  ignore_file_path: ".reposaurusignore"

  # Additional patterns to always exclude
  additional_excludes:
    - ".git/"
    - ".idea/"
    - ".venv/"
    - "__pycache__/"
    - "*.pyc"

output:
  # Template for output filename (without extension)
  filename_template: "{repo_name}_repository_contents"

  # Output directory (relative to repository root)
  directory: "."

  # Version control for output files
  versioning:
    enabled: true
    # Format: none, numeric, date
    # none: no versioning
    # numeric: _v1, _v2, etc.
    # date: _YYYYMMDD_HHMMSS
    format: "numeric"
    # Whether to start from v1 or continue from highest
    start_fresh: false

  # Section separator style (line, double-line, hash, none)
  section_separator: "line"
  separator_length: 48

git:
  # Automatically add output files to .gitignore
  auto_update_gitignore: true"""