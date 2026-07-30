# MCP Integration Proposal — Draft Index

> **Status**: DRAFT / PROPOSAL — not adopted, not part of the governed surface.
> **Claim ceiling**: `proposal_only`. Nothing in this folder is validated, tracked,
> or referenced by `exports/hub_governed_surface_manifest.yaml`.
> **Owner decision required before build**: this folder documents a design, not
> an approved implementation plan.

## Why this exists

This repo's governed reference surface (`exports/hub_governed_surface_manifest.yaml`,
15 tables, USB 2.0 + USB 3.x) is a candidate data source for a read-only MCP
(Model Context Protocol) server, to be consumed by Microsoft Copilot Studio or
other MCP clients. This folder drafts what that integration would look like
**without** building it yet.

## Contents

- [mcp_tool_schema.md](mcp_tool_schema.md) — draft MCP tool definitions
  (input schema, response envelope, source-table mapping) for exposing the 15
  governed tables as query tools instead of raw file access.
- [copilot_studio_agent_instructions.md](copilot_studio_agent_instructions.md) —
  draft system/topic instructions for a Copilot Studio agent consuming this
  MCP server, including mandatory refusal rules and a red-team test checklist.

## Non-negotiable design constraints carried over from this repo's governance

These are not new rules — they are restatements of existing constraints this
proposal must not weaken:

1. **Manifest is the only entry point.** No tool may read `tables/*.yaml`
   directly; every tool response must be traceable to a `governed_tables[]`
   entry in the manifest (`id`, `path`, `validator`, `verified_scope`).
2. **`claim_ceiling.cannot_establish` travels with every answer.** Per
   `exports/hub_governed_surface_manifest.yaml`, this MCP server can never
   assert firmware behavior, LTSSM runtime behavior, xHCI port management,
   electrical/timing compliance, or USB-IF certification completeness — the
   response envelope must carry this list, not just the source table.
3. **Drift-awareness is mandatory, not optional.** Any caching layer in the
   MCP server must be validated against
   `evidence/table_fingerprint_baseline.jsonl` via
   `scripts/probe_table_fingerprint.py` before being trusted as current.
   Serving stale governed data silently is a governance violation, not just a
   staleness bug.
4. **Standard vs. project fact conflicts are not resolved here.** Per
   `AGENTS.md`, this repo (and by extension its MCP surface) only supplies the
   standard-side input; conflict resolution belongs to the consuming repo's
   escalation process.

## Open items before implementation

- [x] Decided MCP transport hosting: Streamable HTTP only (SSE is unsupported
  by Copilot Studio after August 2025 — confirmed against Microsoft Learn).
  Implemented in `mcp-server/src/index.ts` via
  `StreamableHTTPServerTransport({ sessionIdGenerator: undefined })`
  (stateless mode — a fresh `McpServer`/transport pair per request).
- [x] Decided auth model for pilot: API key (owner choice, 2026-07-30).
  Implemented in `mcp-server/src/auth.ts` — `Authorization: Bearer <key>` or
  `X-MCP-API-Key` header, constant-time comparison via
  `crypto.timingSafeEqual`, fails closed (503) if `MCP_API_KEYS` is unset.
  Enterprise rollout (OAuth 2.0) remains a future decision, not built.
- [x] `AskAI.vue`'s browser-side Anthropic key pattern has been removed
  (component and its usage in `.vitepress/theme/index.ts` deleted; site build
  verified). This MCP proposal is now the only planned AI-query path for this
  repo's governed surface.
- [x] Resolved `usb32_spec_page` source provenance: the underlying normative
  gap is closed by registering `usb32_spec` (authority_level
  `normative_official`, fetch-verified official document page) in
  `evidence/source_registry.yaml`. `usb32_spec_page` itself remains
  `discovery_only` by design (it is an index page, not a document page) and
  now cross-references `usb32_spec` in its notes. Residual, intentionally
  unresolved: the `archive_usb32_pdf` fallback_source_id referenced by the 48
  `evidence/entry_verification_packets/usb3/*.yaml` packets is NOT registered
  — no verifiable free mirror exists (archive.org search returned zero
  results) and USB-IF's document-library terms prohibit redistributing the
  actual spec file, so it is not committed into this repo either. This is
  documented as an accepted residual gap in `evidence/source_registry.yaml`'s
  top-level `notes`.
- [x] Registered this folder (`README.md`, `mcp_tool_schema.md`,
  `copilot_studio_agent_instructions.md`) in `contract.yaml`'s `documents`
  list (2026-07-30), for governance tracking/freshness purposes only. At the
  time of that registration this did not change the status above (still
  DRAFT/PROPOSAL, `proposal_only`, no implementation started). That has since
  changed — see the next item.
- [x] MCP Server implementation started and built (2026-07-30, owner
  decision "前置作業做完就可以開始動工MCP"): `mcp-server/` (Node.js/TypeScript,
  `@modelcontextprotocol/sdk`) implements all 9 tools from
  `mcp_tool_schema.md`, Streamable HTTP transport, and API key auth. `tsc`
  build passes with 0 errors. This is **Tier 1 only** (static identity —
  field/bit/selector/request lookup over the 15 governed tables); it is not
  the runtime-semantics/state-machine layer discussed separately for a
  possible future Tier 2 (e.g. LTSSM transition validation), which remains
  unbuilt and would require its own governed table + evidence packets +
  explicit `claim_ceiling` re-scoping before any work starts.
- [x] Tier 1 pilot validation — server-side only (2026-07-30): ran the MCP
  server locally and issued live `tools/call` requests covering red-team
  checklist rows 1, 2/3 (grounding only), 4, 5, 6, 9 from
  `copilot_studio_agent_instructions.md`. Confirmed the server itself
  correctly emits `match_found`, `claim_level`, `verified_scope`,
  `cannot_establish` (always includes `LTSSM_runtime_behavior` and
  `USB_IF_certification_completeness`), and refuses to guess values for
  fabricated/non-existent terms (`match_found: false`, `claim_level:
  not_governed`, empty `result`). `escalate_spec_conflict` correctly marks
  caller-supplied `project_fact`/`observed_fact` as `verified: false,
  source: caller_supplied` and never declares a winner.
  **Not claimed**: rows 3 (social-engineering rephrasing resistance), 7
  (live drift-detected surfacing to an agent), and 8 (agent attaching
  disclaimer to generated code) test *agent* behavior under a live Copilot
  Studio deployment with the system instructions loaded — this requires an
  actual Copilot Studio connector, which has not been provisioned. Per
  `copilot_studio_agent_instructions.md`, a failure on those rows would be a
  finding against the agent configuration, not the MCP server; server-side
  data correctness for those rows was spot-checked (drift_status field
  present and reads `"clean"`; every result item carries `claim_level` for
  the agent layer to surface) but the enforcement behavior itself is
  untested.

