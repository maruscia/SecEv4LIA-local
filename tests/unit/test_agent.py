# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Tests for SecEv4LIA class (secev4lia/agent.py)."""

import unittest
from unittest.mock import MagicMock, patch

from secev4lia.errors import SecEv4LIAError


class TestSecEv4LIAInitialization(unittest.TestCase):
    """Test SecEv4LIA initialization."""

    @patch("secev4lia.agent.AgentRouter")
    @patch("secev4lia.agent.utils.resolve_agent_type")
    def test_basic_initialization(self, mock_resolve_type, mock_router):
        """Test basic SecEv4LIA initialization."""
        from secev4lia.agent import SecEv4LIA

        agent = SecEv4LIA(
            endpoint="http://localhost:8000",
        )

        self.assertIsNotNone(agent.router)
        self.assertIsNotNone(agent.router)
        mock_router.assert_called_once()

    @patch("secev4lia.agent.AgentRouter")
    @patch("secev4lia.agent.utils.resolve_agent_type")
    def test_attack_strategies_lazy_loaded(self, mock_resolve_type, mock_router):
        """Test attack strategies are None initially (lazy-loaded)."""
        from secev4lia.agent import SecEv4LIA

        agent = SecEv4LIA(
            endpoint="http://localhost:8000",
        )

        self.assertIsNone(agent._attack_strategies)

    @patch("secev4lia.agent.AgentRouter")
    @patch("secev4lia.agent.utils.resolve_agent_type")
    def test_with_metadata(self, mock_resolve_type, mock_router):
        """Test initialization with metadata."""
        from secev4lia.agent import SecEv4LIA

        metadata = {"key": "value"}
        SecEv4LIA(
            endpoint="http://localhost:8000",
            metadata=metadata,
        )

        # metadata should be passed to the router
        call_kwargs = mock_router.call_args
        self.assertEqual(call_kwargs.kwargs.get("metadata"), metadata)

    @patch("secev4lia.agent.AgentRouter")
    @patch("secev4lia.agent.utils.resolve_agent_type")
    def test_target_config_is_merged_into_router_defaults(
        self, mock_resolve_type, mock_router
    ):
        """Test target_config becomes the router-owned victim request default."""
        from secev4lia.agent import SecEv4LIA

        SecEv4LIA(
            endpoint="http://localhost:8000",
            target_config={"max_tokens": 321, "temperature": 0.2},
            adapter_operational_config={"name": "demo-model", "temperature": 0.4},
            metadata={"label": "demo"},
        )

        call_kwargs = mock_router.call_args.kwargs
        self.assertEqual(call_kwargs["adapter_operational_config"]["max_tokens"], 321)
        self.assertEqual(call_kwargs["adapter_operational_config"]["temperature"], 0.4)
        self.assertEqual(call_kwargs["metadata"]["temperature"], 0.2)
        self.assertEqual(call_kwargs["metadata"]["label"], "demo")


class TestSecEv4LIAAttackStrategies(unittest.TestCase):
    """Test SecEv4LIA.attack_strategies lazy loading."""

    @patch("secev4lia.agent.AgentRouter")
    @patch("secev4lia.agent.utils.resolve_agent_type")
    def test_attack_strategies_loaded_on_access(self, mock_resolve_type, mock_router):
        """Test that attack_strategies are loaded on first access."""
        from secev4lia.agent import SecEv4LIA

        agent = SecEv4LIA(
            endpoint="http://localhost:8000",
        )

        strategies = agent.attack_strategies

        self.assertIn("advprefix", strategies)
        self.assertIn("baseline", strategies)
        self.assertIn("pair", strategies)

    @patch("secev4lia.agent.AgentRouter")
    @patch("secev4lia.agent.utils.resolve_agent_type")
    def test_attack_strategies_cached(self, mock_resolve_type, mock_router):
        """Test that attack_strategies are cached after first access."""
        from secev4lia.agent import SecEv4LIA

        agent = SecEv4LIA(
            endpoint="http://localhost:8000",
        )

        strategies1 = agent.attack_strategies
        strategies2 = agent.attack_strategies

        self.assertIs(strategies1, strategies2)


