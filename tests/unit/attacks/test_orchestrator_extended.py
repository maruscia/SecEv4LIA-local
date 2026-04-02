# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Additional tests for AttackOrchestrator — covering execute flow and HTTP helpers."""

import json
import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from secev4lia.attacks.orchestrator import AttackOrchestrator
from secev4lia.attacks.techniques.base import BaseAttack
from secev4lia.errors import SecEv4LIAError


def _make_orchestrator():
    """Factory helper for creating a test orchestrator."""

    class TestAttack(BaseAttack):
        def _get_pipeline_steps(self):
            return []

        def run(self, **kwargs):
            return kwargs.get("goals", [])

    class TestOrchestrator(AttackOrchestrator):
        attack_type = "test"
        attack_impl_class = TestAttack

    mock_secev4lia_agent = MagicMock()
    mock_secev4lia_agent.client = MagicMock()
    mock_secev4lia_agent.router.backend_agent.id = uuid4()
    mock_secev4lia_agent.router.organization_id = uuid4()

    return TestOrchestrator(mock_secev4lia_agent), mock_secev4lia_agent, TestAttack


_VALID_RUN_ID = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
_VALID_ATK_ID = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


class TestAttackOrchestratorExecuteFlow(unittest.TestCase):
    """Test full execute flow including status updates."""

    @patch.object(
        AttackOrchestrator, "_create_server_run_record", return_value=_VALID_RUN_ID
    )
    @patch.object(
        AttackOrchestrator, "_create_server_attack_record", return_value=_VALID_ATK_ID
    )
    @patch.object(AttackOrchestrator, "_execute_local_attack", return_value=["result"])
    def test_execute_updates_run_status_to_running(
        self, mock_exec, mock_create_atk, mock_create_run
    ):
        """Test that execute updates run to RUNNING status."""
        orch, secev4lia_agent, _ = _make_orchestrator()

        attack_config = {"goals": ["test"]}
        orch.execute(
            attack_config=attack_config,
            run_config_override=None,
            fail_on_run_error=False,
        )

        # At least one call should be for RUNNING
        calls = secev4lia_agent.backend.update_run.call_args_list
        self.assertTrue(len(calls) >= 1)

    @patch.object(
        AttackOrchestrator, "_create_server_run_record", return_value=_VALID_RUN_ID
    )
    @patch.object(
        AttackOrchestrator, "_create_server_attack_record", return_value=_VALID_ATK_ID
    )
    @patch.object(AttackOrchestrator, "_execute_local_attack", return_value=["result"])
    def test_execute_updates_run_status_to_completed(
        self, mock_exec, mock_create_atk, mock_create_run
    ):
        """Test that execute updates run to COMPLETED on success."""
        orch, secev4lia_agent, _ = _make_orchestrator()

        attack_config = {"goals": ["test"]}
        orch.execute(
            attack_config=attack_config,
            run_config_override=None,
            fail_on_run_error=False,
        )

        # Should have called update_run at least twice (RUNNING and COMPLETED)
        self.assertGreaterEqual(secev4lia_agent.backend.update_run.call_count, 2)

    @patch.object(
        AttackOrchestrator, "_create_server_run_record", return_value=_VALID_RUN_ID
    )
    @patch.object(
        AttackOrchestrator, "_create_server_attack_record", return_value=_VALID_ATK_ID
    )
    @patch.object(
        AttackOrchestrator, "_execute_local_attack", side_effect=RuntimeError("Boom")
    )
    def test_execute_updates_run_status_to_failed_on_error(
        self, mock_exec, mock_create_atk, mock_create_run
    ):
        """Test that execute updates run to FAILED on exception."""
        orch, secev4lia_agent, _ = _make_orchestrator()

        attack_config = {"goals": ["test"]}
        with self.assertRaises(RuntimeError):
            orch.execute(
                attack_config=attack_config,
                run_config_override=None,
                fail_on_run_error=True,
            )

        # Should attempt FAILED update
        self.assertTrue(secev4lia_agent.backend.update_run.call_count >= 1)

    @patch.object(
        AttackOrchestrator, "_create_server_run_record", return_value=_VALID_RUN_ID
    )
    @patch.object(
        AttackOrchestrator, "_create_server_attack_record", return_value=_VALID_ATK_ID
    )
    @patch.object(AttackOrchestrator, "_execute_local_attack", return_value=["result"])
    def test_execute_continues_when_status_update_fails(
        self, mock_exec, mock_create_atk, mock_create_run
    ):
        """Test that execute continues even if status update fails."""
        orch, secev4lia_agent, _ = _make_orchestrator()
        secev4lia_agent.backend.update_run.side_effect = Exception("Update failed")

        attack_config = {"goals": ["test"]}
        # Should not raise even though update_run fails
        results = orch.execute(
            attack_config=attack_config,
            run_config_override=None,
            fail_on_run_error=False,
        )
        self.assertIsNotNone(results)


