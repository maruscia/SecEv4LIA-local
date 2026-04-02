# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Threat profile for CredentialExposure vulnerability."""

from secev4lia.risks.profile_types import ThreatProfile
from secev4lia.risks.profile_helpers import BASELINE_ONLY
from secev4lia.risks.credential_exposure import CredentialExposure

CREDENTIAL_EXPOSURE_PROFILE = ThreatProfile(
    vulnerability=CredentialExposure,
    datasets=[],  # No standard public dataset — requires custom goals
    attacks=BASELINE_ONLY,
    objective="policy_violation",
    metrics=["asr"],
    description="Tests for hardcoded credentials, token leakage, and misconfigured access.",
)
