# USB-IF Hub Spec Reference — MCP Server

> **Status**: Tier 1 (static identity) implementation. See
> [../docs/mcp_proposal/README.md](../docs/mcp_proposal/README.md) for the
> design constraints this server must honor and
> [../docs/mcp_proposal/mcp_tool_schema.md](../docs/mcp_proposal/mcp_tool_schema.md)
> for the tool contract. **Not yet published/adopted** — this is a working
> implementation used for pilot validation, not a released product.

Exposes the repo's 15 governed USB 2.0 / USB 3.x hub spec tables
(`exports/hub_governed_surface_manifest.yaml`) as 9 read-only MCP tools over
Streamable HTTP, so an MCP client (e.g. Microsoft Copilot Studio) can query
field/bit/selector/request identity instead of reading raw YAML.

## What this server does NOT do

Every tool response carries a `cannot_establish` list
(`firmware_behavior`, `LTSSM_runtime_behavior`, `xHCI_port_management`,
`electrical_or_timing_compliance`, `USB_IF_certification_completeness`,
`observed_device_behavior`, `vendor_specific_behavior`,
`project_specific_truth`). This server only confirms static identity —
field names, bit positions, encodings — never runtime/firmware behavior. See
`../AGENTS.md` for the repo-wide claim boundary this inherits.

## Build & run

```powershell
cd mcp-server
npm install
npm run build
$env:MCP_API_KEYS = "<your-key>"; node dist/index.js
```

In a Codespaces **Bash** terminal, use this equivalent command (do not prefix
`env` with `$`):

```bash
export MCP_API_KEYS='<your-key>'
node dist/index.js
```

- `GET /healthz` — unauthenticated liveness check.
- `ALL /mcp` — MCP JSON-RPC endpoint (Streamable HTTP, stateless — a fresh
  server/transport pair per request). Requires `Authorization: Bearer <key>`
  or `X-MCP-API-Key: <key>`, matching one entry in `MCP_API_KEYS`.

## Demo hosting: GitHub Codespaces (fastest, temporary)

For a one-off demo (not a persistent/production deployment), the fastest
public HTTPS endpoint is a Codespace's forwarded port — no separate hosting
account, and the code is already in this repo:

1. Open a Codespace on this repo.
2. `cd mcp-server && npm install && npm run build`
3. Set a real key in the Codespaces **Bash** terminal:
   `export MCP_API_KEYS='<random-key>'` (or add it as a Codespace secret
   instead of typing it inline).
4. `node dist/index.js`
5. In the **Ports** panel, forward port `8787` and set visibility to
   **Public**. Copy the generated `https://<name>-8787.app.github.dev` URL.
6. In Copilot Studio's MCP onboarding wizard, use that URL as the Server URL,
   authentication type **API key → Header**, header name `X-MCP-API-Key`.

Caveats: the URL changes every time the Codespace is recreated, the
Codespace stops after its idle timeout (so the demo endpoint goes down with
it), and this is a genuinely public endpoint on the internet — the API key
is the only access control. Since this server exposes no confidential data
(only USB-IF public-spec-derived structured metadata, no company secrets),
that exposure is low-risk for a short demo, but this is not a substitute for
deciding real hosting (internal VM + on-prem data gateway vs. a proper public
deployment) before any non-demo rollout — see the conversation in
`../docs/mcp_proposal/README.md`'s open items.

## Environment variables

See [.env.example](.env.example).
