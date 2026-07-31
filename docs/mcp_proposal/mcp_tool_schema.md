# MCP Tool Schema (Tier 1 Pilot)

> **Status**: implemented as a Tier 1 pilot in `mcp-server/`; not part of the
> governed USB reference surface. See [README.md](README.md) for the
> constraints the implementation must honor.
>
> **Protocol alignment**: the current server uses
> `@modelcontextprotocol/sdk` v1 with Streamable HTTP and negotiates the
> legacy 2025-era MCP protocol supported by that SDK and client. It does
> **not** implement or claim MCP `2026-07-28`. A future v2 migration must be
> handled as a separate compatibility slice. The tools remain stateless,
> single-round-trip, and read-only.

## Response envelope (shared by every tool)

Every tool response — success, partial match, or no-match — MUST use this
envelope. No tool may return a bare value without it.

```json
{
  "resultType": "complete",
  "query_echo": "<the input the tool received>",
  "match_found": true,
  "result": [ /* zero or more matched entries, shape defined per tool below */ ],
  "claim_level": "verified | reviewed | not_governed",
  "verified_scope": "<verbatim string from the matched governed_tables[] entry, or null>",
  "reviewed_meaning": "<verbatim string if claim_level=reviewed, else null>",
  "spec_family": "usb20 | usb3 | null",
  "source": {
    "table_id": "<governed_tables[].id>",
    "path": "<governed_tables[].path>",
    "validator": "<governed_tables[].validator>",
    "manifest_version": "0.3"
  },
  "evidence_packet_id": "<id from evidence/entry_verification_packets, or null>",
  "cannot_establish": [
    "firmware_behavior",
    "project_specific_truth",
    "observed_device_behavior",
    "vendor_specific_behavior",
    "LTSSM_runtime_behavior",
    "xHCI_port_management",
    "electrical_or_timing_compliance",
    "USB_IF_certification_completeness"
  ],
  "drift_status": "clean | drift_detected | unknown"
}
```

Each object in `result` also carries its own `claim_level`,
`verified_scope`, `reviewed_meaning`, `spec_family`, `source`, and
`evidence_packet_id`. For a multi-match response, the root fields are a
conservative summary: `claim_level` is `verified` only when every match is
verified, and provenance fields are non-null only when the value is shared by
all matches. A mixed result must never inherit the strongest claim or source
from its first item.

`resultType` is a repository-defined envelope field used by this Tier 1 pilot.
Its presence does not claim MCP `2026-07-28` protocol conformance.

`cannot_establish` is copied verbatim from
`exports/hub_governed_surface_manifest.yaml#/claim_ceiling/cannot_establish`
on every response, regardless of the question asked. It is not conditional —
the agent-side instructions (see
[copilot_studio_agent_instructions.md](copilot_studio_agent_instructions.md))
decide when to surface it to the end user, but the server must always emit it.

If `match_found` is `false`, `result` is an empty array and `claim_level` is
`"not_governed"`. The MCP server must **not** attempt to answer from general
USB knowledge — that is the agent's job to refuse, not the server's job to
guess.

For `lookup_hub_field`, a descriptor field name matches `field_name`; a
characteristics bit group matches `semantic_group`. The parent `field` value
on a bit-group row is not a lookup alias, so querying `wHubCharacteristics`
does not implicitly return every child bit group.

---

## Tool 1 — `lookup_hub_field`

Looks up a hub/port descriptor field or characteristics bit group by name.

- **Source tables**: `usb20_hub_descriptor_field_matrix`,
  `usb3_ss_hub_descriptor_field_matrix`, `usb20_hub_characteristics_bit_matrix`,
  `usb3_ss_hub_characteristics_bit_matrix`, `usb20_hub_interrupt_endpoint_matrix`,
  `usb3_ss_hub_interrupt_endpoint_matrix`

```json
{
  "name": "lookup_hub_field",
  "description": "Look up a USB hub descriptor field, wHubCharacteristics bit group, or hub interrupt endpoint field by name. Returns identity/position/encoding only. Does not return firmware behavior.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "field_name": { "type": "string", "description": "Field name, e.g. bDescLength, wHubCharacteristics, PORT_INDICATOR bit group" },
      "spec_family": { "type": "string", "enum": ["usb20", "usb3", "any"], "default": "any" }
    },
    "required": ["field_name"]
  }
}
```

## Tool 2 — `lookup_feature_selector`

Looks up a `SetFeature`/`ClearFeature` selector by name or numeric value.

- **Source tables**: `usb_hub_feature_selector_matrix`, `usb3_ss_feature_selector_matrix`

```json
{
  "name": "lookup_feature_selector",
  "description": "Look up a USB hub feature selector by name or value (e.g. PORT_RESET, PORT_U1_TIMEOUT). Returns selector name, value, applicable recipient, and spec family. Does not confirm host or firmware runtime behavior when the feature is set.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "selector_name": { "type": "string" },
      "selector_value": { "type": "integer" },
      "spec_family": { "type": "string", "enum": ["usb20", "usb3", "any"], "default": "any" }
    }
  }
}
```

## Tool 3 — `lookup_port_status_bit`

Looks up a `wPortStatus`/`wPortChange`/`wHubStatus`/`wHubChange` bit.

- **Source tables**: `usb20_hub_port_status_bit_matrix`, `usb3_ss_hub_port_status_bit_matrix`

