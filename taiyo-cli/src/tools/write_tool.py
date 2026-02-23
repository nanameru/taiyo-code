"""File writing tool."""
from __future__ import annotations
import os
from typing import Any
from .base import BaseTool, ToolResult


class WriteTool(BaseTool):
    name = "write"
    description = "Write content to a file. Creates the file if it doesn't exist, overwrites if it does."

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute or relative path to the file to write",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        }

    async def execute(self, **kwargs: Any) -> ToolResult:
        file_path = kwargs.get("file_path", "")
        content = kwargs.get("content", "")

        if not file_path:
            return ToolResult(error="No file path provided", is_error=True)

        file_path = os.path.expanduser(file_path)
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            lines = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
            return ToolResult(output=f"File written successfully: {file_path} ({lines} lines)")

        except Exception as e:
            return ToolResult(error=str(e), is_error=True)
