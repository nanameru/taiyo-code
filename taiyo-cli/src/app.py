"""Taiyo CLI - TUI Application using Textual."""
from __future__ import annotations
import os
import asyncio
from datetime import datetime

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.css.query import NoMatches
from textual.widgets import (
    Header,
    Footer,
    Static,
    Input,
    TextArea,
    Label,
    RichLog,
    LoadingIndicator,
)
from textual.message import Message as TextualMessage

from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from .config import Config
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

LOGO = r"""
 ___________  _____  ___  __   __  _____
|_   _|  _  ||_   _||   \ \ \ / / |  _  |
  | | | |_| |  | |  | |\ \ \ V /  | | | |
  | | |  _  |  | |  | | \ \  | |  | | | |
  | | | | | | _| |_ | |  \ | | |  \ \_/ /
  |_| |_| |_||_____||_|   \| |_|   \___/
           C  L  I
"""

WELCOME = """Welcome to **Taiyo CLI** - AI-Powered Coding Assistant

Type your message below and press **Enter** to send.
Commands: `/clear` - clear chat, `/model` - change model, `/quit` - exit

Working directory: `{cwd}`
Model: `{model}`
"""


class ChatMessage(Static):
    """A single chat message widget."""

    def __init__(self, role: str, content: str, **kwargs):
        super().__init__(**kwargs)
        self.role = role
        self.msg_content = content

    def compose(self) -> ComposeResult:
        yield Static(id="msg-content")

    def on_mount(self):
        widget = self.query_one("#msg-content", Static)
        if self.role == "user":
            text = Text()
            text.append("  You ", style="bold white on blue")
            text.append(f"  {self.msg_content}")
            widget.update(text)
            self.styles.margin = (1, 0, 0, 0)
        elif self.role == "assistant":
            try:
                md = Markdown(self.msg_content)
                panel = Panel(
                    md,
                    title="[bold green]Taiyo[/]",
                    border_style="green",
                    padding=(0, 1),
                )
                widget.update(panel)
            except Exception:
                widget.update(f"Taiyo: {self.msg_content}")
            self.styles.margin = (0, 0, 1, 0)
        elif self.role == "tool":
            panel = Panel(
                self.msg_content,
                title="[bold yellow]Tool[/]",
                border_style="yellow",
                padding=(0, 1),
            )
            widget.update(panel)
            self.styles.margin = (0, 2, 0, 2)
        elif self.role == "error":
            panel = Panel(
                self.msg_content,
                title="[bold red]Error[/]",
                border_style="red",
                padding=(0, 1),
            )
            widget.update(panel)


