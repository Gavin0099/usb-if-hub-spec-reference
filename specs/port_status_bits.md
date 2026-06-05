---
title: Port Status Bits
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port Status Bits

> 來源範圍：USB 2.0 規範 Rev 2.0，章節 11.24.2.7。  
> 本頁為參考摘要，不是 USB 2.0 規格逐位元逐語意的完整驗證重建。

## 頁面目的

這頁的目標是讓讀者快速掌握：

- `GET_STATUS` 可回傳哪些 hub-level / port-level 欄位
- `Status` 與 `Change` bit 的差異
- 哪些 hub/port status 與 change bits 已納入機器可讀層
- 哪些 entry 目前是 `verified`，以及 `verified` 的語意邊界

這頁不代表：

- 所有 port bits 已完成 PDF 章節級驗證
- 時序、去抖、重置、錯誤復原行為已完成 correctness 驗證
- `SET_FEATURE` / `CLEAR_FEATURE` 已有完整 host 行為模型

## Status 欄位模型

- `GET_STATUS` 可回傳 hub-level 的 `wHubStatus` / `wHubChange`
- 也可回傳 port-level 的 `wPortStatus` / `wPortChange`
- `Status` bit 呈現目前狀態
- `Change` bit 表示自上次清除後該狀態是否有改變
- 對 change bit，通常可理解為：`CLEAR_FEATURE(...)` 用來「確認並清除已紀錄的變更事件」

## Hub-Level Bits

| Field | Bit | Name | 意義 |
|---|---|---|---|
| `wHubStatus` | 0 | `HUB_LOCAL_POWER` | Hub local power 狀態 |
| `wHubStatus` | 1 | `HUB_OVER_CURRENT` | Hub 過流狀態 |
| `wHubChange` | 0 | `C_HUB_LOCAL_POWER` | 紀錄自上次 clear 後 local power 狀態是否有變更 |
| `wHubChange` | 1 | `C_HUB_OVER_CURRENT` | 紀錄自上次 clear 後過流狀態是否有變更 |

## Port-Level Bits

| Field | Bit | Name | 狀態類型 | 意義 |
|---|---|---|---|---|
| `wPortStatus` | 0 | `PORT_CONNECTION` | defined | Port 連線狀態 |
| `wPortStatus` | 1 | `PORT_ENABLE` | defined | Port 啟用狀態 |
| `wPortStatus` | 2 | `PORT_SUSPEND` | defined | Port suspend 狀態 |
| `wPortStatus` | 3 | `PORT_OVER_CURRENT` | defined | Port 過流狀態 |
| `wPortStatus` | 4 | `PORT_RESET` | defined | Port reset 狀態 |
| `wPortStatus` | 8 | `PORT_POWER` | defined | Port 電源供應狀態 |
| `wPortStatus` | 9 | `PORT_LOW_SPEED` | defined | Port 低速端口指示 |
| `wPortStatus` | 10 | `PORT_HIGH_SPEED` | defined | Port 高速端口指示 |
| `wPortStatus` | 11 | `PORT_TEST` | defined | Port 測試模式狀態 |
| `wPortStatus` | 12 | `PORT_INDICATOR` | defined | Port 指示燈狀態 |
| `wPortStatus` | 15 | `PORT_STATUS_HIGH_BIT_BOUNDARY` | reserved | 16-bit status 欄位的邊界位 |
| `wPortChange` | 0 | `C_PORT_CONNECTION` | defined | 紀錄自上次 clear 後 connection 狀態是否有變更 |
| `wPortChange` | 1 | `C_PORT_ENABLE` | defined | 紀錄自上次 clear 後 enable 狀態是否有變更 |
| `wPortChange` | 2 | `C_PORT_SUSPEND` | defined | 紀錄自上次 clear 後 suspend 狀態是否有變更 |
| `wPortChange` | 3 | `C_PORT_OVER_CURRENT` | defined | 紀錄自上次 clear 後 over-current 狀態是否有變更 |
| `wPortChange` | 4 | `C_PORT_RESET` | defined | 紀錄自上次 clear 後 reset 狀態是否有變更 |
| `wPortChange` | 15 | `PORT_CHANGE_HIGH_BIT_BOUNDARY` | reserved | 16-bit change 欄位的邊界位 |

## 已完成 `verified` 的 tracked entries

目前有 19 個 live entry 被標為 `verified`（僅限 entry-level）。

