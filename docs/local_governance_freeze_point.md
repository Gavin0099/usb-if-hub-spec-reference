# Local Governance Freeze Point

> **Status**: Active  
> **Established**: 2026-05-30  
> **Purpose**: Prevent governance loop by defining the ceiling of local governance investment.

## Why This Document Exists

This repository can fall into a governance loop:

> supplement validator → supplement contract binding → supplement CI →
> supplement receipt → supplement audit → supplement the audit's audit → …

This loop produces governance infrastructure that is never consumed by a real use case.

This document defines the **freeze point**: the level of local governance this repository targets before exporting its first authority surface to a consuming repository.

**The goal is to be useful to a consuming repo, not to achieve internal governance perfection.**

---

## The Five-Layer Gap

The following layers are distinct and must not be conflated:

| Layer | Meaning | Current Status |
|-------|---------|----------------|
| **L1** script exists | A validator script is present in `scripts/` | ✓ Present |
| **L2** contract declared | `contract.yaml` lists the validator in `validators:` | ✗ `validators: []` |
| **L3** CI runs | A GitHub Actions workflow actually executes the validator | ✓ Partial (fixture smoke only, see G1) |
| **L4** framework invokes | The ai-governance-framework runtime calls the validator | ✗ Unconfirmed |
| **L5** consumer uses | A consuming repo reads and enforces the result | ✗ Not started |

**L1 → L2 → L3 → L4 → L5 are not transitive.**  
Presence at any layer does not imply presence at higher layers.

### Implication for `contract.yaml`

`contract.yaml` currently has `validators: []`. Even if validators are added to this field in the future, that entry is a **documentation inventory**, not a runtime binding, unless the ai-governance-framework runtime is confirmed to read and invoke it. Do not treat `contract.yaml` validator entries as execution guarantees.

---

## Freeze Criteria

Local governance is considered frozen at a level sufficient to export the first authority surface when the following conditions hold:

1. **Validator scripts exist** — covering structural invariants for the content being exported.
2. **Fixture smoke can run** — deterministic fixture tests protect validator logic from regression.
3. **Real repo validation can run manually or as advisory CI** — not required to be a blocking gate.
4. **Receipts are marked with ceiling and non-goals** — so consumers understand what the receipt does and does not certify.
5. **No false upgrade of claim levels** — no content entry is marked `verified` without PDF section-level review evidence.

These five criteria define the freeze point. **No further local governance work is required before the first export.**

---

## What This Repository Currently Has

As of the freeze point date:

- **L1** — 18+ validator scripts in `scripts/`, covering source registry, reachability, wiki frontmatter, source coverage, staleness impact, class request matrix, and class request coverage.
- **L2** — `contract.yaml` has `validators: []`. Not filled. Intentional: see above.
- **L3** — Fixture smoke CI (required gate) established. Real content validation CI (advisory) established.
- **L4** — Framework runtime invocation: unconfirmed. Not a freeze requirement.
- **L5** — Consumer enforcement: not started. Not a freeze requirement.

**Content state:**
- `tables/class_request_matrix.yaml`: 10 entries, USB 2.0 hub class requests, `claim_level: inferred`, `evidence_status: review_required`.
- `evidence/source_registry.yaml`: source definitions with authority levels.
- `specs/`: hub descriptor, port status bits, hub class requests, transaction translator, escalation table.

---

## What Cannot Be Claimed

The following claims are **prohibited** at the current freeze point:

| Prohibited Claim | Reason |
|-----------------|--------|
| "Governance framework runtime enforcement complete" | L4 unconfirmed |
| "All validators are executed by the framework" | L4 unconfirmed |
| "CI fully protects all repo governance" | Advisory CI is not a blocking gate |
| "Consumer-side enforcement complete" | L5 not started |
| "USB 2.0 class request set complete" | `GET_DESCRIPTOR` / `SET_DESCRIPTOR` not yet extracted |
| "USB 2.0 spec PDF section-level verified" | All entries are `claim_level: inferred` |
| "USB 3.2 / USB4 hub content covered" | Out of scope at freeze point |

---

## Governance Non-Goals (Frozen Out)

The following items are **explicitly out of scope** until a consuming repo provides feedback that demands them:

- Filling `contract.yaml validators:` to create the appearance of framework binding.
- Achieving 100% internal governance maturity before the first export.
- Expanding class request coverage beyond the minimum viable export surface.
- Building consumer-side enforcement before the first consumer use case is defined.
- Adding audit trails for the audit trails.

---

## What Comes Next

After the first export surface (`exports/usb20_hub_class_request_manifest.yaml`) is consumed by a real repo, the next governance investment is determined by **consumer feedback**, not by internal completeness metrics.

Candidate next steps (priority to be decided post-consumer feedback):
- Phase 3E: USB 2.0 class request family coverage report
- Phase 3F: `GET_DESCRIPTOR` / `SET_DESCRIPTOR` setup entries
- Phase 4A: Port/hub status matrix scaffold
- Feature selector matrix
- USB 3.2 / USB4 delta
