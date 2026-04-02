# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
TUI Widgets

Reusable Textual widgets for the SecEv4LIA TUI interface.
"""

from secev4lia.cli.tui.widgets.actions import AgentActionsViewer
from secev4lia.cli.tui.widgets.logs import AttackLogViewer

__all__ = ["AttackLogViewer", "AgentActionsViewer"]
