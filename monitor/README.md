# USB-IF Source Monitor

This monitor tracks source drift from configured URLs.

## Scope

- Detects drift signals (status code, content hash, link set hash).
- Writes evidence snapshots and drift events.
- Does not auto-edit wiki or contract files.

## Non-goals

- No automatic semantic validation of USB spec text.
- No automatic promotion of claims to normative.

## Contract Link

Drift effects are governed by `contract/staleness_rules.yaml`.
