# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Configuration Commands

Manage SecEv4LIA CLI configuration settings.
"""

import click
from rich.console import Console
from rich.table import Table

from secev4lia.cli.config import CLIConfig
from secev4lia.cli.utils import display_info, display_success, handle_errors

console = Console()


@click.group()
def config():
    """🔧 Manage SecEv4LIA CLI configuration"""
    pass


@config.command()
@click.option(
    "--verbose",
    type=str,
    help="Default verbosity level: 0/error, 1/warning, 2/info, 3/debug",
)
@click.pass_context
@handle_errors
def set(ctx, verbose):
    """Set configuration values"""

    cli_config: CLIConfig = ctx.obj["config"]

    updated = False

    if verbose is not None:
        from secev4lia.cli.config import VERBOSITY_LEVELS, VERBOSITY_NAMES

        try:
            verbose_int = int(verbose)
            if 0 <= verbose_int <= 3:
                cli_config.verbose = verbose_int
                updated = True
                if cli_config.verbose > 0:
                    display_success(
                        f"Verbosity level updated to: {verbose_int} ({VERBOSITY_NAMES[verbose_int]})"
                    )
            else:
                display_info("Verbosity level must be between 0 and 3")
        except ValueError:
            verbose_lower = verbose.lower()
            if verbose_lower in VERBOSITY_LEVELS:
                verbose_int = VERBOSITY_LEVELS[verbose_lower]
                cli_config.verbose = verbose_int
                updated = True
                if cli_config.verbose > 0:
                    display_success(
                        f"Verbosity level updated to: {verbose_int} ({VERBOSITY_NAMES[verbose_int]})"
                    )
            else:
                display_info(
                    f"Invalid verbosity level. Use: 0-3 or {', '.join(VERBOSITY_LEVELS.keys())}"
                )

    if updated:
        cli_config.save()
        display_success("✅ Configuration saved")
    else:
        display_info("No configuration changes made")


@config.command()
@click.pass_context
@handle_errors
def show(ctx):
    """Show current configuration"""

    cli_config: CLIConfig = ctx.obj["config"]

    table = Table(
        title="SecEv4LIA Configuration", show_header=True, header_style="bold cyan"
    )
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Source", style="dim")

    from secev4lia.cli.config import VERBOSITY_NAMES

    verbosity_display = (
        f"{cli_config.verbose} ({VERBOSITY_NAMES.get(cli_config.verbose, 'UNKNOWN')})"
    )
    table.add_row("Verbosity", verbosity_display, "Default/Config")
    table.add_row(
        "Config File", str(cli_config.default_config_path), "Default location"
    )
    table.add_row("Storage", "~/.local/share/secev4lia/secev4lia.db", "Local SQLite")

    console.print(table)

    if cli_config.should_show_info():
        if cli_config.default_config_path.exists():
            display_info(f"Configuration file: {cli_config.default_config_path}")
        else:
            display_info(
                "No configuration file found. Use 'secev config set' to create one."
            )


@config.command()
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
@handle_errors
def reset(ctx, confirm):
    """Reset configuration to defaults"""

    cli_config: CLIConfig = ctx.obj["config"]

    if not confirm:
        if not click.confirm(
            "⚠️ This will reset all configuration to defaults. Continue?"
        ):
            display_info("Configuration reset cancelled")
            return

    if cli_config.default_config_path.exists():
        cli_config.default_config_path.unlink()
        display_success("✅ Configuration reset to defaults")
    else:
        display_info("No configuration file to reset")


@config.command()
@click.pass_context
@handle_errors
def validate(ctx):
    """Validate current configuration"""

    cli_config: CLIConfig = ctx.obj["config"]

    try:
        cli_config.validate()
        display_success("✅ Configuration valid")
    except ValueError as e:
        console.print(f"[red]❌ Configuration validation failed: {e}")
        raise click.ClickException("Configuration validation failed")


@config.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.pass_context
@handle_errors
def import_config(ctx, config_file):
    """Import configuration from a file"""

    from secev4lia.cli.utils import load_config_file

    try:
        config_data = load_config_file(config_file)

        cli_config: CLIConfig = ctx.obj["config"]

        updated_fields = []
        if "verbose" in config_data:
            cli_config.verbose = config_data["verbose"]
            updated_fields.append("Verbosity")

        if updated_fields:
            cli_config.save()
            display_success(f"✅ Configuration imported: {', '.join(updated_fields)}")
            if cli_config.should_show_info():
                display_info(f"Saved to: {cli_config.default_config_path}")
        else:
            display_info("No valid configuration found in file")

    except Exception as e:
        raise click.ClickException(f"Failed to import configuration: {e}")
