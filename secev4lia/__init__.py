# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""A client library for SecEv4LIA — AI Agent Security Testing"""

from .agent import SecEv4LIA
from .server.client import AuthenticatedClient, Client
from .logger import setup_package_logging
from .router.types import AgentTypeEnum
from .server.storage.base import StorageBackend
from .server.storage.local import LocalBackend
from .server.storage.remote import RemoteBackend

# Configure RichHandler for all secev4lia.* loggers on first import.
setup_package_logging()

__all__ = (
    "AgentTypeEnum",
    "AuthenticatedClient",
    "Client",
    "SecEv4LIA",
    "LocalBackend",
    "RemoteBackend",
    "StorageBackend",
)
