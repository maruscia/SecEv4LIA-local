---
sidebar_label: utils
title: secev4lia.utils
---

#### display\_secev4lia\_splash

```python
def display_secev4lia_splash()
```

Displays the SecEv4LIA splash screen using the pre-defined ASCII art.

#### resolve\_agent\_type

```python
def resolve_agent_type(
        agent_type_input: Union[AgentTypeEnum, str]) -> AgentTypeEnum
```

Resolves the agent type from a string or AgentTypeEnum member.

#### resolve\_api\_token

```python
def resolve_api_token(direct_api_key_param: Optional[str] = None,
                      config_file_path: Optional[str] = None) -> Optional[str]
```

Resolves the API token. Returns None — SecEv4LIA operates in local-only mode.

Kept for backward compatibility with code that calls this function.

**Returns**:

- `None` - Always returns None (local mode only).