class TestSecEv4LIAHack(unittest.TestCase):
    """Test SecEv4LIA.hack method."""

    @patch("secev4lia.agent.AgentRouter")
    @patch("secev4lia.agent.utils.resolve_agent_type")
    def setUp(self, mock_resolve_type, mock_router):
        """Set up SecEv4LIA for hack tests."""
        from secev4lia.agent import SecEv4LIA

        self.agent = SecEv4LIA(
            endpoint="http://localhost:8000",
        )

        # Mock the router's backend_agent
        mock_backend = MagicMock()
        mock_backend.name = "test-agent"
        mock_backend.id = "agent-123"
        mock_backend.agent_type = "litellm"
        self.agent.router.backend_agent = mock_backend

    def test_hack_missing_attack_type_raises(self):
        """Test that missing attack_type raises SecEv4LIAError."""
        with self.assertRaises(SecEv4LIAError) as ctx:
            self.agent.hack(attack_config={})
        self.assertIn("attack_type", str(ctx.exception))

    def test_hack_unsupported_attack_type_raises(self):
        """Test that unsupported attack_type raises SecEv4LIAError."""
        with self.assertRaises(SecEv4LIAError) as ctx:
            self.agent.hack(attack_config={"attack_type": "nonexistent"})
        self.assertIn("Unsupported", str(ctx.exception))

    def test_hack_delegates_to_strategy(self):
        """Test that hack delegates to the correct strategy."""
        mock_strategy = MagicMock()
        mock_strategy.execute.return_value = [{"result": "test"}]
        self.agent._attack_strategies = {"test_attack": mock_strategy}

        result = self.agent.hack(
            attack_config={"attack_type": "test_attack", "goals": ["test"]}
        )

        mock_strategy.execute.assert_called_once()
        self.assertEqual(result, [{"result": "test"}])

    def test_hack_passes_run_config_override(self):
        """Test that run_config_override is passed to strategy."""
        mock_strategy = MagicMock()
        mock_strategy.execute.return_value = []
        self.agent._attack_strategies = {"test_attack": mock_strategy}

        run_config = {"custom": "override"}
        self.agent.hack(
            attack_config={"attack_type": "test_attack"},
            run_config_override=run_config,
        )

        call_kwargs = mock_strategy.execute.call_args.kwargs
        self.assertEqual(call_kwargs["run_config_override"], run_config)

    def test_hack_passes_fail_on_run_error(self):
        """Test that fail_on_run_error is passed to strategy."""
        mock_strategy = MagicMock()
        mock_strategy.execute.return_value = []
        self.agent._attack_strategies = {"test_attack": mock_strategy}

        self.agent.hack(
            attack_config={"attack_type": "test_attack"},
            fail_on_run_error=False,
        )

        call_kwargs = mock_strategy.execute.call_args.kwargs
        self.assertFalse(call_kwargs["fail_on_run_error"])

    def test_hack_wraps_value_error(self):
        """Test that ValueError is wrapped in SecEv4LIAError."""
        mock_strategy = MagicMock()
        mock_strategy.execute.side_effect = ValueError("Bad config")
        self.agent._attack_strategies = {"test_attack": mock_strategy}

        with self.assertRaises(SecEv4LIAError) as ctx:
            self.agent.hack(attack_config={"attack_type": "test_attack"})
        self.assertIn("Configuration error", str(ctx.exception))

    def test_hack_wraps_runtime_error(self):
        """Test that RuntimeError is wrapped in SecEv4LIAError."""
        mock_strategy = MagicMock()
        mock_strategy.execute.side_effect = RuntimeError("Something broke")
        self.agent._attack_strategies = {"test_attack": mock_strategy}

        with self.assertRaises(SecEv4LIAError) as ctx:
            self.agent.hack(attack_config={"attack_type": "test_attack"})
        self.assertIn("unexpected runtime error", str(ctx.exception).lower())

    def test_hack_wraps_backend_runtime_error(self):
        """Test backend-specific RuntimeErrors are wrapped."""
        mock_strategy = MagicMock()
        mock_strategy.execute.side_effect = RuntimeError(
            "Failed to create backend agent"
        )
        self.agent._attack_strategies = {"test_attack": mock_strategy}

        with self.assertRaises(SecEv4LIAError) as ctx:
            self.agent.hack(attack_config={"attack_type": "test_attack"})
        self.assertIn("Backend agent operation failed", str(ctx.exception))

    def test_hack_wraps_generic_exception(self):
        """Test that generic exceptions are wrapped in SecEv4LIAError."""
        mock_strategy = MagicMock()
        mock_strategy.execute.side_effect = Exception("Unknown error")
        self.agent._attack_strategies = {"test_attack": mock_strategy}

        with self.assertRaises(SecEv4LIAError):
            self.agent.hack(attack_config={"attack_type": "test_attack"})

    def test_hack_reraises_secev4lia_error(self):
        """Test that SecEv4LIAError is re-raised as-is."""
        mock_strategy = MagicMock()
        mock_strategy.execute.side_effect = SecEv4LIAError("Direct error")
        self.agent._attack_strategies = {"test_attack": mock_strategy}

        with self.assertRaises(SecEv4LIAError) as ctx:
            self.agent.hack(attack_config={"attack_type": "test_attack"})
        self.assertEqual(str(ctx.exception), "Direct error")


if __name__ == "__main__":
    unittest.main()
