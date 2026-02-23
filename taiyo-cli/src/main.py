"""Taiyo CLI - Main entry point."""
from __future__ import annotations
import os
import sys
import asyncio
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

        try:
            async for chunk in client.chat_stream(user_input):
                if chunk["type"] == "text":
                    # Print text character by character for streaming effect
                    print(chunk["content"], end="", flush=True)
                    full_response += chunk["content"]

                elif chunk["type"] == "tool_call":
                    name = chunk["name"]
                    args = chunk["arguments"]
                    console.print(
                        Panel(
                            "\n".join(f"  {k}: {v}" for k, v in args.items()),
                            title=f"[bold yellow]Tool: {name}[/]",
                            border_style="yellow",
                        )
                    )

                elif chunk["type"] == "tool_result":
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
                    full_response = ""  # Reset for follow-up response

            if full_response:
                print()  # Newline after streaming
            console.print()

        except Exception as e:
            error_msg = str(e)
            if "Connection refused" in error_msg:
                console.print("[bold red]Lost connection to Ollama![/]")
            else:
                console.print(f"[bold red]Error: {error_msg}[/]")
            console.print()

    await client.close()


if __name__ == "__main__":
    main()