| Entry | Field | Bit | Verified Scope |
|---|---|---|---|
| `PORT_CONNECTION` | `wPortStatus` | bit 0 | 僅限位元名稱與位元位置 |
| `PORT_ENABLE` | `wPortStatus` | bit 1 | 僅限位元名稱與位元位置 |
| `PORT_SUSPEND` | `wPortStatus` | bit 2 | 僅限位元名稱與位元位置 |
| `PORT_OVER_CURRENT` | `wPortStatus` | bit 3 | 僅限位元名稱與位元位置 |
| `PORT_RESET` | `wPortStatus` | bit 4 | 僅限位元名稱與位元位置 |
| `PORT_POWER` | `wPortStatus` | bit 8 | 僅限位元名稱與位元位置 |
| `PORT_LOW_SPEED` | `wPortStatus` | bit 9 | 僅限位元名稱與位元位置 |
| `PORT_HIGH_SPEED` | `wPortStatus` | bit 10 | 僅限位元名稱與位元位置 |
| `PORT_TEST` | `wPortStatus` | bit 11 | 僅限位元名稱與位元位置 |
| `PORT_INDICATOR` | `wPortStatus` | bit 12 | 僅限位元名稱與位元位置 |
| `C_PORT_CONNECTION` | `wPortChange` | bit 0 | 僅限位元名稱與位元位置 |
| `C_PORT_ENABLE` | `wPortChange` | bit 1 | 僅限位元名稱與位元位置 |
| `C_PORT_SUSPEND` | `wPortChange` | bit 2 | 僅限位元名稱與位元位置 |
| `C_PORT_OVER_CURRENT` | `wPortChange` | bit 3 | 僅限位元名稱與位元位置 |
| `C_PORT_RESET` | `wPortChange` | bit 4 | 僅限位元名稱與位元位置 |
| `HUB_LOCAL_POWER` | `wHubStatus` | bit 0 | 僅限位元名稱與位元位置 |
| `HUB_OVER_CURRENT` | `wHubStatus` | bit 1 | 僅限位元名稱與位元位置 |
| `C_HUB_LOCAL_POWER` | `wHubChange` | bit 0 | 僅限位元名稱與位元位置 |
| `C_HUB_OVER_CURRENT` | `wHubChange` | bit 1 | 僅限位元名稱與位元位置 |

### 已明示的 verified scope

- 位元名稱（bit name）
- 位元位置（bit position）

### 本頁不主張已完成

- 時序、去抖、重置、state-transition 行為
- host-side `SET_FEATURE` / `CLEAR_FEATURE` 實作語義
- `PORT_ENABLE` enable/disable 的完整狀態機
- 將整頁內容全部視為 `verified` 或 `port_status_bit_matrix` 全表驗證完成

本頁 frontmatter 仍保有：

- `claim_level: inferred`
- `status: review_required`
- `semantic_verification_claimed: false`

## reviewed 邊界項（非 verified）

目前沒有其他 defined 的 status/change entry 是「已 reviewed 但未 verified」。

這些 reviewed 項目只提供 namespace 邊界，不延伸 timing、state machine、清除序列、錯誤復原、速度解碼、test-mode、power/power-indicator 行為的驗證。

## Reviewed Boundary Markers

高位界限項目僅作為 reviewed 邊界標記：

| Entry | Field | Bit | Reviewed Scope |
|---|---|---|---|
| `PORT_STATUS_HIGH_BIT_BOUNDARY` | `wPortStatus` | bit 15 | 16-bit status 邊界位 |
| `PORT_CHANGE_HIGH_BIT_BOUNDARY` | `wPortChange` | bit 15 | 16-bit change 邊界位 |

這兩個 boundary marker 不代表額外的 status/change 行為定義，只保留 16-bit 欄位結構邊界語意。

## Change bit 與 `CLEAR_FEATURE`

`wPortChange` / `wHubChange` 可視為「是否有事件記錄」的 latch：

- bit = `1`：自上次 clear 後有至少一次對應事件變更
- bit = `0`：自上次 clear 後未再次記錄該變更
- `CLEAR_FEATURE(...)`：host 確認事件後清除該紀錄位元

範例：

- `C_PORT_CONNECTION = 1` 表示 connection 已變更過
- 讀取 `GET_STATUS` 後，host 可發 `CLEAR_FEATURE(C_PORT_CONNECTION)` 清除該事件紀錄
- 若連線再次變更，位元可再次被設為 1

## `PORT_*` 與 `C_PORT_*` 行為註解（中文）

這段保留「可供 consuming repo 對齊的行為邊界」，不做完整時序證明。

### `PORT_*`（status bits）

- `PORT_CONNECTION`
  - `0`：預期表示未接上設備或尚未可供通信；`1`：表示當前連線建立完成。
  - 常見用途是做接続變化的基礎可見性；是否可視為「剛剛連上」需結合 `C_PORT_CONNECTION`。
- `PORT_ENABLE`
  - 表示 port 的邏輯啟用結果；對應主機對資源使能的可見狀態。
  - 狀態本身可受 host 配置、錯誤恢復和中斷事件影響，但本頁不保證完整 state-machine。
- `PORT_SUSPEND`
  - `1` 時表示 port 處於 suspend 狀態（已暫停流量/節電或功率管理路徑）; `0` 表示未暫停。
  - 不以本頁宣告完整 suspend/resume 邊界與時序。
- `PORT_OVER_CURRENT`
  - `1` 表示該 port 的過流條件被偵測到。
  - 常見與 hub 過流保護策略有關，但實際閾值、恢復條件須以 firmware 實作與硬體資料校驗。
- `PORT_RESET`
  - 表示 reset 已被主機請求並反映端口重置狀態。