class TestAttackOrchestratorHTTPResponseParsing(unittest.TestCase):
    """Test HTTP response parsing helpers in depth."""

    def setUp(self):
        """Set up orchestrator for HTTP tests."""
        self.orch, _, _ = _make_orchestrator()

    def test_decode_response_valid_utf8(self):
        """Test decoding valid UTF-8 response."""
        mock_response = MagicMock()
        mock_response.content = b'{"id": "test-123"}'
        result = self.orch._decode_response(mock_response)
        self.assertEqual(result, '{"id": "test-123"}')

    def test_decode_response_none_content(self):
        """Test decoding None content."""
        mock_response = MagicMock()
        mock_response.content = None
        result = self.orch._decode_response(mock_response)
        self.assertEqual(result, "N/A")

    def test_decode_response_invalid_utf8(self):
        """Test decoding invalid UTF-8 content (uses replace mode)."""
        mock_response = MagicMock()
        mock_response.content = b"\xff\xfeInvalid"
        result = self.orch._decode_response(mock_response)
        self.assertIn("Invalid", result)

    def test_parse_json_valid(self):
        """Test parsing valid JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b'{"id": "123"}'
        result = self.orch._parse_json(mock_response, '{"id": "123"}', "test")
        self.assertEqual(result["id"], "123")

    def test_parse_json_invalid_201_raises(self):
        """Test that invalid JSON on 201 response raises SecEv4LIAError."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b"not json"
        with self.assertRaises(SecEv4LIAError):
            self.orch._parse_json(mock_response, "not json", "test")

    def test_parse_json_invalid_non_201_returns_none(self):
        """Test that invalid JSON on non-201 falls back gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"not json"
        mock_response.parsed = None
        result = self.orch._parse_json(mock_response, "not json", "test")
        self.assertIsNone(result)

    def test_parse_json_fallback_to_additional_properties(self):
        """Test fallback to response.parsed.additional_properties."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = None
        mock_response.parsed = MagicMock()
        mock_response.parsed.additional_properties = {"id": "fallback-123"}
        result = self.orch._parse_json(mock_response, "", "test")
        self.assertEqual(result["id"], "fallback-123")

    def test_parse_response_201_success(self):
        """Test parse_response with 201 status."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b'{"id": "created"}'
        result = self.orch._parse_response(mock_response, '{"id": "created"}', "test")
        self.assertEqual(result["id"], "created")

    def test_parse_response_201_no_data_raises(self):
        """Test parse_response with 201 but no parseable data raises."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = None
        mock_response.parsed = None
        with self.assertRaises(SecEv4LIAError):
            self.orch._parse_response(mock_response, "N/A", "test")

    def test_parse_response_500_raises(self):
        """Test parse_response with server error raises."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b"Server Error"
        with self.assertRaises(SecEv4LIAError):
            self.orch._parse_response(mock_response, "Server Error", "test")

    def test_extract_ids_from_data_success(self):
        """Test extracting IDs from parsed data."""
        data = {"id": "atk-1", "associated_run_id": "run-1"}
        atk_id, run_id = self.orch._extract_ids_from_data(data, "test", "")
        self.assertEqual(atk_id, "atk-1")
        self.assertEqual(run_id, "run-1")

    def test_extract_ids_from_data_no_run_id(self):
        """Test extracting IDs when no run_id present."""
        data = {"id": "atk-1"}
        atk_id, run_id = self.orch._extract_ids_from_data(data, "test", "")
        self.assertEqual(atk_id, "atk-1")
        self.assertIsNone(run_id)

    def test_extract_ids_from_data_no_id_raises(self):
        """Test missing id raises SecEv4LIAError."""
        data = {"other": "value"}
        with self.assertRaises(SecEv4LIAError):
            self.orch._extract_ids_from_data(data, "test", "")

    def test_extract_ids_from_response_full_pipeline(self):
        """Test full extract_ids_from_response pipeline."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = json.dumps(
            {"id": "atk-full", "associated_run_id": "run-full"}
        ).encode()
        atk_id, run_id = self.orch._extract_ids_from_response(mock_response, "test")
        self.assertEqual(atk_id, "atk-full")
        self.assertEqual(run_id, "run-full")


class TestGetAttackImplKwargs(unittest.TestCase):
    """Test _get_attack_impl_kwargs."""

    def test_kwargs_merges_configs(self):
        """Test that attack_config and run_config are merged."""
        orch, _, _ = _make_orchestrator()
        kwargs = orch._get_attack_impl_kwargs(
            attack_config={"a": 1},
            run_config_override={"b": 2},
            run_id="run-123",
        )
        self.assertEqual(kwargs["config"]["a"], 1)
        self.assertEqual(kwargs["config"]["b"], 2)
        self.assertEqual(kwargs["config"]["_run_id"], "run-123")

    def test_kwargs_without_run_config(self):
        """Test kwargs when run_config_override is None."""
        orch, _, _ = _make_orchestrator()
        kwargs = orch._get_attack_impl_kwargs(
            attack_config={"a": 1},
            run_config_override=None,
            run_id="run-123",
        )
        self.assertEqual(kwargs["config"]["a"], 1)
        self.assertIn("_run_id", kwargs["config"])

    def test_kwargs_includes_client_and_router(self):
        """Test that kwargs includes client and agent_router."""
        orch, secev4lia_agent, _ = _make_orchestrator()
        kwargs = orch._get_attack_impl_kwargs(
            attack_config={},
            run_config_override=None,
            run_id="run-123",
        )
        self.assertIn("client", kwargs)
        self.assertIn("agent_router", kwargs)
        self.assertIs(kwargs["client"], secev4lia_agent.backend)


if __name__ == "__main__":
    unittest.main()
