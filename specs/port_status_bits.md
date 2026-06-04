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

> Source scope: USB 2.0 規格 Rev 2.0，11.24.2.7。  
> 本頁是參考摘要，不是完整逐位元還原規格行為的真值表。

## 頁面用途

本頁目的是說明：

- `GET_STATUS` 可回傳哪些 hub-level / port-level 欄位
- `Status` bit 與 `Change` bit 的差異
- 機器可讀層目前暴露了哪些 hub/port status 與 change entries
- 目前哪些 entry 已有 live `verified` 票，且其 `verified` 範圍是何種程度

本頁不主張：

- 全部 port bit 都完成 PDF 段落驗證
- 時序、抖動消除、重設、錯誤恢復語義都完成 correctness 驗證
- `SetPortFeature` / `ClearPortFeature` 的完整 host 行為模型

## 狀態欄位模型

- `GET_STATUS` 可回傳 hub-level 的 `wHubStatus` / `wHubChange`
- 也可回傳 port-level 的 `wPortStatus` / `wPortChange`
- `Status` bits 表示「目前狀態」
- `Change` bits 表示「自上次清除後是否有變更」
- 對 change bits 來說，`CLEAR_FEATURE(...)` 可理解為「確認並清除該變更事件」

## Hub-Level Bits

| Field | Bit | Name | Meaning |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power 狀態 |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub 過流狀態 |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | 上次清除後是否曾改變 local power |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | 上次清除後是否曾改變過流狀態 |

## Port-Level Bits

| Field | Bit | Name | State | Meaning |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port 連線狀態 |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port 啟用狀態 |
| `wPortStatus` | 2 | `PORT_SUSPEND` | defined | Port 暫停狀態 |
| `wPortStatus` | 3 | `PORT_OVER_CURRENT` | defined | Port 過流狀態 |
| `wPortStatus` | 4 | `PORT_RESET` | defined | Port 重設狀態 |
| `wPortStatus` | 8 | `PORT_POWER` | defined | Port 電源狀態 |
| `wPortStatus` | 9 | `PORT_LOW_SPEED` | defined | Port 低速指示 |
| `wPortStatus` | 10 | `PORT_HIGH_SPEED` | defined | Port 高速指示 |
| `wPortStatus` | 11 | `PORT_TEST` | defined | Port 測試模式狀態 |
| `wPortStatus` | 12 | `PORT_INDICATOR` | defined | Port 指示燈狀態 |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | 16 位元欄位邊界標示 |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | 上次清除後是否曾改變連線狀態 |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | 上次清除後是否曾改變啟用狀態 |
| `wPortChange` | 2 | `C_PORT_SUSPEND` | defined | 上次清除後是否曾改變暫停狀態 |
| `wPortChange` | 3 | `C_PORT_OVER_CURRENT` | defined | 上次清除後是否曾改變過流狀態 |
| `wPortChange` | 4 | `C_PORT_RESET` | defined | 上次清除後是否曾改變重設狀態 |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | 16 位元變更欄位邊界標示 |

本頁新增追蹤的 status / change entries 僅屬 reviewed namespace，未自動擴大 verified 範圍。

## Live Verified Entries

目前有 8 筆 live `verified` entries：

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| `PORT_CONNECTION` | `wPortStatus` | bit 0 | 名稱 + bit 位置 |
| `PORT_ENABLE` | `wPortStatus` | bit 1 | 名稱 + bit 位置 |
| `C_PORT_CONNECTION` | `wPortChange` | bit 0 | 名稱 + bit 位置 |
| `C_PORT_ENABLE` | `wPortChange` | bit 1 | 名稱 + bit 位置 |
| `HUB_LOCAL_POWER` | `wHubStatus` | bit 0 | 名稱 + bit 位置 |
| `HUB_OVER_CURRENT` | `wHubStatus` | bit 1 | 名稱 + bit 位置 |
| `C_HUB_LOCAL_POWER` | `wHubChange` | bit 0 | 名稱 + bit 位置 |
| `C_HUB_OVER_CURRENT` | `wHubChange` | bit 1 | 名稱 + bit 位置 |

這個 verified 範圍故意限定為窄範圍，只覆蓋：

- bit 名稱
- bit 位置

它不表示已完成以下完整驗證：

- timing、debounce、reset、state-transition 的行為語意
- host-side `SetPortFeature` / `ClearPortFeature` 行為
- `PORT_ENABLE` enable/disable 的完整狀態機
- 全域 `port_status_bit_matrix` 的行為真值

本頁 frontmatter 仍維持：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## Reviewed Entries Outside Verified Scope

