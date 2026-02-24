"""Taiyo CLI - Main entry point with Claude Code-like REPL."""
from __future__ import annotations
import os
import sys
import asyncio
import json
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime

import click

from .config import Config


# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------
VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# Click entry point
# ---------------------------------------------------------------------------
@click.command()
@click.option("--model", "-m", default=None, help="Ollama model to use")
@click.option("--host", default=None, help="Ollama host URL")
@click.option("--cwd", "-d", default=None, help="Working directory")
@click.option("--tui", is_flag=True, default=False, help="Use TUI mode instead of REPL")
@click.version_option(version=VERSION, prog_name="Taiyo CLI")
def main(model: str | None, host: str | None, cwd: str | None, tui: bool):
    """Taiyo CLI - AI-Powered Coding Assistant

    An interactive terminal-based AI assistant for software engineering tasks.
    Uses local Ollama models for inference.

    Examples:
        taiyo                    # Start REPL mode (default)
        taiyo --tui              # Start TUI mode
        taiyo -m codellama       # Use a specific model
    """
    config = Config.from_env()

    if model:
        config.model = model
    if host:
        config.ollama_host = host
    if cwd:
        config.working_dir = os.path.abspath(cwd)

    if tui:
        run_tui(config)
    else:
        asyncio.run(run_repl(config))


