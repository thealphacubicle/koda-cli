# koda

**AI-powered project bootstrapper for developers.** Spin up new projects with interactive menus, AI-generated READMEs, and git + GitHub setup in seconds.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![macOS · Linux](https://img.shields.io/badge/platform-macOS%20%C2%B7%20Linux-lightgrey.svg)](https://github.com/thealphacubicle/koda-cli)

---

## What is koda?

Koda is a CLI that bootstraps new projects from scratch. Choose your project type (data science, API, or web app), pick an AI provider (Claude, OpenAI, or Gemini), and let koda scaffold the structure, generate a README with AI, and optionally set up git and push to GitHub. No more copy-pasting boilerplate—just run `koda new my-project` and go.

---

## Demo

```
$ koda new my-project

  ╔═══════════════════════════════════════╗
  ║            koda v1.0.0               ║
  ║   AI-powered project bootstrapper    ║
  ╚═══════════════════════════════════════╝

  ───────────────────────────────────────

  Where do you want to create the project?
  ❯ Current directory (~/Projects)
    Desktop (~/Desktop)
    Documents (~/Documents)
    Projects (~/Projects)
    Other (enter custom path)

  What type of project?
  ❯ Python data science
    Python API / backend
    Web app (HTML/JS)

  AI provider?
  ❯ Claude
    OpenAI
    Gemini

  Which features to set up?
  ❯ ◉ Create folder structure
  ❯ ◉ Set up git
  ❯ ◉ Generate README with AI

  ───────────────────────────────────────

  Checking tools...
  ✓ gh CLI authenticated
  ✓ Claude Code ready

  Creating project structure...
  ✓ Created my-project/

  Generating README and starter code...
  ✓ Updated README.md
  ✓ Updated src/main.py

  Initializing git...
  ✓ Git initialized
  ✓ Initial commit created

  ───────────────────────────────────────

  Done! Project at ~/Projects/my-project
```

---

## Install

```bash
pip install git+https://github.com/thealphacubicle/koda-cli.git
```

---

## Usage

| Command | Description |
|---------|-------------|
| `koda` | Opens interactive REPL |
| `koda new <name>` | Bootstrap a new project |
| `koda auth` | Check and set up tool logins (gh CLI, Claude Code) |
| `koda config` | View and edit settings |
| `koda help` | Show all commands |

---

## Configuration

Koda stores settings in `~/.koda/config.json`. API keys and preferences live there:

```json
{
  "anthropic": "sk-ant-...",
  "openai": "sk-...",
  "google": "...",
  "default_provider": "claude",
  "name": "Your Name",
  "projects_path": "~/Projects"
}
```

Set API keys with:

```bash
koda config set anthropic
koda config set openai
koda config set google
```

---

## Supported AI Providers

- **Claude** (Anthropic)
- **OpenAI** (GPT models)
- **Gemini** (Google)

You're prompted to choose a provider when creating a new project. Make sure the corresponding API key is set via `koda config set <provider>`.

---

## Requirements

- **Python 3.9+**
- **git** — for version control and first commit
- **gh CLI** — for creating and pushing to GitHub (optional, used when you choose "Push to GitHub")

---

## Contributing

1. Fork the repo
2. Clone and install in editable mode: `pip install -e .`
3. Make your changes
4. Open a PR

---

## License

MIT © 2026 thealphacubicle
