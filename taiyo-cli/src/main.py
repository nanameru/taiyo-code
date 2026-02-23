"""Taiyo CLI - Main entry point."""
from __future__ import annotations
import os
import sys
import asyncio
import threading
import time
import click

from .config import Config


@click.command()
@click.option("--model", "-m", default=None, help="Ollama model to use")
@click.option("--host", default=None, help="Ollama host URL")
@click.option("--cwd", "-d", default=None, help="Working directory")
@click.option("--repl", is_flag=True, default=False, help="Use simple REPL mode instead of TUI")
@click.version_option(version="1.0.0", prog_name="Taiyo CLI")
def main(model: str | None, host: str | None, cwd: str | None, repl: bool):
    """Taiyo CLI - AI-Powered Coding Assistant

    An interactive terminal-based AI assistant for software engineering tasks.
    Uses local Ollama models for inference.

    Examples:
        taiyo                    # Start TUI mode
        taiyo --repl             # Start simple REPL mode
        taiyo -m codellama       # Use a specific model
    """
    config = Config.from_env()

    if model:
        config.model = model
    if host:
        config.ollama_host = host
    if cwd:
        config.working_dir = os.path.abspath(cwd)

    if repl:
        asyncio.run(run_repl(config))
    else:
        run_tui(config)


def run_tui(config: Config):
    """Run the TUI application."""
    from .app import TaiyoApp
    app = TaiyoApp(config=config)
    app.run()


class ThinkingSpinner:
    """Animated thinking spinner for REPL mode."""

    FRAMES = ["◐", "◓", "◑", "◒"]
    LABELS = ["Processing", "Analyzing", "Reasoning", "Formulating", "Composing", "Generating"]

    def __init__(self, console):
        self.console = console
        self._running = False
        self._thread = None
        self._frame = 0
        self._start_time = 0.0
        self._phase = "thinking"

    def start(self, phase: str = "thinking"):
        self._phase = phase
        self._running = True
        self._start_time = time.time()
        self._frame = 0
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        # Clear the spinner line
        print(f"\r\033[K", end="", flush=True)

    def set_phase(self, phase: str):
        self._phase = phase

    def _animate(self):
        while self._running:
            elapsed = time.time() - self._start_time
            spinner = self.FRAMES[self._frame % len(self.FRAMES)]
            label = self.LABELS[self._frame % len(self.LABELS)]

            bar_len = 20
            progress = min(int((self._frame % 12) / 12 * bar_len), bar_len - 1)
            bar = "▓" * (progress + 1) + "░" * (bar_len - progress - 1)

            if self._phase == "thinking":
                line = f"\r  \033[36m{spinner}\033[0m \033[1mThinking\033[0m ({elapsed:.1f}s)  {label}...  \033[36m{bar}\033[0m"
            else:
                line = f"\r  \033[33m{spinner}\033[0m \033[1mExecuting Tool\033[0m ({elapsed:.1f}s)  Running...  \033[33m{bar}\033[0m"

            print(line, end="", flush=True)
            self._frame += 1
            time.sleep(0.25)


async def run_repl(config: Config):
    """Run a simple REPL mode (no TUI, just stdin/stdout)."""
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.text import Text

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

    # Print banner
    console.print(
        Panel(
            """[bold cyan]
 ___________  _____  ___  __   __  _____
|_   _|  _  ||_   _||   \\ \\ \\ / / |  _  |
  | | | |_| |  | |  | |\\ \\ \\ V /  | | | |
  | | |  _  |  | |  | | \\ \\  | |  | | | |
  | | | | | | _| |_ | |  \\ | | |  \\ \\_/ /
  |_| |_| |_||_____||_|   \\| |_|   \\___/
           C  L  I[/]

[dim]AI-Powered Coding Assistant (REPL Mode)[/]
[dim]Model: {model} | Dir: {cwd}[/]
[dim]Type /help for commands, /quit to exit[/]""".format(
                model=config.model, cwd=config.working_dir
            ),
            border_style="green",
            padding=(0, 2),
        )
    )

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

    # Check connection
    connected = await client.check_connection()
    if not connected:
        console.print("[bold red]Cannot connect to Ollama![/]")
        console.print("Start Ollama with: [bold]ollama serve[/]")
        console.print(f"Then pull a model: [bold]ollama pull {config.model}[/]")
        await client.close()
        return

    models = await client.list_models()
    if models:
        if not any(config.model in m or m in config.model for m in models):
            config.model = models[0]
            client.config.model = models[0]
            console.print(f"[yellow]Model auto-selected: {models[0]}[/]")

    console.print(f"[green]Connected to Ollama | Model: {config.model}[/]\n")

    spinner = ThinkingSpinner(console)

    while True:
        try:
            user_input = console.input("[bold blue]You >[/] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/]")
            break

        if not user_input:
            continue

        # Handle commands
        if user_input.startswith("/"):
            cmd = user_input.split()[0].lower()
            if cmd in ("/quit", "/exit"):
                console.print("[dim]Goodbye![/]")
                break
            elif cmd == "/clear":
                client.clear_history()
                console.print("[dim]Chat history cleared.[/]")
                continue
            elif cmd == "/model":
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    config.model = parts[1].strip()
                    client.config.model = parts[1].strip()
                    console.print(f"[green]Model switched to: {config.model}[/]")
                else:
                    models = await client.list_models()
                    for m in models:
                        console.print(f"  - {m}")
                continue
            elif cmd == "/help":
                console.print(
                    Panel(
                        "/clear - Clear history\n/model [name] - List/switch models\n/help - Show help\n/quit - Exit",
                        title="Commands",
                        border_style="cyan",
                    )
                )
                continue

        # Process message
        console.print()
        full_response = ""

        # Start thinking spinner
        spinner.start("thinking")

        try:
            first_text = True

            async for chunk in client.chat_stream(user_input):
                if chunk["type"] == "text":
                    if first_text:
                        spinner.stop()
                        first_text = False
                    print(chunk["content"], end="", flush=True)
                    full_response += chunk["content"]

                elif chunk["type"] == "tool_call":
                    spinner.stop()
                    name = chunk["name"]
                    args = chunk["arguments"]
                    console.print(
                        Panel(
                            "\n".join(f"  {k}: {v}" for k, v in args.items()),
                            title=f"[bold yellow]Tool: {name}[/]",
                            border_style="yellow",
                        )
                    )
                    # Start spinner for tool execution
                    spinner.start("tool_exec")

                elif chunk["type"] == "tool_result":
                    spinner.stop()
                    result = chunk["result"]
                    output = result.to_text()
                    if len(output) > 1500:
                        output = output[:1500] + "\n... (truncated)"
                    style = "red" if result.is_error else "green"
                    console.print(
                        Panel(
                            output,
                            title=f"[bold {style}]{chunk['name']} Result[/]",
                            border_style=style,
                        )
                    )
                    full_response = ""
                    first_text = True
                    # Start thinking for follow-up
                    spinner.start("thinking")

            spinner.stop()
            if full_response:
                print()
            console.print()

        except Exception as e:
            spinner.stop()
            error_msg = str(e)
            if "Connection refused" in error_msg:
                console.print("[bold red]Lost connection to Ollama![/]")
            else:
                console.print(f"[bold red]Error: {error_msg}[/]")
            console.print()

    await client.close()


if __name__ == "__main__":
    main()
