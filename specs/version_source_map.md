---
title: Version Source Map
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Version Source Map

This page defines which USB source materials this repo uses for hub semantics and how version scope should be interpreted.

## Purpose

- Define the source authority hierarchy used by this reference layer.
- Separate normative USB-IF authority from community context.
- Provide a stable starting point for consuming repos to evaluate version scope and staleness.

## Source Categories

| Category | Authority Level | Usage |
|---|---|---|
| USB-IF specification documents | normative_official | Primary source for field and behavior definitions. |
| USB-IF ECNs / addenda | normative_official or official_index | Official deltas and corrections for the baseline. |
| USB-IF index pages | official_index | Canonical navigation to normative package and revision context. |
| Community references | community_reference | Secondary orientation only; never primary claim source. |
| Archive mirrors | archive_reference | Historical fallback when official sources are not directly reachable. |

## Version Summary

| Version | Primary Source | Hub-Relevant Note |
|---|---|---|
| USB 2.0 | USB 2.0 Specification | Primary source boundary for this repo's hub reference layer. |
| USB 2.1 | USB 2.0 / 2.1 LPM and relevant ECN updates | Used only when this repo explicitly documents that delta. |
| USB 3.2 | USB 3.x / USB 3.2 family specs | Out-of-scope as primary authority; reference only for context. |
| USB4 | USB4 specification family | Out-of-scope as primary authority; for cross-family context only. |

## Review Flow

1. Confirm the page claim scope and required USB version.
2. Resolve assertions first from USB-IF spec docs and official index entries.
3. Use community/archive materials only for supporting context.
4. Never replace consuming-repo confirmed implementation facts with this repo's standard-side interpretation.

## Notes

- This repo is a USB-2.0 hub standard-side clarification layer.
- Canonical authority bindings are defined in `contract/*.yaml` and `evidence/source_registry.yaml`.
- Any scope expansion to new version/authority inputs must go through existing review artifacts and evidence updates.
