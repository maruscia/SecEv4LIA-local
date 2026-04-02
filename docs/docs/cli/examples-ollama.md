---
sidebar_position: 5
title: "Examples: Ollama Demo"
---

# Ollama Examples Demo

The `secev examples ollama` command launches a ready-to-run TUI demo using a local Ollama model.
It preconfigures a small attack scenario and starts the TUI with auto-execution enabled.

## Prerequisites

- Ollama installed and in your PATH
- Ollama server running: `ollama serve`
- Required models available locally (the CLI will prompt and pull missing models)
- TUI dependencies installed: `uv add textual`

## Run the demo

```bash
secev examples ollama
```

The CLI will:
1. Check that the Ollama server is reachable.
2. Validate required models from the demo config.
3. Open the TUI and run the demo automatically.

## What it runs

The demo configuration lives in:
- `examples/ollama/demo.py`

Key fields (edit these to customize the run):
- Target model (`TARGET_MODEL`)
- Attack configuration (`attack_config`)
- Goals and dataset slice

## Troubleshooting

- **Ollama not running**: start it with `ollama serve`.
- **Model missing**: the CLI will run `ollama run <model> ping` to pull it.
- **TUI dependency missing**: install with `uv add textual` or `pip install textual`.
