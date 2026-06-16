---
title: USB Signaling and Bus States
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Signaling and Bus States

> 來源範圍：USB 2.0 Specification Rev 2.0，§7.1。  
> 本頁是 USB 2.0 電氣 bus 狀態、資料編碼與 hub 操作相關信號事件的 reviewed reference summary。

## 頁面目的

本頁回答：

- USB 2.0 bus 信號狀態（J、K、SE0、SE1）是什麼。
- USB 資料如何編碼（NRZI + bit stuffing）。
- 哪些 bus 事件對應到 reset、suspend 和 resume。

本頁不回答：

- HS 偵測的 chirp sequence —— 請見 `specs/hs_detection.md`。
- 電氣規格（電壓位準、阻抗、ESD）—— 不在本 repo 範圍內。

## USB D+ 與 D− 信號對

USB 使用差分信號對（D+ 和 D−）：

| Bus 狀態 | D+ | D− | FS/HS 含義 | LS 含義 |
|---|---|---|---|---|
| **J** | High | Low | 閒置（無 activity）| 活躍（差分 1）|
| **K** | Low | High | 活躍（差分 1 / 封包開始 / resume）| 閒置 |
| **SE0** | Low | Low | Reset / End-of-Packet (EOP) | Reset / EOP |
| **SE1** | High | High | 非法（正常操作中不使用）| 非法 |

> LS（低速）設備的 J 和 K 與 FS/HS 相反。

## NRZI 編碼

USB 2.0 使用 **NRZI（Non-Return-to-Zero Inverted）** 編碼：

| 資料 bit | 對信號的影響 |
|---|---|
| `0` | 信號**轉換**（J→K 或 K→J）|
| `1` | 信號**保持**（不轉換）|

NRZI 確保接收器可以從信號轉換中恢復時脈。

## Bit Stuffing

連續 **6 個 `1` bits** 後，傳送方插入一個 `0` bit 強制信號轉換（保持時脈同步）。接收方移除這些插入的零 bit。

影響：由於 stuffed zero bits，bus 上的原始 bitstream 可能比邏輯資料更長。

## 封包框架

每個 USB 封包以 SYNC pattern 開始，以 EOP（End-of-Packet）結束：

- **SYNC**：`00000001`（7 個零 + 1 個一），建立 bit-clock 對齊。
- **EOP**：SE0 持續 2 個 bit time，接著 J 持續 1 個 bit time。

## Bus 事件與信號

### USB Reset

- 信號方式：SE0（D+=0, D−=0）持續 ≥10ms。
- 發出者：Host（root hub）或 hub（透過 `SET_FEATURE(PORT_RESET)` 的 port reset）。
- 設備回應：設備 reset 到 Default 狀態（位址 0），所有 configuration 丟失。

### Suspend

- 信號方式：J 狀態（閒置）持續 >3ms。
- 效果：設備進入 Suspended 狀態；設備可降低功耗。
- 注意：Hub 將 suspend 向下傳播到 downstream ports，除非另行設定。

### Resume

- 信號方式：Hub/host 驅動 K 狀態持續 20ms（±1ms）。
- 效果：Downstream 設備返回正常操作。
- Remote wakeup：被 suspend 的 downstream 設備可驅動 K 狀態 1–15ms 來發起 resume。

### SOF（Start of Frame）

- 由 host 每 1ms（FS）或 125µs（HS micro-frame）發送一次。
- 在正常操作期間防止設備進入 suspend。
- Hub 為 downstream FS/LS 段重新產生 SOF。

## FS vs. HS Bus 信號

| 面向 | Full-Speed (FS) | High-Speed (HS) |
|---|---|---|
| Bit rate | 12 Mbps | 480 Mbps |
| 閒置狀態 | J（D+=High, D−=Low）| HS idle（雙端終端主動）|
| Reset 偵測 | SE0 ≥10ms | SE0 ≥10ms + chirp sequence |
| SOF 間隔 | 1ms | 125µs micro-frame |

HS 設備和 hub 在 reset 期間透過 chirp sequence 協商速度。請見 `specs/hs_detection.md`。

## Governed Linkage

- `specs/hs_detection.md`：port reset 期間的 HS chirp 協商 sequence
- `specs/port_state_machine.md`：Port reset 時序（最短 10ms SE0 持續）
- `specs/hub_power_management.md`：hub 角度的 suspend/resume
- `specs/hub_enumeration.md`：Port 枚舉期間的 reset 信號

## Non-claims

- 本頁不宣告 USB 電氣規格（電壓閾值、阻抗）已驗證。
- 本頁不宣告 NRZI 或 bit-stuffing 實作已驗證。
- 本頁不定義完整的 USB 2.0 protocol layer 行為。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/usb_signaling.md: English counterpart topic (en).
