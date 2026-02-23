"""Ollama API client with tool calling support."""
from __future__ import annotations
import json
import re
import httpx
from typing import Any, AsyncIterator
from dataclasses import dataclass, field

from .config import Config
from .tools.base import BaseTool, ToolResult


@dataclass
class Message:
    role: str  # "system", "user", "assistant", "tool"
    content: str = ""
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None
    name: str | None = None


class OllamaClient:
    """Client for Ollama API with tool calling."""

    def __init__(self, config: Config, tools: list[BaseTool]):
        self.config = config
        self.tools = {t.name: t for t in tools}
        self.messages: list[Message] = []
        self.client = httpx.AsyncClient(timeout=300.0)
        self._max_tool_rounds = 15

    def _build_tools_schema(self) -> list[dict]:
        return [t.to_api_schema() for t in self.tools.values()]

    def _build_messages(self) -> list[dict]:
        # Inject working directory into system prompt
        system_content = self.config.system_prompt
        system_content += f"\n\n## CURRENT CONTEXT\n- Working directory: {self.config.working_dir}\n- When using file paths, use this as the base directory.\n"
        msgs = [{"role": "system", "content": system_content}]
        for m in self.messages:
            msg: dict[str, Any] = {"role": m.role, "content": m.content}
            if m.tool_calls:
                msg["tool_calls"] = m.tool_calls
            msgs.append(msg)
        return msgs

    def _try_parse_tool_call(self, text: str) -> dict | None:
        """Try to parse a tool call from text content. Handles many formats."""
        text = text.strip()

        # Strip markdown code blocks if present
        # ```json ... ``` or ``` ... ```
        code_block = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if code_block:
            text = code_block.group(1).strip()

        # 1. Direct JSON parse
        try:
            data = json.loads(text)
            result = self._extract_tool_from_json(data)
            if result:
                return result
        except json.JSONDecodeError:
            pass

        # 2. Find JSON objects containing "name" in text
        # Match nested JSON (handles {"name": "x", "arguments": {"key": "val"}})
        brace_depth = 0
        json_start = -1
        candidates = []
        for i, ch in enumerate(text):
            if ch == '{':
                if brace_depth == 0:
                    json_start = i
                brace_depth += 1
            elif ch == '}':
                brace_depth -= 1
                if brace_depth == 0 and json_start >= 0:
                    candidates.append(text[json_start:i + 1])
                    json_start = -1

        for candidate in candidates:
            try:
                data = json.loads(candidate)
                result = self._extract_tool_from_json(data)
                if result:
                    return result
            except json.JSONDecodeError:
                continue

        # 3. Try line-by-line (model might output tool call on one line with text around it)
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    data = json.loads(line)
                    result = self._extract_tool_from_json(data)
                    if result:
                        return result
                except json.JSONDecodeError:
                    continue

        return None

    def _extract_tool_from_json(self, data: Any) -> dict | None:
        """Extract tool name and arguments from a parsed JSON object."""
        if not isinstance(data, dict):
            return None

        # Format: {"name": "tool", "arguments": {...}}
        if "name" in data:
            name = data["name"]
            args = data.get("arguments", data.get("params", data.get("parameters", {})))
            if name in self.tools:
                return {"name": name, "arguments": args if isinstance(args, dict) else {}}

        # Format: {"function": {"name": "tool", "arguments": {...}}}
        if "function" in data and isinstance(data["function"], dict):
            return self._extract_tool_from_json(data["function"])

        # Format: {"tool": "bash", "command": "ls"} (flat format)
        if "tool" in data and data["tool"] in self.tools:
            name = data["tool"]
            args = {k: v for k, v in data.items() if k != "tool"}
            return {"name": name, "arguments": args}

        return None

    async def chat_stream(
        self, user_message: str
    ) -> AsyncIterator[dict[str, Any]]:
        """Send a message and stream the response, handling tool calls."""
        self.messages.append(Message(role="user", content=user_message))

        tool_rounds = 0
        while tool_rounds < self._max_tool_rounds:
            tool_rounds += 1
            response_text = ""
            tool_calls = []

            # Use non-streaming for reliable tool call detection
            response_data = await self._request()
            msg_data = response_data.get("message", {})
            response_text = msg_data.get("content", "")

            # Check for proper tool_calls field first (native Ollama tool calling)
            if msg_data.get("tool_calls"):
                tool_calls = msg_data["tool_calls"]
            else:
                # Try to parse tool calls from text content
                parsed = self._try_parse_tool_call(response_text)
                if parsed:
                    tool_calls = [{"function": parsed}]
                else:
                    # Regular text response - yield it
                    if response_text:
                        yield {"type": "text", "content": response_text}

            # Save assistant message
            self.messages.append(
                Message(
                    role="assistant",
                    content=response_text,
                    tool_calls=tool_calls if tool_calls else None,
                )
            )

            # If no tool calls, we're done
            if not tool_calls:
                break

            # Execute tool calls
            for tc in tool_calls:
                func = tc.get("function", tc)
                tool_name = func.get("name", "")
                arguments = func.get("arguments", {})

                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {}

                yield {
                    "type": "tool_call",
                    "name": tool_name,
                    "arguments": arguments,
                }

                # Execute the tool
                tool = self.tools.get(tool_name)
                if tool:
                    result = await tool.execute(**arguments)
                    yield {
                        "type": "tool_result",
                        "name": tool_name,
                        "result": result,
                    }
                    self.messages.append(
                        Message(
                            role="tool",
                            content=result.to_text(),
                            name=tool_name,
                        )
                    )
                else:
                    error_result = ToolResult(
                        error=f"Unknown tool: {tool_name}", is_error=True
                    )
                    yield {
                        "type": "tool_result",
                        "name": tool_name,
                        "result": error_result,
                    }
                    self.messages.append(
                        Message(
                            role="tool",
                            content=error_result.to_text(),
                            name=tool_name,
                        )
                    )

    async def _request(self) -> dict:
        """Make a non-streaming request to Ollama for reliable tool calling."""
        url = f"{self.config.ollama_host}/api/chat"
        payload = {
            "model": self.config.model,
            "messages": self._build_messages(),
            "stream": False,
            "tools": self._build_tools_schema(),
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            },
        }

        resp = await self.client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    async def _stream_request(self) -> AsyncIterator[dict]:
        """Make a streaming request to Ollama."""
        url = f"{self.config.ollama_host}/api/chat"
        payload = {
            "model": self.config.model,
            "messages": self._build_messages(),
            "stream": True,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            },
        }

        async with self.client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.strip():
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue

    async def check_connection(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            resp = await self.client.get(f"{self.config.ollama_host}/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                models = [m["name"] for m in data.get("models", [])]
                for m in models:
                    if self.config.model in m or m in self.config.model:
                        return True
                return True
            return False
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        """List available Ollama models."""
        try:
            resp = await self.client.get(f"{self.config.ollama_host}/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                return [m["name"] for m in data.get("models", [])]
            return []
        except Exception:
            return []

    def clear_history(self):
        """Clear conversation history."""
        self.messages.clear()

    async def close(self):
        await self.client.aclose()
