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
> This page is a consumer-facing reference summary, not a field-by-field PDF verification record; without section-level evidence, it does not upgrade to `verified`.

## 頁面目的

本頁回答：

- hub descriptor 的主要欄位有哪些
- 哪些欄位常見於 firmware、enumeration log、descriptor dump 與 consuming-repo 規則
- 哪些欄位與埠數、電源切換、過流行為、TT 行為有關

本頁不回答：

- 某個 descriptor dump 是否已逐位與 USB-IF PDF 完整比對
- 某個特定 firmware 實作是否正確
- `wHubCharacteristics` 的每個 bit pattern 在本 repo 是否已全部語意驗證

## 主要描述欄位

hub descriptor 由 class-specific `GET_DESCRIPTOR` 回傳，descriptor type 為 `0x29`。  
在本 repo 的 reviewed request surface 中，`GET_DESCRIPTOR` 與 `SET_DESCRIPTOR` 已明確連回 descriptor-type boundary，但這不代表整頁升級為 page-level verified claim。

| Offset | Field | Size | Role Summary |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | 整體 hub descriptor 長度 |
| 1 | `bDescriptorType` | 1 byte | hub descriptor type，本頁預期為 `0x29` |
| 2 | `bNbrPorts` | 1 byte | hub 報告的 downstream port 數量 |
| 3 | `wHubCharacteristics` | 2 bytes | 含有 power switching、compound device、過流模式、TT think time、port indicators 等 bitfield |
| 5 | `bPwrOn2PwrGood` | 1 byte | 開機到 power-good 的延遲，單位 2ms |
| 6 | `bHubContrCurrent` | 1 byte | hub controller 電流需求，常以 mA 口徑解讀 |
| 7 | `DeviceRemovable` | variable | 每個 port 是否可移除的 bitmap |
| 7+x | `PortPwrCtrlMask` | variable | 與 per-port power control 相關的 reserved/mask 欄位；實務中常見 `0xFF` pattern，但本頁不將其視為 universal truth |

## 欄位摘要

### `bDescLength`

- 定義 hub descriptor 的總長度。
- consuming repo 可拿來做 descriptor dump 的結構 sanity check。
- 本頁不聲明任一裝置的特定值是正確值。

### `bDescriptorType`

- 指示 class-specific hub descriptor type。
- 在本 repo 的 reference summary 中，hub descriptor type 使用 `0x29`。
- 若 firmware 或 dump 回報 type 與預期不符，應先比對 spec 與 descriptor capture，不能直接以本頁覆蓋 project fact。

### `bNbrPorts`

- 這是下行 port 數量的直接 descriptor 欄位。
- 常與實際硬體 port 數、firmware 公開的 port 數、consuming-repo 的 topology 假設做比對。
- 若 `bNbrPorts` 與已確認的硬體或 firmware 事實衝突，應視為 escalation 敏感，並 cross-check `E-01`。

### `wHubCharacteristics`

- 這個 16-bit 欄位包含多種 descriptor 語意，不該當作單一 boolean。
- 常見關聯群組：
  - power switching mode
  - over-current protection mode
  - TT think time
  - port indicators 支援
- 本頁僅彙總欄位角色，未聲明所有 bit pattern 都已有 section-level 驗證。

### `bPwrOn2PwrGood`

- 代表從 power-on 到 power-good 的延遲。
- 常影響主機或 firmware 在電源順序上的討論，但本頁不建立 timing 保證。
- consuming repo 若要轉為具體 timing 事實，需再以原始 PDF 與 project-side 硬體資料驗證。

### `bHubContrCurrent`

- 描述 hub controller 電流需求。
- 可作為 descriptor dump 與設計文件的對照欄位。
- 本頁不把它升級為板級電流正確性驗證。

### `DeviceRemovable`

- 此 bitmap 標示各 downstream port 是否標記為可移除。
- consuming repo 可用作 descriptor-side 語意背景，但不應單獨用本頁覆蓋固定裝置、焊接裝置或拓撲相關已確認事實。
- 若可移除/不可移除行為有爭議，應保留 escalation。

### `PortPwrCtrlMask`

- 此欄位常與每 port power-control 語意一併解讀。
- `0xFF` 類模式在實務中常見，但在本 repo 這是常見模式而非全域 verified 真值。
- 若 consuming repo 要據此做 firmware 決策，需先確認 project facts 與 spec anchor。

## `wHubCharacteristics` Bit Groups

| Bits | Group | Role Summary |
|---|---|---|
| `1:0` | Logical Power Switching Mode | 描述 hub 的 power-switching 模式 |
| `2` | Compound Device | 描述 hub 是否為 compound device |
| `4:3` | Over-current Protection Mode | 描述過流保護模式 |
| `6:5` | TT Think Time | 描述 Transaction Translator think-time 分類 |
| `7` | Port Indicators Supported | 描述是否支援 port indicators |
| `15:8` | Reserved | 保留位元，非本頁聲明可被 firmware 重用 |

### `wHubCharacteristics` 的安全解讀邊界

- `1:0` 與 `6:5` 常直接影響 power switching 與 TT 行為，容易被 consuming repo 過度套用。
- 本 repo 只提供 standard-side reference summary，不是 project-truth authority。
- 若 descriptor power switching mode 或 TT think time 與已確認 project fact 衝突，請啟動 Standard Escalation Mode，而非直接改 firmware 假設。

## Governed Linkage

- `tables/hub_descriptor_matrix.yaml`: 受治理的 8 個 hub descriptor 欄位 role surface。
- `tables/class_request_matrix.yaml`: `GET_DESCRIPTOR` 家族提供 hub descriptor access 的請求連結。
- `specs/escalation_table.md`: `E-01`、`E-07`、`E-08` 直接關聯 `bNbrPorts`、`wHubCharacteristics[6:5]`、`wHubCharacteristics[1:0]`。
- `specs/transaction_translator.md`: 提供 TT type 與 TT think-time 的高階摘要。

本頁的 hub descriptor table 仍是 field-role surface；不會把頁面提升為逐欄位逐位驗證，也不會建立 descriptor dump 正確性。

## 本頁可答與不可答

本頁可答：

- hub descriptor 的核心欄位有哪些
- 哪些欄位與 port count、power switching、over-current、TT、removable bitmap 有關
- 哪些欄位是 escalation-sensitive 比對點

本頁不可答：

- 某特定裝置 descriptor dump 是否已在 section level 驗證
- `DeviceRemovable` 或 `PortPwrCtrlMask` 的每個 bit pattern 是否已完整驗證
- consuming repo 是否可以僅根據本頁直接調整 firmware descriptor 值

## Non-claims

- 本頁不是 field-by-field 或 bit-by-bit 的 USB 2.0 PDF 驗證紀錄。
- 本頁不宣告任何特定 descriptor dump 為正確或錯誤。
- 本頁不建立 `wHubCharacteristics` 的完整語意真值表。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
