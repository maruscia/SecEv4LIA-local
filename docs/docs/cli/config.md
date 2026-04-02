---
sidebar_position: 3
---

# Config

The `secev config` command allows you to view and manage your SecEv4LIA configuration.

## Commands

### Show Configuration

Display your current configuration:

```bash
secev config show
```

**Example output:**

```
                                SecEv4LIA Configuration
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Setting       ┃ Value                                                          ┃ Source            ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ Storage       │ ~/.local/share/secev4lia/secev4lia.db                          │ Local SQLite      │
│ Verbosity     │ 3 (DEBUG)                                                      │ Default/Config    │
│ Config File   │ /home/user/.config/secev4lia/config.json                       │ Default location  │
└───────────────┴────────────────────────────────────────────────────────────────┴───────────────────┘
```

### Set Configuration

Update individual configuration values:

```bash
# Set verbosity level
secev config set --verbose 2
```

## Storage

SecEv4LIA stores all results locally in a SQLite database:

| Storage | Location | Network |
|---------|----------|---------|
| **Local SQLite** | `~/.local/share/secev4lia/secev4lia.db` | None — fully offline |

The TUI, CLI, SDK, and all attack types work fully offline.

## Configuration Priority

Configuration is loaded in this order (highest to lowest priority):

1. **Command-line arguments** — Override everything
2. **Config file** — `~/.config/secev4lia/config.json`
3. **Environment variables** — Fallback
4. **Default values** — Built-in defaults

## Environment Variables

You can configure SecEv4LIA using environment variables:

| Variable | Required | Description | Example |
|----------|----------|-------------|----------|
| `SECEV4LIA_DEBUG` | ❌ Optional | Enable debug output | `export SECEV4LIA_DEBUG=1` |

**Example:**

```bash
# Just run — SecEv4LIA stores results locally with no configuration required
secev attack advprefix --agent-name "my-agent" --agent-type "ollama" --endpoint "http://localhost:11434" --goals "Test"
```

## Configuration File

Default location: `~/.config/secev4lia/config.json`

```json
{
  "verbose": 0
}
```

### Custom Configuration File

Use a different configuration file:

```bash
secev --config-file ./custom-config.json config show
```

## Verbosity Levels

Control the amount of logging output:

| Level | Name | Description |
|-------|------|-------------|
| 0 | ERROR | Only show errors |
| 1 | WARNING | Show warnings and errors |
| 2 | INFO | Show info, warnings, and errors |
| 3 | DEBUG | Show all messages including debug |

**Command-line override:**

```bash
secev -v config show          # Verbose (INFO)
secev -vv config show         # More verbose (DEBUG)
secev -vvv config show        # Maximum verbosity
```

## Debug Mode

Enable full error tracebacks for troubleshooting:

```bash
export SECEV4LIA_DEBUG=1
secev config show
```
