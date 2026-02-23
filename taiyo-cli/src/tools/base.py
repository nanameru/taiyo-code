"""Base tool class and result type."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    """Result from a tool execution."""
    output: str = ""
    error: str = ""
    is_error: bool = False

    def to_text(self) -> str:
        if self.is_error:
            return f"Error: {self.error}"
        return self.output


class BaseTool(ABC):
    """Base class for all tools."""

    name: str = ""
    description: str = ""

    @abstractmethod
    def get_schema(self) -> dict[str, Any]:
        """Return the tool's JSON schema for API."""
        ...

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute the tool with given parameters."""
        ...

    def to_api_schema(self) -> dict[str, Any]:
        """Convert to Ollama/OpenAI-compatible tool schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_schema(),
            },
        }
