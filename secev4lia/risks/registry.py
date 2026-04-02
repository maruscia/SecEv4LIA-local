# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Vulnerability registry.

Central catalogue of every built-in vulnerability. Each vulnerability
lives in its own folder under ``risks/``.

To add a new vulnerability:
1. Create a new folder under ``risks/`` (e.g. ``my_vulnerability/``)
2. Implement ``types.py`` and ``vulnerabilities.py``
3. Import and register it here
"""

from typing import Dict, List, Type

from secev4lia.risks.base import BaseVulnerability

from secev4lia.risks.model_evasion import ModelEvasion

from secev4lia.risks.craft_adversarial_data import CraftAdversarialData

from secev4lia.risks.prompt_injection import PromptInjection

from secev4lia.risks.jailbreak import Jailbreak

from secev4lia.risks.vector_embedding_weaknesses_exploit import (
    VectorEmbeddingWeaknessesExploit,
)

from secev4lia.risks.sensitive_information_disclosure import (
    SensitiveInformationDisclosure,
)

from secev4lia.risks.system_prompt_leakage import SystemPromptLeakage

from secev4lia.risks.excessive_agency import ExcessiveAgency

from secev4lia.risks.input_manipulation_attack import InputManipulationAttack

from secev4lia.risks.public_facing_application_exploitation import (
    PublicFacingApplicationExploitation,
)

from secev4lia.risks.malicious_tool_invocation import MaliciousToolInvocation

from secev4lia.risks.credential_exposure import CredentialExposure

from secev4lia.risks.misinformation import Misinformation


# =====================================================================
# VULNERABILITY_REGISTRY  —  name → class
# =====================================================================

VULNERABILITY_REGISTRY: Dict[str, Type[BaseVulnerability]] = {
    "ModelEvasion": ModelEvasion,
    "CraftAdversarialData": CraftAdversarialData,
    "PromptInjection": PromptInjection,
    "Jailbreak": Jailbreak,
    "VectorEmbeddingWeaknessesExploit": VectorEmbeddingWeaknessesExploit,
    "SensitiveInformationDisclosure": SensitiveInformationDisclosure,
    "SystemPromptLeakage": SystemPromptLeakage,
    "ExcessiveAgency": ExcessiveAgency,
    "InputManipulationAttack": InputManipulationAttack,
    "PublicFacingApplicationExploitation": PublicFacingApplicationExploitation,
    "MaliciousToolInvocation": MaliciousToolInvocation,
    "CredentialExposure": CredentialExposure,
    "Misinformation": Misinformation,
}


# =====================================================================
# Helpers
# =====================================================================


def get_all_vulnerability_names() -> List[str]:
    """Return all registered vulnerability names."""
    return list(VULNERABILITY_REGISTRY.keys())


__all__ = [
    "VULNERABILITY_REGISTRY",
    "get_all_vulnerability_names",
    "ModelEvasion",
    "CraftAdversarialData",
    "PromptInjection",
    "Jailbreak",
    "VectorEmbeddingWeaknessesExploit",
    "SensitiveInformationDisclosure",
    "SystemPromptLeakage",
    "ExcessiveAgency",
    "InputManipulationAttack",
    "PublicFacingApplicationExploitation",
    "MaliciousToolInvocation",
    "CredentialExposure",
    "Misinformation",
]
