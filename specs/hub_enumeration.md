---
title: Hub Enumeration Sequence
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub Enumeration Sequence

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.9 和 §11.24。  
> 本頁是 USB 2.0 hub enumeration sequence 的 reviewed reference summary；不是 firmware 實作指南，也不是 section-level USB 2.0 合規驗證紀錄。

## 頁面目的

本頁回答：

- Host 枚舉 USB 2.0 hub 時發出哪些 USB 請求。
- `GET_STATUS` 回應資料的格式（4-byte 結構）。
- Port reset 完成後，host 如何判斷設備速度。

本頁不回答：

- 每個枚舉步驟的完整時序保證。
- 枚舉失敗時的錯誤恢復流程。
- HS 或 FS 下游設備的完整匯流排時序需求。

## Hub Enumeration 概覽

當 USB 2.0 hub 連接到 host 時，host 先將 hub 當成一般 USB 設備進行枚舉，再執行 hub 專用初始化以啟動各個 port。

### 第一階段：標準 USB 設備枚舉

1. Hub 出現在預設位址 0（bus reset 狀態）。
2. Host 對位址 0 發出 `GET_DESCRIPTOR (device)`，識別 `bDeviceClass=0x09`（Hub class）。
3. Host 指定 bus 位址：`SET_ADDRESS(n)`。
4. Host 讀取 configuration descriptor：`GET_DESCRIPTOR (configuration)`。
5. Host 設定啟用的 configuration：`SET_CONFIGURATION(1)`（hub 通常只有一個 configuration）。

`SET_CONFIGURATION` 完成後，hub 已完成尋址，status change endpoint 也開始運作。

### 第二階段：Hub 專用初始化

標準設備枚舉完成後，host 讀取 hub class descriptor 並為各 port 上電：

1. Host 發出 `GET_DESCRIPTOR`（`wValue = 0x2900`，class descriptor type 0x29，index 0），讀取 hub class descriptor。
2. Hub 回傳 hub descriptor：`bNbrPorts`、`wHubCharacteristics`、`bPwrOn2PwrGood`、`DeviceRemovable`。
3. Host 對 port 1 到 `bNbrPorts` 各發一次 `SET_FEATURE(PORT_POWER)`。
4. Host 在最後一次 `SET_FEATURE(PORT_POWER)` 後等待至少 `bPwrOn2PwrGood × 2ms`。
5. Host 開始監聽 status change endpoint（interrupt IN endpoint）。

> `bPwrOn2PwrGood × 2ms` 是上電穩定等待時間。在此期間結束前，host 不得對 port 發出 `SET_FEATURE(PORT_RESET)`。

### 第三階段：Port 監聽與設備連接

Port 上電後，host 監聽 status change endpoint 並處理變化事件：

1. Hub 在有變化時，於 interrupt endpoint 回傳非零的 status change bitmap。
2. Bit 0 = hub status change；bit N = port N status change。
3. Host 對發生變化的 port N 發出 `GET_STATUS(port N)`，讀取 `wPortStatus` 與 `wPortChange`。
4. 若 `C_PORT_CONNECTION=1`：連接狀態已變化。Host 發出 `CLEAR_FEATURE(C_PORT_CONNECTION)` 清除記錄。
5. 若 `PORT_CONNECTION=1`：設備已連接。Host 發出 `SET_FEATURE(PORT_RESET)`。
6. Reset 完成後，hub 在 `wPortChange` 中設 `C_PORT_RESET=1`。
7. Host 再次讀 `GET_STATUS(port N)`，並發出 `CLEAR_FEATURE(C_PORT_RESET)` 清除。
8. Host 確認 `PORT_LOW_SPEED` 與 `PORT_HIGH_SPEED` 以判斷設備速度。
9. Host 對連接的設備進行標準 USB 設備枚舉。

## `GET_STATUS` 回應格式

`GET_STATUS` 一律回傳 4 個 bytes。hub-recipient 與 port-recipient 格式相同：

| Bytes | 欄位 | Hub recipient | Port recipient |
|---|---|---|---|
| `[1:0]` | `wStatus` | `wHubStatus` | `wPortStatus` |
| `[3:2]` | `wChange` | `wHubChange` | `wPortChange` |

- **`wStatus`**（bytes 0–1）：目前硬體狀態——連接、enable、suspend、過電流、reset、電源、速度 bits。
- **`wChange`**（bytes 2–3）：累積的事件記錄——每個 bit 在對應的 status bit 發生轉換時置 1，並持續設 1 直到 host 以 `CLEAR_FEATURE` 清除。

`wPortStatus`、`wPortChange`、`wHubStatus`、`wHubChange` 的 bit 定義，請見 `specs/port_status_bits.md`。

## Port Reset 後的速度判斷

`SET_FEATURE(PORT_RESET)` 發出後，reset 完成（`C_PORT_RESET=1`），host 讀取 `GET_STATUS(port)` 並確認 `wPortStatus` 中的速度 bits：

| `PORT_LOW_SPEED`（bit 9）| `PORT_HIGH_SPEED`（bit 10）| 設備速度 |
|---|---|---|
| `0` | `0` | Full-speed (FS) |
| `1` | `0` | Low-speed (LS) |
| `0` | `1` | High-speed (HS) |
| `1` | `1` | 無效組合 |

- 速度 bits 只在 port reset 完成且 port 處於 Enabled 狀態後才有效。
- 非 HS-capable 的 hub（`bDeviceProtocol=0x00`）永遠不會設 `PORT_HIGH_SPEED`。
- 速度判斷是透過 `GET_STATUS` 讀取；沒有速度選擇指令。

## 時序參考

| 限制條件 | 數值 | 來源 |
|---|---|---|
| Port 上電穩定等待 | `bPwrOn2PwrGood × 2ms` | §11.11，hub descriptor |
| PORT_RESET 最短持續時間 | 10 ms | §11.5.1.5 |
| Port reset 恢復時間（debounce）| 10 ms | §7.1.7.3 |

> 10 ms 最短 reset 持續時間是 hub 的要求；hub 維持 USB reset 信號並在完成後設 `C_PORT_RESET`。Host 不直接計時 reset 持續時間。

## Governed Linkage

- `specs/hub_descriptor.md`：hub class descriptor 欄位（`bNbrPorts`、`bPwrOn2PwrGood`、`DeviceRemovable`）
- `specs/hub_class_requests.md`：`GET_DESCRIPTOR`、`GET_STATUS`、`SET_FEATURE`、`CLEAR_FEATURE` request family
- `specs/port_status_bits.md`：`wPortStatus`、`wPortChange`、速度 bits、change-bit 語意
- `specs/port_state_machine.md`：枚舉過程中的 port state transition
- `specs/hub_power_management.md`：上電時序與 `bPwrOn2PwrGood` 語意
- `specs/hub_configuration.md`：hub class 的 device 與 configuration descriptor 結構
- `specs/hub_compound_device.md`：`DeviceRemovable` bitmap 與不可移除 port 的處理

## Non-claims

- 本頁不宣告 hub enumeration sequence 已針對實體 hub 逐步驗證。
- 本頁不建立任何枚舉步驟的 firmware 時序正確性。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