- `PORT_POWER`
  - 表示 port 目標電源供應啟用。實作上常有「啟用中」狀態延遲，建議搭配 `wPortChange`/firmware telemetry 判斷過渡。
- `PORT_LOW_SPEED`、`PORT_HIGH_SPEED`
  - 速度位元需聯合解讀，請見下一節「Speed bits 需共同解讀」。
- `PORT_TEST`
  - 指出 port 測試模式狀態，不足以直接映射到 host 測試流程成功與否。
- `PORT_INDICATOR`
  - 指示燈（LED）相關狀態；本頁只保留欄位角色，不做面板映射規格。

### `C_PORT_*`（change bits）

- `C_PORT_CONNECTION`
  - 代表自上次清除後，port 連線事件已發生過至少一次。
- `C_PORT_ENABLE`
  - 代表自上次清除後，port enable 相關事件曾改變。
- `C_PORT_SUSPEND`
  - 代表自上次清除後，port suspend 狀態曾改變（進入或離開 suspend）。
- `C_PORT_OVER_CURRENT`
  - 代表自上次清除後，過流事件曾發生與/或狀態變更過。
- `C_PORT_RESET`
  - 代表自上次清除後，port reset 相關事件曾發生；host 可視為 reset 邊界確認信號。

通用補充：

- `C_PORT_*` 的值語意是「事件已記錄」而非「目前唯一真實狀態」，  
- 在實務上通常採取 `GET_STATUS` 查閱 port status + `C_PORT_*` 查閱事件邊界（再配合 `CLEAR_FEATURE` 清除）。

## Speed bits 需共同解讀

`PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 不能獨立解讀，需組合判斷：

| `PORT_LOW_SPEED` | `PORT_HIGH_SPEED` | 解讀 |
|---|---|---|
| 0 | 0 | Full-speed |
| 1 | 0 | Low-speed |
| 0 | 1 | High-speed |
| 1 | 1 | 保留 / 非預期 |

因此 `PORT_LOW_SPEED = 0` 不能單獨判為 full-speed，需 `PORT_HIGH_SPEED` 一起為 0。

## section_refs 與 verified 邊界

這個 repo 的 evidence 關係包含兩種訊號：

- `section_refs`：作為 evidence metadata 的附件
- `verified`：已完成的 live entry-level promotion

兩者不可混淆。

目前狀態：

- selected pilot entries 帶有 `section_refs`
- `wPortStatus.bit0.PORT_CONNECTION`、`wPortStatus.bit1.PORT_ENABLE`、`wPortStatus.bit2.PORT_SUSPEND`、`wPortStatus.bit3.PORT_OVER_CURRENT`、`wPortStatus.bit4.PORT_RESET`、`wPortStatus.bit8.PORT_POWER`、`wPortStatus.bit9.PORT_LOW_SPEED`、`wPortStatus.bit10.PORT_HIGH_SPEED`、`wPortStatus.bit11.PORT_TEST`、`wPortStatus.bit12.PORT_INDICATOR`、`wPortChange.bit0.C_PORT_CONNECTION`、`wPortChange.bit1.C_PORT_ENABLE`、`wPortChange.bit2.C_PORT_SUSPEND`、`wPortChange.bit3.C_PORT_OVER_CURRENT`、`wPortChange.bit4.C_PORT_RESET`、`wHubStatus.bit0.HUB_LOCAL_POWER`、`wHubStatus.bit1.HUB_OVER_CURRENT`、`wHubChange.bit0.C_HUB_LOCAL_POWER`、`wHubChange.bit1.C_HUB_OVER_CURRENT` 為 live `verified`
- 所有 live verified scope 保持 `bit_name_and_position_only`
- 剩餘 defined status/change entries 無額外 verified 推進（目前為空）
- 仍不代表 USB 2.0 PDF semantic verification 完整

如果未來頁面或模組需要 `section_refs`，請採用 Phase 7A metadata 結構，例如：

```yaml
section_refs:
  - spec: usb20
    section: "11.24.2.7.1"
    anchor_type: section
    evidence_status: review_required
    applies_to: "PORT_CONNECTION summary block"
```

此 metadata 僅為 evidence 附件，不能單獨將頁面或條目推高為 `verified`。

## Governed Linkage

- `tables/port_status_bit_matrix.yaml`：hub/port status-change bit 的主要機器可讀來源
- `specs/hub_class_requests.md`：`GET_STATUS` / `SET_FEATURE` / `CLEAR_FEATURE` 的請求族群對照
- `specs/feature_selectors.md`：`C_PORT_*` selector 的命名邊界
- `specs/escalation_table.md`：如 E-02、E-03、E-09 等 escalation context

## Non-claims

- 本頁不主張所有 port status bit 已完成 PDF-level 完整驗證。
- 不主張速度位元、reset 位元、電源位元與 indicator 行為已完整驗證。
- 不將 19 筆 verified entries 的存在，等同於整頁 verified。
- 不將高位 boundary placeholder 當成已定義 status/change 行為。
- 不將本頁升級為 firmware 實作權威。
