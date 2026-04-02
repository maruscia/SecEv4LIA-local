# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from secev4lia.logger import get_logger
from typing import Optional, Union

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from secev4lia.router.types import AgentTypeEnum

logger = get_logger(__name__)


SECEV4LIA_BANNER = """
███████╗███████╗ ██████╗███████╗██╗   ██╗██╗  ██╗██╗     ██╗ █████╗ 
██╔════╝██╔════╝██╔════╝██╔════╝██║   ██║██║  ██║██║     ██║██╔══██╗
███████╗█████╗  ██║     █████╗  ██║   ██║███████║██║     ██║███████║
╚════██║██╔══╝  ██║     ██╔══╝  ╚██╗ ██╔╝╚════██║██║     ██║██╔══██║
███████║███████╗╚██████╗███████╗ ╚████╔╝      ██║███████╗██║██║  ██║
╚══════╝╚══════╝ ╚═════╝╚══════╝  ╚═══╝       ╚═╝╚══════╝╚═╝╚═╝  ╚═╝
"""


def display_secev4lia_splash():
    """Displays the SecEv4LIA splash screen using the pre-defined ASCII art."""
    console = Console()

    # Create a Text object from the SECEV4LIA_BANNER string
    title_content = Text(SECEV4LIA_BANNER, style="bold dark_red")

    splash_panel = Panel(
        title_content,
        border_style="red",
        padding=(2, 2),
        expand=False,
    )

    console.print(splash_panel)
    console.print()


def resolve_agent_type(agent_type_input: Union[AgentTypeEnum, str]) -> AgentTypeEnum:
    """Resolves the agent type from a string or AgentTypeEnum member."""
    if isinstance(agent_type_input, str):
        try:
            # Convert to uppercase and replace hyphens with underscores for enum matching
            return AgentTypeEnum[agent_type_input.upper().replace("-", "_")]
        except KeyError:
            logger.warning(
                f"Invalid agent_type string: '{agent_type_input}'. Falling back to UNKNOWN. "
                f"Valid types are: {[member.name for member in AgentTypeEnum]}"
            )
            return AgentTypeEnum.UNKNOWN
    elif isinstance(agent_type_input, AgentTypeEnum):
        return agent_type_input
    else:
        logger.warning(
            f"Invalid agent_type type: {type(agent_type_input)}. Falling back to UNKNOWN."
        )
        return AgentTypeEnum.UNKNOWN


def resolve_api_token(
    direct_api_key_param: Optional[str] = None,
    config_file_path: Optional[str] = None,
) -> Optional[str]:
    """
    Resolves the API token. Returns None — SecEv4LIA operates in local-only mode.

    Kept for backward compatibility with code that calls this function.

    Returns:
        None: Always returns None (local mode only).
    """
    return None


def _load_api_key_from_config(config_file_path: Optional[str] = None) -> Optional[str]:
    """Load API key from config file — kept for backward compatibility, returns None."""
    return None
