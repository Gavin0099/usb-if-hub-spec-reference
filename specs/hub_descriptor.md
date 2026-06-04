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

> Source scope: USB 2.0 規格 Rev 2.0, Section 11.23.2.1。  
> 本頁為消費者友善的參考摘要，不是欄位逐位逐項的 PDF 驗證紀錄；若無段落級 evidence，不代表升級為 `verified`。

## 頁面用途

本頁回答：

- hub descriptor 的主要欄位有哪些。
- 哪些欄位常被 firmware、列舉流程、descriptor dump、consuming repo 規則引用。
- 哪些欄位與 downstream port 計數、電源切換、過流保護、TT 行為有關。

本頁不回答：

- 某個特定 descriptor dump 是否已逐位與 USB-IF PDF 驗證過。
- 某個特定 firmware 實作是否正確。
- `wHubCharacteristics` 的每個 bit pattern 是否在本 repo 已有完整語義驗證。

## 主要欄位

hub descriptor 透過 class-specific `GET_DESCRIPTOR` 回傳，descriptor type 為 `0x29`。  
在本 repo 現行 reviewed request surface 中，`GET_DESCRIPTOR` 與 `SET_DESCRIPTOR` 已明確回連到該 descriptor-type 邊界，但這仍不會將本頁升為頁面級 verified 主張。

| Offset | Field | Size | Role Summary |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | hub descriptor 總長度。 |
| 1 | `bDescriptorType` | 1 byte | hub descriptor type；這個參考摘要預期為 `0x29`。 |
| 2 | `bNbrPorts` | 1 byte | hub 公告的 downstream port 數量。 |
| 3 | `wHubCharacteristics` | 2 bytes | 包含 power switching、compound device、over-current、TT think time、port indicators 等位元欄位。 |
| 5 | `bPwrOn2PwrGood` | 1 byte | 上電到 power-good 的延遲（2ms 單位）。 |
| 6 | `bHubContrCurrent` | 1 byte | hub controller 電流需求，通常以 mA 解讀。 |
| 7 | `DeviceRemovable` | variable | 表示各 port 是否 removable 的 bitmap。 |
| 7+x | `PortPwrCtrlMask` | variable | 每個 port power-control 的保留/掩碼欄位；`0xFF` 類型模式常見，但本頁不將其視為普遍真值。 |

## 欄位摘要

### `bDescLength`

- 定義 hub descriptor 的總長度。
- consuming repo 可將其作為讀取 descriptor dump 的結構 sanity check。
- 本頁不聲明任何特定設備值正確。

### `bDescriptorType`

- 指定 class-specific hub descriptor type。
- 本 repo 的參考摘要中，hub descriptor type 代表為 `0x29`。
- 若 firmware 或 dump 報告與預期不同，請先對照規格段落與 descriptor capture，不可用本頁覆蓋已確認的 project fact。

### `bNbrPorts`

- 這是 hub 的 downstream port 數量描述欄位。
- 常被用來對應實體連接數、firmware 暴露 port 計數、consuming repo 的拓撲假設。
- 若 `bNbrPorts` 與已確認硬體或 firmware 事實衝突，應視為 escalation-sensitive 並比對 `E-01`。

### `wHubCharacteristics`

- 這個 16-bit 欄位包含多個 descriptor 語義，不應視為單一布林屬性。
- 常見欄位族群：
  - power switching mode
  - over-current protection mode
  - TT think time
  - port indicators 支援
- 本頁只做欄位角色摘要，不聲明所有 bit pattern 都有段落級驗證。

### `bPwrOn2PwrGood`

- 表示從 power-on 到 power-good 的延遲。
- 常影響 host / firmware 對時序描述，但本頁不建立 timing 保證。
- 若 consuming repo 要轉為具體 timing 事實，需再對照規格 PDF 與專案實測/硬體資料。

### `bHubContrCurrent`

- 描述 hub controller 的電流需求。
- 可作為 descriptor dump 與設計文件的比較參考。
- 本頁不把它提升為板級電流正確性驗證結論。

### `DeviceRemovable`

- 此 bitmap 表示每個 downstream port 的 removable 標註。
- consuming repo 可用作 descriptor-side 的語義上下文，但不可僅以本頁覆蓋「固定設備/可拔除設備」等已確認事實。
- 若 removable 判定有爭議，保留 escalation。

### `PortPwrCtrlMask`

- 這欄位常與每 port power control 行為一併解讀。
- `0xFF` 類值在實務常見，但只是共通模式，不是本 repo 的 universal truth。
- 若 consuming repo 要用於 firmware 決策，應先確認專案事實與 spec anchor。

## `wHubCharacteristics` bit 群組

| Bits | Group | Role Summary |
|---|---|---|
| `1:0` | Logical Power Switching Mode | 定義 hub power-switching 模式。 |
| `2` | Compound Device | 描述 hub 是否為 compound device。 |
| `4:3` | Over-current Protection Mode | 定義 over-current 保護模式。 |
| `6:5` | TT Think Time | 描述 Transaction Translator 的 think-time 類別。 |
| `7` | Port Indicators Supported | 描述是否支援 port indicators。 |
| `15:8` | Reserved | 保留位元；本頁不聲明 firmware 可任意重用。 |

### `wHubCharacteristics` 的安全解讀邊界

- `1:0` 與 `6:5` 常直接影響 power switching 與 TT 行為，因此是 consuming repo 容易過度套用的欄位。
- 本 repo 提供標準側參考摘要，不是專案事實 authority。
- 若 descriptor power switching mode 或 TT think time 與確認事實衝突，應先進入 Standard Escalation Mode 再調整。

## Governed Linkage

- `tables/hub_descriptor_matrix.yaml`：9 個 tracked hub descriptor 欄位的規範來源面。
- `tables/class_request_matrix.yaml`：class-specific 請求用於 `GET_DESCRIPTOR` / `SET_DESCRIPTOR` 的連結。
- `specs/escalation_table.md`：`E-01`、`E-07`、`E-08` 分別關聯 `bNbrPorts`、`wHubCharacteristics[6:5]`、`wHubCharacteristics[1:0]`。
- `specs/transaction_translator.md`：提供高層 TT 類型與 TT think-time 摘要。

本頁為欄位角色參考面，不是逐欄位驗證，不宣告 descriptor dump 的正確性。

## 本頁可回答與不可回答

本頁可以回答：

- hub descriptor 的核心欄位有哪些。
- 哪些欄位與 port count、power switching、過流、TT、可移除位元組有關。
- 哪些欄位是 escalation-sensitive 的比對點。

本頁不能回答：

- 某個具體 device 的 descriptor 是否已完成 section-level verification。
- 是否每個 `DeviceRemovable` 或 `PortPwrCtrlMask` bit pattern 都已完全驗證。
- consuming repo 是否可直接以本頁為依據變更 firmware descriptor 值。

## Non-claims

- 本頁不是 field-by-field 或 bit-by-bit 的 USB 2.0 PDF 驗證紀錄。
- 本頁不宣告任何特定 descriptor dump 正確或錯誤。
- 本頁不建立 `wHubCharacteristics` 的完整 semantic truth table。
- 本頁不取代 consuming repo 的 project facts。
