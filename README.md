# Qimiao Productivity for Dify

Discover Qimiao file creation and processing services, find templates, prepare material uploads, and follow existing tasks from Dify. The remote service includes capabilities such as presentations, covers, websites, music and document/media processing; use its live catalogue for availability.

## Setup

Install the plugin in Dify 1.9.0 or newer with Python plugin runtime 3.12. No provider API key or account connection is required for discovery. The plugin contacts only `https://mcp.longxia.sale/mcp` using the official MCP SDK over Streamable HTTP. It does not run a local production engine.

1. Choose `list_tools` with `{}` to read current input schemas.
2. Choose `get_service_overview` with `{"mode":"compact"}` for capabilities.
3. Choose `get_tool` with `{"tool_id":"ppt-maker"}` for a specific tool.
4. For free material preparation use `prepare_task`, then `get_task_materials`. Users upload files on the returned first-party upload page; this plugin does not read local files or upload file bytes.
5. For an existing task, provide only its own service ID and credential using the exact current schema. Use `get_order`, `get_run_events`, `respond_to_run` or `get_run_result`. Keep returned links and credentials private.

## Scope and service costs

The plugin is free. Production services may be paid and their availability and costs are determined by the remote service. This plugin does not create orders, connect accounts, charge balances, renew purchases, cancel orders or initiate revisions. If a requested production requires a purchase, the user must complete it separately on the first-party service; never represent this plugin as free production. Existing completed tasks can return downloadable artifact links. Downloading or opening those links is a separate user/client action.

## Examples

- Find a suitable PPT template for a concise product introduction.
- Show which tools can add Chinese subtitles to an interview video.
- Check the status of my existing task and return its completed files.

## Security and privacy

`operation` is checked against a fixed allowlist before any request. Arguments must be a JSON object of at most 1 MiB. The endpoint is fixed and redirects are disabled. HTTP and total request timeouts are bounded. No subprocesses, local file operations, arbitrary URLs, account access or payment tools are exposed. Network errors never echo private inputs or SDK exceptions. The plugin does not persist credentials or arguments; Dify and the remote service process supplied content according to their respective policies. See [PRIVACY.md](PRIVACY.md).

Source repository: https://github.com/StarSailAI/qimiao-productivity-integrations

Contact: xingfanai2026@163.com

License: MIT for this integration only. The hosted service and production backend are separate.
