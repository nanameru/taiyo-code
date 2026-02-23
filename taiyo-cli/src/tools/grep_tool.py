"""Content search tool using regex."""
from __future__ import annotations
import os
import re
from typing import Any
from .base import BaseTool, ToolResult


class GrepTool(BaseTool):
    name = "grep"
    description = "Search file contents using regex patterns. Returns matching lines with file paths and line numbers."

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for",
                },
                "path": {
                    "type": "string",
                    "description": "Directory or file to search in (default: current dir)",
                },
                "glob": {
                    "type": "string",
                    "description": "File glob pattern to filter (e.g. '*.py', '*.js')",
                },
                "case_insensitive": {
                    "type": "boolean",
                    "description": "Case insensitive search",
                    "default": False,
                },
            },
            "required": ["pattern"],
        }

    async def execute(self, **kwargs: Any) -> ToolResult:
        pattern = kwargs.get("pattern", "")
        path = kwargs.get("path", ".")
        glob_filter = kwargs.get("glob", "")
        case_insensitive = kwargs.get("case_insensitive", False)

        if not pattern:
            return ToolResult(error="No pattern provided", is_error=True)

        path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        flags = re.IGNORECASE if case_insensitive else 0
        try:
            compiled = re.compile(pattern, flags)
        except re.error as e:
            return ToolResult(error=f"Invalid regex: {e}", is_error=True)

        results = []
        max_results = 200

        try:
            if os.path.isfile(path):
                results.extend(self._search_file(path, compiled))
            else:
                import pathspec
                spec = None
                if glob_filter:
                    spec = pathspec.PathSpec.from_lines("gitwildmatch", [glob_filter])

                for root, dirs, files in os.walk(path):
                    # Skip hidden and common ignore dirs
                    dirs[:] = [
                        d for d in dirs
                        if not d.startswith(".") and d not in ("node_modules", "__pycache__", "venv", ".git")
                    ]
                    for fname in files:
                        if fname.startswith("."):
                            continue
                        fpath = os.path.join(root, fname)
                        if spec and not spec.match_file(os.path.relpath(fpath, path)):
                            continue
                        results.extend(self._search_file(fpath, compiled))
                        if len(results) >= max_results:
                            break
                    if len(results) >= max_results:
                        break

            if not results:
                return ToolResult(output="No matches found.")

            output = "\n".join(results[:max_results])
            if len(results) > max_results:
                output += f"\n... and {len(results) - max_results} more matches"
            return ToolResult(output=output)

        except Exception as e:
            return ToolResult(error=str(e), is_error=True)

    def _search_file(self, fpath: str, pattern: re.Pattern) -> list[str]:
        results = []
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    if pattern.search(line):
                        results.append(f"{fpath}:{i}: {line.rstrip()}")
        except (OSError, UnicodeDecodeError):
            pass
        return results
