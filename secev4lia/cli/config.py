# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
CLI Configuration Management

Handles configuration loading from environment variables, files, and command line arguments.
Uses standardized priority order: CLI args > Config file > Environment > Default
"""

import json
from pathlib import Path
from typing import Optional

# Sentinel object to detect if a parameter was explicitly passed
_UNSET = object()

# Verbosity level constants (aligned with logging levels)
VERBOSITY_ERROR = 0  # Only errors
VERBOSITY_WARNING = 1  # Errors and warnings
VERBOSITY_INFO = 2  # Errors, warnings, and info
VERBOSITY_DEBUG = 3  # Everything including debug

VERBOSITY_NAMES = {
    0: "ERROR",
    1: "WARNING",
    2: "INFO",
    3: "DEBUG",
}

VERBOSITY_LEVELS = {
    "error": 0,
    "warning": 1,
    "info": 2,
    "debug": 3,
}


class CLIConfig:
    """CLI configuration management with multiple sources"""

    def __init__(
        self,
        config_file=_UNSET,
        verbose=_UNSET,
    ):
        """Initialize with explicit tracking of what was passed via CLI"""
        # Store defaults
        self._defaults = {
            "verbose": VERBOSITY_WARNING,  # Default to WARNING level
        }

        # Track what was explicitly passed using sentinel values
        self._cli_overrides = set()

        if config_file is not _UNSET:
            self.config_file = config_file
        else:
            self.config_file = None

        if verbose is not _UNSET:
            self.verbose = verbose
            if verbose is not None and verbose > 0:
                self._cli_overrides.add("verbose")
        else:
            self.verbose = self._defaults["verbose"]

        # STANDARDIZED PRIORITY ORDER:
        # 1. CLI arguments (tracked in _cli_overrides)
        # 2. Config file
        # 3. Defaults (already set)

        # Initialize config overrides tracking
        self._config_overrides = set()

        if self.config_file:
            self._load_from_file(self.config_file)
        else:
            self._load_default_config()

    def _load_from_file(self, config_path: str):
        """Load from configuration file (JSON or YAML)"""
        path = Path(config_path)
        if not path.exists():
            return

        try:
            with open(path) as f:
                if path.suffix.lower() in [".yaml", ".yml"]:
                    try:
                        import yaml

                        config_data = yaml.safe_load(f)
                    except ImportError:
                        raise ImportError(
                            "PyYAML required for YAML config files. Install with: pip install pyyaml"
                        )
                else:
                    config_data = json.load(f)

                for key, value in config_data.items():
                    if key in self._cli_overrides:
                        continue
                    if hasattr(self, key):
                        setattr(self, key, value)
                        self._config_overrides.add(key)
        except Exception as e:
            raise ValueError(f"Failed to load config file {config_path}: {e}")

    def _load_default_config(self):
        """Load from default config file"""
        default_config = Path.home() / ".config" / "secev4lia" / "config.json"
        if default_config.exists():
            self._load_from_file(str(default_config))

    def save(self, path: Optional[str] = None):
        """Save configuration to file"""
        if not path:
            config_dir = Path.home() / ".config" / "secev4lia"
            config_dir.mkdir(parents=True, exist_ok=True)
            path = config_dir / "config.json"

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            config_dict = {}
            if self.verbose is not None:
                config_dict["verbose"] = self.verbose
            json.dump(config_dict, f, indent=2)

    def validate(self):
        """Validate configuration."""
        pass

    def should_show_info(self) -> bool:
        """Check if INFO level messages should be displayed"""
        return self.verbose >= VERBOSITY_INFO

    def should_show_warning(self) -> bool:
        """Check if WARNING level messages should be displayed"""
        return self.verbose >= VERBOSITY_WARNING

    def should_show_debug(self) -> bool:
        """Check if DEBUG level messages should be displayed"""
        return self.verbose >= VERBOSITY_DEBUG

    def get_verbosity_name(self) -> str:
        """Get the name of the current verbosity level"""
        return VERBOSITY_NAMES.get(self.verbose, "UNKNOWN")

    @property
    def default_config_path(self) -> Path:
        """Get the default configuration file path"""
        return Path.home() / ".config" / "secev4lia" / "config.json"
