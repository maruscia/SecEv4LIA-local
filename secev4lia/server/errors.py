# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Re-export secev errors for server/api relative imports.

The auto-generated server/api/ code uses ``from ... import errors`` which
resolves to this module (secev4lia.server.errors) when the api/ tree lives
under server/.  All symbols are forwarded from the canonical errors module so
callers that reference e.g. ``errors.UnexpectedStatus`` continue to work.
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
