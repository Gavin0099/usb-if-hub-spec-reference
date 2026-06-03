---
title: Hub Descriptor
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Descriptor

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.23.2.1.  
> 本頁是提供 consuming repo 使用的 reference summary，不是逐欄位 PDF 驗證紀錄；在沒有 section-level evidence 前，不升級為 `verified`。

## Page Purpose

本頁回答：

- Hub descriptor 的主要欄位有哪些。
- 哪些欄位最常被 firmware、enumeration log、descriptor dump 與 consuming-repo 規則引用。
- 哪些欄位和 port 數量、power switching、over-current 行為與 TT 行為有關。

本頁不回答：

- 某一份 descriptor dump 是否已逐 bit 對照 USB-IF PDF 驗證。
- 某個 firmware implementation 是否正確。
- `wHubCharacteristics` 的所有 bit pattern 是否都已在本 repo 完成 semantic verification。

## Main Descriptor Fields

Hub descriptor 由 class-specific `GET_DESCRIPTOR` request 讀出，descriptor type 為 `0x29`。

| Offset | Field | Size | Role Summary |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | Hub descriptor 的總長度。 |
| 1 | `bDescriptorType` | 1 byte | Hub descriptor type；本頁以 `0x29` 為 reference summary。 |
| 2 | `bNbrPorts` | 1 byte | Hub 宣告的 downstream port 數量。 |
| 3 | `wHubCharacteristics` | 2 bytes | 涵蓋 power switching、compound device、over-current mode、TT think time、port indicators 的 bitfield。 |
| 5 | `bPwrOn2PwrGood` | 1 byte | 從 power-on 到 power-good 的延遲，單位為 2 ms。 |
| 6 | `bHubContrCurrent` | 1 byte | Hub controller current requirement，通常以 mA 解讀。 |
| 7 | `DeviceRemovable` | variable | 描述各 port 是否 removable 的 bitmap。 |
| 7+x | `PortPwrCtrlMask` | variable | 與 per-port power control 相關的 reserved / mask 欄位；`0xFF` 類型值在實務上常見，但本頁不把它升級成 verified truth。 |

## Field Summaries

### `bDescLength`

- 定義 hub descriptor 的總長度。
- Consuming repo 可以把它當成讀 descriptor dump 時的結構性 sanity check。
- 本頁不宣告任何特定裝置的值一定正確。

### `bDescriptorType`

- 識別 class-specific hub descriptor type。
- 在本 repo 的 reference summary 中，hub descriptor type 以 `0x29` 表示。
- 若 firmware 或 dump 出現與預期不同的 type，應先回頭比對 spec section 與 descriptor capture，而不是直接用本頁覆蓋 project facts。

### `bNbrPorts`

- 這是 downstream port 數量的直接 descriptor 欄位。
- 它常被拿來對照實際硬體 port 數、firmware 暴露的 port 數，以及 consuming repo 的 topology 假設。
- 若 `bNbrPorts` 與已確認的硬體或 firmware 事實衝突，應視為 escalation-sensitive，至少交叉檢查 `E-01`。

### `wHubCharacteristics`

- 這是一個 16-bit 欄位，承載多組 descriptor 語意，不應被當成單一布林屬性。
- 最常被消費的群組包括：
  - power switching mode
  - over-current protection mode
  - TT think time
  - port indicators support
- 本頁只整理欄位角色，不宣告所有 bit pattern 都已完成 section-level verification。

### `bPwrOn2PwrGood`

- 表示 power-on 到 power-good 之間的延遲。
- 這個欄位常影響 host 或 firmware 對 power sequencing 的描述，但本頁不把它升級成 timing guarantee。
- 若 consuming repo 需要把它換算成具體 timing 事實，應回到原始 PDF 與 project-side hardware data 驗證。

### `bHubContrCurrent`

- 描述 hub controller current requirement。
- 它適合作為 descriptor dump 與設計文件的比對點。
- 本頁不把它升級成 board-level current validation claim。

### `DeviceRemovable`

- 這個 bitmap 用來表示 downstream ports 是否標示為 removable。
- Consuming repo 可以把它當成 descriptor-side semantic context，但不應只依賴本頁去覆蓋 fixed device、soldered device 或 topology 的既有事實。
- 若 removable 與 non-removable 行為有爭議，應保留 escalation。

### `PortPwrCtrlMask`

- 這個欄位常和 per-port power-control semantics 一起被解讀。
- `0xFF` 類型值在實務上常見，但那只是常見模式，不是本 repo 已驗證的普遍真相。
- 如果 consuming repo 想根據這個欄位做 firmware 決策，應先確認 project facts 與 spec anchors。

## `wHubCharacteristics` Bit Groups

| Bits | Group | Role Summary |
|---|---|---|
| `1:0` | Logical Power Switching Mode | 描述 hub 的 power-switching mode。 |
| `2` | Compound Device | 描述 hub 是否為 compound device。 |
| `4:3` | Over-current Protection Mode | 描述 over-current protection mode。 |
| `6:5` | TT Think Time | 描述 Transaction Translator think-time 類別。 |
| `7` | Port Indicators Supported | 描述是否支援 port indicators。 |
| `15:8` | Reserved | Reserved bits；本頁不宣告 firmware 可以重用它們。 |

### Safe Interpretation Boundary for `wHubCharacteristics`

- `1:0` 和 `6:5` 常直接影響 power switching 與 TT 行為，因此最容易被 consuming repo 過度套用。
- 本 repo 提供的是標準側 reference summary，不是 project-truth authority。
- 若 descriptor 中的 power switching mode 或 TT think time 與 confirmed project facts 衝突，應進入 Standard Escalation Mode，而不是直接改寫 firmware 假設。

## Governed Linkage

- `tables/class_request_matrix.yaml`: `GET_DESCRIPTOR` family 提供 hub descriptor access 的 request-level linkage。
- `specs/escalation_table.md`: `E-01`、`E-07`、`E-08` 直接涉及 `bNbrPorts`、`wHubCharacteristics[6:5]`、`wHubCharacteristics[1:0]`。
- `specs/transaction_translator.md`: 提供較高層的 TT type 與 TT think-time summary。

目前沒有獨立的 governed hub-descriptor table，因此本頁主要透過 request family、escalation rule 與相鄰 summary page 建立 linkage。

## What This Page Can and Cannot Answer

本頁可以回答：

- Hub descriptor 的核心欄位有哪些。
- 哪些欄位和 port 數量、power switching、over-current 行為、TT 行為與 removable bitmap 有關。
- 哪些欄位是 escalation-sensitive 的比較點。

本頁不能回答：

- 某個裝置的 descriptor 是否已達 section-level verified。
- `DeviceRemovable` 或 `PortPwrCtrlMask` 的每一種 bit pattern 是否都已在本 repo fully verified。
- Consuming repo 是否應只根據本頁就直接修改 firmware descriptor 值。

## Non-claims

- 本頁不是逐欄位或逐 bit 的 USB 2.0 PDF 驗證紀錄。
- 本頁不宣告任何特定 descriptor dump 必然正確或錯誤。
- 本頁不建立 `wHubCharacteristics` 的完整 semantic truth table。
- 本頁不覆蓋 consuming repo 中已確認的 project facts。
