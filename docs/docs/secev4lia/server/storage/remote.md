---
sidebar_label: remote
title: secev4lia.server.storage.remote
---

RemoteBackend — StorageBackend implementation backed by api.secev4lia.dev.

This backend centralises all HTTP calls that were previously scattered across
AgentRouter, AttackOrchestrator, Tracker, and StepTracker.  It is instantiated
when an API key is available and selected automatically by SecEv4LIA.

## RemoteBackend Objects

```python
class RemoteBackend()
```

StorageBackend implementation that talks to api.secev4lia.dev.

Wraps all HTTP calls behind the StorageBackend interface so that the rest
of the SDK is entirely decoupled from HTTP concerns.

#### get\_context

```python
def get_context() -> OrganizationContext
```

Fetch org_id and user_id from the first agent (cached after first call).

#### count\_result\_buckets

```python
def count_result_buckets() -> Dict[str, int]
```

Efficiently count results by evaluation status using filtered API calls.

