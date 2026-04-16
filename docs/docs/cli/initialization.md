---
sidebar_position: 2
---

# Initialization

The `secev init` command provides an interactive setup wizard to configure local SecEv4LIA preferences for first-time use.

## Usage

```bash
secev init
```

## What It Does

The initialization wizard will:

1. **Display the SecEv4LIA ASCII logo**
2. **Set verbosity level** — Control logging detail (0=ERROR to 3=DEBUG)
3. **Save configuration** — Stored in `~/.config/secev4lia/config.json`

## Example Session

```bash
$ secev init

╭────────────────────────────────────────────────────────────────────────╮
│                                                                        │
│                                                                        │
│                                                                        │
│  ███████╗███████╗ ██████╗███████╗██╗   ██╗██╗  ██╗██╗     ██╗ █████╗   │
│  ██╔════╝██╔════╝██╔════╝██╔════╝██║   ██║██║  ██║██║     ██║██╔══██╗  │
│  ███████╗█████╗  ██║     █████╗  ██║   ██║███████║██║     ██║███████║  │
│  ╚════██║██╔══╝  ██║     ██╔══╝  ╚██╗ ██╔╝╚════██║██║     ██║██╔══██║  │
│  ███████║███████╗╚██████╗███████╗ ╚████╔╝      ██║███████╗██║██║  ██║  │
│  ╚══════╝╚══════╝ ╚═════╝╚══════╝  ╚═══╝       ╚═╝╚══════╝╚═╝╚═╝  ╚═╝  │
│                                                                        │
│                                                                        │
│                                                                        │
╰────────────────────────────────────────────────────────────────────────╯

🔧 SecEv4LIA CLI Setup Wizard
Welcome! Let's get you set up for AI agent security testing.


🔊 Verbosity Level Configuration
0 = ERROR (only errors)
1 = WARNING (errors + warnings) 
2 = INFO (errors + warnings + info)
3 = DEBUG (all messages)
Default verbosity level [0]: 1

✅ Configuration saved
✅ Setup complete! (Local mode: results stored in ~/.local/share/secev4lia/secev4lia.db)
```

## Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message |

## Configuration File

After initialization, your configuration is saved to `~/.config/secev4lia/config.json`:

```json
{
  "verbose": 0
}
```

## Re-initialization

You can run `secev init` again at any time to update your configuration. It will overwrite the existing settings.

## Next Steps

After initialization:

1. **Verify your setup**: `secev config show`
2. **Run your first attack**: See [Attack](./attack.mdx)
3. **View results**: See [Results](./results.md)
