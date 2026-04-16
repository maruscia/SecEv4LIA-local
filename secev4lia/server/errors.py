# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Compatibility re-export of canonical SecEv4LIA errors.

All symbols are forwarded from ``secev4lia.errors`` so imports that resolve
through ``secev4lia.server.errors`` continue to work.
"""

from secev4lia.errors import (  # noqa: F401
    ApiError,
    SecEv4LIAError,
    UnexpectedStatus,
    UnexpectedStatusError,
)

__all__ = [
    "ApiError",
    "SecEv4LIAError",
    "UnexpectedStatus",
    "UnexpectedStatusError",
]
