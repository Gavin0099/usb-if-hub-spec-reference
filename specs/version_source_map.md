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

> 本頁摘要說明 USB hub 相關 standards sources 應從哪裡取得。  
> 它是 source-location map，不代表不同 USB 版本的 hub semantics 可以直接互換。

## Purpose

- 協助定位 USB 2.0、2.1、3.2 與 USB4 的官方 hub 相關 sources
- 區分 normative official、official index 與 community-level references
- 支援 consuming repos 在檢查 version scope 與 staleness 時有一致入口

## Source Categories

| Category | Authority Level | Usage |
|---|---|---|
| USB-IF specification documents | normative_official | fields、bits、requests 與 semantics 的 primary source |
| USB-IF ECNs / addenda | normative_official or official_index | 版本特定的補充文件或 delta |
| USB-IF index pages | official_index | 文件存在性、版本與取得入口 |
| Community references | community_reference | 可輔助理解，但不足以單獨支撐 normative claims |
| Archive mirrors | archive_reference | 可用性備援，不代表 authority promotion |

## Version Summary

| Version | Primary Source | Hub-Relevant Note |
|---|---|---|
| USB 2.0 | USB 2.0 Specification | 目前本 repo 的主要 anchor |
| USB 2.1 | USB 2.0 加上 LPM / ECN 材料 | 通常是補充層，不是獨立的 hub semantic baseline |
| USB 3.2 | USB 3.x / USB 3.2 family specs | 可能引入與 USB 2.0 hub semantics 不等價的架構與術語變化 |
| USB4 | USB4 specification family | 不可直接等同於傳統 USB 2.0 hub class semantics |

## Review Flow

1. 先確認 claim 所屬的 USB version scope。
2. 回到對應的 USB-IF specification 或 official index source。
3. 將 community 或 archive sources 視為 supporting context，不是 primary authority。
4. 若 version mapping 會影響 consuming firmware behavior，應先進入 Standard Escalation Mode。

## Notes

- 本頁不宣告 USB 2.0、2.1、3.2 與 USB4 的 hub semantics 可直接互換。
- 若新的 version document 進入 source registry，本 repo 應同步檢查 `contract/*.yaml` 與 `evidence/source_registry.yaml`。
- 即使某個 claim 是根據本頁得到的高信心結論，仍必須回到該版本對應的 normative official source 才能成立。
