# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Taiyo CLI** is a locally-running AI coding assistant (Claude Code clone) built with Python. It uses Ollama for local LLM inference and provides both a REPL and TUI interface for interactive terminal-based coding assistance.

## Commands

```bash
# Install (editable mode, from taiyo-cli/)
cd taiyo-cli && pip install -e .

# Run
taiyo                        # REPL mode (default)
taiyo --tui                  # TUI mode (Textual framework)
taiyo -m codellama           # Use specific Ollama model
taiyo --host http://host:11434  # Custom Ollama host
taiyo -d /path/to/project    # Set working directory
```

No test suite or linter is configured yet.

## Architecture

```
taiyo-cli/src/
├── main.py      # Click CLI entry point + REPL loop + Session persistence
├── app.py       # TUI application (Textual framework, alternative to REPL)
├── api.py       # OllamaClient - manages conversation history, tool call detection, streaming
├── config.py    # Config dataclass with env var overrides + system prompt
├── tools/       # Tool implementations (all async, inherit from BaseTool)
│   ├── base.py       # BaseTool ABC + ToolResult dataclass
│   ├── bash_tool.py  # Shell command execution
│   ├── read_tool.py  # File reading with offset/limit
│   ├── write_tool.py # File creation/overwrite
│   ├── edit_tool.py  # String replacement editing
│   ├── grep_tool.py  # Regex content search with gitignore filtering
│   ├── glob_tool.py  # File pattern matching
│   └── web_tool.py   # Web search (placeholder)
└── ui/          # UI components for TUI mode
```

### Key Design Patterns

- **Tool Factory**: All tools extend `BaseTool` (ABC) with `get_schema()` and async `execute()`. They expose `to_api_schema()` for Ollama/OpenAI-compatible function calling format.
- **OllamaClient** (`api.py`): Central orchestrator. Implements flexible tool call detection (direct JSON parsing, code block extraction, brace-depth tracking) to handle local LLMs that don't strictly follow API formats. Runs up to 15 tool rounds per request in an agentic loop.
- **REPL** (`main.py`): Claude Code-style interface with ThinkingSpinner (◐◓◑◒ animation), session persistence as JSONL in `.taiyo/`, slash commands (`/help`, `/clear`, `/compact`, `/model`, `/status`, `/init`, `/quit`), multi-line input (backslash continuation), and auto-loading of CLAUDE.md from the working directory.
- **Config** (`config.py`): Dataclass with `Config.from_env()` factory. Contains the 154-line system prompt that forces local LLMs to use tools.

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `TAIYO_MODEL` | `qwen2.5-coder:7b` | LLM model name |
| `TAIYO_CWD` | Current directory | Working directory |

## Tech Stack

- **Python 3.10+** with async/await throughout
- **httpx** - Async HTTP client for Ollama API
- **Textual** - TUI framework (app.py)
- **Rich** - Terminal formatting
- **prompt-toolkit** - REPL input handling
- **Click** - CLI argument parsing
- **Hatchling** - Build backend (`pyproject.toml`)

## Session Data

Sessions are stored as JSONL files at `.taiyo/session_YYYYMMDD_HHMMSS.jsonl` with timestamped message entries. The `.taiyo/` directory is gitignored.
