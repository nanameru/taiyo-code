"""File pattern matching tool."""
from __future__ import annotations
import os
import glob as glob_module
from typing import Any
from .base import BaseTool, ToolResult


class GlobTool(BaseTool):
    name = "glob"
    description = "Find files matching a glob pattern (e.g. '**/*.py', 'src/**/*.ts')."

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern to match files (e.g. '**/*.py')",
                },
                "path": {
                    "type": "string",
                    "description": "Base directory to search from (default: current dir)",
                },
            },
            "required": ["pattern"],
        }

    async def execute(self, **kwargs: Any) -> ToolResult:
        pattern = kwargs.get("pattern", "")
        path = kwargs.get("path", ".")

        if not pattern:
            return ToolResult(error="No pattern provided", is_error=True)

        path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        full_pattern = os.path.join(path, pattern)

        try:
            matches = sorted(glob_module.glob(full_pattern, recursive=True))
            # Filter out hidden dirs and common ignores
            filtered = []
            for m in matches:
                parts = m.split(os.sep)
                if any(
                    p.startswith(".") or p in ("node_modules", "__pycache__", "venv")
                    for p in parts
                ):
                    continue
                if os.path.isfile(m):
                    filtered.append(m)

            if not filtered:
                return ToolResult(output="No files found matching pattern.")

            max_files = 500
            output = "\n".join(filtered[:max_files])
            if len(filtered) > max_files:
                output += f"\n... and {len(filtered) - max_files} more files"
            return ToolResult(output=output)

        except Exception as e:
            return ToolResult(error=str(e), is_error=True)
