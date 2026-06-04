---
title: Version Source Map
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
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
| USB 3.2 | USB 3.x / USB 3.2 family specs | May introduce architecture and terminology changes not equivalent to USB 2.0 hub semantics |
| USB4 | USB4 specification family | Not directly equivalent to traditional USB 2.0 hub class semantics |

## Review Flow

1. Confirm the USB version scope of the claim.
2. Go to the corresponding USB-IF specification or official index source.
3. Treat community or archive sources as supporting context only.
4. If the version mapping would affect consuming firmware behavior, enter Standard Escalation Mode first.

## Notes

- This page does not assert that USB 2.0, 2.1, 3.2, and USB4 hub semantics are directly interchangeable.
- If a new version document enters the source registry, this repo should sync checks for `contract/*.yaml` and `evidence/source_registry.yaml`.
- Any high-confidence claim based on this page still requires returning to the corresponding normative official source for the target version.
