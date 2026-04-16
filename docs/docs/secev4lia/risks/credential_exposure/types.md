---
sidebar_label: types
title: secev4lia.risks.credential_exposure.types
---

Credential Exposure and Mismanagement risk patterns.

## CredentialExposureType Objects

```python
class CredentialExposureType(Enum)
```

risk patterns for Credential Exposure and Mismanagement.

#### HARDCODED\_CREDENTIALS

Credentials embedded in prompts or model context.

#### TOKEN\_LEAKAGE

Auth tokens exposed in LLM outputs or logs.

#### MISCONFIGURED\_ACCESS

Weak or default credentials on model-facing services.

