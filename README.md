<div align="center">
  <img src="docs/static/img/ascii-text-art.svg" alt="SecEv4LIA - AI Agent Security Testing Toolkit" width="100%" />

  <strong>The Open-Source AI Security Red-Team Toolkit</strong>

  <p>Discover vulnerabilities in your AI agents before attackers do.</p>

  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python Version" />
  <img src="https://img.shields.io/badge/license-Apache%202.0-green" alt="License" />
  <img src="https://img.shields.io/codecov/c/github/AISecurityLab/secev4lia" alt="Test Coverage" />
  <img src="https://img.shields.io/github/actions/workflow/status/AISecurityLab/secev4lia/ci.yml" alt="CI Status" />
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv" />
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" />
</div>

## What is SecEv4LIA?

SecEv4LIA is a comprehensive Python SDK and CLI designed to help security researchers, developers, and AI safety practitioners evaluate and strengthen the security of AI agents.

<div align="center">
  <img src="docs/static/gifs/terminal.gif" alt="SecEv4LIA CLI Demo" width="100%" />
  <p><em>Interactive TUI with real-time attack progress and visual reporting.</em></p>
</div>

As AI agents become more powerful and autonomous, they face security challenges that traditional testing tools cannot address:

| Threat | Description |
|--------|-------------|
| **Prompt Injection** | Malicious inputs that hijack agent behavior |
| **Jailbreaking** | Bypassing safety guardrails and content filters |
| **Goal Hijacking** | Manipulating agents to pursue unintended objectives |
| **Tool Misuse** | Exploiting agent capabilities for unauthorized actions |

SecEv4LIA automates testing for these vulnerabilities using research-backed attack techniques, helping you identify and fix security issues before they are exploited.

## Get Started Now

### Quick Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/AISecurityLab/SecEv4LIA.git
```

No API key required: SecEv4LIA works locally out of the box.

### Quick Links

- [Quick Start](docs/docs/getting-started/quick-start.mdx)
- [Installation](docs/docs/getting-started/installation.mdx)
- [CLI Reference](docs/docs/cli/overview.md)
- [Attack Techniques](docs/docs/attacks/index.md)
- [Integrations](docs/docs/agents/index.mdx)

Questions? Join [community discussions](https://github.com/AISecurityLab/secev4lia/discussions) or email ais@ai4i.it.

## Architecture

SecEv4LIA uses a modular pipeline to test agent robustness end-to-end.

| Component | Description |
|-----------|-------------|
| **Attack Engine** | Orchestrates attacks using AdvPrefix, AutoDAN-Turbo, PAIR, TAP, FlipAttack, BoN, h4rm3l, CipherChat, PAP, and Baseline |
| **Generator** | LLM role that creates adversarial prompts to test the target agent |
| **Judge** | LLM role that evaluates whether attacks bypass safety measures |
| **Target Agent** | Your AI agent under test across supported frameworks |
| **Datasets** | Pre-built benchmark presets plus custom HuggingFace/file datasets |

## Supported Frameworks

[![Google ADK](https://img.shields.io/badge/Google-ADK-green?style=for-the-badge&logo=google)](https://google.github.io/adk-docs/)
[![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-412991?style=for-the-badge&logo=openai)](https://platform.openai.com/docs)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-blue?style=for-the-badge&logo=github)](https://github.com/BerriAI/litellm)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge)](https://python.langchain.com)

## Reporting

SecEv4LIA stores test results locally and includes a built-in dashboard for analysis and visualization.

```bash
secev web
```

## Responsible Use

SecEv4LIA is designed for authorized security testing only. Always obtain explicit permission before testing any AI system.

### Do

- Test your own agents
- Conduct authorized pentesting
- Follow coordinated disclosure
- Share security knowledge responsibly

### Don't

- Test systems without permission
- Exploit vulnerabilities maliciously
- Violate terms of service
- Share harmful exploit instructions irresponsibly

Read the full guidelines: [Responsible Disclosure](docs/docs/security/responsible-disclosure.md)

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Licensed under Apache-2.0. See [LICENSE](LICENSE).

## Disclaimer

SecEv4LIA is intended for security research and AI safety improvement. The authors are not responsible for misuse.
