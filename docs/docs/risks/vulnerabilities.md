---
sidebar_position: 3
---

# Vulnerabilities

SecEv4LIA's current vulnerability reference is focused on a single implemented vulnerability: **Jailbreak**.

## Jailbreak

### Example

```python
from secev4lia.risks import Jailbreak

vuln = Jailbreak()
```

### Description

`Jailbreak` tests if an LLM can be manipulated into violating safety policy.

## Threat Profile

**Objective**: `jailbreak`

**Recommended Datasets**:
- **strongreject** (PRIMARY): 324 forbidden prompts designed for jailbreak evaluation
- **harmbench** (PRIMARY): 200 harmful behaviors for bypass testing
- **advbench** (PRIMARY): 520 adversarial goals for jailbreak attacks
- **jailbreakbench** (PRIMARY): 100 curated misuse behaviours from NeurIPS 2024 benchmark
- **simplesafetytests** (SECONDARY): 100 clear-cut harmful prompts as baseline
- **donotanswer** (SECONDARY): 939 refusal questions for comprehensive coverage
- **saladbench_attack** (SECONDARY): 5K attack-enhanced prompts with jailbreak methods

**Attack Techniques**:
- h4rm3l (PRIMARY): Composable decorator-chain jailbreak for fast high-yield probing
- TAP (PRIMARY): Tree-search jailbreak with pruning for efficient discovery
- PAIR (PRIMARY): Iterative attacker-guided refinement for adaptive bypass

**Metrics**: `asr`, `judge_score`

### Registry Lookup

```python
from secev4lia.risks import VULNERABILITY_REGISTRY

jailbreak_cls = VULNERABILITY_REGISTRY["Jailbreak"]
jailbreak_vuln = jailbreak_cls()
print(jailbreak_vuln.name)
```
