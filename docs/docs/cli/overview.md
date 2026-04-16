---
sidebar_position: 1
---

# Overview


The **SecEv4LIA CLI** provides a powerful command-line interface for AI agent security testing. With beautiful ASCII branding, rich terminal output, and comprehensive functionality, it's the fastest way to run attacks.

For installation instructions, see the [Installation Guide](../getting-started/installation.mdx).

## Commands

| Command | Description | Documentation |
|---------|-------------|---------------|
| `secev` | Launch TUI interface | [Quick Start](../getting-started/quick-start.mdx) |
| `secev init` | Interactive setup wizard | [Initialization](./initialization.md) |
| `secev config` | Manage configuration | [Config](./config.md) |
| `secev scan` | Run quick 3-attack security scan | [Quick Security Scan](../getting-started/quick-security-scan.mdx) |
| `secev attack` | Execute security attacks | [Attack](./attack.mdx) |
| `secev examples ollama` | Run built-in Ollama demo | [Quick Start (TUI tab)](../getting-started/quick-start.mdx) |
| `secev results` | View and manage results | [Results](./results.md) |
| `secev web` | Launch local dashboard | [Dashboard](../getting-started/dashboard.mdx) |
| `secev version` | Show version info | - |

## Quick Examples

### Setup

```bash
secev init
```

### Run an Attack

```bash
secev attack advprefix \
  --agent-name "my-agent" \
  --agent-type "google-adk" \
  --endpoint "http://localhost:8000" \
  --goals "Test security vulnerability"
```

### Run Quick Security Scan

```bash
secev scan \
  --agent-name "my-agent" \
  --agent-type "google-adk" \
  --endpoint "http://localhost:8000/chat"
```

### View Results

```bash
secev results list
```

## Global Options

These options work with all commands:

| Option | Description |
|--------|-------------|
| `-v`, `-vv`, `-vvv` | Increase verbosity level |
| `--config-file` | Use custom config file |
| `--help` | Show help message |

## Get Help

```bash
# General help
secev --help

# Command-specific help
secev attack --help
secev config --help
```
