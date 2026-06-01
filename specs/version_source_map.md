---
title: USB Version Source Map (Hub-Focused)
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Version Source Map (Hub-Focused)

> Usage: Reference layer only. Do not use to override confirmed project facts.
> Last verified: 2026-05-30

## Scope Notes

- This file maps **where to find official USB-IF sources** for hub-related behavior across USB 2.0, 2.1, 3.2, and 4.0 naming.
- This is a source index, not a firmware requirement document.
- Normative claim policy is governed by `contract/*.yaml`, not by this file alone.

## Authority and Usage Rule

Use source types with explicit authority boundaries:

| Source Type | Primary Authority Use | Notes |
|---|---|---|
| USB-IF official specifications | Yes (normative) | Use for descriptor/request/state/field definitions. |
| USB-IF ECN/addendum | Yes (normative delta) | Must indicate applicable base version and scope. |
| USB-IF compliance/test specs | Auxiliary | Use for validation/compliance interpretation, not sole base definitions. |
| USB-IF document library/search/index pages | Discovery only | Use for locating official documents and lineage tracking. |
| Community references (e.g., OSDev) | Non-normative | Use for fast orientation/cross-check only. |
| Mirrors (e.g., Archive.org) | Fallback only | Use for traceability when official link access is blocked. |

See also:

- `contract/authority_levels.yaml`
- `contract/claim_rules.yaml`
- `contract/evidence_requirements.yaml`
- `contract/version_scope.yaml`

## Version Classification (Hub First)

| Version Label | Official Source Anchor | Hub-Relevant Interpretation | Source Type |
|---|---|---|---|
| USB 2.0 | USB-IF Document Library: USB 2.0 Specification | Primary normative source for classic hub class semantics (descriptor 0x29, port status/change bits, hub class requests, TT behavior in HS hubs). | Core base spec + ECNs bundle |
| USB 2.1 (industry shorthand) | USB 2.0 page file contents include "USB 2.0 Link Power Management Addendum ECN" and later USB 2.0 ECNs | No separate standalone "USB 2.1" base spec in USB-IF library. Treat as USB 2.0 + ECN/addenda set when comparing hub behavior. | ECN/addendum set under USB 2.0 |
| USB 3.2 | USB-IF USB 3.2 technology page + USB 3.2 spec document library entry | USB 3.x hub behavior is covered by USB 3.2 family materials; USB-IF states USB 3.2 absorbed prior 3.x specs and includes minor hub spec update for lane transition behavior. | 3.2 umbrella spec + compliance/docs |
| USB4 (4.0 naming) | USB-IF USB4 specification page (currently USB4 v2.0 page) | USB4 system behavior is specified in USB4 docs; USB4 topology includes hub-equivalent routing entities, while backward compatibility paths retain USB 3.2/2.0 tunneling context. | USB4 base spec line |

## Practical Retrieval Order (for Future Spec Extraction)

1. Pull the official USB-IF Document Library page for the target generation.
2. Download the cited base package (zip/pdf) and capture exact section numbers in downstream files.
3. For "USB 2.1" requests, resolve to USB 2.0 + specific ECN/addendum item names (do not treat as independent base revision).
4. If hub semantics appear to differ from confirmed firmware facts, escalate in consuming repo per Standard Escalation Mode.

## Primary Links

- USB 2.0 Specification (USB-IF): https://www.usb.org/document-library/usb-20-specification
- USB 3.2 page (USB-IF): https://www.usb.org/usb-32-0
- USB 3.2 compliance/index page (USB-IF): https://www.usb.org/usb-32
- USB4 specification page (USB-IF, redirects to current USB4 v2.0 entry): https://www.usb.org/document-library/usb4tm-specification
- USB4 v2.0 page (USB-IF): https://www.usb.org/document-library/usb4r-specification-v20

## Secondary/Discovery Links (non-authoritative)

- USB-IF document search entry point: https://www.usb.org/documents
- Prior discovery query used by user workflow: https://www.usb.org/documents?search=hub&tid_2%5B0%5D=40&items_per_page=50
- OSDev USB Hubs page (background only): https://wiki.osdev.org/USB_Hubs
- Archive.org USB 2.0 mirror page: https://archive.org/details/USB-2.0
- Archive.org mirrored USB 2.0 PDF: https://archive.org/download/USB-2.0/Universal%20Serial%20Bus%20Specification%2C%20Revision%202.0.pdf

## Verification Caveat

Some USB-IF pages are dynamically rendered and may be difficult to open through certain tooling. When this occurs, keep the canonical USB-IF URL recorded and verify content by direct browser access in a normal environment.
