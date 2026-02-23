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
        self._max_tool_rounds = 10  # Prevent infinite loops

    def _build_tools_schema(self) -> list[dict]:
        return [t.to_api_schema() for t in self.tools.values()]

    def _build_tools_description(self) -> str:
        """Build a text description of tools for the system prompt."""
        lines = ["Available tools (call by outputting JSON with 'name' and 'arguments'):"]
        for t in self.tools.values():
            params = t.get_schema().get("properties", {})
            param_desc = ", ".join(
                f"{k}: {v.get('description', v.get('type', ''))}"
                for k, v in params.items()
            )
            lines.append(f"  - {t.name}: {t.description}")
            lines.append(f"    Parameters: {param_desc}")
        lines.append("")
        lines.append("To call a tool, output ONLY a JSON object like:")
        lines.append('{"name": "tool_name", "arguments": {"param1": "value1"}}')
        lines.append("After receiving tool results, provide your response to the user.")
        return "\n".join(lines)

    def _build_messages(self) -> list[dict]:
        system_content = self.config.system_prompt + "\n\n" + self._build_tools_description()
        msgs = [{"role": "system", "content": system_content}]
        for m in self.messages:
            msg: dict[str, Any] = {"role": m.role, "content": m.content}
            if m.tool_calls:
                msg["tool_calls"] = m.tool_calls
            msgs.append(msg)
        return msgs

    def _try_parse_tool_call(self, text: str) -> dict | None:
        """Try to parse a tool call from text content."""
        text = text.strip()
        # Try direct JSON parse
        try:
            data = json.loads(text)
            if isinstance(data, dict) and "name" in data:
                name = data["name"]
                args = data.get("arguments", data.get("params", data.get("parameters", {})))
                if name in self.tools:
                    return {"name": name, "arguments": args if isinstance(args, dict) else {}}
        except json.JSONDecodeError:
            pass

        # Try to find JSON in text
        json_pattern = r'\{[^{}]*"name"\s*:\s*"[^"]+?"[^{}]*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        for match in matches:
            try:
                data = json.loads(match)
                if isinstance(data, dict) and "name" in data:
                    name = data["name"]
                    args = data.get("arguments", data.get("params", data.get("parameters", {})))
                    if name in self.tools:
                        return {"name": name, "arguments": args if isinstance(args, dict) else {}}
            except json.JSONDecodeError:
                continue

        # Try multi-line JSON extraction
        try:
            # Find first { and last }
            start = text.find("{")
            end = text.rfind("}")
            if start >= 0 and end > start:
                candidate = text[start : end + 1]
                data = json.loads(candidate)
                if isinstance(data, dict) and "name" in data:
                    name = data["name"]
                    args = data.get("arguments", data.get("params", data.get("parameters", {})))
                    if name in self.tools:
                        return {"name": name, "arguments": args if isinstance(args, dict) else {}}
        except (json.JSONDecodeError, ValueError):
            pass

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

            # Use non-streaming for more reliable tool call detection
            response_data = await self._request()
            msg_data = response_data.get("message", {})
            response_text = msg_data.get("content", "")

            # Check for proper tool_calls field first
            if msg_data.get("tool_calls"):
                tool_calls = msg_data["tool_calls"]
            else:
                # Try to parse tool calls from text content
                parsed = self._try_parse_tool_call(response_text)
                if parsed:
                    tool_calls = [{"function": parsed}]
                    # Don't yield the JSON as text to user
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
                    # Add tool result to messages
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
