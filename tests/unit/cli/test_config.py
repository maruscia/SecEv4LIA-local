# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for CLI configuration functionality.
CLIConfig is now local-only: only 'verbose' is configurable.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from secev4lia.cli.config import CLIConfig


class TestCLIConfig:
    """Test CLI configuration management"""

    def test_default_config(self):
        """Test default configuration values"""
        with (
            patch("pathlib.Path.exists", return_value=False),
            patch("pathlib.Path.home", return_value=Path("/fake/home")),
            patch.dict("os.environ", {}, clear=True),
        ):
            config = CLIConfig()
            # verbose defaults to 1 (WARNING level)
            assert config.verbose == 1

    def test_verbose_from_constructor(self):
        """Test verbose can be set via constructor"""
        config = CLIConfig(verbose=2)
        assert config.verbose == 2

    def test_verbose_from_config_file(self):
        """Test verbose is loaded from config file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"verbose": 3}, f)
            config_file = f.name
        try:
            with patch.dict("os.environ", {}, clear=True):
                config = CLIConfig(config_file=config_file)
                assert config.verbose == 3
        finally:
            Path(config_file).unlink()

    def test_default_config_path(self):
        """Test default configuration path"""
        fake_home = Path("/fake/home")
        with (
            patch("pathlib.Path.home", return_value=fake_home),
            patch.dict("os.environ", {}, clear=True),
        ):
            config = CLIConfig()
            expected_path = fake_home / ".config" / "secev4lia" / "config.json"
            assert config.default_config_path == expected_path

    def test_validate_passes(self):
        """Test validate() passes for local-only config"""
        config = CLIConfig()
        config.validate()  # should not raise

    def test_save_config(self):
        """Test saving configuration to file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.json"
            config = CLIConfig(verbose=2)
            config.save(str(config_path))

            assert config_path.exists()
            with open(config_path) as f:
                saved_data = json.load(f)
            assert saved_data["verbose"] == 2

    def test_nonexistent_config_file(self):
        """Test non-existent config file doesn't raise, uses defaults"""
        with patch.dict("os.environ", {}, clear=True):
            config = CLIConfig(config_file="/nonexistent/config.json")
            assert config.verbose == 1

    def test_invalid_json_config(self):
        """Test invalid JSON raises ValueError"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            config_file = f.name
        try:
            with patch.dict("os.environ", {}, clear=True):
                with pytest.raises(ValueError, match="Failed to load config file"):
                    CLIConfig(config_file=config_file)
        finally:
            Path(config_file).unlink()

    def test_empty_config_file(self):
        """Test empty config file falls back to defaults"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({}, f)
            config_file = f.name
        try:
            with patch.dict("os.environ", {}, clear=True):
                config = CLIConfig(config_file=config_file)
                assert config.verbose == 1
        finally:
            Path(config_file).unlink()

    def test_config_file_with_unknown_fields(self):
        """Test unknown fields in config file are ignored"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"verbose": 2, "unknown_field": "ignored", "other": 42}, f)
            config_file = f.name
        try:
            with patch.dict("os.environ", {}, clear=True):
                config = CLIConfig(config_file=config_file)
                assert config.verbose == 2
        finally:
            Path(config_file).unlink()
