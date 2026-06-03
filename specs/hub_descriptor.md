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
> 本頁是給 consuming repos 使用的 reference summary，不是逐欄位 PDF verification record；沒有 section-level evidence 時，不會升成 `verified`。

## Page Purpose

本頁回答：

- hub descriptor 裡有哪些主要欄位
- 哪些欄位最常被 firmware、enumeration logs、descriptor dumps 與 consuming-repo 規則引用
- 哪些欄位和 port 數量、power switching、over-current behavior、TT behavior 有關

本頁不回答：

- 某份 descriptor dump 是否已逐 bit 對照 USB-IF PDF 驗證
- 某個 firmware implementation 是否正確
- 每一種 `wHubCharacteristics` bit pattern 是否都已在本 repo 完成 semantic verification

## Main Descriptor Fields

Hub descriptor 由 class-specific `GET_DESCRIPTOR` request 回傳，descriptor type 為 `0x29`。

| Offset | Field | Size | Role Summary |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | Hub descriptor 總長度 |
| 1 | `bDescriptorType` | 1 byte | Hub descriptor type；本 reference summary 預期為 `0x29` |
| 2 | `bNbrPorts` | 1 byte | Hub 回報的 downstream ports 數量 |
| 3 | `wHubCharacteristics` | 2 bytes | bitfield，涵蓋 power switching、compound device、over-current mode、TT think time、port indicators |
| 5 | `bPwrOn2PwrGood` | 1 byte | 從 power-on 到 power-good 的延遲，單位為 2 ms |
| 6 | `bHubContrCurrent` | 1 byte | Hub controller current requirement，通常以 mA 解讀 |
| 7 | `DeviceRemovable` | variable | 描述各 port 是否可移除的 bitmap |
| 7+x | `PortPwrCtrlMask` | variable | 與 per-port power control 相關的 reserved / mask 欄位；`0xFF` 類型值在實務上常見，但本頁不把它升成 verified truth |

## Field Summaries

### `bDescLength`

- 定義 hub descriptor 的總長度
- consuming repo 可以把它當成讀 descriptor dump 時的 structural sanity check
- 本頁不宣告任何特定裝置值一定正確

### `bDescriptorType`

- 用來識別 class-specific hub descriptor type
- 在本 repo 的 reference summary 中，hub descriptor type 表示為 `0x29`
- 如果 firmware 或 dump 顯示出不同 type，應先對照 spec section 與 descriptor capture，而不是直接用本頁覆蓋 project facts

### `bNbrPorts`

- 這是 downstream port count 的直接 descriptor 欄位
- 常被拿來和實際硬體 port 數、firmware 對外宣告的 port 數、consuming repo 的 topology 假設互相比對
- 若 `bNbrPorts` 與已確認的硬體或 firmware facts 衝突，應視為 escalation-sensitive，並交叉檢查 `E-01`

### `wHubCharacteristics`

- 這個 16-bit 欄位承載多組 descriptor semantics，不應被當成單一布林屬性
- 最常被消費的 group 包括：
  - power switching mode
  - over-current protection mode
  - TT think time
  - port indicators support
- 本頁只摘要欄位角色，不宣告所有 bit patterns 都已完成 section-level verification

### `bPwrOn2PwrGood`

- 表示 power-on 到 power-good 之間的延遲
- 這個欄位常影響 host 或 firmware 對 power sequencing 的討論，但本頁不建立 timing guarantee
- 如果 consuming repo 要把它轉成具體 timing facts，應回頭驗證原始 PDF 與 project-side hardware data

### `bHubContrCurrent`

- 描述 hub controller current requirement
- 對 descriptor dump 與設計文件比對很有用
- 本頁不把它升成 board-level current validation claim

### `DeviceRemovable`

- 這個 bitmap 指示 downstream ports 是否標記為 removable
- consuming repo 可把它當作 descriptor-side semantic context，但不應只靠本頁去覆蓋 fixed device、soldered device 或 topology 的既有確認事實
- 若 removable 與 non-removable 的判讀發生爭議，應保留 escalation

### `PortPwrCtrlMask`

- 這個欄位常和 per-port power-control semantics 一起被解讀
- `0xFF` 類型值在實務上常見，但那只是常見 pattern，不是本 repo 的 verified universal truth
- 如果 consuming repo 想根據它做 firmware 決策，應先確認 project facts 與 spec anchors

## `wHubCharacteristics` Bit Groups

| Bits | Group | Role Summary |
|---|---|---|
| `1:0` | Logical Power Switching Mode | 描述 hub 的 power-switching mode |
| `2` | Compound Device | 描述 hub 是否為 compound device |
| `4:3` | Over-current Protection Mode | 描述 over-current protection mode |
| `6:5` | TT Think Time | 描述 Transaction Translator think-time 類別 |
| `7` | Port Indicators Supported | 描述是否支援 port indicators |
| `15:8` | Reserved | Reserved bits；本頁不宣告 firmware 可以重新定義它們 |

### Safe Interpretation Boundary for `wHubCharacteristics`

- `1:0` 與 `6:5` 常會直接影響 power switching 與 TT behavior，因此 consuming repos 最容易過度套用
- 本 repo 提供的是 standards-side reference summary，不是 project-truth authority
- 若 descriptor 的 power switching mode 或 TT think time 與已確認的 project facts 衝突，應進入 Standard Escalation Mode，而不是直接改寫 firmware 假設

## Governed Linkage

- `tables/class_request_matrix.yaml`: `GET_DESCRIPTOR` family 提供 hub descriptor access 的 request-level linkage
- `specs/escalation_table.md`: `E-01`、`E-07`、`E-08` 直接涉及 `bNbrPorts`、`wHubCharacteristics[6:5]`、`wHubCharacteristics[1:0]`
- `specs/transaction_translator.md`: 提供較高層的 TT type 與 TT think-time summary

目前沒有專屬的 governed hub-descriptor table，因此本頁是透過 request-family coverage、escalation rules 與相鄰 summary pages 建立 linkage。

## What This Page Can and Cannot Answer

本頁可以回答：

- hub descriptor 中有哪些核心欄位
- 哪些欄位和 port count、power switching、over-current behavior、TT behavior、removable bitmap 有關
- 哪些欄位屬於 escalation-sensitive comparison points

本頁不能回答：

- 某個裝置 descriptor 是否已完成 section-level verification
- 每一種 `DeviceRemovable` 或 `PortPwrCtrlMask` bit pattern 是否都已在本 repo 完整驗證
- consuming repo 是否應只根據本頁直接改 firmware descriptor values

## Non-claims

- 本頁不是逐欄位或逐 bit 的 USB 2.0 PDF verification record
- 本頁不宣告任何特定 descriptor dump 正確或錯誤
- 本頁不建立 `wHubCharacteristics` 的完整 semantic truth table
- 本頁不覆蓋 consuming repos 中已確認的 project facts
