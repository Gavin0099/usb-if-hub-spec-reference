---
title: Hub 描述符
claim_level: inferred
status: review_required
last_reviewed: "2026-06-02"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub 描述符

> 來源範圍：USB 2.0 Specification Rev 2.0，Section 11.23.2.1。
> 本頁是供 consuming repo 使用的 reference summary，不是逐欄位 PDF 驗證結果；沒有 section-level evidence 前，不升級為 `verified`。

## 頁面用途

本頁回答的問題是：

- Hub descriptor 由哪些主要欄位組成。
- 哪些欄位最常被 firmware、enumeration log、descriptor dump 或 consuming repo 規則引用。
- 哪些欄位和 power switching、over-current、TT 行為、port 數量有關。

本頁不回答的問題是：

- 某個 descriptor dump 是否已被 USB-IF PDF 逐位元驗證。
- 某個 firmware 實作是否一定正確。
- `wHubCharacteristics` 的所有 bit 組合是否已在本 repo 完成 semantic verification。

## Descriptor 主要欄位

Hub descriptor 由 class-specific `GET_DESCRIPTOR` 取得，descriptor type 為 `0x29`。

| Offset | 欄位 | 大小 | 角色摘要 |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | 整個 hub descriptor 的總長度。 |
| 1 | `bDescriptorType` | 1 byte | Hub descriptor 類型；reference summary 中預期為 `0x29`。 |
| 2 | `bNbrPorts` | 1 byte | Hub 宣告的 downstream port 數量。 |
| 3 | `wHubCharacteristics` | 2 bytes | 描述 power switching、compound device、over-current、TT think time、port indicators 的位元欄位。 |
| 5 | `bPwrOn2PwrGood` | 1 byte | 從 power-on 到 power-good 的延遲，單位是 2 ms。 |
| 6 | `bHubContrCurrent` | 1 byte | Hub controller 所需電流，通常以 mA 解讀。 |
| 7 | `DeviceRemovable` | variable | 描述各 port 是否為 removable 的 bitmap。 |
| 7+x | `PortPwrCtrlMask` | variable | 與 per-port power control bitmap 相關的保留/遮罩欄位；常見實作會看到 `0xFF` 類型模式，但本頁不把該模式升級成 verified truth。 |

## 欄位摘要

### `bDescLength`

- 用途是界定 hub descriptor 的總長度。
- consuming repo 可用它判斷 descriptor dump 是否至少在長度層面自洽。
- 本頁不宣告任意特定裝置的 `bDescLength` 一定正確。

### `bDescriptorType`

- 這是 class-specific hub descriptor 的型別欄位。
- 在本 repo 的 reference summary 中，hub descriptor type 以 `0x29` 表示。
- 若 firmware 或 dump 顯示的 type 不符合 consuming repo 期待，應先回到 descriptor capture 與 spec section 比對，而不是直接用本頁覆寫專案事實。

### `bNbrPorts`

- 這是最直接反映 downstream port 數量的 descriptor 欄位。
- 它常被拿來和實際硬體 port 數、firmware 暴露 port 數、以及 consuming repo 的拓撲假設互相比對。
- 若 `bNbrPorts` 與已確認的硬體/firmware 事實不一致，屬於 escalation-sensitive 差異，應參照 `E-01`。

### `wHubCharacteristics`

- 這個 16-bit 欄位承載多個 descriptor 語意，不應被當成單一布林值解讀。
- 其中最常被 consuming repo 依賴的是：
  - power switching mode
  - over-current protection mode
  - TT think time
  - port indicators support
- 本頁只做欄位角色摘要，不宣告所有 bit pattern 都已完成 section-level verification。

### `bPwrOn2PwrGood`

- 用來表示從 power-on 到 power-good 可觀察狀態之間的延遲。
- 這個欄位常影響 host 或 firmware 對 power sequencing 的理解，但本頁不建 timing guarantee。
- 若 consuming repo 需要把它轉成具體等待時間或硬體時序事實，應進一步查證原始 PDF 與專案硬體資料。

### `bHubContrCurrent`

- 這是 hub controller current requirement 的描述欄位。
- 可作為 descriptor dump 與設計文件的比對參考。
- 本頁不把它升級為 board-level 電流驗證結論。

### `DeviceRemovable`

- 這是 bitmap 類欄位，描述各 downstream port 是否被標示為 removable。
- consuming repo 可以把它當作 descriptor 語意摘要，但不應單靠本頁推翻專案對內建裝置、焊接裝置或固定拓撲的已確認事實。
- 若某裝置對 removable/non-removable 的行為解讀有爭議，應保留 escalation。

### `PortPwrCtrlMask`

- 這個欄位通常與 per-port power control bitmap 一起被解讀。
- 實務上常見 `0xFF` 型態，但那是常見模式，不是本頁可直接宣告的通用真值。
- 若 consuming repo 需要依賴此欄位作出 firmware 決策，應先確認專案端事實與 spec section anchor。

## `wHubCharacteristics` 位元群組

| Bits | 群組 | 角色摘要 |
|---|---|---|
| `1:0` | Logical Power Switching Mode | 描述 hub 的 power switching 模式。 |
| `2` | Compound Device | 描述 hub 是否為 compound device。 |
| `4:3` | Over-current Protection Mode | 描述 over-current protection 的模式。 |
| `6:5` | TT Think Time | 描述 Transaction Translator think time 類別。 |
| `7` | Port Indicators Supported | 描述是否支援 port indicator。 |
| `15:8` | Reserved | 保留位元；本頁不主張 firmware 可以任意重用。 |

### `wHubCharacteristics` 的安全解讀邊界

- `1:0` 和 `6:5` 常直接影響 power switching 與 TT 行為，因此最容易被 consuming repo 過度套用。
- 本 repo 的用途是提供標準側 reference summary，不是把這些欄位當成專案真相來源。
- 如果 descriptor 中的 power switching mode 或 TT think time 與已確認專案事實衝突，應進入 Standard Escalation Mode，而不是直接覆寫 firmware 假設。

## Governed linkage

- `tables/class_request_matrix.yaml`：`GET_DESCRIPTOR` family 提供 hub class request 的 request-level linkage。
- `specs/escalation_table.md`：`E-01`、`E-07`、`E-08` 直接涉及 `bNbrPorts`、`wHubCharacteristics[6:5]`、`wHubCharacteristics[1:0]`。
- `specs/transaction_translator.md`：補充 TT 類型與 TT think time 的高層摘要。

目前沒有專用的 hub descriptor governed table；因此本頁的 linkage 以 request family、escalation 規則、相關摘要頁為主。

## 本頁可回答與不可回答的問題

本頁可回答：

- Hub descriptor 中有哪些核心欄位。
- 哪些欄位與 port 數量、power switching、over-current、TT、removable bitmap 有關。
- 哪些欄位屬於 escalation-sensitive 對照點。

本頁不可回答：

- 某個裝置 descriptor 是否已被 PDF section-level 驗證。
- `DeviceRemovable` 或 `PortPwrCtrlMask` 的每一個 bit pattern 是否已被本 repo fully verified。
- 專案端是否應依本頁直接修改 firmware descriptor 值。

## Non-claims

- 本頁不是 USB 2.0 PDF 的逐欄位、逐位元驗證紀錄。
- 本頁不宣告任何具體 descriptor dump 為正確或錯誤。
- 本頁不建立 `wHubCharacteristics` 的完整 semantic truth table。
- 本頁不覆寫 consuming repo 已確認的 project facts。
