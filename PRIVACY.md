# Privacy policy

This policy covers the Qimiao Productivity Dify integration maintained by StarSailAI.

## Data transmitted and purposes

The plugin transmits the selected operation and its JSON arguments over HTTPS to `https://mcp.longxia.sale/mcp` to discover services, prepare materials, create a service agreement/order, follow production and return files. Depending on the operation, inputs include search queries, requirements, template choices, source URLs allowed by the chosen service, draft/task/file identifiers, per-task access credentials, interaction replies, change requests and idempotency keys. Outputs can include private material summaries, task state, access/recovery credentials, upload links, checkout links and result/download links. Public discovery requires no Qimiao account or API key.

Optional account operations send the user-provided connection ID and connection credential to that same service. The returned account information can include masked identity, balance and grant state. `pay_with_balance` sends the service/contract references, account connection references, the exact confirmed amount/currency, and any applicable confirmation token to authorize that specific service-balance charge. This is financial and authentication data. Account linking alone is not consent to spend. Passwords, Alipay credentials, bank-card details and login verification codes are not requested by the plugin and must remain on the relevant first-party login/payment pages.

## Storage, access and logging

The plugin has no persistent storage, analytics or logging of user arguments, credentials or financial confirmations. Values exist in memory for the bounded invocation. **Dify can retain workflow inputs and outputs**, including credentials and private links, according to the workspace operator's configuration and privacy policy (https://dify.ai/privacy). Access to apps, traces and results must be restricted. Do not publish traces containing real user data, share account grants across unrelated users, or expose task credentials and owner-checkout links in public examples.

The Qimiao service stores submitted task data, billing records and artifacts under its current service rules. This client does not override retention or promise automatic deletion. Read `get_service_rules` and the selected tool's data arrangements before submitting sensitive content. Contact support for retention and deletion requests. Users can revoke an account connection through `disconnect_account` or the first-party account management interface; revocation does not imply deletion of billing records.

## Destinations and external payments

All runtime MCP calls go to `mcp.longxia.sale`, with verified TLS and redirects disabled. The plugin does not fetch checkout/upload/download URLs. Users may separately open the returned first-party Qimiao pages. Anonymous checkout does not require a Qimiao account; actual Alipay authentication and payment happen outside Dify through the first-party checkout and payment provider. Merchant keys remain on the Qimiao server and are not supplied to the plugin. Payment providers process transaction data under their own policies. The production service can use processing providers described by its live tool/service rules; this adapter does not make a local-only processing promise.

The service's confirmed payment state is authoritative; a browser return URL does not prove payment. The adapter does not retry spending automatically or invent user consent. It exposes neither general money transfer nor a refund API. Billing disputes use the service's support procedure.

## Contact

For access, privacy, billing or deletion questions: xingfanai2026@163.com.
