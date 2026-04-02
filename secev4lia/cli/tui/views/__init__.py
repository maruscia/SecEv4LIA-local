# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
TUI Views

Tab views/panels for the SecEv4LIA TUI application.
Each view represents a different functional area of the interface.
"""

from secev4lia.cli.tui.views.agents import AgentsTab
from secev4lia.cli.tui.views.attacks import AttacksTab
from secev4lia.cli.tui.views.config import ConfigTab
from secev4lia.cli.tui.views.results import ResultsTab

__all__ = ["AgentsTab", "AttacksTab", "ConfigTab", "ResultsTab"]

"""
TUI Tabs Module

Individual tab implementations for the SecEv4LIA TUI.
"""
