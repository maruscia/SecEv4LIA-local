---
sidebar_label: types
title: secev4lia.risks.system_prompt_leakage.types
---

System Prompt Leakage risk patterns.

## SystemPromptLeakageType Objects

```python
class SystemPromptLeakageType(Enum)
```

risk patterns for System Prompt Leakage.

#### SECRETS\_AND\_CREDENTIALS

Reveals API keys, database credentials, or system architecture from the prompt.

#### INSTRUCTIONS

Discloses internal instructions, rules, or operational procedures.

#### GUARD\_EXPOSURE

Exposes guard mechanisms, rejection rules, or filtering criteria.

#### PERMISSIONS\_AND\_ROLES

Reveals role-based permissions, access controls, or internal configurations.

