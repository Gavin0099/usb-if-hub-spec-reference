---
title: Version Source Map
claim_level: inferred
status: review_required
last_reviewed: "2026-06-08"
usb_versions:
  - usb_2_0
  - usb_3_2
source_refs:
  - usb20_spec
  - usb32_spec
semantic_verification_claimed: false
---

# Version Source Map

> This page summarizes where to find USB hub-related standards sources.
> It is a source-location map, not a claim that different USB version semantics are interchangeable.

## Purpose

- Help locate official hub-related sources for USB 2.0, 2.1, 3.2, and USB4
- Distinguish normative official, official index, and community-level references
- Support consuming repos when checking version scope and staleness

## Source Categories

| Category | Authority Level | Usage |
|---|---|---|
| USB-IF specification documents | normative_official | Primary source for fields, bits, requests, and semantics |
| USB-IF ECNs / addenda | normative_official or official_index | Version-specific supplements or deltas |
| USB-IF index pages | official_index | Existence, version, and acquisition entry points |
| Community references | community_reference | Helpful for interpretation, but insufficient for normative claims alone |
| Archive mirrors | archive_reference | Availability fallback, not authority promotion |

## Version Summary

| Version | Primary Source | Hub-Relevant Note |
|---|---|---|
| USB 2.0 | USB 2.0 Specification | Current primary anchor for this repo |
| USB 2.1 | USB 2.0 plus LPM / ECN material | Usually a supplement, not a separate hub semantic baseline |
| USB 3.2 | USB 3.2 Specification Rev 1.0 | USB 3.x hub class governed surface added (6 matrices, 53 entries); primary source for SS hub descriptor, port status, characteristics, feature selectors, interrupt endpoint |
| USB4 | USB4 specification family | Not directly equivalent to traditional USB 2.0 hub class semantics |

## Review Flow

1. Confirm the USB version scope of the claim.
2. Go to the corresponding USB-IF specification or official index source.
3. Treat community or archive sources as supporting context only.
4. If the version mapping would affect consuming firmware behavior, enter Standard Escalation Mode first.

## USB 3.2 Governed Surface Summary

This repo's USB 3.2 coverage:

| Category | Section (USB 3.2 Rev 1.0) | Governed State |
|---|---|---|
| SS Hub Descriptor fields | §10.14.2 | 9 entries verified |
| SS Hub Class Requests | §10.14.1 | 10 entries verified |
| SS Port Status / Change bits | §10.14.2 | 15 defined entries verified |
| SS Feature Selectors | §10.14.1 | 6 entries verified |
| SS wHubCharacteristics bits | §10.14.2 Table 10-10 | 4 entries verified, 1 reviewed |
| SS Hub Interrupt Endpoint fields | §10.14.2 | 4 entries verified |

Wiki pages (ZH + EN): 25 pages per locale (CORE, EXT, FULL-1, FULL-2 phases).

## Notes

- This repo was originally scoped as a USB 2.0 hub standard-side reference layer; the USB 3.x governed surface was added in subsequent phases.
- Canonical authority bindings are defined in `contract/*.yaml` and `evidence/source_registry.yaml`.
- Any scope expansion to new version/authority inputs must go through the existing review artifacts and evidence update workflow.

## Reference Navigation

- specs/en/usb2.md: USB 2.0 topic index (en).
- specs/version_source_map.md: 中文對應主題（中文頁）
