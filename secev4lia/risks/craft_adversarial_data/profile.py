# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Threat profile for CraftAdversarialData vulnerability."""

from secev4lia.risks.profile_types import ThreatProfile
from secev4lia.risks.profile_helpers import (
    ds,
    PRIMARY,
    BASELINE_ONLY,
)
from secev4lia.risks.craft_adversarial_data import CraftAdversarialData

CRAFT_ADVERSARIAL_DATA_PROFILE = ThreatProfile(
    vulnerability=CraftAdversarialData,
    datasets=[
        ds(
            "advbench",
            PRIMARY,
            "Adversarial goals that may involve crafted perturbations",
        ),
    ],
    attacks=BASELINE_ONLY,
    objective="jailbreak",
    metrics=["asr", "judge_score"],
    description="Tests whether adversarially crafted data can compromise model behaviour.",
)
