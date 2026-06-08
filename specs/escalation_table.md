---
title: Standard Escalation Trigger Table
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

# Standard Escalation Trigger Table

> **用途：**本頁為 consuming firmware repo 的參考邊界。  
> 任一條件符合時，需依 consuming repo 的 Standard Escalation Mode 流程判定是否升階。

## USB 2.0 觸發條件

| # | 條件 | 規格參考 | 是否需要 Escalation |
|---|---|---|---|
| E-01 | firmware `bNbrPorts` 與 hub descriptor 欄位值不一致 | 11.23.2.1 offset 2 | Yes |
| E-02 | Port status bit 3 被 firmware 當成非 `PORT_OVER_CURRENT` 用途 | 11.24.2.7.1 bit 3 | Yes |
| E-03 | 保留位元 `(7:5, 15:13)` 被 firmware 使用 | 11.24.2.7.1 | Yes |
| E-04 | Hub descriptor `GET_DESCRIPTOR` 未實作 | 11.24.2 | Yes |
| E-05 | vendor 指令 selector 與標準 selector 範圍 `(0-22)` 重疊 | 11.24.2 table | Yes |
| E-06 | full-speed-only hub 卻出現 TT 行為 | 11.17-11.18 | Yes |
| E-07 | Descriptor TT Think Time 與實際硬體時序不一致 | 11.23.2.1 `wHubCharacteristics[6:5]` | Yes |
| E-08 | Descriptor power switching mode 與確認過的 project fact 不一致 | 11.23.2.1 `wHubCharacteristics[1:0]` | Yes |
| E-09 | 在 full-speed-only hub 中觀察到 `PORT_HIGH_SPEED` | 11.24.2.7.1 bit 10 | Yes |
| E-10 | TT-capable hub 需要 `CLEAR_TT_BUFFER` 或 `RESET_TT` 但未實作 | 11.24.2 | Yes |

## SS（USB 3.x）觸發條件

以下條件適用於 SuperSpeed hub；與 E-01 到 E-10 的 USB 2.0 觸發條件獨立。

| # | 條件 | 規格參考 | 是否需要 Escalation |
|---|---|---|---|
| SE-01 | firmware `bDeviceProtocol` 為 `0x01` 或 `0x02`（TT 型別）但裝置聲稱為 SS hub | USB 3.2 §10.14 / Device Descriptor | Yes |
| SE-02 | SS hub 未實作 `GET_DESCRIPTOR(0x2A)`（SS Hub Descriptor） | USB 3.2 §10.14.2 | Yes |
| SE-03 | SS hub 的 `SET_HUB_DEPTH` 未在 `SET_CONFIGURATION` 後發送 | USB 3.2 §10.14.1 | Yes |
| SE-04 | firmware 對 SS port status bits `wPortStatus[8:5]`（PORT_LINK_STATE）的解讀與規格編碼表不一致 | USB 3.2 §10.14.2.1 | Yes |
| SE-05 | SS feature selector 值（PORT_U1_ENABLE=17、PORT_U2_ENABLE=18、PORT_U1_TIMEOUT=23、PORT_U2_TIMEOUT=24、PORT_REMOTE_WAKE_MASK=27、BH_PORT_RESET=28）與 firmware 實際使用的 selector 不符 | USB 3.2 §10.14.1 Table | Yes |

## Escalation 邊界

本表只列出標準側最小化升階邊界。  
即使上述條件不成立，consuming repo 仍可依確認專案事實、架構決策或安全治理需求，新增其他 escalation 條件。

目標是讓 consuming repo 區分「應進入 escalation 流程」與「可留在文件參考」的界線。

## 非 Escalation 情境

以下使用不必單獨觸發 escalation（僅做一般規格參考）：

- 使用 `specs/port_status_bits.md` 做 port status bit 定義參考
- 使用 `specs/hub_class_requests.md` 做欄位對照參考
- 使用 `specs/hub_descriptor.md` 對 `GET_DESCRIPTOR` 回傳格式做核對

## Governed Linkage

**USB 2.0（E-01 到 E-10）：**
- `tables/escalation_trigger_matrix.yaml`：受治理的 E-01 到 E-10 trigger boundary
- `tables/hub_descriptor_matrix.yaml`：E-01、E-07、E-08 相關 descriptor 欄位
- `tables/port_status_bit_matrix.yaml`：E-02、E-03、E-09 相關 status 位元
- `tables/feature_selector_matrix.yaml`：E-05 涉及 selector 命名空間
- `tables/transaction_translator_matrix.yaml`：E-06、E-07、E-10 涉及 TT 適用性與請求面

**USB 3.x（SE-01 到 SE-05）：**
- `tables/ss_hub_descriptor_matrix.yaml`：SE-01、SE-02 相關 descriptor 欄位（bDeviceProtocol、Descriptor type 0x2A）
- `tables/ss_hub_class_request_matrix.yaml`：SE-03 相關（SET_HUB_DEPTH 強制要求）
- `tables/ss_port_status_bit_matrix.yaml`：SE-04 相關（PORT_LINK_STATE bits[8:5]）
- `tables/ss_feature_selector_matrix.yaml`：SE-05 相關（6 個 SS-only feature selectors）

本表是標準-side 參考邊界，**不**執行 escalation、**不**取代 project fact，也**不**授權直接改 firmware 行為。

## Escalation 輸出格式（範本）

遇到 escalation 時，建議 consuming repo 記錄：

```text
[Standard Conflict Detected]

Trigger: <E-NN from this table>

Standard says: <this repo 的標準解讀>

Project fact says: <已確認的專案事實>

Classification: Project Implementation Constraint | Standards Compliance Risk | Documentation Error

Resolution: <採用的處理路徑>
```
