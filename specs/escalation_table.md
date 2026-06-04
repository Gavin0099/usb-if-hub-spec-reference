---
title: Standard Escalation Trigger Table
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Standard Escalation Trigger Table

> **Usage:** This table is for consuming firmware repositories.
> When any trigger condition is met, Standard Escalation Mode defined by the consuming repo must be activated.

## 觸發條件

| # | 條件 | 規格參考 | 必須升級 |
|---|---|---|---|
| E-01 | firmware 的 `bNbrPorts` 不符合 hub descriptor 欄位值 | 11.23.2.1 offset 2 | Yes |
| E-02 | Port status bit 3 被 firmware 用於非過流用途 | 11.24.2.7.1 bit 3 | Yes |
| E-03 | reserved port status bits `(7:5, 15:13)` 被 firmware 使用 | 11.24.2.7.1 | Yes |
| E-04 | 沒有實作 hub descriptor `GET_DESCRIPTOR` | 11.24.2 | Yes |
| E-05 | vendor command selector 與 standard selector range `(0-22)` 重疊 | 11.24.2 table | Yes |
| E-06 | 在 full-speed-only hub 上出現 TT 行為 | 11.17-11.18 | Yes |
| E-07 | descriptor TT Think Time 與硬體時序不一致 | 11.23.2.1 `wHubCharacteristics[6:5]` | Yes |
| E-08 | descriptor power switching mode 與已確認專案事實不一致 | 11.23.2.1 `wHubCharacteristics[1:0]` | Yes |
| E-09 | 在 full-speed-only hub 上測試 `PORT_HIGH_SPEED` | 11.24.2.7.1 bit 10 | Yes |
| E-10 | TT-capable hub 需要 `CLEAR_TT_BUFFER` / `RESET_TT` 但未實作 | 11.24.2 | Yes |

## 不屬於 escalation 的使用

以下僅是標準參考用途，單獨不構成 escalation 需求：

- 使用 `specs/port_status_bits.md` 釐清 port status bit 語意
- 使用 `specs/hub_class_requests.md` 做 field encoding 參考
- 使用 `specs/hub_descriptor.md` 確認 `GET_DESCRIPTOR` 回傳格式

## Governed Linkage

- `tables/escalation_trigger_matrix.yaml`: E-01 到 E-10 的 trigger-boundary surface。
- `tables/hub_descriptor_matrix.yaml`: 涉及 E-01、E-07、E-08 的 descriptor 欄位。
- `tables/port_status_bit_matrix.yaml`: 涉及 E-02、E-03、E-09 的 port status bits。
- `tables/feature_selector_matrix.yaml`: 涉及 E-05 的 selector namespace。
- `tables/transaction_translator_matrix.yaml`: 涉及 E-06、E-07、E-10 的 TT 應用與 request surface。

此標準觸發表僅作為 standard-side reference boundary。它不會直接執行 escalation，不會取代 consuming repo 的 project facts，也不授權 firmware 行為變更。

## Escalation 輸出格式

當觸發 escalation 時，請於 consuming repo 紀錄：

```text
[Standard Conflict Detected]

Trigger: <E-NN from this table>

Standard says: <standard-based interpretation from this repo>

Project fact says: <confirmed project-specific behavior>

Classification: Project Implementation Constraint | Standards Compliance Risk | Documentation Error

Resolution: <chosen path>
```
