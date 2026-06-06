---
title: Hub Power Management
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Power Management

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.11 / §11.4 / §11.7。  
> 本頁是 hub power management 的 reviewed reference summary；不是電源時序或 firmware 行為驗證。

## 頁面目的

本頁回答：

- Hub 的 power switching 模式（ganged vs per-port）如何影響 `SET_FEATURE(PORT_POWER)` 的行為。
- `bPwrOn2PwrGood` 代表的延遲語意。
- Hub suspend 與 resume 的概念邊界。
- Remote wakeup 的機制概述。

本頁不回答：

- 特定 hub 硬體的電源規格是否已驗證。
- Hub firmware 的電源切換時序是否正確。
- 完整的電源管理狀態機。

## Power Switching 模式

`wHubCharacteristics bits[1:0]` 定義 hub 的電源切換模式（詳見 `specs/hub_descriptor.md`）：

| 模式 | bits[1:0] | 說明 |
|---|---:|---|
| Ganged power switching | `0b00` | 所有 port 同時上電/斷電；`SET_FEATURE(PORT_POWER)` 對單一 port 的效果取決於 hub 實作 |
| Individual (per-port) power switching | `0b01` | 每個 port 可獨立控制電源；`SET_FEATURE(PORT_POWER)` 和 `CLEAR_FEATURE(PORT_POWER)` 各自生效 |
| No power switching | `0b10` / `0b11` | 電源無法控制（Reserved；部分 hub 以此表示 always-on） |

### Ganged vs Per-port 的實作差異

- **Ganged hub**：`SET_FEATURE(PORT_POWER)` 可能同時對所有 port 上電，即使只指定一個 port number。Host 應在枚舉時通過 `wHubCharacteristics` 確認模式。
- **Per-port hub**：`SET_FEATURE(PORT_POWER, portN)` 僅對 port N 上電；需逐 port 發送請求完成初始化。

## bPwrOn2PwrGood 延遲

Hub descriptor 的 `bPwrOn2PwrGood` 欄位（offset 5）定義從 port 上電到 power-good 的等待時間：

- 單位：2 ms（值 × 2 ms = 實際等待時間）
- Host 必須在 power-good 延遲結束後才能繼續枚舉（如發送 `SET_FEATURE(PORT_RESET)`）。
- 例：bPwrOn2PwrGood = 50 → 等待 100 ms。

本頁不驗證任何 hub 的 bPwrOn2PwrGood 值是否正確，也不宣告延遲時序是保守還是精確的。

## Over-current Protection

`wHubCharacteristics bits[4:3]` 定義 over-current 保護模式：

| 模式 | bits[4:3] | 說明 |
|---|---:|---|
| Global over-current | `0b00` | 整個 hub 共用過電流保護；任一 port 觸發時影響所有 port |
| Per-port over-current | `0b01` | 各 port 獨立偵測過電流；`HUB_OVER_CURRENT` bit 對應 hub 整體，個別 port 由 `PORT_OVER_CURRENT` 反映 |
| No over-current reporting | `0b10` | Hub 不報告過電流；host 不能依賴 `PORT_OVER_CURRENT` 或 `HUB_OVER_CURRENT` |

Hub 偵測到 over-current 時，應在 `wPortStatus.PORT_OVER_CURRENT`（port 層級）或 `wHubStatus.HUB_OVER_CURRENT`（hub 整體）中設置相應 bit，並透過 interrupt endpoint 通知 host。

## Hub Suspend 與 Resume

### Suspend 觸發

Hub port 可透過以下方式進入 suspend 狀態：

- Host 發送 `SET_FEATURE(PORT_SUSPEND)` → port 進入 Suspended state（`wPortStatus.PORT_SUSPEND = 1`）
- 下游設備在 3 ms 無活動後自動進入 suspend（由 hub 偵測）

### Resume 觸發

Hub port 從 Suspended 恢復到 Enabled 有兩種路徑：

1. **Host-initiated resume**：Host 發送 `CLEAR_FEATURE(PORT_SUSPEND)` → hub 驅動 resume signaling（20 ms K-state），然後 port 恢復 Enabled。
2. **Device-initiated remote wakeup**：下游設備發出 resume signaling → hub 向上游傳遞 wakeup 信號 → host 偵測並處理。

### 全 Hub Suspend

USB 2.0 spec §11.7 說明 hub 本身也可能進入 suspend（透過 USB suspend signaling）。此時所有 port 都應保持其現有狀態（通常為 Suspended），並在 hub resume 後恢復。

## Remote Wakeup

- Hub 若支援 remote wakeup，在 host 允許的情況下可在 suspend 期間被下游設備喚醒。
- Hub 以 `CLEAR_FEATURE(C_PORT_SUSPEND)` 的 change 事件通知 host port resume。
- Remote wakeup 功能是否啟用由 `SET_FEATURE(DEVICE_REMOTE_WAKEUP)` 控制（標準 USB 請求，不是 hub class 請求）。

## 安全解讀邊界

- 本頁描述電源管理的概念框架，不提供具體時序保證或電氣規格。
- `bPwrOn2PwrGood` 與 over-current 行為依 hub 硬體設計不同而異；請參閱硬體資料表。
- 若 consuming repo 的 hub 電源行為與預期不符，應進入 Standard Escalation Mode（E-07 或 E-08）。

## Governed Linkage

- `specs/hub_descriptor.md`：`wHubCharacteristics` 位元欄位（power switching 和 over-current 模式）
- `specs/port_state_machine.md`：Suspended 狀態與 Powered-off 狀態的詳細 transition
- `specs/port_status_bits.md`：`PORT_SUSPEND`、`PORT_OVER_CURRENT`、`HUB_OVER_CURRENT` bits
- `specs/hub_class_requests.md`：`SET_FEATURE(PORT_POWER)`、`SET_FEATURE(PORT_SUSPEND)` 等請求

## Non-claims

- 本頁不宣告任何 hub 的電源管理實作已驗證。
- 本頁不提供電源時序保證或電氣規格。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
