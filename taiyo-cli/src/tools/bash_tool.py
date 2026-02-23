"""Bash command execution tool."""
from __future__ import annotations
import asyncio
import os
from typing import Any
from .base import BaseTool, ToolResult


class BashTool(BaseTool):
    name = "bash"
    description = "Execute a bash command and return output. Use for git, npm, system commands, etc."

    def __init__(self, cwd: str | None = None):
        self.cwd = cwd or os.getcwd()

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (default 120)",
                    "default": 120,
                },
            },
            "required": ["command"],
        }

    async def execute(self, **kwargs: Any) -> ToolResult:
        command = kwargs.get("command", "")
        timeout = kwargs.get("timeout", 120)

        if not command:
            return ToolResult(error="No command provided", is_error=True)

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.cwd,
                env={**os.environ, "TERM": "dumb"},
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout
            )

            output = stdout.decode("utf-8", errors="replace")
            err_output = stderr.decode("utf-8", errors="replace")

            if proc.returncode != 0:
                combined = output + ("\n" + err_output if err_output else "")
                return ToolResult(
                    output=combined.strip(),
                    error=f"Exit code: {proc.returncode}",
                    is_error=True,
                )

            combined = output + ("\n" + err_output if err_output else "")
            return ToolResult(output=combined.strip())

        except asyncio.TimeoutError:
            return ToolResult(error=f"Command timed out after {timeout}s", is_error=True)
        except Exception as e:
            return ToolResult(error=str(e), is_error=True)
