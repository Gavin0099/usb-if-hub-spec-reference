---
title: 標準升級觸發表
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# 標準升級觸發表

> **用途：** 本表供 consuming firmware repo 使用。
> 當任何觸發條件成立時，必須啟動 consuming repo 的 `AGENTS.md` Section 10 所定義的 Standard Escalation Mode。

## 觸發條件

| # | 條件 | 規格參考 | 需升級 |
|---|------|---------|-------|
| E-01 | 韌體 `bNbrPorts` 與 hub descriptor 欄位值不一致 | 11.23.2.1 offset 2 | 是 |
| E-02 | Port status bit 3 用於非 OC 目的 | 11.24.2.7.1 bit 3 | 是 |
| E-03 | Reserved port status bits (7:5, 15:13) 被韌體使用 | 11.24.2.7.1 | 是 |
| E-04 | Hub descriptor `GET_DESCRIPTOR` 未實作 | 11.24.2 | 是 |
| E-05 | Vendor command selector 與標準 selector (0-22) 重疊 | 11.24.2 table | 是 |
| E-06 | Full-speed-only hub 出現 TT 行為 | 11.17-11.18 | 是 |
| E-07 | Descriptor 中 TT Think Time 與硬體實際時序不一致 | 11.23.2.1 `wHubCharacteristics[6:5]` | 是 |
| E-08 | Descriptor 中 Power switching mode 與已確認的專案事實不一致 | 11.23.2.1 `wHubCharacteristics[1:0]` | 是 |
| E-09 | 在 Full-speed-only hub 中測試 `PORT_HIGH_SPEED` bit | 11.24.2.7.1 bit 10 | 是 |
| E-10 | 具 TT 的 hub 需要 `CLEAR_TT_BUFFER` / `RESET_TT` 但未實作 | 11.24.2 | 是 |

## 不需升級的情況

以下標準參考用途不需要啟動升級模式：

- 使用 `specs/port_status_bits.md` 的 port status bit 定義澄清語意
- 使用 `specs/hub_class_requests.md` 的 hub 類別請求表作為欄位編碼參考
- 使用 `specs/hub_descriptor.md` 確認 `GET_DESCRIPTOR` 回應格式

## Governed Linkage

- `tables/escalation_trigger_matrix.yaml`: 管理 E-01 到 E-10 的 trigger-boundary surface
- `tables/hub_descriptor_matrix.yaml`: E-01、E-07、E-08 涉及的 descriptor fields
- `tables/port_status_bit_matrix.yaml`: E-02、E-03、E-09 涉及的 port status bits
- `tables/feature_selector_matrix.yaml`: E-05 涉及的 selector namespace
- `tables/transaction_translator_matrix.yaml`: E-06、E-07、E-10 涉及的 TT applicability 與 request surfaces

Governed trigger table 只代表 standard-side reference boundary。它不執行 escalation、不解決 consuming-repo project facts，也不授權 firmware behavior changes。

## 升級輸出格式

觸發升級時，在 consuming repo 的 `memory/03_decisions.md` 中記錄：

```text
[Standard Conflict Detected]

Trigger: <本表的 E-NN>

Standard says: <來自本 repo 的 standard-based interpretation>

Project fact says: <已確認的 project-specific behavior>

Classification: Project Implementation Constraint | Standards Compliance Risk | Documentation Error

Resolution: <選擇的處理路徑>
```
