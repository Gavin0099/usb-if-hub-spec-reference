---
title: High-Speed Detection
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# High-Speed Detection

> 來源範圍：USB 2.0 Specification Rev 2.0，§7.1.7.1。  
> 本頁是 USB 2.0 高速（HS）設備偵測機制的 reviewed reference summary，重點在於 port reset 期間的 chirp 握手序列。

## 頁面目的

本頁回答：

- USB 2.0 hub 如何偵測新連接設備是否支援 HS。
- Chirp K/J 序列是什麼，如何運作。
- Hub 針對 HS 與 FS/LS 設備在 reset 後的處理方式。

本頁不回答：

- FS 和 LS 信號狀態定義 —— 請見 `specs/usb_signaling.md`。
- Reset 後的 port state machine 轉換 —— 請見 `specs/port_state_machine.md`。

## HS 偵測概覽

當設備連接到 HS-capable hub 時，hub 與設備在 bus reset 期間協商速度。協商使用 **chirp 握手**——一組特定的短 K/J 脈衝——確認雙方都支援 HS。

若其中一方不支援 HS（或未回應 chirp），設備以 FS 或 LS 速度操作。

## Chirp 握手序列

### 步驟 1：Hub 發出 Reset（SE0）

Hub 在 port 上維持 SE0（D+=0, D−=0）持續 ≥10ms。這是標準 USB bus reset 信號。

### 步驟 2：設備回應 Chirp K

**HS-capable 設備**在偵測到 SE0 reset 的 2.5ms 內，驅動 **Chirp K**（短暫的 K 狀態）約 1–7ms。這向 hub 表示設備支援 HS。

- FS/LS 設備不驅動 Chirp K → Hub 繼續以 FS/LS 模式處理。

### 步驟 3：Hub 偵測 Chirp K 並回應

偵測到設備 Chirp K 的 **HS-capable hub** 以交替的 KJ 脈衝序列回應：

```
Hub 回應：K J K J K J（3 個 KJ 對，各約 100µs）
```

這向設備確認 hub 支援 HS。

### 步驟 4：設備確認 HS 模式

設備偵測到 hub 的 KJ chirp 序列，切換到 HS 模式。設備現在以 HS 設備身份枚舉。

### 步驟 5：HS Bus 閒置

Chirp 交換後，hub 與設備均切換到 HS bus 信號（480 Mbps）。Hub 結束 SE0，正常 HS 通訊開始。

## 結果矩陣

| 設備 HS-capable | Hub HS-capable | 設備 Chirp K | Hub KJ 回應 | 結果 |
|---|---|---|---|---|
| 是 | 是 | ✓（已發送）| ✓（已發送）| **HS 操作** |
| 是 | 否（FS hub）| ✓（已發送）| ✗（未發送）| **FS fallback**（設備未收到回應）|
| 否（FS 設備）| 是 | ✗（未發送）| N/A | **FS 操作** |
| 否（LS 設備）| 是/否 | ✗（未發送）| N/A | **LS 操作** |

Reset sequence 完成後，host 透過 `GET_STATUS(port)` 確認速度，並檢查 `PORT_LOW_SPEED` 和 `PORT_HIGH_SPEED` bits。

## 時序參考

| 事件 | 時序 |
|---|---|
| Hub SE0 持續時間 | ≥10ms |
| SE0 後設備 Chirp K 開始 | ≤2.5ms |
| 設備 Chirp K 持續時間 | 1–7ms |
| Hub KJ 回應（每個 K 或 J）| 約 100µs |
| Hub KJ 對數 | 3 對（6 次轉換）|

## HS vs. FS Hub 行為

| Hub 類型 | `bDeviceProtocol` | Chirp 偵測 | Chirp 回應 |
|---|---|---|---|
| FS hub（無 TT）| `0x00` | 否 | 否 |
| HS hub，single TT | `0x01` | 是 | 是 |
| HS hub，multi TT | `0x02` | 是 | 是 |

只有 HS hub（`bDeviceProtocol=0x01` 或 `0x02`）參與 chirp 偵測。連接到 HS hub 的 FS 設備以 FS 操作（若需要透過 TT）。

## Governed Linkage

- `specs/usb_signaling.md`：J/K/SE0 bus 狀態與 reset 信號
- `specs/port_state_machine.md`：Port reset 時序與 reset 後的速度 bits
- `specs/hub_device_class.md`：指示 hub 速度和 TT 類型的 `bDeviceProtocol` 值
- `specs/transaction_translator.md`：HS hub port 上 FS/LS 設備的 TT 操作

## Non-claims

- 本頁不宣告 chirp 握手序列已針對實體 hub 或設備驗證。
- 本頁不規定 chirp 序列的所有電氣時序容差。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/hs_detection.md: English counterpart topic (en).
