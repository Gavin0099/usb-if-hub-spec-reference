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
| USB 3.2 | USB 3.2 Specification Rev 1.0 | USB 3.x hub class governed surface added (6 matrices, 53 entries); primary source for SS hub descriptor, port status, characteristics, feature selectors, interrupt endpoint. |
| USB4 | USB4 specification family | Out-of-scope as primary authority; for cross-family context only. |

## Review Flow

1. Confirm the page claim scope and required USB version.
2. Resolve assertions first from USB-IF spec docs and official index entries.
3. Use community/archive materials only for supporting context.
4. Never replace consuming-repo confirmed implementation facts with this repo's standard-side interpretation.

## USB 3.2 Governed Surface Summary

本 repo 對 USB 3.2 的覆蓋範圍：

| 類別 | 章節（USB 3.2 Rev 1.0） | Governed 狀態 |
|---|---|---|
| SS Hub Descriptor fields | §10.14.2 | 9 entries verified |
| SS Hub Class Requests | §10.14.1 | 10 entries verified |
| SS Port Status / Change bits | §10.14.2 | 15 defined entries verified |
| SS Feature Selectors | §10.14.1 | 6 entries verified |
| SS wHubCharacteristics bits | §10.14.2 Table 10-10 | 4 entries verified, 1 reviewed |
| SS Hub Interrupt Endpoint fields | §10.14.2 | 4 entries verified |

Wiki 頁面（ZH + EN）：25 頁每語系（含 CORE、EXT、FULL-1、FULL-2）。

## Notes

- 本 repo 最初定位為 USB 2.0 hub 標準側說明層；USB 3.x governed surface 已於後續階段加入。
- 正式 authority bindings 定義於 `contract/*.yaml` 與 `evidence/source_registry.yaml`。
- 任何新 version / authority input 的 scope 擴充，都需通過既有的 review artifacts 與 evidence 更新流程。
