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

> 資料範圍：USB 2.0 規範 Rev 2.0，第 11.23.2.1 章節。  
> 本頁是消費端參考摘要，不是欄位逐位元 PDF 驗證紀錄；未提供 section-level 佐證時不會被當作 `verified`。

## 頁面目的

本頁回答：

- hub descriptor 的主要欄位有哪些。
- 哪些欄位常見於 firmware、enumeration log、descriptor dump 與 consuming repo 規則中。
- 哪些欄位與 `port count`、電源切換、過電流行為、TT 行為有關。

本頁不回答：

- 是否已針對特定 descriptor dump 做過逐位元 PDF 驗證。
- 是否某個 firmware 實作在此處可視為正確。
- 是否 `wHubCharacteristics` 的所有位元組合已在本 repo 被完整語意驗證。

## 主要 descriptor 欄位

hub descriptor 由 class-specific `GET_DESCRIPTOR` 取得，`descriptor type` 為 `0x29`。  
在本 repo 的 reviewed request surface 目前已明確將 `GET_DESCRIPTOR` 與 `SET_DESCRIPTOR` 鏈回這個 descriptor type 邊界，但這只是一層參考鏈接，不代表頁面可被視為 page-level verified。

| Offset | 欄位 | 大小 | 角色摘要 |
|---|---|---|---|
| 0 | `bDescLength` | 1 byte | hub descriptor 全長。 |
| 1 | `bDescriptorType` | 1 byte | hub descriptor 類型，本頁參考語境預期為 `0x29`。 |
| 2 | `bNbrPorts` | 1 byte | hub 報告的下游 port 數量。 |
| 3 | `wHubCharacteristics` | 2 bytes | 包含 power switching、compound device、過電流模式、TT think time、port indicators 等位元欄位。 |
| 5 | `bPwrOn2PwrGood` | 1 byte | 從上電到 power-good 的延遲（2 ms 為單位）。 |
| 6 | `bHubContrCurrent` | 1 byte | hub controller 電流需求，常以 mA 解讀。 |
| 7 | `DeviceRemovable` | 變長 | 各 port 是否可拆卸的 bitmap。 |
| 7+x | `PortPwrCtrlMask` | 變長 | 與各 port 電源控制相關的對應欄位；`0xFF` 型態常見，但本頁不將其提升為 verified 真值。 |

## 欄位摘要

### `bDescLength`

- 定義 hub descriptor 的總長度。
- consuming repo 可在讀取 descriptor dump 時做基本結構 sanity check。
- 本頁不聲明任何特定設備的值本身是正確的。

### `bDescriptorType`

- 指定 class-specific hub descriptor type。
- 在本 repo 參考摘要中，hub descriptor type 以 `0x29` 表述。
- 若 firmware 或 dump 報出的 type 不一致，先回到規格章節與 descriptor 擷取結果交叉確認，不以本頁覆蓋已確認 project fact。

### `bNbrPorts`

- 這是下游 port 數量的直接 descriptor 欄位。
- 常用於對照硬體實體 port、firmware 暴露的 port 數量與 consuming repo 的 topology 假設。
- 若 `bNbrPorts` 與已確認事實衝突，應納入 escalation 檢核，對齊 `E-01`。

### `wHubCharacteristics`

- 這個 16-bit 欄位攜帶多個 descriptor 語意，不能視為單一布林屬性。
- 常被消費的子群組：
  - power switching 模式
  - over-current 保護模式
  - TT think time
  - port indicators 支援情況
- 本頁僅整理欄位角色，不聲明所有位元組合都有 section-level 驗證。

### `bPwrOn2PwrGood`

- 表示上電到 power-good 的延遲。
- 常影響 host/firmware 對 power sequence 的推理，但本頁不提供時序保證。
- 如果 consuming repo 需要轉成具體 timing 事實，需回到 USB-IF PDF 與專案側硬體資料交叉驗證。

### `bHubContrCurrent`

- 描述 hub controller 的電流需求。
- 可作為 descriptor dump 或設計文件比對的參考點。
- 本頁不把它升級為版圖/電路級電流驗證結論。

### `DeviceRemovable`

- 這個 bitmap 表示各下游 port 是否被標註為可拆卸。
- consuming repo 可將其當作 descriptor-side 的語意上下文，但不能單靠本頁覆蓋已確認的固定型硬體、焊接型硬體或 topology 事實。
- 若「可拆卸 vs 不可拆卸」有爭議，應保持 escalation 流程。

### `PortPwrCtrlMask`

- 此欄位通常與各 port 電源控制語意一起解讀。
- `0xFF` 類型數值在實務上常見，但這是常見模式，本 repo 不視為普遍且已驗證的真值。
- consuming repo 要據此做 firmware 決策前，請先對照專案事實與 spec anchor。