def run_tui(config: Config):
    """Run the TUI application."""
    from .app import TaiyoApp
    app = TaiyoApp(config=config)
    app.run()


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _get_git_branch(working_dir: str) -> str | None:
    """Get the current git branch name, or None if not in a git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=3,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def _load_claude_md(working_dir: str) -> str | None:
    """Load CLAUDE.md from the working directory if it exists."""
    claude_path = os.path.join(working_dir, "CLAUDE.md")
    if os.path.isfile(claude_path):
        try:
            with open(claude_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return None


def _estimate_tokens(text: str) -> int:
    """Rough token estimation (1 token ~ 4 chars for English, ~2 chars for CJK)."""
    return max(1, len(text) // 3)


def _get_terminal_width() -> int:
    """Get terminal width, defaulting to 80."""
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 80


# ---------------------------------------------------------------------------
# Thinking Spinner (Claude Code style - single line)
# ---------------------------------------------------------------------------

class ThinkingSpinner:
    """Single-line animated thinking spinner."""

    FRAMES = ["◐", "◓", "◑", "◒"]

    def __init__(self):
        self._running = False
        self._thread: threading.Thread | None = None
        self._frame = 0
        self._start_time = 0.0

    def start(self):
        self._running = True
        self._start_time = time.time()
        self._frame = 0
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None
        # Clear spinner line
        print(f"\r\033[K", end="", flush=True)

    def _animate(self):
        while self._running:
            spinner = self.FRAMES[self._frame % len(self.FRAMES)]
            elapsed = time.time() - self._start_time
            line = f"\r  \033[3;36m{spinner} Thinking...\033[0m \033[2m({elapsed:.1f}s)\033[0m"
            print(line, end="", flush=True)
            self._frame += 1
            time.sleep(0.15)


# ---------------------------------------------------------------------------
# Session - Conversation persistence
# ---------------------------------------------------------------------------

class Session:
    """Manages conversation persistence as JSONL."""

    def __init__(self, working_dir: str):
        self._dir = os.path.join(working_dir, ".taiyo")
        os.makedirs(self._dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._path = os.path.join(self._dir, f"session_{ts}.jsonl")

    def append(self, role: str, content: str, **extra):
        entry = {"ts": datetime.now().isoformat(), "role": role, "content": content}
        entry.update(extra)
        try:
            with open(self._path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass


# ---------------------------------------------------------------------------
# REPL core
# ---------------------------------------------------------------------------

async def run_repl(config: Config):
    """Run a Claude Code-style REPL."""
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.text import Text
    from rich.rule import Rule

    from prompt_toolkit import PromptSession
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.keys import Keys
    from prompt_toolkit.key_binding import KeyBindings

    from .api import OllamaClient
    from .tools import (
        BashTool,
        ReadTool,
        WriteTool,
        EditTool,
        GrepTool,
        GlobTool,
        WebSearchTool,
    )

    console = Console()
    tw = _get_terminal_width()

    # ---- Build startup banner (Claude Code style rounded box) ----
    git_branch = _get_git_branch(config.working_dir)
    claude_md = _load_claude_md(config.working_dir)

    tokens_up = 0
    tokens_down = 0

    # Prepare raw content lines (no Rich markup for width calc)
    raw_lines: list[tuple[str, str]] = []  # (display_markup, raw_text)
    raw_lines.append((f"[bold cyan]* Taiyo CLI v{VERSION}[/]", f"* Taiyo CLI v{VERSION}"))
    raw_lines.append(("", ""))
    raw_lines.append(("[dim]/help for help[/]", "/help for help"))
    raw_lines.append(("", ""))
    raw_lines.append((f"[dim]cwd: {config.working_dir}[/]", f"cwd: {config.working_dir}"))
    model_raw = f"model: {config.model} (local)"
    model_markup = f"[dim]model: {config.model} (local)[/]"
    if git_branch:
        model_raw += f"  git: {git_branch}"
        model_markup += f"  [dim]git: {git_branch}[/]"
    raw_lines.append((model_markup, model_raw))
    raw_lines.append((f"[dim]tokens: {tokens_up} ^ / {tokens_down} v[/]", f"tokens: {tokens_up} ^ / {tokens_down} v"))

    # Calculate box width
    max_raw_len = max(len(raw) for _, raw in raw_lines)
    box_inner = max(max_raw_len + 4, 42)
    box_inner = min(box_inner, tw - 4)

    # Draw rounded box
    console.print()
    # Top border
    console.print(f"[dim]\u256d{'─' * box_inner}\u256e[/]")
    for markup, raw in raw_lines:
        padding = box_inner - len(raw) - 2
        if padding < 0:
            padding = 0
        console.print(f"[dim]\u2502[/] {markup}{' ' * padding} [dim]\u2502[/]")
    # Bottom border
    console.print(f"[dim]\u2570{'─' * box_inner}\u256f[/]")
    console.print()

    # ---- Initialize tools & client ----
    tools = [
        BashTool(cwd=config.working_dir),
        ReadTool(),
        WriteTool(),
        EditTool(),
        GrepTool(),
        GlobTool(),
        WebSearchTool(),
    ]
    client = OllamaClient(config, tools)

    # Inject CLAUDE.md into system prompt
    if claude_md:
        config.system_prompt += f"\n\n## PROJECT INSTRUCTIONS (from CLAUDE.md)\n{claude_md}\n"
        console.print("[dim]  Loaded CLAUDE.md from working directory.[/]")

    # ---- Check connection ----
    connected = await client.check_connection()
    if not connected:
        console.print("[bold red]  Cannot connect to Ollama![/]")
        console.print("  Start Ollama with: [bold]ollama serve[/]")
        console.print(f"  Then pull a model: [bold]ollama pull {config.model}[/]")
        await client.close()
        return

    models = await client.list_models()
    if models:
        if not any(config.model in m or m in config.model for m in models):
            config.model = models[0]
            client.config.model = models[0]
            console.print(f"[yellow]  Model auto-selected: {models[0]}[/]")

    console.print(f"[dim]  Connected to Ollama. Model: {config.model}[/]")
    console.print()

    # ---- Session ----
    session = Session(config.working_dir)

    # ---- prompt_toolkit setup ----
    history = InMemoryHistory()

    # Key bindings: backslash-newline for multi-line
    kb = KeyBindings()

    @kb.add(Keys.ControlC)
    def _ctrl_c(event):
        """Signal cancellation."""
        event.app.exit(result=None)

    prompt_session: PromptSession = PromptSession(
        history=history,
        key_bindings=kb,
        multiline=False,
        enable_history_search=True,
    )

    spinner = ThinkingSpinner()

    # ---- Render helpers ----
    def _draw_rule(label: str = "", style: str = "dim"):
        """Draw a horizontal rule with optional label."""
        if label:
            console.print(Rule(label, style=style))
        else:
            console.print(Rule(style=style))

    def _print_tool_call(name: str, args: dict):
        """Print a tool call header (Claude Code style)."""
        header = f" {name} "
        dash_count = max(0, min(tw, 50) - len(header) - 4)
        left_dashes = dash_count // 2
        right_dashes = dash_count - left_dashes
        console.print()
        console.print(
            f"  [bold yellow]{'─' * left_dashes}{header}{'─' * right_dashes}[/]"
        )
        for k, v in args.items():
            val_str = str(v)
            if len(val_str) > 200:
                val_str = val_str[:200] + "..."
            console.print(f"  [dim]{k}:[/] {val_str}")
        console.print(f"  [bold yellow]{'─' * min(tw - 4, 50)}[/]")

    def _print_tool_result(name: str, result, elapsed: float):
        """Print tool result (Claude Code style)."""
        output = result.to_text()
        output_lines = output.split("\n")
        max_lines = 30

        is_error = result.is_error
        style = "bold red" if is_error else "dim"
        status = "Error" if is_error else "Result"

        header = f" {name} {status} ({elapsed:.1f}s) "
        dash_count = max(0, min(tw, 50) - len(header) - 4)
        left_dashes = dash_count // 2
        right_dashes = dash_count - left_dashes

        console.print()
        console.print(
            f"  [{style}]{'─' * left_dashes}{header}{'─' * right_dashes}[/{style}]"
        )

        if len(output_lines) > max_lines:
            for line in output_lines[:max_lines]:
                console.print(f"  [dim]{line}[/]")
            remaining = len(output_lines) - max_lines
            console.print(f"  [dim italic]... {remaining} more lines[/]")
        else:
            for line in output_lines:
                console.print(f"  [dim]{line}[/]")

        console.print(f"  [{style}]{'─' * min(tw - 4, 50)}[/{style}]")

    # ---- Slash commands ----
    async def _handle_command(cmd_input: str) -> bool:
        """Handle a slash command. Returns True if should continue loop, False to exit."""
        parts = cmd_input.split(maxsplit=1)
        cmd = parts[0].lower()

        if cmd in ("/quit", "/exit", "/q"):
            console.print("[dim]Goodbye![/]")
            return False

        elif cmd == "/clear":
            client.clear_history()
            nonlocal tokens_up, tokens_down
            tokens_up = 0
            tokens_down = 0
            console.print("[dim]  Conversation history cleared.[/]")
            console.print()

        elif cmd == "/compact":
            console.print("[dim]  Compacting conversation...[/]")
            msg_count = len(client.messages)
            if msg_count > 4:
                # Keep system context but summarize the rest
                summary_prompt = "Summarize the conversation so far in a few bullet points for context preservation."
                # Simple approach: keep last 4 messages
                client.messages = client.messages[-4:]
                console.print(f"[dim]  Compacted: {msg_count} messages -> {len(client.messages)} messages.[/]")
            else:
                console.print("[dim]  Conversation is already short. No compaction needed.[/]")
            console.print()

        elif cmd == "/model":
            if len(parts) > 1:
                new_model = parts[1].strip()
                config.model = new_model
                client.config.model = new_model
                console.print(f"[dim]  Model switched to: [bold]{new_model}[/bold][/]")
            else:
                avail = await client.list_models()
                console.print("[dim]  Available models:[/]")
                for m in avail:
                    marker = " [bold cyan]*[/]" if m == config.model else ""
                    console.print(f"    {m}{marker}")
                console.print()
                console.print("[dim]  Usage: /model <name>[/]")
            console.print()

        elif cmd == "/status":
            branch = _get_git_branch(config.working_dir)
            console.print("[dim]  --- Status ---[/]")
            console.print(f"  [dim]model:[/]   {config.model}")
            console.print(f"  [dim]cwd:[/]     {config.working_dir}")
            if branch:
                console.print(f"  [dim]branch:[/]  {branch}")
            console.print(f"  [dim]tokens:[/]  {tokens_up} ^ / {tokens_down} v")
            console.print(f"  [dim]history:[/] {len(client.messages)} messages")
            console.print()

        elif cmd == "/help":
            console.print()
            console.print("  [bold]Slash Commands[/]")
            console.print("  [dim]─────────────────────────────────[/]")
            console.print("  [bold]/help[/]           Show this help")
            console.print("  [bold]/clear[/]          Clear conversation history")
            console.print("  [bold]/compact[/]        Summarize and compress conversation")
            console.print("  [bold]/model[/] [name]   List or switch models")
            console.print("  [bold]/status[/]         Show current status")
            console.print("  [bold]/init[/]           Create CLAUDE.md in current directory")
            console.print("  [bold]/quit[/]           Exit Taiyo CLI")
            console.print()
            console.print("  [bold]Tips[/]")
            console.print("  [dim]─────────────────────────────────[/]")
            console.print("  [dim]End a line with \\ for multi-line input[/]")
            console.print("  [dim]Ctrl+C to cancel current request[/]")
            console.print()

        elif cmd == "/init":
            claude_path = os.path.join(config.working_dir, "CLAUDE.md")
            if os.path.exists(claude_path):
                console.print(f"[yellow]  CLAUDE.md already exists at {claude_path}[/]")
            else:
                template = f"""# Project Instructions

