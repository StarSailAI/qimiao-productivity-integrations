"""Fixed-service MCP adapter for discovery, production and authorized commerce.

All account permissions, per-order confirmation, ownership, idempotency and
billing checks remain enforced by the existing Qimiao service. This adapter
does not infer consent, insert confirmation fields or retry write operations.
"""
import asyncio
import json
import ssl
import certifi
import httpx2
from gevent import get_hub, monkey
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

ENDPOINT = "https://mcp.longxia.sale/mcp"
ALLOWED = frozenset({
    "get_service_overview", "get_service_rules", "search_tools", "get_tool",
    "search_templates", "prepare_task", "get_task_materials", "quote_order",
    "renew_quote", "create_order", "get_order", "wait_order", "get_run_events",
    "respond_to_run", "get_run_result", "request_change", "resume_order",
    "cancel_order", "connect_account", "get_connected_account",
    "disconnect_account", "pay_with_balance",
})
MAX_INPUT_BYTES = 1024 * 1024


def parse_arguments(raw):
    if not isinstance(raw, str) or len(raw.encode("utf-8")) > MAX_INPUT_BYTES:
        raise ValueError("Arguments must be a JSON object of at most 1 MiB.")
    try:
        result = json.loads(raw or "{}")
    except (ValueError, RecursionError):
        raise ValueError("Arguments must be valid JSON.") from None
    if not isinstance(result, dict):
        raise ValueError("Arguments must be one JSON object.")
    return result


async def call_remote(operation, arguments):
    async with asyncio.timeout(90):
        # Explicit verified TLS context avoids macOS truststore/gevent recursion.
        tls = ssl.create_default_context(cafile=certifi.where())
        async with httpx2.AsyncClient(timeout=40, follow_redirects=False, verify=tls) as http:
            async with streamable_http_client(ENDPOINT, http_client=http, max_sse_event_size=8 * 1024 * 1024) as streams:
                async with ClientSession(streams[0], streams[1], read_timeout_seconds=60) as session:
                    await session.initialize()
                    if operation == "list_tools":
                        result = await session.list_tools()
                        payload = result.model_dump(mode="json", by_alias=True, exclude_none=True)
                        payload["tools"] = [tool for tool in payload.get("tools", []) if tool.get("name") in ALLOWED]
                        return payload
                    result = await session.call_tool(operation, arguments)
                    return result.model_dump(mode="json", by_alias=True, exclude_none=True)


def _run(operation, arguments):
    return asyncio.run(call_remote(operation, arguments))


def invoke(operation, raw="{}"):
    # Validate before opening any network connection; never proxy an arbitrary tool.
    if not isinstance(operation, str) or operation not in ALLOWED | {"list_tools"}:
        return {"isError": True, "error": "Unsupported operation. Use list_tools for this plugin's supported operations."}
    try:
        arguments = parse_arguments(raw)
    except ValueError as error:
        return {"isError": True, "error": str(error)}
    try:
        if monkey.is_module_patched("threading"):
            # Dify dispatches concurrent greenlets. Each asyncio loop must run in
            # its own native worker, never share a loop across greenlets.
            return get_hub().threadpool.spawn(_run, operation, arguments).get(timeout=95)
        return _run(operation, arguments)
    except Exception:
        # SDK/HTTP exceptions can contain task credentials. Do not echo or log them.
        return {"isError": True, "error": "Qimiao service request failed or timed out. Check connectivity and the original task status before retrying."}
