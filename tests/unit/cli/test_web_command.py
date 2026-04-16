# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the `secev web` CLI command."""

import unittest
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from secev4lia.cli.commands.web import web


class _DummyLocalBackend:
    pass


class TestWebCommand(unittest.TestCase):
    """Test backend selection and command execution for web CLI."""

    def _free_port_socket(self):
        mock_socket = MagicMock()
        mock_socket.__enter__.return_value.connect_ex.return_value = 1
        return mock_socket

    def test_web_uses_local_backend(self):
        runner = CliRunner()
        config = MagicMock()
        local_backend = _DummyLocalBackend()
        app = MagicMock()

        with (
            patch(
                "secev4lia.server.storage.local.LocalBackend",
                return_value=local_backend,
            ) as mock_local_cls,
            patch(
                "secev4lia.server.dashboard.create_app", return_value=app
            ) as mock_create_app,
            patch("socket.socket", return_value=self._free_port_socket()),
        ):
            result = runner.invoke(
                web,
                ["--db-path", "/tmp/test-dashboard.db", "--no-browser"],
                obj={"config": config},
            )

        self.assertEqual(result.exit_code, 0)
        mock_local_cls.assert_called_once_with(db_path="/tmp/test-dashboard.db")
        mock_create_app.assert_called_once_with(backend=local_backend)
        app.run.assert_called_once_with(host="127.0.0.1", port=7860, show=False)


if __name__ == "__main__":
    unittest.main()
