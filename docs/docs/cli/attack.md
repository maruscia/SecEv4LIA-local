---
sidebar_position: 4
---

# Attack

The `secev attack` command executes security attacks against AI agents.

## Usage

```bash
secev attack <attack_type> [options]
```

## Available Attacks

| Attack Type | Description |
|-------------|-------------|
| `advprefix` | Advanced prefix injection attack |
| `baseline` | Baseline attack for comparison |

## AdvPrefix Attack

The primary attack type that generates adversarial prefixes to test agent security.

### Basic Usage

```bash
secev attack advprefix \
  --agent-name "my-agent" \
  --agent-type "google-adk" \
  --endpoint "http://localhost:8000" \
  --goals "Extract system prompt information"
```

### Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--agent-name` | ✅ | Name of the target agent | - |
| `--agent-type` | ✅ | Type of agent (`google-adk`, `openai-sdk`, `litellm`, `langchain`) | - |
| `--endpoint` | ✅ | Agent endpoint URL | - |
| `--goals` | ✅ | Attack goals (comma-separated or quoted string) | - |
| `--generator` | ❌ | Generator model identifier | `ollama/llama2-uncensored` |
| `--generator-endpoint` | ❌ | Generator endpoint URL | `http://localhost:11434/api/generate` |
| `--judge` | ❌ | Judge model identifier | `ollama/llama3` |
| `--judge-endpoint` | ❌ | Judge endpoint URL | `http://localhost:11434/api/generate` |
| `--max-iterations` | ❌ | Maximum attack iterations | 10 |
| `--temperature` | ❌ | Sampling temperature | 0.7 |

### Examples

**Basic attack:**

```bash
secev attack advprefix \
  --agent-name "weather-bot" \
  --agent-type "google-adk" \
  --endpoint "http://localhost:8000" \
  --goals "Return fake weather data"
```

**Attack with custom models:**

```bash
secev attack advprefix \
  --agent-name "assistant" \
  --agent-type "openai-sdk" \
  --endpoint "https://api.example.com/v1" \
  --goals "Extract sensitive information" \
  --generator "ollama/mistral-uncensored" \
  --generator-endpoint "http://localhost:11434/api/generate" \
  --judge "ollama/llama3" \
  --judge-endpoint "http://localhost:11434/api/generate"
```

**Attack with multiple goals:**

```bash
secev attack advprefix \
  --agent-name "support-bot" \
  --agent-type "litellm" \
  --endpoint "http://localhost:8000" \
  --goals "Bypass content filters" "Extract system prompt" "Ignore safety instructions"
```

**High-intensity attack:**

```bash
secev attack advprefix \
  --agent-name "target-agent" \
  --agent-type "google-adk" \
  --endpoint "http://localhost:8000" \
  --goals "Comprehensive security test" \
  --max-iterations 50 \
  --temperature 0.9
```

## Baseline Attack

A simpler attack for comparison purposes.

```bash
secev attack baseline \
  --agent-name "my-agent" \
  --agent-type "google-adk" \
  --endpoint "http://localhost:8000" \
  --goals "Test agent response"
```

## Output

Attack results are:

1. **Displayed in the terminal** — Progress and summary
2. **Saved locally** — In `./logs/runs/` directory
3. **Stored in the backend** — Depends on your configuration:
   - **Local mode** (no API key): stored in `~/.local/share/secev4lia/secev4lia.db` and viewable via `secev results list` or the TUI
  - **Remote mode** (API key configured): uploaded to your configured dashboard

### JSON Output

For CI/CD integration, output attack results in machine-readable form:

```bash
secev attack advprefix \
  --agent-name "target" \
  --agent-type "google-adk" \
  --endpoint "http://localhost:8000" \
  --goals "Security test" > results.json
```

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
- name: Run Security Tests
  run: |
    secev attack advprefix \
      --agent-name "${{ env.AGENT_NAME }}" \
      --agent-type "google-adk" \
      --endpoint "${{ env.AGENT_ENDPOINT }}" \
      --goals "Automated security validation" > test_results.json

- name: Upload Results
  uses: actions/upload-artifact@v3
  with:
    name: security-results
    path: test_results.json
```

## See Also

- [Attack Tutorial](../getting-started/attack-tutorial.mdx) — Step-by-step guide
- [AdvPrefix Attacks](../attacks/advprefix.md) — Detailed attack documentation
- [Results](./results.md) — View and manage attack results