## Overview
Working directory: {config.working_dir}
Created: {datetime.now().strftime('%Y-%m-%d')}

## Guidelines
- Add project-specific instructions here.
- Taiyo CLI will read this file automatically.
"""
                try:
                    with open(claude_path, "w", encoding="utf-8") as f:
                        f.write(template)
                    console.print(f"[green]  Created CLAUDE.md at {claude_path}[/]")
                except Exception as e:
                    console.print(f"[red]  Failed to create CLAUDE.md: {e}[/]")
            console.print()

        else:
            console.print(f"[red]  Unknown command: {cmd}. Type /help for available commands.[/]")
            console.print()

        return True

    # ---- Main loop ----
    while True:
        try:
            # Multi-line support: if line ends with \, continue reading
            input_lines: list[str] = []
            first_line = True
            while True:
                if first_line:
                    try:
                        line = await asyncio.get_event_loop().run_in_executor(
                            None,
                            lambda: prompt_session.prompt(
                                HTML("<b><skyblue>You</skyblue></b> <b>&gt;</b> "),
                            ),
                        )
                    except KeyboardInterrupt:
                        # Ctrl+C on empty prompt - ignore
                        line = None
                        break
                    except EOFError:
                        line = None
                        break
                    first_line = False
                else:
                    try:
                        line = await asyncio.get_event_loop().run_in_executor(
                            None,
                            lambda: prompt_session.prompt(
                                HTML("  <b>...</b> "),
                            ),
                        )
                    except (KeyboardInterrupt, EOFError):
                        break

                if line is None:
                    break

                if line.endswith("\\"):
                    input_lines.append(line[:-1])
                    continue
                else:
                    input_lines.append(line)
                    break

            if line is None and not input_lines:
                console.print("\n[dim]Goodbye![/]")
                break

            user_input = "\n".join(input_lines).strip()
            if not user_input:
                continue

            # Slash commands
            if user_input.startswith("/"):
                should_continue = await _handle_command(user_input)
                if not should_continue:
                    break
                continue

            # Track tokens
            tokens_up += _estimate_tokens(user_input)
            session.append("user", user_input)

            # ---- Process message ----
            console.print()
            full_response = ""
            spinner.start()
            cancelled = False
            tool_start_time = 0.0

            try:
                first_text = True

                async for chunk in client.chat_stream(user_input):
                    if chunk["type"] == "text":
                        if first_text:
                            spinner.stop()
                            # Print response prefix
                            console.print("[bold]Taiyo[/] [bold]>[/] ", end="")
                            first_text = False
                        content = chunk["content"]
                        print(content, end="", flush=True)
                        full_response += content

                    elif chunk["type"] == "tool_call":
                        spinner.stop()
                        # If we were streaming text, close it
                        if full_response and not first_text:
                            print()
                            console.print()

                        name = chunk["name"]
                        args = chunk["arguments"]
                        _print_tool_call(name, args)

                        # Record start time for tool execution
                        tool_start_time = time.time()

                        # Restart spinner for tool execution
                        spinner.start()

                    elif chunk["type"] == "tool_result":
                        spinner.stop()
                        result = chunk["result"]
                        name = chunk["name"]
                        elapsed = time.time() - tool_start_time if tool_start_time else 0.0
                        _print_tool_result(name, result, elapsed)
                        tool_start_time = 0.0

                        # Reset for next text
                        full_response = ""
                        first_text = True

                        # Restart spinner for follow-up thinking
                        spinner.start()

                spinner.stop()
                if full_response:
                    print()  # End the raw streaming line

                tokens_down += _estimate_tokens(full_response)
                session.append("assistant", full_response)

                console.print()

            except KeyboardInterrupt:
                spinner.stop()
                cancelled = True
                console.print("\n[dim italic]  Cancelled.[/]")
                console.print()
            except Exception as e:
                spinner.stop()
                error_msg = str(e)
                if "Connection refused" in error_msg:
                    console.print("[bold red]  Lost connection to Ollama![/]")
                else:
                    console.print(f"[bold red]  Error: {error_msg}[/]")
                console.print()

        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/]")
            break

    await client.close()


if __name__ == "__main__":
    main()
