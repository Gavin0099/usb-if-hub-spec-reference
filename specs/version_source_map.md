---
title: 版本來源對應
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# 版本來源對應

> 本頁整理 USB hub 相關標準來源的查找路徑。
> 它提供的是「去哪裡找」的對應，不是版本內容等價性聲明。

## 用途

- 協助定位 USB 2.0、2.1、3.2、USB4 的 hub 相關官方來源
- 區分 normative official、official index、community reference 等不同權威層級
- 提供 consuming repo 做版本查核與 staleness review 的入口

## 來源類型

| 類型 | 權威層級 | 用途 |
|---|---|---|
| USB-IF 規格文件 | normative_official | 欄位、位元、request 語意的主要來源 |
| USB-IF ECN / addendum | normative_official 或 official_index | 補充特定版本差異或增補內容 |
| USB-IF 文件索引頁 | official_index | 用來確認文件存在、版本與入口 |
| 社群參考資料 | community_reference | 僅能輔助理解，不可單獨支撐 normative claim |
| 封存鏡像 | archive_reference | 用於可取得性補充，不提升權威層級 |

## 版本對應摘要

| 版本 | 主要來源 | Hub 關聯說明 |
|---|---|---|
| USB 2.0 | USB 2.0 Specification | 本 repo 目前主要錨定版本，涵蓋 hub class request、descriptor、port status 與 TT 摘要 |
| USB 2.1 | USB 2.0 + LPM / ECN 補充 | 通常不是獨立 hub 語意來源，需檢查增補內容是否真的影響 hub |
| USB 3.2 | USB 3.x / USB 3.2 系列規格 | 可能引入與 USB 2.0 hub 不同的架構與術語，不能直接等價映射 |
| USB4 | USB4 specification family | 與傳統 USB 2.0 hub class 語意並不直接等價，需特別區分 |

## 查核流程

1. 先確認 claim 所屬 USB 版本範圍。
2. 回到對應的 USB-IF 官方文件或索引頁查找原始來源。
3. 若只有 community 或 archive 來源，最多只能做輔助說明。
4. 若版本語意可能改變 consuming repo 行為，應啟動 Standard Escalation Mode。

## 注意事項

- 本頁不主張 USB 2.0、2.1、3.2、USB4 的 hub 語意可以自動互相替代。
- 若有新版本文件進入 source registry，應同步檢查 `contract/*.yaml` 與 `evidence/source_registry.yaml`。
- 任何以本頁為基礎的高信度 claim，仍應回到對應版本的 normative official source。
