# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for BaseEvaluationStep judge type resolution."""

import unittest
from unittest.mock import MagicMock, patch

from secev4lia.attacks.evaluator.evaluation_step import BaseEvaluationStep


class TestBaseEvaluationStepJudgeResolution(unittest.TestCase):
    """Validate judge type inference and config resolution precedence."""

    def setUp(self):
        self.step = BaseEvaluationStep(
            config={},
            logger=MagicMock(),
            client=MagicMock(),
        )

    def test_infer_judge_type_harmbench_variant_identifier(self):
        """Model ids containing HarmBenchVariant must map to harmbench_variant."""
        inferred = self.step.infer_judge_type("foo/HarmBenchVariant-7B")
        self.assertEqual(inferred, "harmbench_variant")

    def test_prepare_judge_configs_prefers_type_over_evaluator_type(self):
        """If both keys are present, explicit 'type' should win."""
        judges_to_run = self.step._prepare_judge_configs(
            [
                {
                    "identifier": "Abel-24-HarmClassifier",
                    "type": "harmbench_variant",
                    "evaluator_type": "harmbench",
                }
            ],
            base_config={},
        )

        self.assertEqual(len(judges_to_run), 1)
        judge_type, _cfg = judges_to_run[0]
        self.assertEqual(judge_type, "harmbench_variant")

    def test_enrich_items_preserves_existing_success_without_judge_votes(self):
        """Rows without eval_* columns should keep upstream success values."""
        data = [{"goal": "g1", "success": True}]

        self.step._enrich_items_with_scores(data)

        self.assertTrue(data[0]["success"])
        self.assertEqual(data[0]["best_score"], 1.0)

    def test_enrich_items_uses_is_success_for_scorer_runs(self):
        """Scorer-based results should drive success from is_success."""
        data = [{"goal": "g1", "is_success": True, "best_score": 7.5}]

        self.step._enrich_items_with_scores(data)

        self.assertTrue(data[0]["success"])
        self.assertEqual(data[0]["best_score"], 7.5)

    def test_enrich_items_uses_scorer_verdict(self):
        """Scorer verdict should map to success even without is_success."""
        data = [{"goal": "g1", "scorer_verdict": "safe", "attack_score": 3.0}]

        self.step._enrich_items_with_scores(data)

        self.assertFalse(data[0]["success"])
        self.assertEqual(data[0]["best_score"], 3.0)

    def test_run_evaluation_derives_completion_from_response(self):
        """Rows that only have response should still merge judge scores correctly."""
        input_data = [{"goal": "g1", "response": "model output"}]
        judges_config = [{"identifier": "judge-x", "type": "harmbench_variant"}]

        with (
            patch.object(
                self.step,
                "_prepare_judge_configs",
                return_value=[("harmbench_variant", {})],
            ),
            patch.object(
                self.step,
                "_run_single_evaluator",
                return_value=[
                    {
                        "goal": "g1",
                        "prefix": "",
                        "completion": "model output",
                        "eval_hbv": 1,
                    }
                ],
            ),
        ):
            out = self.step._run_evaluation(
                input_data=input_data,
                judges_config=judges_config,
                evaluator_base_config={},
            )

        self.assertEqual(out[0].get("eval_hbv"), 1)

    def test_prepare_and_sync_resolves_result_id_from_backend(self):
        """Ensure result_id is resolved using backend list_results when missing."""
        fake_result = MagicMock()
        fake_result.id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        fake_result.goal_index = 0
        fake_result.goal = "g1"

        backend = MagicMock()
        backend.list_results.return_value = MagicMock(items=[fake_result], total=1)

        step = BaseEvaluationStep(
            config={"_run_id": "r1"}, logger=MagicMock(), client=backend
        )
        step._tracking_client = backend

        items = [{"goal": "g1", "goal_index": 0, "success": True}]
        step._sync_to_server = MagicMock()
        step.prepare_and_sync(items, run_id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

        assert items[0]["result_id"] == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

    def test_prepare_and_sync_skips_without_eval_signals(self):
        """prepare_and_sync should not call sync when no eval or success data exists."""
        backend = MagicMock()
        step = BaseEvaluationStep(
            config={"_run_id": "r1"}, logger=MagicMock(), client=backend
        )
        step._tracking_client = backend
        step._sync_to_server = MagicMock()

        items = [{"goal": "g1"}]
        step.prepare_and_sync(items, run_id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

        step._sync_to_server.assert_not_called()


if __name__ == "__main__":
    unittest.main()