class StreamingMessage(Static):
    """Widget that displays streaming assistant response."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._text = ""

    def append_text(self, text: str):
        self._text += text
        try:
            md = Markdown(self._text)
            panel = Panel(
                md,
                title="[bold green]Taiyo[/] [dim italic]typing...[/]",
                border_style="green",
                padding=(0, 1),
            )
            self.update(panel)
        except Exception:
            self.update(self._text)

    def finalize(self):
        try:
            md = Markdown(self._text)
            panel = Panel(
                md,
                title="[bold green]Taiyo[/]",
                border_style="green",
                padding=(0, 1),
            )
            self.update(panel)
        except Exception:
            self.update(self._text)

    @property
    def text(self) -> str:
        return self._text


class TaiyoApp(App):
    """Main TUI Application."""

    TITLE = "Taiyo CLI"
    SUB_TITLE = "AI-Powered Coding Assistant"

    CSS = """
    Screen {
        background: $surface;
    }

    #chat-container {
        height: 1fr;
        overflow-y: auto;
        padding: 0 1;
    }

    #input-area {
        dock: bottom;
        height: auto;
        max-height: 8;
        padding: 0 1;
        background: $surface-darken-1;
    }

    #user-input {
        width: 1fr;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: $primary-darken-2;
        color: $text;
        padding: 0 1;
    }

    #logo-area {
        height: auto;
        content-align: center middle;
        color: $accent;
        text-align: center;
        padding: 1 0;
    }

    #welcome-msg {
        padding: 0 2;
        margin: 0 0 1 0;
    }

    .tool-panel {
        margin: 0 2;
        padding: 0 1;
    }

    LoadingIndicator {
        height: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True),
        Binding("ctrl+l", "clear_chat", "Clear", show=True),
        Binding("escape", "cancel", "Cancel", show=False),
    ]

    def __init__(self, config: Config | None = None):
        super().__init__()
        self.config = config or Config.from_env()
        self._is_processing = False
        self._current_stream: StreamingMessage | None = None
        self._init_tools()

    def _init_tools(self):
        self.tool_instances = [
            BashTool(cwd=self.config.working_dir),
            ReadTool(),
            WriteTool(),
            EditTool(),
            GrepTool(),
            GlobTool(),
            WebSearchTool(),
        ]
        self.client = OllamaClient(self.config, self.tool_instances)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(id="chat-container"):
            yield Static(LOGO, id="logo-area")
            yield Static(
                Markdown(
                    WELCOME.format(
                        cwd=self.config.working_dir, model=self.config.model
                    )
                ),
                id="welcome-msg",
            )
        yield Static("", id="status-bar")
        with Horizontal(id="input-area"):
            yield Input(
                placeholder="Type your message... (Enter to send, Ctrl+C to quit)",
                id="user-input",
            )

    async def on_mount(self):
        self._update_status("Connecting to Ollama...")
        connected = await self.client.check_connection()
        if connected:
            models = await self.client.list_models()
            if models:
                # Auto-select first available model if configured one isn't available
                model_names = [m.split(":")[0] for m in models]
                if not any(self.config.model in m or m in self.config.model for m in models):
                    self.config.model = models[0]
                    self.client.config.model = models[0]
                self._update_status(
                    f"Connected | Model: {self.config.model} | {self.config.working_dir}"
                )
            else:
                self._update_status("Connected | No models found - run: ollama pull qwen2.5-coder:7b")
        else:
            self._update_status("Ollama not running! Start with: ollama serve")
        self.query_one("#user-input", Input).focus()

    def _update_status(self, text: str):
        try:
            bar = self.query_one("#status-bar", Static)
            styled = Text()
            styled.append(" Taiyo ", style="bold white on dark_green")
            styled.append(f"  {text}", style="dim")
            bar.update(styled)
        except NoMatches:
            pass

    def _scroll_to_bottom(self):
        container = self.query_one("#chat-container", VerticalScroll)
        container.scroll_end(animate=False)

    def _add_message(self, role: str, content: str) -> ChatMessage:
        container = self.query_one("#chat-container", VerticalScroll)
        msg = ChatMessage(role=role, content=content)
        container.mount(msg)
        self.call_after_refresh(self._scroll_to_bottom)
        return msg

    @on(Input.Submitted, "#user-input")
    async def handle_input(self, event: Input.Submitted):
        text = event.value.strip()
        if not text:
            return

        input_widget = self.query_one("#user-input", Input)
        input_widget.value = ""

        # Handle slash commands
        if text.startswith("/"):
            await self._handle_command(text)
            return

        if self._is_processing:
            return

        self._add_message("user", text)
        self._process_message(text)

    async def _handle_command(self, cmd: str):
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()

        if command == "/clear":
            self.client.clear_history()
            container = self.query_one("#chat-container", VerticalScroll)
            # Remove all children except logo and welcome
            children = list(container.children)
            for child in children[2:]:
                child.remove()
            self._update_status(f"Chat cleared | {self.config.model}")

        elif command == "/quit" or command == "/exit":
            self.exit()

        elif command == "/model":
            models = await self.client.list_models()
            if models:
                model_list = "\n".join(f"  - `{m}`" for m in models)
                self._add_message(
                    "assistant",
                    f"Available models:\n{model_list}\n\nUse `/model <name>` to switch.",
                )
                if len(parts) > 1:
                    new_model = parts[1].strip()
                    self.config.model = new_model
                    self.client.config.model = new_model
                    self._update_status(f"Model changed to: {new_model}")
                    self._add_message("assistant", f"Switched to model: **{new_model}**")
            else:
                self._add_message("error", "No models available. Is Ollama running?")

        elif command == "/help":
            help_text = """**Available Commands:**
- `/clear` - Clear chat history
- `/model` - List models or switch model (`/model <name>`)
- `/help` - Show this help
- `/quit` - Exit Taiyo CLI

**Keyboard Shortcuts:**
- `Enter` - Send message
- `Ctrl+C` - Quit
- `Ctrl+L` - Clear chat
"""
            self._add_message("assistant", help_text)
        else:
            self._add_message("error", f"Unknown command: `{command}`. Type `/help` for available commands.")

    @work(exclusive=True)
    async def _process_message(self, text: str):
        self._is_processing = True
        self._update_status(f"Thinking... | {self.config.model}")

        container = self.query_one("#chat-container", VerticalScroll)

        # Create streaming message widget
        stream_widget = StreamingMessage()
        container.mount(stream_widget)
        self._current_stream = stream_widget

        try:
            async for chunk in self.client.chat_stream(text):
                if chunk["type"] == "text":
                    stream_widget.append_text(chunk["content"])
                    self.call_after_refresh(self._scroll_to_bottom)

                elif chunk["type"] == "tool_call":
                    name = chunk["name"]
                    args = chunk["arguments"]
                    args_str = "\n".join(f"  {k}: {v}" for k, v in args.items())
                    tool_msg = f"[bold]Tool:[/] {name}\n{args_str}"
                    self._add_message("tool", tool_msg)

                elif chunk["type"] == "tool_result":
                    result = chunk["result"]
                    name = chunk["name"]
                    output = result.to_text()
                    if len(output) > 1000:
                        output = output[:1000] + "\n... (truncated)"
                    status = "[red]Error[/]" if result.is_error else "[green]Success[/]"
                    self._add_message(
                        "tool", f"[bold]{name}[/] {status}\n{output}"
                    )

                    # After tool result, create new streaming widget for follow-up
                    stream_widget.finalize()
                    stream_widget = StreamingMessage()
                    container.mount(stream_widget)
                    self._current_stream = stream_widget

            # Finalize streaming
            stream_widget.finalize()
            if not stream_widget.text:
                stream_widget.remove()

        except Exception as e:
            stream_widget.remove()
            error_msg = str(e)
            if "Connection refused" in error_msg:
                error_msg = "Cannot connect to Ollama. Make sure it's running: `ollama serve`"
            elif "404" in error_msg:
                error_msg = f"Model not found: {self.config.model}. Pull it: `ollama pull {self.config.model}`"
            self._add_message("error", error_msg)

        finally:
            self._is_processing = False
            self._current_stream = None
            self._update_status(
                f"Ready | Model: {self.config.model} | {self.config.working_dir}"
            )
            self.query_one("#user-input", Input).focus()

    def action_clear_chat(self):
        asyncio.create_task(self._handle_command("/clear"))

    def action_cancel(self):
        if self._is_processing:
            self._is_processing = False
            self._update_status("Cancelled")
