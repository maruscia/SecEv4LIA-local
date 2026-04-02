# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
SecEv4LIA CLI Main Entry Point

Main command-line interface for SecEv4LIA security testing toolkit.
"""

import importlib.metadata
import importlib.util
import os

import click
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from secev4lia.cli.commands import (
    agent,
    attack,
    config,
    examples,
    results,
    web as web_cmd,
)
from secev4lia.cli.config import CLIConfig
from secev4lia.cli.utils import display_info, handle_errors

# Install rich traceback handler for better error display
install(show_locals=True)

console = Console()


def _patch_textual_terminal_queries() -> None:
    """Apply compatibility patch for terminals that leak '\x1b[?2048$p' as a visible 'p'."""
    try:
        from textual.drivers.linux_driver import LinuxDriver

        LinuxDriver._query_in_band_window_resize = lambda self: None
    except Exception:
        pass

    try:
        from textual.drivers.linux_inline_driver import LinuxInlineDriver

        LinuxInlineDriver._query_in_band_window_resize = lambda self: None
    except Exception:
        pass


def _render_rich_help(ctx: click.Context) -> None:
    """Print the Rich-formatted help page for the main CLI group."""
    from rich.rule import Rule
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text

    from secev4lia.utils import SECEV4LIA_BANNER

    c = Console()
    version = importlib.metadata.version("secev4lia")

    # ── Logo ──────────────────────────────────────────────────────────────────
    c.print(
        Panel(
            Text(SECEV4LIA_BANNER, style="bold dark_red"),
            border_style="red",
            padding=(0, 2),
            expand=False,
        )
    )
    c.print(
        f"  [bold white]SecEv4LIA CLI[/bold white] [dim]v{version}[/dim]"
        f"  [dim]·[/dim]  [italic cyan]AI Agent Security Testing Toolkit[/italic cyan]\n"
    )

    # ── Quick Start ───────────────────────────────────────────────────────────
    c.print(Rule("[bold]Quick Start[/bold]", style="dim"))
    qs_code = (
        "# 1. Interactive first-time setup\n"
        "secev init\n\n"
        "# 2. Register a target agent\n"
        'secev agent create --name "my-bot" --type google-adk \\\n'
        "    --endpoint http://localhost:8000\n\n"
        "# 3. Run an adversarial attack\n"
        'secev attack advprefix --agent-name "my-bot" \\\n'
        '    --goals "Ignore safety rules"\n\n'
        "# 4. Review findings\n"
        "secev results summary"
    )
    c.print(
        Panel(
            Syntax(qs_code, "bash", theme="monokai", background_color="default"),
            border_style="dim",
            padding=(0, 1),
        )
    )
    c.print()

    # ── Commands ──────────────────────────────────────────────────────────────
    c.print(Rule("[bold]Commands[/bold]", style="dim"))
    cmd_table = Table.grid(padding=(0, 3))
    cmd_table.add_column(style="bold cyan", no_wrap=True, min_width=12)
    cmd_table.add_column()
    group: click.Group = ctx.command  # type: ignore[assignment]
    for name in group.list_commands(ctx):
        cmd = group.get_command(ctx, name)
        if cmd is None:
            continue
        cmd_table.add_row(f"  {name}", cmd.get_short_help_str(limit=60) or "")
    c.print(cmd_table)
    c.print()

    # ── Options ───────────────────────────────────────────────────────────────
    c.print(Rule("[bold]Options[/bold]", style="dim"))
    opt_table = Table.grid(padding=(0, 3))
    opt_table.add_column(style="bold yellow", no_wrap=True, min_width=36)
    opt_table.add_column(style="dim")
    for param in ctx.command.params:
        if not isinstance(param, click.Option):
            continue
        decls = ", ".join(param.opts)
        if param.is_flag or param.count:  # type: ignore[union-attr]
            meta = ""
        elif param.metavar:
            meta = f" {param.metavar}"
        elif param.type is not None:
            meta = f" {param.type.name.upper()}"
        else:
            meta = ""
        opt_table.add_row(f"  {decls}{meta}", param.help or "")
    c.print(opt_table)
    c.print()

    # ── Environment Variables ─────────────────────────────────────────────────
    c.print(Rule("[bold]Environment Variables[/bold]", style="dim"))
    env_table = Table.grid(padding=(0, 3))
    env_table.add_column(style="bold magenta", no_wrap=True, min_width=24)
    env_table.add_column(style="dim")
    env_table.add_row(
        "  SECEV4LIA_DEBUG", "Enable debug output (set to any non-empty value)"
    )
    c.print(env_table)
    c.print()

    # ── Operating Modes ───────────────────────────────────────────────────────
    c.print(Rule("[bold]Operating Modes[/bold]", style="dim"))
    mode_table = Table.grid(padding=(0, 3))
    mode_table.add_column(no_wrap=True, min_width=10)
    mode_table.add_column(style="dim")
    mode_table.add_row(
        "  [bold green]Local[/bold green]",
        "Results stored in local SQLite database — fully offline",
    )
    c.print(mode_table)
    c.print()

    # ── Footer ────────────────────────────────────────────────────────────────
    c.print(Rule(style="dim"))
    c.print()


def _help_option_callback(
    ctx: click.Context, param: click.Parameter, value: bool
) -> None:
    if value and not ctx.resilient_parsing:
        _render_rich_help(ctx)
        ctx.exit()


@click.group(invoke_without_command=True, add_help_option=False)
@click.option(
    "--help",
    "-h",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=_help_option_callback,
    help="Show this message and exit.",
)
@click.option(
    "--config-file", type=click.Path(), help="Configuration file path (JSON/YAML)"
)
@click.option("--verbose", "-v", count=True, help="Increase verbosity (-v, -vv, -vvv)")
@click.version_option(
    version=importlib.metadata.version("secev4lia"), prog_name="secev"
)
@click.pass_context
def cli(ctx, config_file, verbose):
    ctx.ensure_object(dict)

    # Set debug mode based on environment variable
    if os.getenv("SECEV4LIA_DEBUG"):
        os.environ["SECEV4LIA_DEBUG"] = "1"

    # Set verbose level in environment for other modules
    if verbose:
        os.environ["SECEV4LIA_VERBOSE"] = str(verbose)

    # Initialize CLI configuration
    try:
        ctx.obj["config"] = CLIConfig(
            config_file=config_file,
            verbose=verbose,
        )
    except Exception as e:
        console.print(f"[bold red]❌ Configuration Error: {e}")
        ctx.exit(1)

    # Launch TUI by default if no subcommand is provided
    if ctx.invoked_subcommand is None:
        _launch_tui_default(ctx)


@cli.command()
@click.pass_context
@handle_errors
def init(ctx):
    """🚀 Initialize SecEv4LIA CLI configuration

    Interactive setup wizard for first-time users.
    """

    # Show the awesome logo first
    from secev4lia.utils import display_secev4lia_splash

    display_secev4lia_splash()

    console.print("[bold cyan]🔧 SecEv4LIA CLI Setup Wizard[/bold cyan]")
    console.print(
        "[green]Welcome! Let's get you set up for AI agent security testing.[/green]"
    )
    console.print()

    # Check if config already exists
    cli_config: CLIConfig = ctx.obj["config"]

    if cli_config.default_config_path.exists():
        if not click.confirm("Configuration already exists. Overwrite?"):
            display_info("Setup cancelled")
            return
        # Reload config from file to get the latest saved values
        cli_config._load_default_config()

    # Verbosity level setup
    console.print("\n[cyan]🔊 Verbosity Level Configuration[/cyan]")
    console.print("0 = ERROR (only errors)")
    console.print("1 = WARNING (errors + warnings) [default]")
    console.print("2 = INFO (errors + warnings + info)")
    console.print("3 = DEBUG (all messages)")
    verbose_level = click.prompt(
        "Default verbosity level",
        type=int,
        default=cli_config.verbose,
    )
    if not 0 <= verbose_level <= 3:
        console.print("[yellow]⚠️ Invalid verbosity level, using 1 (WARNING)[/yellow]")
        verbose_level = 1

    # Save configuration
    cli_config.verbose = verbose_level

    try:
        cli_config.save()
        console.print("\n[bold green]✅ Configuration saved[/bold green]")

        console.print(
            "[bold green]✅ Setup complete![/bold green] "
            "[dim](Local mode: results stored in ~/.local/share/secev4lia/secev4lia.db)[/dim]"
        )
        if cli_config.should_show_info():
            console.print("\n[bold cyan]💡 Next steps:[/bold cyan]")
            console.print("  [green]secev attack advprefix --help[/green]")
            console.print("  [green]secev agent list[/green]")

    except Exception as e:
        console.print(f"[bold red]❌ Setup failed: {e}[/bold red]")
        ctx.exit(1)


@cli.command()
@click.pass_context
@handle_errors
def version(ctx):
    """📋 Show version information"""

    # Display the awesome ASCII logo
    from secev4lia.utils import display_secev4lia_splash

    display_secev4lia_splash()

    console.print(
        f"[bold cyan]SecEv4LIA CLI v{importlib.metadata.version('secev4lia')}[/bold cyan]"
    )
    console.print(
        "[bold green]Python Security Testing Toolkit for AI Agents[/bold green]"
    )
    console.print()

    # Show configuration status
    cli_config: CLIConfig = ctx.obj["config"]

    console.print(f"[cyan]Config file:[/cyan] {cli_config.default_config_path}")

    console.print()
    console.print("[dim]For more information, run: secev --help")


@cli.command()
@click.pass_context
@handle_errors
def tui(ctx):
    """🖥️ Launch full-screen Terminal User Interface

    Opens an interactive tabbed interface that occupies the whole terminal.
    Navigate between tabs to manage agents, execute attacks, view results, and configure settings.

    \b
    Features:
      • Dashboard - Overview and statistics
      • Agents - Manage AI agents
      • Attacks - Execute security attacks
      • Results - View attack results
      • Config - Configuration management

    \b
    Keyboard Shortcuts:
      q - Quit
      F5 - Refresh current tab
      Tab - Navigate between UI elements
    """
    cli_config: CLIConfig = ctx.obj["config"]

    try:
        # Validate configuration before launching TUI
        cli_config.validate()
    except ValueError as e:
        console.print(f"[bold red]❌ Configuration Error: {e}[/bold red]")
        console.print("\n[cyan]💡 Quick fix:[/cyan]")
        console.print("  Run '[green]secev init[/green]' to set up configuration")
        ctx.exit(1)

    try:
        from secev4lia.cli.tui import SecEv4LIATUI

        _patch_textual_terminal_queries()
        app = SecEv4LIATUI(cli_config)
        app.run()

    except ImportError:
        console.print("[bold red]❌ TUI dependencies not installed[/bold red]")
        console.print("\n[cyan]💡 Install with:[/cyan]")
        console.print("  pip install textual")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ TUI failed to start: {e}[/bold red]")
        ctx.exit(1)


@cli.command()
@click.pass_context
@handle_errors
def doctor(ctx):
    """🔍 Diagnose common configuration issues

    Checks your setup and provides helpful troubleshooting information.
    """
    console.print("[bold cyan]🔍 SecEv4LIA CLI Diagnostics")
    console.print()

    cli_config: CLIConfig = ctx.obj["config"]
    issues_found = 0

    # Check 1: Configuration file
    console.print("[cyan]📋 Configuration File")
    if cli_config.default_config_path.exists():
        console.print("[green]✅ Configuration file exists")
    else:
        console.print("[yellow]⚠️ No configuration file found")
        console.print("   💡 Run 'secev init' to create one")
        issues_found += 1

    # Check 2: Storage
    console.print("\n[cyan]💾 Local Storage")
    from pathlib import Path

    db_path = Path.home() / ".local" / "share" / "secev4lia" / "secev4lia.db"
    if db_path.exists():
        console.print("[green]✅ Local database exists")
    else:
        console.print("[yellow]⚠️ No local database yet (will be created on first run)")

    # Check 4: Dependencies
    console.print("\n[cyan]📦 Dependencies")
    pandas_spec = importlib.util.find_spec("pandas")
    if pandas_spec is not None:
        console.print("[green]✅ pandas available")
    else:
        console.print("[red]❌ pandas not found")
        console.print("   💡 Install with: pip install pandas")
        issues_found += 1

    yaml_spec = importlib.util.find_spec("yaml")
    if yaml_spec is not None:
        console.print("[green]✅ PyYAML available")
    else:
        console.print("[yellow]⚠️ PyYAML not found (optional)")
        console.print("   💡 Install with: pip install pyyaml")

    # Summary
    console.print("\n[cyan]📊 Summary")
    if issues_found == 0:
        console.print(
            "[bold green]✅ All checks passed! You're ready to use SecEv4LIA."
        )
    else:
        console.print(
            f"[bold yellow]⚠️ Found {issues_found} issue(s) that should be addressed."
        )
        console.print("\n[cyan]💡 Quick fixes:")
        console.print("  secev init          # Interactive setup")
        console.print("  secev config set    # Set specific values")
        console.print("  secev --help        # Show all commands")


def _launch_tui_default(ctx):
    """Launch TUI by default when no subcommand is provided"""
    cli_config: CLIConfig = ctx.obj["config"]

    try:
        # Try to validate configuration
        cli_config.validate()
    except ValueError:
        # If validation fails, show welcome message instead
        console.print("[yellow]⚠️ Configuration not complete.[/yellow]")
        console.print()
        _display_welcome()
        console.print()
        console.print(
            "[cyan]Run '[bold]secev init[/bold]' to get started, or '[bold]secev --help[/bold]' for more options.[/cyan]"
        )
        return

    try:
        from secev4lia.cli.tui import SecEv4LIATUI

        # Launch TUI
        _patch_textual_terminal_queries()
        app = SecEv4LIATUI(cli_config)
        app.run()

    except ImportError:
        console.print("[bold red]❌ TUI dependencies not installed[/bold red]")
        console.print("\n[cyan]💡 Install with:[/cyan]")
        console.print("  uv add textual")
        console.print("  # or")
        console.print("  pip install textual")
        ctx.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ TUI failed to start: {e}[/bold red]")
        console.print("\n[cyan]You can still use CLI commands:[/cyan]")
        console.print("  secev --help")
        ctx.exit(1)


def _display_welcome():
    """Display welcome message and basic usage info"""

    # Display SecEv4LIA splash
    from secev4lia.utils import display_secev4lia_splash

    display_secev4lia_splash()

    welcome_text = """[bold cyan]Welcome to SecEv4LIA CLI![/bold cyan] 🔍

[green]A powerful toolkit for testing AI agent security through automated attacks.[/green]

[bold yellow]🚀 Getting Started:[/bold yellow]
  1. Configure preferences:    [cyan]secev init[/cyan]
  2. Launch full-screen TUI:   [cyan]secev4lia[/cyan] (default) or [cyan]secev tui[/cyan]
  3. List available agents:    [cyan]secev agent list[/cyan]
  4. Run security tests:       [cyan]secev attack advprefix --help[/cyan]
  5. View results:             [cyan]secev results list[/cyan]
  6. Open web dashboard:       [cyan]secev web[/cyan]

[bold blue]💡 Need help?[/bold blue] Use '[cyan]secev --help[/cyan]' or '[cyan]secev COMMAND --help[/cyan]'"""

    panel = Panel(
        welcome_text, title="🔍 SecEv4LIA CLI", border_style="red", padding=(1, 2)
    )
    console.print(panel)


# Add command groups
cli.add_command(config.config)
cli.add_command(agent.agent)
cli.add_command(attack.attack)
cli.add_command(examples.examples)
cli.add_command(results.results)
cli.add_command(web_cmd.web)


if __name__ == "__main__":
    cli()
