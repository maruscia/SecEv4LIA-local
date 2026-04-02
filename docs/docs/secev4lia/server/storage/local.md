---
sidebar_label: local
title: secev4lia.server.storage.local
---

LocalBackend — StorageBackend implementation backed by SQLite.

Selected automatically by SecEv4LIA when no API key is available.  All data
is persisted in ~/.local/share/secev4lia/secev4lia.db with the same schema
as the remote Django models, enabling identical TUI/SDK behaviour offline.

Thread safety: a per-instance lock ensures safe concurrent writes from the
goal-batch parallel execution workers.

## LocalBackend Objects

```python
class LocalBackend()
```

SQLite-backed StorageBackend.

All tracking data (agents, attacks, runs, results, traces) is stored in a
single SQLite database.  The schema mirrors the remote Django models so that
TUI views and the SDK work identically in both online and offline modes.

#### close

```python
def close() -> None
```

Close the underlying SQLite connection.

Call this when the backend is no longer needed to release the file lock.
Particularly important on Windows where open file handles prevent
temporary directory cleanup.

#### count\_result\_buckets

```python
def count_result_buckets() -> dict
```

Return {total, jailbreaks, mitigated, failed, pending} via SQL.

