# USB-IF Source Monitor

This monitor tracks source drift from configured URLs.

Each monitored source declares `source_registry_id`, which must point to the
matching entry in `evidence/source_registry.yaml`. The parity validator treats
the authority registry as canonical for URL and authority metadata.

## Scope

- Detects drift signals (status code, content hash, link set hash).
- Writes evidence snapshots and drift events.
- Does not auto-edit wiki or contract files.

## Non-goals

- No automatic semantic validation of USB spec text.
- No automatic promotion of claims to normative.

## Contract Link

Drift effects are governed by `contract/staleness_rules.yaml`.
