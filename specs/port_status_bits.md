---
title: Port Status Bits
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
> 本頁仍是 reference summary，不是完整逐 bit verified 的規格重建。

## Status Field Model

- `GET_STATUS` 可回傳 hub 層級的 `wHubStatus` / `wHubChange`，或 port 層級的 `wPortStatus` / `wPortChange`。
- `Status` bits 描述目前狀態；`Change` bits 描述自上次清除以來是否發生過變化。
- 對 change bits 來說，`CLEAR_FEATURE` 最好理解成「host 已確認此變更事件，並清除此事件紀錄」。

## Hub-Level Bits

| Field | Bit | Name | Meaning |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power status |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub over-current status |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | 記錄 local power status 是否自上次清除以來發生變化 |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | 記錄 over-current status 是否自上次清除以來發生變化 |

## Minimum Port-Level Boundary

| Field | Bit | Name | State | Meaning |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port connection status |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port enabled status |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | 16-bit status field boundary placeholder |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | 記錄 connection status 是否自上次清除以來發生變化 |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | 記錄 enable status 是否自上次清除以來發生變化 |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | 16-bit change field boundary placeholder |

## Live Verified Entries（Phase 8E、Phase 8H）

目前有兩筆 live governed entry 已升級為 `verified`：

| Entry | 欄位 | 位元 | Verified Scope |
|---|---|---|---|
| PORT_CONNECTION | `wPortStatus` | bit 0 | bit name and bit position only |
| PORT_ENABLE | `wPortStatus` | bit 1 | bit name and bit position only |

這兩筆 verified 的範圍非常窄，只包含 **bit 名稱與 bit 位置**。

這些 verified **不代表**：

- 任何 timing、state-transition、debounce 或 reset 行為已驗證
- `SetPortFeature`、`ClearPortFeature` 的 host-side semantic behavior 已驗證
- PORT_ENABLE 的 enable/disable 狀態機、error recovery 條件已驗證
- 本頁或整張 `port_status_bit_matrix` 已升級為 page-level / table-level verified

所以本頁 frontmatter 仍維持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Change Bits and `CLEAR_FEATURE`

可以把 `wPortChange` / `wHubChange` 想成 latched change-event flags：

- bit = `1`：對應狀態自上次清除以來至少變化過一次
- bit = `0`：自上次清除以來沒有記錄到此類變化
- `CLEAR_FEATURE(...)`：host 確認該事件後，清除此變更紀錄 bit

例子：

- `C_PORT_CONNECTION = 1` 表示 connection state 自上次清除後有變化
- host 讀完 `GET_STATUS` 之後，可以送 `CLEAR_FEATURE(C_PORT_CONNECTION)` 來清除此事件紀錄
- 如果之後又發生新的連接變化，該 bit 仍可再次變成 `1`

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不能各自獨立解讀，它們必須合併成速度編碼：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

因此像「`PORT_LOW_SPEED = 0` 表示 full-speed」這種說法本身不完整。只有在 `PORT_HIGH_SPEED` 也為 `0` 時，才是 full-speed。

## Section Anchor and Verified-Scope Boundary

本 repo 現在同時存在兩層不同訊號：

- `section_refs`：evidence attachment metadata
- 單一 entry 的 live `verified` promotion

這兩者不能混為一談。

目前成立的是：

- 部分 pilot entries 帶有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`（Phase 8E）與 `wPortStatus.bit1.PORT_ENABLE`（Phase 8H）已升為 live `verified`
- 所有 verified scope 仍限於 `bit_name_and_position_only`

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

- 本頁不是完整 bit encyclopedia；它只整理目前 machine-readable layer 已暴露的核心表面。
- `PORT_OVER_CURRENT`、`PORT_RESET`、`PORT_POWER`、速度相關位元與其他細節，仍需要更強的 PDF-level verification。
- `Reserved` bits 不應被 firmware 靜默挪作它用；若發生這種情況，應視為 escalation condition。
