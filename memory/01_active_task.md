# Active Task

## Current Task

Phase 8 — Entry-level verification pipeline for `tables/port_status_bit_matrix.yaml`.

The repo is a controlled read-only spec reference layer. Phase 8 is establishing a narrow, reviewable evidence trail before any entry-level verified promotion.

## Active History

- 2026-06-02: Phase 8A–8G completed. One verified pilot (wPortStatus.bit0.PORT_CONNECTION, bit_name_and_position_only). Phase 8G adds a non-promoting reviewed packet for wPortStatus.bit1.PORT_ENABLE.
- 2026-06-02: Repository-level governance and technical audit recorded in memory/04_review_log.md.

## Phase 8 Pilot Boundary (live)

| Entry | claim_level | packet status | eligible_for_verified |
|---|---|---|---|
| wPortStatus.bit0.PORT_CONNECTION | verified | reviewed_pilot | true (promoted) |
| wPortStatus.bit1.PORT_ENABLE | inferred | reviewed | false (non-promoting) |

## Next Action

- Phase 8H: Decide whether to expand the pilot boundary to include PORT_ENABLE, or continue expanding the reviewed-non-promoting packet surface for additional bits.
- Prerequisite: Gate update required before any second verified promotion.

## 2026-07-30 Update

- New parallel workstream: MCP server (Tier 1, static-identity only) implemented under `mcp-server/` — Streamable HTTP transport, API-key auth, all 9 read-only lookup tools wrapping the existing governed tables. Build passes (`tsc`), server-level red-team-checklist validation passed for 6 of 9 checklist rows (agent-layer rows 3/7/8 explicitly not claimed — require a live Copilot Studio deployment).
- Tier 2 (LTSSM runtime-semantics state machine) is explicitly deferred pending owner decision; not started.
- Current next action: stand up a temporary public demo endpoint via GitHub Codespaces (port 8787, Public visibility) to hand a working MCP URL to Copilot Studio's onboarding wizard. This does not change or supersede the Phase 8H port-status-bit-matrix pilot boundary above.