```json
{
  "name": "lookup_port_status_bit",
  "description": "Look up a hub/port status or change bit by name (e.g. C_PORT_CONNECTION, PORT_LINK_STATE). Returns bit name, position, and encoding identity only. For PORT_LINK_STATE and PORT_SPEED specifically, verified_scope covers bit range and encoding table identity only — LTSSM state transitions are never verified by this tool.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "bit_name": { "type": "string" },
      "spec_family": { "type": "string", "enum": ["usb20", "usb3", "any"], "default": "any" }
    },
    "required": ["bit_name"]
  }
}
```

## Tool 4 — `lookup_class_request`

Looks up a hub class request or standard device request.

- **Source tables**: `usb_hub_class_request_matrix`, `usb3_ss_hub_class_request_matrix`,
  `usb20_standard_device_request_matrix`

```json
{
  "name": "lookup_class_request",
  "description": "Look up a USB hub class request or standard device request by name (e.g. SET_HUB_DEPTH, GET_PORT_ERR_COUNT). Returns bRequest, bmRequestType, recipient, and required/optional identity. Does not confirm host driver call sequence or timing.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "request_name": { "type": "string" },
      "spec_family": { "type": "string", "enum": ["usb20", "usb3", "any"], "default": "any" }
    },
    "required": ["request_name"]
  }
}
```

## Tool 5 — `compare_usb_versions`

Cross-references the same named field/bit/selector/request across `usb20` and
`usb3` governed tables side by side.

```json
{
  "name": "compare_usb_versions",
  "description": "Compare a field, bit, selector, or request name across USB 2.0 and USB 3.x governed tables. Returns both entries (or 'not_governed_in_this_family' for the missing side) side by side. Never infers that identical naming implies identical runtime behavior.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "term": { "type": "string" },
      "term_type": { "type": "string", "enum": ["field", "bit", "selector", "request", "any"], "default": "any" }
    },
    "required": ["term"]
  }
}
```

## Tool 6 — `get_verified_evidence`

Given a governed entry id, returns its entry verification packet reference
(not the packet content re-derived or summarized — the raw pointer).

```json
{
  "name": "get_verified_evidence",
  "description": "Given a governed table entry id, return its evidence_packet_id and source table pointer from the manifest. Does not fetch or reinterpret PDF content; the caller must treat this as a citation pointer only.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "table_id": { "type": "string" },
      "entry_id": { "type": "string" }
    },
    "required": ["table_id", "entry_id"]
  }
}
```

## Tool 7 — `check_reserved_usage`

Checks whether a bit position or field range is marked reserved.

- **Source**: `reviewed_meaning` field on any governed table entry.

```json
{
  "name": "check_reserved_usage",
  "description": "Check whether a given bit position, byte range, or field is marked as a reserved boundary placeholder in the governed tables, as a guard against assuming semantic meaning for reserved bits.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "identifier": { "type": "string", "description": "Bit name, byte offset, or field name to check" },
      "spec_family": { "type": "string", "enum": ["usb20", "usb3", "any"], "default": "any" }
    },
    "required": ["identifier"]
  }
}
```

## Tool 8 — `escalate_spec_conflict`

Does **not** resolve a conflict. Formats a standard/project/observed fact
comparison template using this repo's standard-side lookup result plus
caller-supplied project/observed facts, verbatim and unverified.

```json
{
  "name": "escalate_spec_conflict",
  "description": "Format a three-column (standard fact / project fact / observed fact) comparison table for a named field/bit/selector/request. The 'standard fact' column is populated from this repo's governed lookup tools. The 'project fact' and 'observed fact' columns are taken verbatim from caller input and are NOT verified or endorsed by this server. This tool never outputs a resolution or recommendation — only the comparison table plus a fixed disclaimer.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "term": { "type": "string" },
      "project_fact": { "type": "string", "description": "Caller-supplied, verbatim, unverified" },
      "observed_fact": { "type": "string", "description": "Caller-supplied, verbatim, unverified" }
    },
    "required": ["term", "project_fact"]
  }
}
```

## Tool 9 — `get_governed_surface_status`

Exposes manifest freshness and drift status directly, so the agent (and end
user) can see whether the underlying data is currently trusted.

```json
{
  "name": "get_governed_surface_status",
  "description": "Return the current governed surface summary: table counts, verified/reviewed counts per spec family, manifest version, and the last table-fingerprint drift check result. Use this before treating any other tool's output as current if drift_status is not 'clean'.",
  "inputSchema": {
    "type": "object",
    "properties": {}
  },
  "ttlMs": 60000,
  "cacheScope": "public"
}
```

`ttlMs`/`cacheScope` below are design-time advisory hints only. The current
v1 SDK server does not emit or enforce a 2026 `CacheableResult` contract.
Callers must use the returned `drift_status` and their own cache policy.

**Server-side requirement**: before answering `drift_status: "clean"`, the
server must have run `scripts/probe_table_fingerprint.py --mode check`
against `evidence/table_fingerprint_baseline.jsonl` within its own configured
freshness window (e.g., on cache load and on a periodic re-check — exact
interval is an implementation decision, not specified here). If that check has
never run or is stale beyond the configured window, `drift_status` must be
`"unknown"`, not `"clean"`. The server must never fabricate a `"clean"`
result.

---

## Explicitly out of scope for this tool set

No tool in this draft exposes:

- `wiki/**` free-text pages (unstructured; would reintroduce the
  "Copilot mixes governed and non-governed content" risk this design exists
  to avoid).
- `PLAN.md`, `governance/**`, or phase history — internal project process,
  not spec reference.
- Any write, mutate, or file-modification capability. This MCP server is
  read-only by design; there is no tool that accepts a request to change a
  governed table.
