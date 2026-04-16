---
sidebar_label: types
title: secev4lia.risks.jailbreak.types
---

Jailbreak risk patterns.

## JailbreakType Objects

```python
class JailbreakType(Enum)
```

risk patterns for Jailbreak.

#### ROLEPLAY

Uses fictional scenarios or personas to bypass safety filters.

#### ENCODING

Encodes malicious intent via Base64, ROT13, leetspeak, etc.

#### MULTI\_TURN

Gradually escalates across conversation turns (crescendo).

#### HYPOTHETICAL

Frames harmful requests as hypothetical or academic questions.

#### AUTHORITY\_MANIPULATION

Invokes false authority or urgency to override restrictions.

