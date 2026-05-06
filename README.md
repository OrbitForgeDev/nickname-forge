# 🚀 Nickname Forge

> CLI tool to forge unique nicknames in various styles.
> Built with ❤️ by [OrbitForgeDev](https://github.com/OrbitForgeDev)

![Tests](https://github.com/OrbitForgeDev/nickname-forge/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🌐 Development Notes

Initial code comments and documentation were written in Russian (the author's native language) and subsequently translated to English using AI-assisted tools.

This workflow ensures:
- Faster prototyping in the developer's native language
- Clean, production-ready English documentation for the global community
- Consistent terminology across the entire codebase

*If you find any awkward phrasing in comments — pull requests are welcome!*

## 📖 Overview

**Nickname Forge** is a command-line tool that generates memorable, unique nicknames by combining word parts from different style templates. Whether you need a cyberpunk handle, a fantasy character name, or a space-themed alias — Forge has you covered.

### ✨ Features

- 🎨 **3 built-in styles:** Cyberpunk, Fantasy, Space
- 🔢 **Batch generation:** Generate up to 50 nicknames at once
- 🏷️ **Custom separators:** Dashes, underscores, or seamless concatenation
- 📊 **Readability scoring:** Each nickname gets a quality score (0–100)
- 🧩 **Extensible:** Add your own styles via JSON files
- ✅ **Fully tested:** 45 tests covering engine and CLI
- 🐍 **Modern Python:** 3.11+, typed, linted

---

## 📦 Installation

### From PyPI (coming soon)
```bash
pip install nickname-forge
```

From source (for development)

```bash
git clone https://github.com/OrbitForgeDev/nickname-forge.git
cd nickname-forge
pip install -e .
```

---

🚀 Quick Start

```bash
# Generate 10 cyberpunk nicknames
forge --style cyberpunk --count 10

# Generate 5 fantasy names with underscore separator
forge --style fantasy --count 5 --sep "_"

# Generate space names, hide scores
forge -s space --no-score

# List all available styles
forge --list-styles

# Get help
forge --help
```

---

🎨 Available Styles

Style Example
cyberpunk NeonHackRunner
fantasy StormKnightSeeker
space NebulaForgeTech

---

🧪 Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
python -m pytest tests/ -v
```

---

📁 Project Structure

```
nickname-forge/
├── src/
│   └── nickname_forge/
│       ├── __init__.py        # Package init
│       ├── engine.py          # Core generation engine
│       ├── main.py            # CLI (Typer + Rich)
│       └── data/              # Style templates (JSON)
│           ├── cyberpunk.json
│           ├── fantasy.json
│           └── space.json
├── tests/
│   ├── __init__.py
│   ├── test_engine.py         # 21 tests for the engine
│   └── test_cli.py            # 24 tests for the CLI
├── .github/workflows/
│   └── test.yml               # CI: auto-tests on push
├── pyproject.toml             # Project config & dependencies
├── .gitignore
└── README.md
```

---

🛠️ Built With

· Typer — CLI framework
· Rich — Beautiful terminal output
· Pytest — Testing
· Ruff — Linting & formatting

---

📝 License

This project is licensed under the MIT License.

---

🤝 Contributing

Pull requests are welcome! If you'd like to add a new style, create a JSON file in src/nickname_forge/data/ following the existing format.

---

<p align="center">
  <sub>Crafted in orbit by <a href="https://github.com/OrbitForgeDev">OrbitForgeDev</a></sub>
</p>
