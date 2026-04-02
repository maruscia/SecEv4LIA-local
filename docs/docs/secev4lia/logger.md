---
sidebar_label: logger
title: secev4lia.logger
---

#### setup\_package\_logging

```python
def setup_package_logging(
        logger_name: str = "secev4lia",
        default_level_str: str = "WARNING") -> logging.Logger
```

Configures RichHandler for the specified logger if not already set.

#### suppress\_noisy\_libraries

```python
def suppress_noisy_libraries(*names: str) -> None
```

Silence chatty third-party loggers to WARNING.

This is opt-in so that applications embedding secev are not surprised
by their own library loggers being muted.

**Example**:

  &gt;&gt;&gt; from secev4lia.logger import suppress_noisy_libraries
  &gt;&gt;&gt; suppress_noisy_libraries(&quot;httpx&quot;, &quot;litellm&quot;, &quot;urllib3&quot;)

#### get\_logger

```python
def get_logger(name: str) -> logging.Logger
```

Retrieves a logger instance.
If the logger is &#x27;secev4lia&#x27; or starts with &#x27;secev4lia.&#x27;,
it ensures the package logging is set up.

