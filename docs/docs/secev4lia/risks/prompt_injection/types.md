---
sidebar_label: types
title: secev4lia.risks.prompt_injection.types
---

Prompt Injection risk patterns.

## PromptInjectionType Objects

```python
class PromptInjectionType(Enum)
```

risk patterns for Prompt Injection.

#### DIRECT\_INJECTION

User prompt directly overrides system instructions.

#### INDIRECT\_INJECTION

Malicious instructions are embedded in retrieved/external content.

#### CONTEXT\_MANIPULATION

Crafted context tricks the model into ignoring guardrails.

