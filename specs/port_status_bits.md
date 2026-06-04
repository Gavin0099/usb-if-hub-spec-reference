---
title: Port Status Bits
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port Status Bits

> Source scope: USB 2.0 Specification Rev 2.0, Section 11.24.2.7.  
> This page is a reference summary, not a full bit-by-bit verified reconstruction of the source spec.

## 頁面目的

本頁回答：

- `GET_STATUS` 可以回報的 hub-level 與 port-level 欄位
- `Status` 與 `Change` bits 的差異
- 目前 machine-readable layer 已涵蓋的 hub/port status 與 change entries
- 目前有哪些 entry 已 live `verified`、且可驗證範圍有多窄

本頁不回答：

- 所有 port bits 是否都已完成 PDF section-level 驗證
- timing、debounce、reset、error-recovery 的正確性驗證是否完成
- `SetPortFeature` / `ClearPortFeature` 的完整 host 行為模型

## Status Field Model

- `GET_STATUS` 可以回報 hub-level 的 `wHubStatus` / `wHubChange`
- 也可以回報 port-level 的 `wPortStatus` / `wPortChange`
- `Status` bits 描述目前狀態
- `Change` bits 描述該狀態自上次清除後是否曾改變
- 對於 change bits，`CLEAR_FEATURE(...)` 應以「確認事件、並清除此已記錄變更」來解讀

## Hub-Level Bits

| Field | Bit | Name | Meaning |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power status |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub over-current status |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | Records whether local power status has changed since the last clear |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | Records whether over-current status has changed since the last clear |

## Port-Level Bits

| Field | Bit | Name | State | Meaning |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port connection status |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port enabled status |
| `wPortStatus` | 2 | `PORT_SUSPEND` | defined | Port suspend status |
| `wPortStatus` | 3 | `PORT_OVER_CURRENT` | defined | Port over-current status |
| `wPortStatus` | 4 | `PORT_RESET` | defined | Port reset status |
| `wPortStatus` | 8 | `PORT_POWER` | defined | Port power status |
| `wPortStatus` | 9 | `PORT_LOW_SPEED` | defined | Port low-speed status indicator |
| `wPortStatus` | 10 | `PORT_HIGH_SPEED` | defined | Port high-speed status indicator |
| `wPortStatus` | 11 | `PORT_TEST` | defined | Port test-mode status |
| `wPortStatus` | 12 | `PORT_INDICATOR` | defined | Port indicator status |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | Boundary placeholder for the 16-bit field |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | Records whether connection status has changed since the last clear |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | Records whether enable status has changed since the last clear |
| `wPortChange` | 2 | `C_PORT_SUSPEND` | defined | Records whether suspend status has changed since the last clear |
| `wPortChange` | 3 | `C_PORT_OVER_CURRENT` | defined | Records whether over-current status has changed since the last clear |
| `wPortChange` | 4 | `C_PORT_RESET` | defined | Records whether reset status has changed since the last clear |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | Boundary placeholder for the 16-bit change field |

本頁新增追蹤的 status/change entries 目前僅為 reviewed namespace entries。  
它們不會擴大以下已在 live verified 的八筆：

## Live Verified Entries

目前已提升為 `verified` 的條目為 8 筆：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| `PORT_CONNECTION` | `wPortStatus` | bit 0 | bit name and bit position only |
| `PORT_ENABLE` | `wPortStatus` | bit 1 | bit name and bit position only |
| `C_PORT_CONNECTION` | `wPortChange` | bit 0 | bit name and bit position only |
| `C_PORT_ENABLE` | `wPortChange` | bit 1 | bit name and bit position only |
| `HUB_LOCAL_POWER` | `wHubStatus` | bit 0 | bit name and bit position only |
| `HUB_OVER_CURRENT` | `wHubStatus` | bit 1 | bit name and bit position only |
| `C_HUB_LOCAL_POWER` | `wHubChange` | bit 0 | bit name and bit position only |
| `C_HUB_OVER_CURRENT` | `wHubChange` | bit 1 | bit name and bit position only |

可驗證範圍目前刻意縮窄，只涵蓋：

- bit 名稱
- bit 位置

並不代表本頁已完成以下驗證：

- timing、debounce、reset、state-transition 行為
- host-side `SetPortFeature` / `ClearPortFeature` semantics
- `PORT_ENABLE` 完整 enable/disable 狀態機
- `port_status_bit_matrix` 全頁

因此 frontmatter 仍保持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Reviewed Entries Outside Verified Scope

