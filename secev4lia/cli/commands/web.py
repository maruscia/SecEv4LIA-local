# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
``secev web`` — web dashboard command.

Starts a NiceGUI server that reads from the local SQLite backend
and serves the dashboard at http://<host>:<port>/.
"""

import click
from rich.console import Console

console = Console()


@click.command("web")
@click.option(
    "--host",
    default="127.0.0.1",
    show_default=True,
    help="Host to bind the dashboard server.",
)
@click.option(
    "--port",
    default=7860,
    show_default=True,
    type=int,
    help="Port to run the dashboard server on.",
)
@click.option(
    "--db-path",
    default=None,
    help="SQLite database path (default: ~/.local/share/secev4lia/secev4lia.db).",
)
@click.option(
    "--no-browser",
    is_flag=True,
    default=False,
    help="Do not auto-open a browser tab on start.",
)
@click.pass_context
def web(ctx, host, port, db_path, no_browser):
    """🌐 Launch the local web dashboard.

    Starts a local web server that serves a full-featured security testing
    dashboard backed by the local SQLite database.

    \b
    Examples:
      secev web                    # http://127.0.0.1:7860 (default)
      secev web --port 8080        # custom port
      secev web --host 0.0.0.0     # expose on all interfaces
      secev web --no-browser       # skip opening a browser tab
    """
    try:
        from flask import Flask  # noqa: F401
    except ImportError:
        console.print(
            "[bold red]❌ Flask is required for the web dashboard.[/bold red]"
        )
        console.print("\n[cyan]Install with:[/cyan]")
        console.print("  pip install 'secev4lia[web]'")
        console.print("  # or")
        console.print("  pip install flask")
        ctx.exit(1)
        return

    from secev4lia.server.dashboard import create_app
    from secev4lia.server.storage.local import LocalBackend

    backend = LocalBackend(db_path=db_path)

    # ── Create app ────────────────────────────────────────────────────────
    app = create_app(backend=backend)

    url = f"http://{host}:{port}"

    console.print()
    console.print("[bold]🌐  SecEv4LIA Dashboard[/bold]")
    console.print(f"    [cyan]→  {url}[/cyan]")
    console.print("    Mode : [cyan]local[/cyan]")
    resolved_db = db_path or "~/.local/share/secev4lia/secev4lia.db"
    console.print(f"    DB   : [dim]{resolved_db}[/dim]")
    console.print()
    console.print("    Press [bold]Ctrl+C[/bold] to stop.\n")

    # ── Free port if still occupied by a previous instance ──────────────────
    import signal
    import socket

    def _free_port(host: str, port: int) -> None:
        """Kill any process listening on host:port so we can bind cleanly."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((host, port)) != 0:
                return  # port already free
        try:
            import subprocess

            out = subprocess.check_output(
                ["lsof", "-t", "-i", f"TCP:{port}", "-sTCP:LISTEN"],
                text=True,
            ).strip()
            for pid in out.splitlines():
                pid = pid.strip()
                if pid.isdigit():
                    console.print(
                        f"[yellow]Killing previous process on port {port} (PID {pid})…[/yellow]"
                    )
                    import os

                    os.kill(int(pid), signal.SIGTERM)
            import time

            time.sleep(0.5)
        except Exception:
            pass

    _free_port(host, port)

    # ── Serve (NiceGUI handles browser auto-open via show=...) ──────────────
    app.run(host=host, port=port, show=not no_browser)
