"""HealthAdvocate stdio MCP server."""

from __future__ import annotations

import json
import sys
from typing import Any

from .cli import denial_checklist, project_brief, server_health, visit_questions

PROTOCOL_VERSION = "2024-11-05"

TOOLS = {
    "healthadvocate_project_brief": {
        "description": "Return HealthAdvocate identity, surfaces, and medical boundary.",
        "handler": lambda _args: project_brief(),
        "inputSchema": {"type": "object", "properties": {}},
    },
    "prepare_visit_questions": {
        "description": "Create patient-friendly appointment questions for a stated concern.",
        "handler": visit_questions,
        "inputSchema": {
            "type": "object",
            "properties": {
                "concern": {"type": "string"},
                "context": {"type": "string"},
            },
            "required": ["concern"],
        },
    },
    "insurance_denial_checklist": {
        "description": "Create an appeal checklist for an insurance denial reason.",
        "handler": denial_checklist,
        "inputSchema": {
            "type": "object",
            "properties": {"denial_reason": {"type": "string"}},
            "required": ["denial_reason"],
        },
    },
    "healthadvocate_server_health": {
        "description": "Check the local HealthAdvocate FastAPI health endpoint.",
        "handler": server_health,
        "inputSchema": {
            "type": "object",
            "properties": {"url": {"type": "string", "default": "http://127.0.0.1:8080"}},
        },
    },
}


def handle_tool_call(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    return TOOLS[name]["handler"](arguments or {})


def _tool_list() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "description": spec["description"],
            "inputSchema": spec["inputSchema"],
        }
        for name, spec in TOOLS.items()
    ]


def _response(message_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def _error(message_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}


def handle_message(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    message_id = message.get("id")
    params = message.get("params") or {}
    if message_id is None:
        return None
    if method == "initialize":
        return _response(
            message_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "healthadvocate", "version": "1.0.0"},
            },
        )
    if method == "tools/list":
        return _response(message_id, {"tools": _tool_list()})
    if method == "tools/call":
        try:
            result = handle_tool_call(params.get("name", ""), params.get("arguments") or {})
            return _response(
                message_id,
                {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]},
            )
        except ValueError as exc:
            return _error(message_id, -32602, str(exc))
    return _error(message_id, -32601, f"Unsupported method: {method}")


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            reply = handle_message(json.loads(line))
        except json.JSONDecodeError as exc:
            reply = _error(None, -32700, f"Invalid JSON: {exc}")
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
