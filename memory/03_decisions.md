# Decisions

## Accepted Decisions

- This repository is read-only spec reference only — no firmware implementation guidance
- Content must always cite the USB-IF spec section number
- Conflicts with project facts must be escalated to the consuming repo, not resolved here
- 2026-05-30: Repository created to support USB-Hub-Firmware-Architecture-Contract
  standard conflict resolution workflow

## Pending Decisions

- Which USB-IF spec version to pin (USB 2.0 Rev 2.0 assumed; USB 3.x hub class differences TBD)
- Whether to include USB 3.x hub class extensions in a separate section

## 2026-07-30 Decisions

- MCP server transport: Streamable HTTP only (Copilot Studio dropped SSE support after August 2025).
- MCP server auth model for pilot: API key (Bearer or `X-MCP-API-Key` header), constant-time comparison, fail-closed (503) if no keys configured. OAuth 2.0 remains a future decision for a non-pilot/enterprise rollout, not built this session.
- MCP server scope: Tier 1 (static identity) only. Tier 2 (LTSSM runtime-semantics state machine) is out of scope until a separate governance decision re-scopes the `cannot_establish: LTSSM_runtime_behavior` claim ceiling.
- Demo hosting for pilot: GitHub Codespaces (temporary, public port-forward), not a substitute for a real internal/company hosting decision (On-Premises Data Gateway question remains open).
