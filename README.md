<div align="center">

  <strong>SecEv4LIA — AI Security Red-Team Toolkit</strong> 

<br>

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)
[![Commitizen](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

<br>

</div>


## Overview

SecEv4LIA is an open-source toolkit designed to help security researchers, developers and AI safety practitioners evaluate the security of AI agents. 
It provides a structured approach to discover potential vulnerabilities, including prompt injection, jailbreaking techniques, and other attack vectors.

### 🔌 AI Agent Frameworks Supported

[![LiteLLM](https://img.shields.io/badge/LiteLLM-blue?style=flat&logo=github)](https://github.com/BerriAI/litellm)
[![ADK](https://img.shields.io/badge/Google-ADK-green?style=flat&logo=openai)](https://google.github.io/adk-docs/)
[![OpenAI](https://img.shields.io/badge/OpenAI-SDK-412991?style=flat&logo=openai)](https://platform.openai.com/docs)
[![Ollama](https://img.shields.io/badge/Ollama-black?style=flat&logo=ollama)](https://ollama.com)

## 🚀 Quick Start


### Installation

SecEv4LIA can be installed from PyPI or directly from GitHub:

```bash
pip install git+https://github.com/AISecurityLab/SecEv4LIA.git
```
Activate the environment
```bash
source .venv/bin/activate
```

## 📚 Example

### TUI

Run the interactive CLI to start testing your AI agents:

```bash
secev examples ollama
```

## 📊 Reporting

SecEv4LIA stores all test results locally and provides a built-in dashboard for analysis and visualization.

Launch the local dashboard with:

```bash
secev web
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines.

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

SecEv4LIA is a tool designed for security research and improving AI safety. Always obtain proper authorization before testing any AI systems. The authors are not responsible for any misuse of this software.

---

*This project is for educational and research purposes. Always use responsibly and ethically.*
