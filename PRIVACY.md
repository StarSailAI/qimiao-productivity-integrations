# Privacy policy

This policy covers the Qimiao Productivity Dify integration, maintained by StarSailAI.

## Data sent

The plugin transmits the selected operation and its JSON arguments to `https://mcp.longxia.sale/mcp`. Depending on the selected operation, this can include search queries, template requirements, task requirements, draft or task identifiers, per-task access credentials, file identifiers and replies to a running task. The service can return private task state, upload links, download links and credentials. Users should supply only content they are authorized to process. Discovery does not require account credentials.

## Storage and logging

The plugin has no persistent storage, analytics or logging of user arguments or task credentials. Values exist in memory for the bounded request. Dify can retain workflow inputs and outputs under the operator's Dify configuration and privacy policy (https://dify.ai/privacy). Do not publish workflow traces containing credentials. The Qimiao service stores submitted task data and artifacts under its current service rules; this plugin does not override retention or promise automatic deletion. Read `get_service_rules` before submitting private content. Contact support for current retention and deletion arrangements.

## Destinations and boundaries

Runtime MCP requests go only to `mcp.longxia.sale` over HTTPS, with redirects disabled. The user may separately open first-party links returned by the service. The plugin does not fetch those links or send data to an additional provider. File production, where used outside this plugin, can involve providers described by the remote service; do not submit confidential or sensitive content without reviewing those current arrangements. No user account connection, balance access, order creation or payment operation is exposed by this plugin.

## Contact

For access, privacy or deletion questions: xingfanai2026@163.com.