## `wHubCharacteristics` 位元群組

| Bits | 群組 | 角色摘要 |
|---|---|---|
| `1:0` | Logical Power Switching Mode | hub power-switching 模式 |
| `2` | Compound Device | 是否為 compound device |
| `4:3` | Over-current Protection Mode | 过电流保護模式 |
| `6:5` | TT Think Time | TT think-time 類別 |
| `7` | Port Indicators Supported | 是否支援 port indicator |
| `15:8` | Reserved | 保留位元，頁面不聲明 firmware 可任意重用 |

### 位元欄位編碼參考

> 來源：§11.23.2.1 Table 11-13。Reviewed boundary only；非語意行為驗證。

**bits\[1:0\] — Logical Power Switching Mode**

| 值 | 含義 |
|---|---|
| `0b00` | Ganged power switching（所有 port 同時切換） |
| `0b01` | Individual（逐 port）power switching |
| `0b10` | Reserved |
| `0b11` | Reserved |

**bit\[2\] — Compound Device**

| 值 | 含義 |
|---|---|
| `0` | Hub 不是 compound device |
| `1` | Hub 是 compound device |

**bits\[4:3\] — Over-current Protection Mode**

| 值 | 含義 |
|---|---|
| `0b00` | Global 過電流保護（整個 hub） |
| `0b01` | 逐 port 過電流保護 |
| `0b10` | 不上報過電流保護 |
| `0b11` | Reserved |

**bits\[6:5\] — TT Think Time**

| 值 | 含義 |
|---|---|
| `0b00` | 最多 8 FS bit times inter-transaction gap |
| `0b01` | 最多 16 FS bit times |
| `0b10` | 最多 24 FS bit times |
| `0b11` | 最多 32 FS bit times |

**bit\[7\] — Port Indicators Supported**

| 值 | 含義 |
|---|---|
| `0` | 不支援 port indicator |
| `1` | 支援 port indicator；`SET_FEATURE(PORT_INDICATOR)` 適用 |

**bits\[15:8\] — Reserved**

必須為 zero。USB 2.0 spec 未賦予這些位元含義。

### `wHubCharacteristics` 的安全解讀邊界

- `1:0` 與 `6:5` 常直接影響 power switching 與 TT 行為，消費端容易過度套用。
- 本 repo 提供標準面參考摘要，不是 project-truth 權威。
- 若 descriptor 的 power switching mode 或 TT think time 與已確認 project facts 衝突，應進入 Standard Escalation Mode，而非直接改變 firmware 推論。

## Governed Linkage

- `tables/hub_descriptor_matrix.yaml`：本 repo 對 8 個 USB 2.0 hub descriptor 欄位的 governed field-role surface。
- `tables/wHubCharacteristics_bit_matrix.yaml`：wHubCharacteristics bit-group 語意的 governed surface——power switching [1:0]、compound device [2]、OC mode [4:3]、TT think time [6:5]、port indicators [7]、reserved high byte [15:8]。
- `tables/class_request_matrix.yaml`：`GET_DESCRIPTOR` family 對應 hub descriptor 存取請求 linkage。
- `specs/hub_class_requests.md`：Hub class request 家族對應到 descriptor-side request context。
- `specs/usb2.md`：USB 2.0 入口與題目分類（`zh`）。
- `specs/escalation_table.md`：`E-01`、`E-07`、`E-08` 牽涉 `bNbrPorts`、`wHubCharacteristics[6:5]`、`wHubCharacteristics[1:0]`。
- `specs/transaction_translator.md`：提供 TT type 與 TT think-time 的高階摘要。

Hub descriptor table 僅作欄位角色參考，不會升級頁面為逐位元驗證，也不會聲明 descriptor dump 的正確性。

## 本頁可回答與不可回答

本頁可回答：

- hub descriptor 的核心欄位有哪些。
- 哪些欄位與 `port count`、power switching、over-current、TT、可拆卸 bitmap 有關。
- 哪些欄位是 escalation-sensitive 的比對點。

本頁不可回答：

- 某個特定設備的 descriptor 是否已做過 section-level 驗證。
- `DeviceRemovable` 或 `PortPwrCtrlMask` 的每個位元樣式是否都已完整驗證。
- consuming repo 是否應直接以此頁改變 firmware 值。

## Non-claims

- 本頁不是逐欄位或逐位元的 USB 2.0 PDF 驗證紀錄。
- 本頁不聲明任何特定 descriptor dump 正確或錯誤。
- 本頁不建立 `wHubCharacteristics` 的完整語意真值表。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
