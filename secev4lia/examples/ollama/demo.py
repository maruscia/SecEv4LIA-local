# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Packaged Ollama demo configuration used by `secev examples ollama`."""

from secev4lia.router.types import AgentTypeEnum

TARGET_MODEL = "gemma3:4b"
ATTACKER_MODEL = "gemma3:4b"
OLLAMA_ENDPOINT = "http://localhost:11434"
JUDGE_MODEL = "gemma3:4b"


def build_ollama_demo_config() -> dict:
    """Return the canonical Ollama demo configuration."""
    return {
        "agent": {
            "name": "ollama-target",
            "endpoint": OLLAMA_ENDPOINT,
            "agent_type": AgentTypeEnum.OLLAMA,
            "adapter_operational_config": {
                "name": TARGET_MODEL,
            },
        },
        "attack_config": {
            "attack_type": "flipattack",
            "dataset": {
                "preset": "harmbench",
                "limit": 5,
            },
            "batch_size_judge": 5,
            "goal_batch_size": 5,
            "goal_batch_workers": 1,
            "max_tokens": 400,
            "judges": [
                {
                    "identifier": JUDGE_MODEL,
                    "type": "harmbench_variant",
                    "agent_type": AgentTypeEnum.OLLAMA,
                    "endpoint": OLLAMA_ENDPOINT,
                }
            ],
        },
    }
