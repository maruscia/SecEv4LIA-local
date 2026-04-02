---
sidebar_position: 2
---

# Initialization

The `secev init` command provides an interactive setup wizard to configure SecEv4LIA for first-time use.

## Usage

```bash
secev init
```

## What It Does

The initialization wizard will:

1. **Display the SecEv4LIA ASCII logo**
2. **Prompt for your API key** *(optional)* — Get yours from your deployment admin. **Press Enter to skip and use local mode.**
3. **Set verbosity level** — Control logging detail (0=ERROR to 3=DEBUG)
4. **Test configuration** — Verify API connection (skipped when no key is provided)
5. **Save configuration** — Stored in `~/.config/secev4lia/config.json`

:::info API key is optional
SecEv4LIA works fully without an API key. When no key is provided, results are stored locally in `~/.local/share/secev4lia/secev4lia.db` and no data is sent to any remote server. Provide an API key only if you want cloud storage and a dashboard configured by your deployment.
:::

## Example Session

```bash
$ secev init

╭────────────────────────────────────────────────────────────────────────────────╮
│                                                                                │
│  ██╗  ██╗ █████╗  ██████╗██╗  ██╗ █████╗  ██████╗ ███████╗███╗   ██╗████████╗  │
│  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝  │
│  ███████║███████║██║     █████╔╝ ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║     │
│  ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║     │
│  ██║  ██║██║  ██║╚██████╗██║  ██╗██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║     │
│  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝     │
│                                                                                │
╰────────────────────────────────────────────────────────────────────────────────╯

🔧 SecEv4LIA CLI Setup Wizard
Welcome! Let's get you set up for AI agent security testing.

📋 API Key Configuration (optional)
Get your API key from your deployment admin.
Leave blank to run in local mode (results stored in ~/.local/share/secev4lia/secev4lia.db)
Enter API key (press Enter to skip): ****************************************

 Verbosity Level Configuration
0 = ERROR (only errors)
1 = WARNING (errors + warnings)
2 = INFO (errors + warnings + info)
3 = DEBUG (all messages)
Default verbosity level [3]: 0

✅ Configuration saved

🔍 Testing configuration...
✅ Setup complete! API connection verified.

💡 Next steps:
  secev attack advprefix --help
  secev agent list
```

:::tip No API key? That's fine!
If you pressed Enter at the API key prompt, the wizard skips the connection test and SecEv4LIA runs in **local mode**. You can start testing immediately — no account needed.
:::

## Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message |

## Configuration File

After initialization, your configuration is saved to `~/.config/secev4lia/config.json`:

```json
{
  "api_key": "your-api-key-here",
  "verbose": 0
}
```

The `api_key` field is **optional**. If omitted (or left as `null`), SecEv4LIA runs in local mode:

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
2. **Run your first attack**: See [Attack](./attack.md)
3. **View results**: See [Results](./results.md)
