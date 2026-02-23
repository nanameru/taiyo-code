"""File reading tool."""
from __future__ import annotations
import os
from typing import Any
from .base import BaseTool, ToolResult


class ReadTool(BaseTool):
    name = "read"
    description = "Read the contents of a file. Returns file content with line numbers."

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute or relative path to the file to read",
                },
                "offset": {
                    "type": "integer",
                    "description": "Line number to start reading from (1-based)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of lines to read",
                },
            },
            "required": ["file_path"],
        }

    async def execute(self, **kwargs: Any) -> ToolResult:
        file_path = kwargs.get("file_path", "")
        offset = kwargs.get("offset", 1)
        limit = kwargs.get("limit", 2000)

        if not file_path:
            return ToolResult(error="No file path provided", is_error=True)

        file_path = os.path.expanduser(file_path)
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            return ToolResult(error=f"File not found: {file_path}", is_error=True)

        if os.path.isdir(file_path):
            return ToolResult(error=f"Path is a directory: {file_path}", is_error=True)

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

            start = max(0, offset - 1)
            end = start + limit
            selected = lines[start:end]

            result_lines = []
            for i, line in enumerate(selected, start=start + 1):
                line_content = line.rstrip("\n")
                if len(line_content) > 2000:
                    line_content = line_content[:2000] + "..."
                result_lines.append(f"{i:>6}\t{line_content}")

            return ToolResult(output="\n".join(result_lines))

        except Exception as e:
            return ToolResult(error=str(e), is_error=True)
