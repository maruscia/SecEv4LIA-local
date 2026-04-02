# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
SecEv4LIA Dashboard

A lightweight, self-hosted web dashboard that reads directly from the local
SQLite storage (or a remote backend when an API key is configured).

Usage:
    from secev4lia.server.dashboard import create_app

    app = create_app()          # uses ~/.local/share/secev4lia/secev4lia.db
    app.run(host="127.0.0.1", port=7860)   # starts NiceGUI server

Or via the CLI:
    secev web
    secev web --port 8080 --no-browser
"""

from .app import create_app

__all__ = ("create_app",)
