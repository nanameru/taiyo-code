"""Configuration for Taiyo CLI."""
from __future__ import annotations
import os
from dataclasses import dataclass, field


@dataclass
class Config:
    """Application configuration."""
    # Ollama settings
    ollama_host: str = "http://localhost:11434"
    model: str = "qwen2.5-coder:7b"

    # App settings
    working_dir: str = field(default_factory=os.getcwd)
    max_tokens: int = 4096
    temperature: float = 0.1

    # System prompt
    system_prompt: str = """You are Taiyo CLI, an AI-powered coding assistant running in the terminal.
You help users with software engineering tasks: writing code, debugging, file management, and more.

You have access to the following tools:
- bash: Execute shell commands
- read: Read file contents
- write: Write/create files
- edit: Edit files with string replacement
- grep: Search file contents with regex
- glob: Find files by pattern

When you need to perform actions, use the available tools. Be concise and helpful.
Always explain what you're doing before using tools.
For code changes, read the file first to understand context before editing.
"""

    @classmethod
    def from_env(cls) -> Config:
        return cls(
            ollama_host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
            model=os.environ.get("TAIYO_MODEL", "qwen2.5-coder:7b"),
            working_dir=os.environ.get("TAIYO_CWD", os.getcwd()),
        )