以下 port status/change entries 目前為 `reviewed`，不是 `verified`：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_SUSPEND` | `wPortStatus` | bit 2 | bit name and bit position only |
| `PORT_OVER_CURRENT` | `wPortStatus` | bit 3 | bit name and bit position only |
| `PORT_RESET` | `wPortStatus` | bit 4 | bit name and bit position only |
| `PORT_POWER` | `wPortStatus` | bit 8 | bit name and bit position only |
| `PORT_LOW_SPEED` | `wPortStatus` | bit 9 | bit name and bit position only |
| `PORT_HIGH_SPEED` | `wPortStatus` | bit 10 | bit name and bit position only |
| `PORT_TEST` | `wPortStatus` | bit 11 | bit name and bit position only |
| `PORT_INDICATOR` | `wPortStatus` | bit 12 | bit name and bit position only |
| `C_PORT_SUSPEND` | `wPortChange` | bit 2 | bit name and bit position only |
| `C_PORT_OVER_CURRENT` | `wPortChange` | bit 3 | bit name and bit position only |
| `C_PORT_RESET` | `wPortChange` | bit 4 | bit name and bit position only |

這些條目提升了 namespace coverage，但未驗證 timing、state machine、clear sequencing、error recovery、speed 解碼、test-mode、power-switch policy、indicator 行為。

## Reviewed Boundary Placeholders

兩個高位 placeholder 仍僅作為 boundary markers reviewed：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus` | bit 15 | 16-bit status-field high boundary only |
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange` | bit 15 | 16-bit change-field high boundary only |

這些 reviewed placeholders 並未新增 status semantics。  
它們只保留 machine-readable layer 的範圍資訊，指出 status / change field 都是 16-bit，含高位邊界標記。

## Change Bits and `CLEAR_FEATURE`

可以把 `wPortChange` / `wHubChange` 視為「已鎖存的 change event flag」：

- bit = `1`：代表該狀態自上次 clear 後至少變更過一次
- bit = `0`：代表上次 clear 後未記錄到此變更
- `CLEAR_FEATURE(...)`：host acknowledge event 並清除此已記錄變更位元

範例：

- `C_PORT_CONNECTION = 1` 代表連線狀態自上次 clear 後曾變更
- 取得 `GET_STATUS` 後，host 可發送 `CLEAR_FEATURE(C_PORT_CONNECTION)` 清除此 event record
- 如果之後連線再次改變，這個 bit 可以再次被設為 `1`

## Speed Bits Must Be Decoded Together

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不應獨立解釋。它們是一組組合編碼：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | Interpretation |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / unexpected combination |

因此 `PORT_LOW_SPEED = 0` 單獨無法單獨代表 full-speed。  
只有當 `PORT_HIGH_SPEED = 0` 時，才能表示 full-speed。

## Section Anchor and Verified-Scope Boundary

本頁目前會有兩種證據訊號：

- `section_refs` 作為 evidence attachment metadata
- live `verified` promotions，當前為 `PORT_CONNECTION`、`PORT_ENABLE`、`C_PORT_CONNECTION`、`C_PORT_ENABLE`、`HUB_LOCAL_POWER`、`HUB_OVER_CURRENT`、`C_HUB_LOCAL_POWER`、`C_HUB_OVER_CURRENT`

兩者不能混為一談。

目前狀態：

- 有些 pilot entries 帶有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`、`wPortStatus.bit1.PORT_ENABLE`、`wPortChange.bit0.C_PORT_CONNECTION`、`wPortChange.bit1.C_PORT_ENABLE`、`wHubStatus.bit0.HUB_LOCAL_POWER`、`wHubStatus.bit1.HUB_OVER_CURRENT`、`wHubChange.bit0.C_HUB_LOCAL_POWER`、`wHubChange.bit1.C_HUB_OVER_CURRENT` 目前為 live `verified`
- 所有 verified scopes 皆為 `bit_name_and_position_only`
- 其餘已定義的 port status/change entries 僅為 reviewed namespace entries
- 這仍不代表 USB 2.0 PDF semantic verification 完整完成

若未來 wiki claim block 需要 `section_refs`，應維持 Phase 7A 的 metadata 結構，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

該 metadata 僅為 evidence attachment，不代表頁面或 claim block 自動提升為 `verified`。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`: hub / port status bit namespace 的 primary machine-readable source
- `specs/hub_class_requests.md`: `GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE` 的 request-family summary
- `specs/feature_selectors.md`: `C_PORT_*` 的 selector boundary
- `specs/escalation_table.md`: escalation triggers（例如 E-02、E-03、E-09）

## Non-claims

- 本頁不宣告所有 port status bits 已完成 PDF-level 驗證。
- 本頁不宣告 speed bits、reset bits、power bits 及相鄰語意全部完成驗證。
- 本頁不把 8 筆 verified entries 扩展為「全頁 verified」。
- 本頁不把 boundary placeholders 解讀為定義式 status / change semantics。
- 本頁不將 status-bit summary 升為 firmware implementation authority。
