# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Tests for secev CLI main entry point (cli/main.py).

Uses Click's CliRunner for realistic CLI invocation testing.
"""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from secev4lia.cli.main import cli


class TestCLIVersion(unittest.TestCase):
    """Test the version command."""

    def test_version_flag(self):
        """Test --version flag shows version info."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("secev", result.output)

    @patch("secev4lia.cli.main.CLIConfig")
    def test_version_command(self, mock_config_class):
        """Test 'version' command displays version."""
        mock_config = MagicMock()
        mock_config.api_key = "test-key-123456789"
        mock_config.base_url = ""
        mock_config.default_config_path = Path("/tmp/config.json")
        mock_config_class.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("SecEv4LIA CLI", result.output)


class TestCLIHelp(unittest.TestCase):
    """Test CLI help output."""

    def test_help_flag(self):
        """Test --help flag shows help text."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("SecEv4LIA CLI", result.output)
        self.assertIn("Quick Start", result.output)

    def test_help_shows_commands(self):
        """Test help output lists available commands."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        self.assertIn("config", result.output)
        self.assertIn("attack", result.output)
        self.assertIn("init", result.output)
        self.assertIn("version", result.output)
        self.assertIn("doctor", result.output)


class TestCLIConfigContext(unittest.TestCase):
    """Test CLI configuration context setup."""

    @patch("secev4lia.cli.main.CLIConfig")
    @patch("secev4lia.cli.main._launch_tui_default")
    def test_config_passed_to_context(self, mock_tui, mock_config_class):
        """Test that CLIConfig is initialized and passed to context."""
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config

        runner = CliRunner()
        runner.invoke(cli, [])

        mock_config_class.assert_called_once()

    @patch("secev4lia.cli.main.CLIConfig")
    @patch("secev4lia.cli.main._launch_tui_default")
    def test_verbose_flag(self, mock_tui, mock_config_class):
        """Test that -v verbose flag increments verbosity."""
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config

        runner = CliRunner()
        runner.invoke(cli, ["-vv"])

        call_kwargs = mock_config_class.call_args.kwargs
        self.assertEqual(call_kwargs["verbose"], 2)

    @patch("secev4lia.cli.main.CLIConfig")
    def test_config_error_exits(self, mock_config_class):
        """Test that configuration error causes exit."""
        mock_config_class.side_effect = Exception("Config error")

        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertNotEqual(result.exit_code, 0)


class TestCLIDoctor(unittest.TestCase):
    """Test the doctor command."""

    @patch("secev4lia.cli.main.CLIConfig")
    def test_doctor_without_config_file(self, mock_config_class):
        """Test doctor when no local config file is present."""
        mock_config = MagicMock()
        mock_config.default_config_path = MagicMock()
        mock_config.default_config_path.exists.return_value = False
        mock_config_class.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(cli, ["doctor"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("SecEv4LIA CLI Diagnostics", result.output)

    @patch("secev4lia.cli.main.CLIConfig")
    def test_doctor_with_config_file(self, mock_config_class):
        """Test doctor when local config file is present."""
        mock_config = MagicMock()
        mock_config.default_config_path = MagicMock()
        mock_config.default_config_path.exists.return_value = True
        mock_config_class.return_value = mock_config

        runner = CliRunner()
        result = runner.invoke(cli, ["doctor"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("SecEv4LIA CLI Diagnostics", result.output)


class TestCLINoCommand(unittest.TestCase):
    """Test CLI with no subcommand."""

    @patch("secev4lia.cli.main.CLIConfig")
    @patch("secev4lia.cli.main._launch_tui_default")
    def test_no_command_launches_tui(self, mock_tui, mock_config_class):
        """Test that no subcommand launches TUI."""
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config

        runner = CliRunner()
        runner.invoke(cli, [])

        mock_tui.assert_called_once()


if __name__ == "__main__":
    unittest.main()
