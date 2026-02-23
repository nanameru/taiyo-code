"""File editing tool with string replacement."""
from __future__ import annotations
import os
from typing import Any
from .base import BaseTool, ToolResult


class EditTool(BaseTool):
    name = "edit"
    description = "Edit a file by replacing an exact string match with new content."

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to edit",
                },
                "old_string": {
                    "type": "string",
                    "description": "The exact string to find and replace",
                },
                "new_string": {
                    "type": "string",
                    "description": "The replacement string",
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Replace all occurrences (default: false)",
                    "default": False,
                },
            },
            "required": ["file_path", "old_string", "new_string"],
        }

    async def execute(self, **kwargs: Any) -> ToolResult:
        file_path = kwargs.get("file_path", "")
        old_string = kwargs.get("old_string", "")
        new_string = kwargs.get("new_string", "")
        replace_all = kwargs.get("replace_all", False)

        if not file_path:
            return ToolResult(error="No file path provided", is_error=True)

        file_path = os.path.expanduser(file_path)
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            return ToolResult(error=f"File not found: {file_path}", is_error=True)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if old_string not in content:
                return ToolResult(
                    error=f"String not found in file: {repr(old_string[:100])}",
                    is_error=True,
                )

            if not replace_all:
                count = content.count(old_string)
                if count > 1:
                    return ToolResult(
                        error=f"String found {count} times. Use replace_all=true or provide more context.",
                        is_error=True,
                    )
                new_content = content.replace(old_string, new_string, 1)
            else:
                new_content = content.replace(old_string, new_string)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            return ToolResult(output=f"File edited successfully: {file_path}")

        except Exception as e:
            return ToolResult(error=str(e), is_error=True)
