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

> **Usage:** 此表供 consuming firmware repositories 使用。  
> 只要任一 trigger condition 成立，就必須啟動 consuming repo 所定義的 Standard Escalation Mode。

## Trigger Conditions

| # | Condition | Spec Reference | Escalation Required |
|---|---|---|---|
| E-01 | Firmware `bNbrPorts` 與 hub descriptor 欄位值不一致 | 11.23.2.1 offset 2 | Yes |
| E-02 | Port status bit 3 被拿來表示非 over-current 的用途 | 11.24.2.7.1 bit 3 | Yes |
| E-03 | Reserved port status bits `(7:5, 15:13)` 被 firmware 使用 | 11.24.2.7.1 | Yes |
| E-04 | Hub descriptor `GET_DESCRIPTOR` 未實作 | 11.24.2 | Yes |
| E-05 | Vendor command selector 與標準 selector range `(0-22)` 重疊 | 11.24.2 table | Yes |
| E-06 | TT behavior 出現在 full-speed-only hub 中 | 11.17-11.18 | Yes |
| E-07 | Descriptor TT Think Time 與硬體 timing 不一致 | 11.23.2.1 `wHubCharacteristics[6:5]` | Yes |
| E-08 | Descriptor power switching mode 與已確認的 project fact 不一致 | 11.23.2.1 `wHubCharacteristics[1:0]` | Yes |
| E-09 | 在 full-speed-only hub 中測試 `PORT_HIGH_SPEED` | 11.24.2.7.1 bit 10 | Yes |
| E-10 | TT-capable hub 需要 `CLEAR_TT_BUFFER` / `RESET_TT`，但未實作 | 11.24.2 | Yes |

## Escalation Scope Boundary

此表定義的是最小的 standard-side escalation boundary。  
即使上述條件都未命中，consuming projects 仍可依據已確認的 project facts、architecture decisions 或 safety governance requirements，額外建立自己的 triggers。

本頁的目的，是把「應進入 consuming repo escalation flow 的情況」與「僅供文件參考的使用情況」區分開來。

## Non-Escalation Cases

下列 reference usage 本身不需要 escalation：

- 使用 `specs/port_status_bits.md` 釐清 port status bit semantics
- 使用 `specs/hub_class_requests.md` 作為 field-encoding reference
- 使用 `specs/hub_descriptor.md` 確認 `GET_DESCRIPTOR` response format

## Governed Linkage

- `tables/escalation_trigger_matrix.yaml`：E-01 到 E-10 的 governed trigger-boundary surface
- `tables/hub_descriptor_matrix.yaml`：E-01、E-07 與 E-08 涉及的 descriptor fields
- `tables/port_status_bit_matrix.yaml`：E-02、E-03 與 E-09 涉及的 port status bits
- `tables/feature_selector_matrix.yaml`：E-05 涉及的 selector namespace
- `tables/transaction_translator_matrix.yaml`：E-06、E-07 與 E-10 涉及的 TT applicability 與 request surfaces

這份 governed trigger table 只是 standard-side reference boundary。它不會直接執行 escalation、不會替 consuming repos 解決 project facts，也不授權 firmware behavior changes。

## Escalation Output Format

當 escalation 被觸發時，應在 consuming repo 中記錄：

```text
[Standard Conflict Detected]

Trigger: <E-NN from this table>

Standard says: <standard-based interpretation from this repo>

Project fact says: <confirmed project-specific behavior>

Classification: Project Implementation Constraint | Standards Compliance Risk | Documentation Error

Resolution: <chosen path>
```
