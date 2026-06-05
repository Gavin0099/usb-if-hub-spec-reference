---
title: Hub Descriptor
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Descriptor

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.23.2.1.
> 這個頁面是消費端參考摘要，不是逐欄位 PDF 驗證紀錄；若無 section-level evidence，不可升級為 `verified`。

## 頁面目的

本頁回答：

- hub descriptor 主要欄位有哪些。
- 哪些欄位常被 firmware、enumeration log、descriptor dump 與 consuming-repo 規則引用。
- 哪些欄位與 port 數量、電源切換、過流、TT 行為相關。

本頁不回答：

- 某個特定 descriptor dump 是否已逐位驗證與 USB-IF PDF 完全一致。
- 某個特定 firmware 實作是否正確。
- `wHubCharacteristics` 的每一個 bit pattern 是否都已在本 repo 完成語義驗證。

## 主要 Descriptor 欄位

hub descriptor 由 class-specific 的 `GET_DESCRIPTOR` 請求回傳，descriptor type 為 `0x29`。
在本 repo 的目前 reviewed request surface 中，`GET_DESCRIPTOR` 與 `SET_DESCRIPTOR` 都已明確連結到該 descriptor type 邊界，但仍未將本頁升級為 page-level verified claim。

| Offset | Field | Size | Role Summary |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | 總 hub descriptor 長度。 |
| 1 | `bDescriptorType` | 1 byte | hub descriptor type，本頁索引預期值為 `0x29`。 |
| 2 | `bNbrPorts` | 1 byte | hub 回報的下游 port 數量。 |
| 3 | `wHubCharacteristics` | 2 bytes | bitfield，覆蓋 power switching、compound device、over-current mode、TT think time、port indicators。 |
| 5 | `bPwrOn2PwrGood` | 1 byte | 從 power-on 到 power-good 的延遲，以 2 ms 為單位。 |
| 6 | `bHubContrCurrent` | 1 byte | hub 控制器電流需求，通常以 mA 解讀。 |
| 7 | `DeviceRemovable` | variable | 每個 port 是否可移除的 bitmap。 |
| 7+x | `PortPwrCtrlMask` | variable | 與每 port power control 相關的保留/掩碼欄位；`0xFF` 類型 pattern 在實務中常見，但本頁不將其視為 verified truth。 |

## 欄位摘要

### `bDescLength`

- 定義 hub descriptor 總長度。
- consuming repo 可在讀取 descriptor dump 時拿來做結構 sanity check。
- 本頁不聲明任何特定裝置值是正確的。

### `bDescriptorType`

- 定位 hub class-specific descriptor type。
- 本 repo 的 reference summary 中，hub descriptor type 記錄為 `0x29`。
- 若 firmware 或 dump 回報的 type 與預期不同，應先對照 spec section 與 descriptor 擷取結果，再回到 project facts，不可用本頁覆寫既定事實。

### `bNbrPorts`

- 這是下游 port 數量的直接 descriptor 欄位。
- 常見對齊點包括：實際硬體 port 數、firmware 公布的 port 數、consuming-repo 的 topology 假設。
- 若 `bNbrPorts` 與確認過的硬體或 firmware 事實衝突，應視為 escalation-sensitive，與 `E-01` 交叉核對。

### `wHubCharacteristics`

- 這個 16-bit 欄位承載多個 descriptor semantics，不應視為單一 boolean。
- 常用關注群組：
  - power switching mode
  - over-current protection mode
  - TT think time
  - port indicators 支援
- 本頁只做欄位角色摘要，不聲明所有 bit pattern 已完成 section-level 驗證。

### `bPwrOn2PwrGood`

- 代表從 power-on 到 power-good 的延遲。
- 這欄位常影響 host / firmware 在 power sequencing 的推理，但本頁不建立定量 timing 保證。
- consuming repo 若要將此欄位轉成具體 timing 事實，需先對照 USB-IF PDF 與專案端硬體資料。

### `bHubContrCurrent`

- 描述 hub controller 的電流需求。
- 可作為 descriptor dump 與設計文件的對照參考。
- 本頁不將此欄位提升為板級電流驗證 claim。

### `DeviceRemovable`

- 這個 bitmap 指出每個下游 port 是否可移除。
- consuming repo 可作為 descriptor-side 語義脈絡，但不應僅依本頁覆蓋固定設備、焊接設備或 topology 的已確認事實。
- 如果「可移除/不可移除」行為有爭議，保留 escalation。

### `PortPwrCtrlMask`

- 通常要與每個 port 的 power-control semantics 一起解讀。
- `0xFF` 類值在實務常見，但這是常見模式，不代表本 repo 已 universal 驗證為規範真相。
- 若 consuming repo 想以此欄位直接做 firmware 決策，應先確認 project facts 與 spec anchors。

## `wHubCharacteristics` Bit Groups

| Bits | Group | Role Summary |
|---|---|---|
| `1:0` | Logical Power Switching Mode | 描述 hub power-switching mode。 |
| `2` | Compound Device | 描述 hub 是否為 compound device。 |
| `4:3` | Over-current Protection Mode | 描述 over-current protection mode。 |
| `6:5` | TT Think Time | 描述 Transaction Translator 的 think-time 類別。 |
| `7` | Port Indicators Supported | 描述是否支援 port indicators。 |
| `15:8` | Reserved | 保留位元；本頁不聲稱 firmware 可任意重用。 |

### `wHubCharacteristics` 的安全解讀邊界

- `1:0` 與 `6:5` 常直接影響 power switching 與 TT 行為，容易被 consuming repo 過度套用。
- 本 repo 只提供 standards-side reference summary，不是 project-truth authority。
- 若 descriptor power switching mode 或 TT think time 與確認過的 project facts 衝突，請先走 Standard Escalation Mode，而非直接改寫 firmware 前提。

## Governed Linkage

- `tables/hub_descriptor_matrix.yaml`：本 repo 管控的 USB 2.0 hub descriptor 8 個 tracked fields 的欄位角色 surface。
- `tables/class_request_matrix.yaml`：`GET_DESCRIPTOR` family 提供 hub descriptor access 的 request-level 連結。
- `specs/escalation_table.md`：`E-01`、`E-07`、`E-08` 分別關聯 `bNbrPorts`、`wHubCharacteristics[6:5]`、`wHubCharacteristics[1:0]`。
- `specs/transaction_translator.md`：提供較高階的 TT type 與 TT think-time 摘要。

這個 hub descriptor 表格是欄位角色 surface，不會把頁面提升為逐欄位驗證，也不建立 descriptor dump 的 correctness。

## 本頁可回答與不可回答

本頁可回答：

- hub descriptor 的核心欄位有哪些。
- 哪些欄位與 port count、power switching、over-current、TT 行為、可移除位圖有關。
- 哪些欄位是 escalation-sensitive 的比對點。

本頁不可回答：

- 某個特定裝置 descriptor 是否已 section-level 驗證。
- 每個 `DeviceRemovable` / `PortPwrCtrlMask` bit pattern 是否已完全在本 repo 驗證。
- consuming repo 是否可僅依本頁直接改 firmware descriptor 值。

## Non-claims

- 本頁不是逐欄位或 bit-by-bit 的 USB 2.0 PDF 驗證紀錄。
- 本頁不宣稱任何特定 descriptor dump 為正確或錯誤。
- 本頁不建立 `wHubCharacteristics` 的完整語義真值表。
- 本頁不覆寫 consuming repo 已確認的 project facts。
