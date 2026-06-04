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
> 本頁是面向使用者的 reference summary，不是逐欄位 PDF verification record；在沒有 section-level evidence 的前提下，本頁不會升級為 `verified`。

## Page Purpose

本頁主要回答：

- Hub descriptor 中有哪些主要欄位。
- 哪些欄位常被 firmware、enumeration logs、descriptor dumps 與 consuming-repo rules 引用。
- 哪些欄位與 port count、power switching、over-current behavior 與 TT behavior 有關。

本頁不回答：

- 某個特定 descriptor dump 是否已對照 USB-IF PDF 完成逐 bit 驗證。
- 某個特定 firmware implementation 是否正確。
- `wHubCharacteristics` 的每一種 bit pattern 是否都已在本 repo 完成 semantic verification。

## Main Descriptor Fields

Hub descriptor 由 class-specific `GET_DESCRIPTOR` request 回傳，descriptor type 為 `0x29`。  
在本 repo 目前的 reviewed request surface 中，`GET_DESCRIPTOR` 與 `SET_DESCRIPTOR` 都已明確回連到這個 descriptor-type boundary，但這仍不會把本頁升級為 page-level verified claim。

| Offset | Field | Size | Role Summary |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | Hub descriptor 的總長度。 |
| 1 | `bDescriptorType` | 1 byte | Hub descriptor type；本 reference summary 預期為 `0x29`。 |
| 2 | `bNbrPorts` | 1 byte | Hub 所回報的 downstream ports 數量。 |
| 3 | `wHubCharacteristics` | 2 bytes | 包含 power switching、compound device、over-current mode、TT think time 與 port indicators 的 bitfield。 |
| 5 | `bPwrOn2PwrGood` | 1 byte | 從 power-on 到 power-good 的延遲，單位為 2 ms。 |
| 6 | `bHubContrCurrent` | 1 byte | Hub controller 的電流需求，通常以 mA 解讀。 |
| 7 | `DeviceRemovable` | variable | 描述各 port 是否可移除的 bitmap。 |
| 7+x | `PortPwrCtrlMask` | variable | 與 per-port power control 相關的 reserved / mask field；`0xFF` 類型值在實務上常見，但本頁不將其升級為 verified truth。 |

## Field Summaries

### `bDescLength`

- 定義 hub descriptor 的總長度。
- Consuming repo 可在讀取 descriptor dumps 時，將其作為結構性的 sanity check。
- 本頁不宣告任何特定裝置數值必然正確。

### `bDescriptorType`

- 標示 class-specific hub descriptor type。
- 在本 repo 的 reference summary 中，hub descriptor type 表示為 `0x29`。
- 若 firmware 或 dump 回報的 type 與預期不同，應先對照 spec section 與 descriptor capture，而不是用本頁覆蓋 project facts。

### `bNbrPorts`

- 這是 downstream port count 的直接 descriptor 欄位。
- 它常被拿來與實際硬體 port 數量、firmware 暴露的 port count，以及 consuming-repo topology assumptions 比對。
- 若 `bNbrPorts` 與已確認的硬體或 firmware facts 衝突，應視為 escalation-sensitive，並交叉檢查 `E-01`。

### `wHubCharacteristics`

- 這個 16-bit 欄位承載多種 descriptor semantics，不應被當作單一布林屬性。
- 最常被消費的群組包括：
  - power switching mode
  - over-current protection mode
  - TT think time
  - port indicators support
- 本頁只摘要欄位角色，不宣告所有 bit patterns 都已完成 section-level verification。

### `bPwrOn2PwrGood`

- 表示從 power-on 到 power-good 的延遲。
- 這個欄位常影響 host 或 firmware 對 power sequencing 的推理，但本頁不建立 timing guarantee。
- 若 consuming repo 需要把它轉成具體 timing facts，應回頭對照原始 PDF 與專案端硬體資料。

### `bHubContrCurrent`

- 描述 hub controller 的電流需求。
- 它適合作為 descriptor dumps 與設計文件的比對點。
- 本頁不把它升級為 board-level current validation claim。

### `DeviceRemovable`

- 這個 bitmap 表示 downstream ports 是否被標記為 removable。
- Consuming repo 可以把它當作 descriptor-side semantic context，但不應只靠本頁就覆蓋 fixed devices、soldered devices 或 topology 的已確認事實。
- 若 removable / non-removable behavior 有爭議，應保留 escalation。

### `PortPwrCtrlMask`

- 這個欄位常與 per-port power-control semantics 一起解讀。
- `0xFF` 類型值在實務上常見，但那只是常見模式，不是本 repo 中已驗證的 universal truth。
- 若 consuming repo 想依此欄位做 firmware 決策，應先確認 project facts 與 spec anchors。

## `wHubCharacteristics` Bit Groups

| Bits | Group | Role Summary |
|---|---|---|
| `1:0` | Logical Power Switching Mode | 描述 hub 的 power-switching mode。 |
| `2` | Compound Device | 描述 hub 是否為 compound device。 |
| `4:3` | Over-current Protection Mode | 描述 over-current protection mode。 |
| `6:5` | TT Think Time | 描述 Transaction Translator 的 think-time category。 |
| `7` | Port Indicators Supported | 描述是否支援 port indicators。 |
| `15:8` | Reserved | 保留位元；本頁不宣告 firmware 可重新賦予其用途。 |

### Safe Interpretation Boundary for `wHubCharacteristics`

- `1:0` 與 `6:5` 常直接影響 power switching 與 TT behavior，因此 consuming repos 很容易過度套用。
- 本 repo 提供的是 standards-side reference summary，不是 project-truth authority。
- 若 descriptor 的 power switching mode 或 TT think time 與已確認的 project facts 衝突，應進入 Standard Escalation Mode，而不是直接重寫 firmware assumptions。

## Governed Linkage

- `tables/hub_descriptor_matrix.yaml`：8 個 USB 2.0 hub descriptor fields 的 governed field-role surface。
- `tables/class_request_matrix.yaml`：`GET_DESCRIPTOR` family 提供 hub descriptor access 的 request-level linkage。
- `specs/escalation_table.md`：`E-01`、`E-07` 與 `E-08` 直接涉及 `bNbrPorts`、`wHubCharacteristics[6:5]` 與 `wHubCharacteristics[1:0]`。
- `specs/transaction_translator.md`：提供更高層的 TT type 與 TT think-time summary。

Hub descriptor table 只是 field-role surface。它不會把本頁升級為逐欄位 verification，也不建立 descriptor dump correctness。

## What This Page Can and Cannot Answer

本頁可以回答：

- Hub descriptor 中有哪些核心欄位。
- 哪些欄位與 port count、power switching、over-current behavior、TT behavior 與 removable bitmaps 有關。
- 哪些欄位是 escalation-sensitive 的 comparison points。

本頁不能回答：

- 某個特定裝置 descriptor 是否已在 section level 完成驗證。
- `DeviceRemovable` 或 `PortPwrCtrlMask` 的每一種 bit pattern 是否都已在本 repo 完整驗證。
- Consuming repo 是否應只根據本頁就直接修改 firmware descriptor values。

## Non-claims

- 本頁不是逐欄位或逐 bit 的 USB 2.0 PDF verification record。
- 本頁不宣告任何特定 descriptor dump 正確或錯誤。
- 本頁不建立 `wHubCharacteristics` 的完整 semantic truth table。
- 本頁不覆蓋 consuming repos 中已確認的 project facts。
