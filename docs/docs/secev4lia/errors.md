---
sidebar_label: errors
title: secev4lia.errors
---

Contains shared errors types that can be raised from API functions

## UnexpectedStatus Objects

```python
class UnexpectedStatus(Exception)
```

Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True

## SecEv4LIAError Objects

```python
class SecEv4LIAError(Exception)
```

Base exception class for SecEv4LIA errors

## ApiError Objects

```python
class ApiError(SecEv4LIAError)
```

Raised when an API call fails

