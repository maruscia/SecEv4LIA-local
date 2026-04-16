---
sidebar_position: 6
---

# Custom Vulnerabilities

If the built-in vulnerability coverage is not enough for your domain, you can add a custom vulnerability class and map it to datasets/attacks with a threat profile.

## Minimal Example

```python
from enum import Enum
from typing import List, Optional

from secev4lia.risks.base import BaseVulnerability


class APIRateLimitingSignal(Enum):
    CONCURRENT_REQUESTS = "concurrent_requests"
    TOKEN_EXHAUSTION = "token_exhaustion"
    QUOTA_BYPASS = "quota_bypass"


class APIRateLimiting(BaseVulnerability):
    name = "API Rate Limiting"
    description = "Tests resilience against abuse patterns targeting request and quota controls."

    ALLOWED_TYPES = [s.value for s in APIRateLimitingSignal]
    _type_enum = APIRateLimitingSignal

    def __init__(self, types: Optional[List[str]] = None):
        selected = [APIRateLimitingSignal(t) for t in types] if types else list(APIRateLimitingSignal)
        super().__init__(types=selected)


vuln = APIRateLimiting()
print(vuln.get_name())
```

## Add a Threat Profile

```python
from secev4lia.risks.profile_types import ThreatProfile
from secev4lia.risks.profile_helpers import ds, atk, PRIMARY

API_RATE_LIMITING_PROFILE = ThreatProfile(
    vulnerability=APIRateLimiting,
    datasets=[
        ds("wmdp_cyber", PRIMARY, "Security-oriented goals relevant to abuse scenarios"),
    ],
    attacks=[
        atk("h4rm3l", PRIMARY, "Fast stress testing with diverse prompt transformations"),
        atk("TAP", PRIMARY, "Structured search over attack candidates"),
        atk("PAIR", PRIMARY, "Iterative refinement loop with attacker feedback"),
    ],
    objective="jailbreak",
    metrics=["asr", "judge_score"],
    description="Assesses robustness against request-abuse and quota-bypass behaviors.",
)
```

## Recommended Workflow

1. Define a vulnerability class with clear scope and description.
2. Create one threat profile with primary datasets and attacks.
3. Start with a quick run on a limited dataset sample.
4. Expand with additional datasets and stricter judges.
5. Track trends over time in ASR and judge score.

## Validation Tips

- Keep class naming and profile naming consistent.
- Use small dataset limits first to verify your pipeline quickly.
- Add unit tests for class construction and profile consistency.
- Document business impact and mitigation guidance for each finding.