以下 entries 目前是 `reviewed` 而不是 `verified`：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_SUSPEND` | `wPortStatus` | bit 2 | 名稱 + bit 位置 |
| `PORT_OVER_CURRENT` | `wPortStatus` | bit 3 | 名稱 + bit 位置 |
| `PORT_RESET` | `wPortStatus` | bit 4 | 名稱 + bit 位置 |
| `PORT_POWER` | `wPortStatus` | bit 8 | 名稱 + bit 位置 |
| `PORT_LOW_SPEED` | `wPortStatus` | bit 9 | 名稱 + bit 位置 |
| `PORT_HIGH_SPEED` | `wPortStatus` | bit 10 | 名稱 + bit 位置 |
| `PORT_TEST` | `wPortStatus` | bit 11 | 名稱 + bit 位置 |
| `PORT_INDICATOR` | `wPortStatus` | bit 12 | 名稱 + bit 位置 |
| `C_PORT_SUSPEND` | `wPortChange` | bit 2 | 名稱 + bit 位置 |
| `C_PORT_OVER_CURRENT` | `wPortChange` | bit 3 | 名稱 + bit 位置 |
| `C_PORT_RESET` | `wPortChange` | bit 4 | 名稱 + bit 位置 |

這些條目提供命名空間覆蓋，不代表 timing、state machine、清除順序、錯誤恢復、速度解碼、test-mode、電源開關策略或 indicator 行為已驗證。

## Reviewed Boundary Placeholders

以下兩個高位元占位符僅作為邊界標記 reviewed：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus` | bit 15 | 16-bit status 欄位上界 |
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange` | bit 15 | 16-bit change 欄位上界 |

這些 reviewed placeholder 不新增 status semantics。  
它們僅保持機器可讀層明確：status / change 欄位為 16-bit 並有高位元界線。

## Change Bits 與 `CLEAR_FEATURE`

可將 `wPortChange` / `wHubChange` 理解為「已暫存的變更事件 flag」：

- bit = `1`：自上次清除後，對應狀態至少變更過一次
- bit = `0`：自上次清除後，尚未記錄到該變更
- `CLEAR_FEATURE(...)`：host 確認該事件並清除已記錄變更位元

範例：

- `C_PORT_CONNECTION = 1` 表示連線狀態在上次清除後變更過
- `GET_STATUS` 之後，host 可發 `CLEAR_FEATURE(C_PORT_CONNECTION)` 清除此事件
- 若狀態再次改變，bit 仍可再次被設定

## 速度位元需同時解讀

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不應獨立解讀，需組合判斷：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | 解讀 |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | Reserved / 異常組合 |

因此不能只說「`PORT_LOW_SPEED = 0` 即 full-speed」，完整判斷還要同時檢查 `PORT_HIGH_SPEED = 0`。

## 區段 anchor 與 verified 範圍邊界

目前 repo 同時保有兩種 evidence 相關訊號：

- `section_refs`（供 evidence attachment metadata）
- live `verified`（目前限於 8 筆 entry）

兩者不可混用解讀。

目前情況：

- 部分 pilot entries 有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`、`wPortStatus.bit1.PORT_ENABLE`、`wPortChange.bit0.C_PORT_CONNECTION`、`wPortChange.bit1.C_PORT_ENABLE`、`wHubStatus.bit0.HUB_LOCAL_POWER`、`wHubStatus.bit1.HUB_OVER_CURRENT`、`wHubChange.bit0.C_HUB_LOCAL_POWER`、`wHubChange.bit1.C_HUB_OVER_CURRENT` 是 live `verified`
- 以上 verified scope 仍維持為 `bit_name_and_position_only`
- 其他定義的 port status/change entries 仍只是 reviewed namespace entries
- 這不表示 USB 2.0 PDF semantic verification 完整完成

若未來 wiki claim block 需要 `section_refs`，請維持 Phase 7A 的 metadata 結構，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

上述 metadata 僅為 evidence 附屬標記，並不自動將頁面或 claim block 提升為 `verified`。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`：hub / port status bit 命名空間的主要機器可讀來源
- `specs/hub_class_requests.md`：`GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE` 的請求族摘要
- `specs/feature_selectors.md`：`C_PORT_*` 的 selector boundary 對照
- `specs/escalation_table.md`：E-02、E-03、E-09 等 escalation triggers

## Non-claims

- 本頁不聲明全部 port status bits 已完成 PDF 逐段驗證。
- 本頁不聲明速度位、重設位、電源位與鄰近語義已完整驗證。
- 本頁不將 8 筆 verified entries 視為整頁都已 verified。
- 本頁不將高位元 boundary placeholder 轉成已定義 status / change semantics。
- 本頁不將 status-bit summary 提升為 firmware implementation authority。
