---
title: 連接埠狀態位元
claim_level: inferred
status: review_required
last_reviewed: "2026-06-02"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# 連接埠狀態位元

> 來源範圍：USB 2.0 Specification Rev 2.0，Section 11.24.2.7。  
> 本頁目前是 reference summary，不是完整的逐 bit verified 規格重建。

## Status Field Model

- `GET_STATUS` 可能回傳 hub 層級的 `wHubStatus` / `wHubChange`，或 port 層級的 `wPortStatus` / `wPortChange`。
- `Status` bits 描述目前狀態；`Change` bits 描述自上次清除以來是否發生過對應變化。
- 對 change bits 而言，`CLEAR_FEATURE` 最好理解成「確認並清除此變更事件紀錄」。

## Hub-Level Bits

| 欄位 | Bit | 名稱 | 意義 |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power status |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub over-current status |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | 記錄 local power status 是否自上次清除以來發生變化 |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | 記錄 over-current status 是否自上次清除以來發生變化 |

## Minimum Port-Level Boundary

| 欄位 | Bit | 名稱 | 狀態 | 意義 |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port connection status |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port enabled status |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | 16-bit status field boundary placeholder |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | 記錄 connection status 是否自上次清除以來發生變化 |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | 記錄 enable status 是否自上次清除以來發生變化 |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | 16-bit change field boundary placeholder |

## Change Bits 與 `CLEAR_FEATURE`

可以把 `wPortChange` / `wHubChange` 理解成 latched change-event flags：

- bit = `1`：對應狀態自上次清除後至少變化過一次
- bit = `0`：自上次清除後沒有記錄到這類變化
- `CLEAR_FEATURE(...)`：host 確認該事件後，清除這個記錄用的 change bit

例子：

- `C_PORT_CONNECTION = 1` 表示 connection state 自上次清除後有變化
- host 讀完 `GET_STATUS` 之後，可以送 `CLEAR_FEATURE(C_PORT_CONNECTION)` 來清除此事件紀錄
- 若之後 connection 再次變化，這個 bit 仍可重新被設為 `1`

## 速度位元必須合併解碼

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不能獨立解讀，它們共同構成速度編碼：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | 解讀 |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

所以像「`PORT_LOW_SPEED = 0` 表示 full-speed」這種說法本身不完整。只有在 `PORT_HIGH_SPEED` 也為 `0` 時，才是 full-speed。

## Section Anchor Pilot Note

Phase 7B 已在 `tables/port_status_bit_matrix.yaml` 的部分 entry 掛上 `section_refs`，用途是測試 entry-level anchor metadata 是否能安全附著。

這代表：

- pilot entries 現在可以帶 `section_refs`
- 但 `claim_level` 仍然是 `inferred`
- `evidence_status` 仍然是 `review_required`
- 這不等於 USB 2.0 PDF bit-level semantic verification 已完成

如果未來要在 wiki claim block 掛 `section_refs`，應採用 Phase 7A 定義的結構，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

這個 metadata block 本身只是 evidence attachment，不會自動把頁面或 claim block 升成 `verified`。

## Usage Notes

- 本頁不是完整的 bit encyclopedia；它是目前已進入 machine-readable layer 的最小摘要面。
- `PORT_OVER_CURRENT`、`PORT_RESET`、`PORT_POWER`、速度指示位元與其他細節，仍需要更強的 PDF-level verification。
- `Reserved` bits 不應被 firmware 靜默重用；若有此情況，屬於 escalation condition。
