#!/usr/bin/env python3
"""Saymon RU Data API — MCP stdio server.

Thin stdio client for the hosted remote MCP endpoint at https://payforapi.com/mcp.

Why a local stdio server at all:
  * MCP clients that only speak stdio (Claude Desktop, Cursor, Cline, ...) can use
    the same paid tool catalogue without an SSE/HTTP-capable client.
  * Introspection (initialize / tools/list) works fully offline — the tool catalogue
    is read from tools.json, so no network or API key is needed to start the server.
  * Tools are paid per call via x402 (USDC on Base mainnet, eip155:8453). No signup,
    no API keys. A call without payment returns the x402 payment requirement, which
    this server passes through to the client unchanged.

Environment:
  PAYFORAPI_MCP_URL  override the hosted endpoint (default https://payforapi.com/mcp)
  PAYFORAPI_TIMEOUT  HTTP timeout in seconds (default 90)
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import anyio
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

HOSTED_URL = os.environ.get("PAYFORAPI_MCP_URL", "https://payforapi.com/mcp")
TIMEOUT = float(os.environ.get("PAYFORAPI_TIMEOUT", "90"))

_HERE = Path(__file__).resolve().parent
TOOLS_SPEC = json.loads((_HERE / "tools.json").read_text(encoding="utf-8"))

server = Server("saymon-ru-data-api")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name=t["name"], description=t["description"], inputSchema=t["inputSchema"])
        for t in TOOLS_SPEC
    ]


def _parse_rpc(body: str) -> dict:
    """Accept both plain JSON and text/event-stream MCP responses."""
    body = body.strip()
    if not body:
        raise ValueError("empty response from hosted MCP endpoint")
    if body.startswith("{"):
        return json.loads(body)
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            return json.loads(line[5:].strip())
    raise ValueError(f"unparsable MCP response: {body[:200]}")


async def _call_hosted(name: str, arguments: dict) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments or {}},
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "saymon-ru-data-api-mcp/1.0 (+https://payforapi.com)",
    }
    async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:
        resp = await client.post(HOSTED_URL, json=payload, headers=headers)
    return _parse_rpc(resp.text)


def _payment_hint(requirement: dict) -> str:
    accepts = (requirement or {}).get("accepts") or []
    if not accepts:
        return (
            "Payment required (x402). Pay per call in USDC on Base — "
            "see https://payforapi.com for payment details."
        )
    a = accepts[0]
    amount = a.get("amount")
    try:
        usd = f"{int(amount) / 1_000_000:.4f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        usd = str(amount)
    return (
        f"Payment required (x402): ${usd} USDC on {a.get('network')} to "
        f"{a.get('payTo')} (asset {a.get('asset')}). "
        "Retry the same call with a signed x402 payment header (X-PAYMENT). "
        "Docs: https://payforapi.com"
    )


@server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    known = {t["name"] for t in TOOLS_SPEC}
    if name not in known:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    try:
        reply = await _call_hosted(name, arguments or {})
    except (httpx.HTTPError, ValueError) as exc:
        return [
            TextContent(
                type="text",
                text=(
                    f"Saymon RU Data API is unreachable ({type(exc).__name__}: {exc}). "
                    f"Endpoint: {HOSTED_URL}. Retry shortly or check https://payforapi.com/health"
                ),
            )
        ]

    if "error" in reply:
        err = reply["error"]
        return [TextContent(type="text", text=f"MCP error {err.get('code')}: {err.get('message')}")]

    result = reply.get("result") or {}
    structured = result.get("structuredContent")
    if result.get("isError"):
        # x402 payment requirement (or a tool-level failure) — pass it through verbatim
        # plus a human-readable hint so agents know how to complete the payment.
        parts = [c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"]
        text = "\n".join(p for p in parts if p)
        if structured and "accepts" in structured:
            text = f"{_payment_hint(structured)}\n\nRaw x402 requirement:\n{json.dumps(structured, ensure_ascii=False)}"
        return [TextContent(type="text", text=text or "Tool call failed.")]

    texts = [c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"]
    body = "\n".join(t for t in texts if t)
    if structured is not None:
        try:
            body = json.dumps(structured, ensure_ascii=False)
        except (TypeError, ValueError):
            pass
    return [TextContent(type="text", text=body or "(empty result)")]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    anyio.run(main)
