---
title: USB Transactions
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Transactions

> 來源範圍：USB 2.0 Specification Rev 2.0，§8.5 和 §8.6。  
> 本頁是 USB 2.0 transaction 結構與錯誤處理的 reviewed reference summary。Transaction 是 USB 通訊的最小完整單元：一個 token + 可選資料 + 可選 handshake。

## 頁面目的

本頁回答：

- IN、OUT、SETUP transaction 的結構是什麼。
- Control transfer 三個階段（SETUP + DATA + STATUS）如何運作。
- NAK、STALL、NYET 對 transaction 重試和錯誤恢復意味著什麼。

## Transaction 結構

一個 **transaction** 最多由三個封包組成：

```
[Token packet] → [Data packet] → [Handshake packet]
```

不是所有 transaction 都有三個階段：

| Transaction 類型 | Token | Data | Handshake |
|---|---|---|---|
| SETUP | SETUP | DATA0（固定）| ACK（來自設備）|
| IN | IN | DATA0 或 DATA1（來自設備）| ACK / NAK（來自 host）|
| OUT | OUT | DATA0 或 DATA1（來自 host）| ACK / NAK / STALL（來自設備）|
| SOF | SOF | — | —（無 handshake）|

## SETUP Transaction

僅用於 control transfer 的 SETUP 階段（endpoint 0）：

```
Host → Device:   SETUP token
Host → Device:   DATA0（8-byte setup packet）
Device → Host:   ACK
```

- 設備對有效的 SETUP packet 一律回應 ACK。
- ACK 後，設備處理 setup packet 並準備回應。
- SETUP 階段的 data toggle 固定為 DATA0。

## IN Transaction

Host 從設備 endpoint 請求資料：

```
Host → Device:   IN token
Device → Host:   DATA0 或 DATA1（payload）— 或 NAK / STALL
Host → Device:   ACK（若收到資料）— 或無回應（發生錯誤時）
```

- 設備尚未就緒：設備發 `NAK`；host 在下一個 poll interval 重試。
- Endpoint 停用：設備發 `STALL`；host 必須 `CLEAR_FEATURE(ENDPOINT_HALT)`。
- 成功 ACK 後 data toggle 前進（DATA0→DATA1→DATA0...）。

## OUT Transaction

Host 向設備 endpoint 傳送資料：

```
Host → Device:   OUT token
Host → Device:   DATA0 或 DATA1（payload）
Device → Host:   ACK / NAK / STALL
```

- `ACK`：資料已接受；toggle 前進。
- `NAK`：設備忙碌；host 重試。
- `STALL`：endpoint 停用；需 `CLEAR_FEATURE(ENDPOINT_HALT)`。

## Control Transfer：三階段序列

Control transfer 結合 SETUP + 可選 DATA + STATUS transaction：

### 第一階段：SETUP

```
SETUP token + DATA0（8-byte setup packet）+ ACK
```

傳送請求（bmRequestType、bRequest、wValue、wIndex、wLength）。

### 第二階段：DATA（選用）

若 `wLength > 0`，一個或多個 IN 或 OUT transaction 傳輸資料 payload：

- 方向與 `bmRequestType[7]` 一致。
- Data toggle 從 DATA1 開始交替。
- 若 payload 超過 `bMaxPacketSize0`，需多次 transaction。

### 第三階段：STATUS

確認整個 transfer 完成：

- 方向與 DATA 階段**相反**。
- 攜帶零長度 DATA1 封包。
- 設備發 `ACK`（或仍在處理中時發 `NAK`）。

```
範例：GET_DESCRIPTOR（Device→Host，18 bytes）
  SETUP:   SETUP + DATA0(8B: GET_DESCRIPTOR request) + ACK
  DATA:    IN + DATA1(8B) + ACK → IN + DATA0(8B) + ACK → IN + DATA1(2B) + ACK
  STATUS:  OUT + DATA1(0B) + ACK
```

## Interrupt Transfer Transaction

Hub status change endpoint 使用 interrupt IN transaction：

```
Host → Device（hub）：IN token（以 bInterval 為週期）
Device → Host：DATA0 或 DATA1（status change bitmap）— 或無變化時 NAK
Host → Device：ACK（若收到資料）
```

- 無 port 變化：hub 發 `NAK` → host 在下個 interval 重試。
- 有 port 變化：hub 發 status change bitmap；bit 0=hub，bit N=port N。

## 錯誤處理摘要

| 回應 | 含義 | Host 操作 |
|---|---|---|
| `ACK` | 成功 | 前進 toggle，繼續 |
| `NAK` | 暫時忙碌 | 重試（自動，在 transfer timeout 內）|
| `STALL` | Endpoint 停用 | 發出 `CLEAR_FEATURE(ENDPOINT_HALT)` 恢復 |
| `NYET`（HS）| 尚未就緒（split）| 在下一個 micro-frame 發 CSPLIT |
| 無回應 / CRC 錯誤 | 封包遺失 | 重試（最多 3 次）；超出後回報錯誤 |

## Data Toggle 與重複封包偵測

每個 endpoint 維護一個 toggle bit（DATA0/DATA1）：

- 傳送方在每個成功 ACK 的 transaction 後切換 toggle。
- 接收方在發送 ACK 後切換 toggle。
- 若接收方收到不符預期的 toggle（例如預期 DATA1 卻收到 DATA0）：資料是重傳 → 接收方發 ACK 但丟棄資料（不重複處理）。

這允許在 ACK 遺失但資料實際已傳遞的情況下靜默恢復。

## Governed Linkage

- `specs/usb_packet_types.md`：個別封包類型（PID 值、結構）
- `specs/split_transaction_packets.md`：TT hub 的 SSPLIT / CSPLIT transaction 結構
- `specs/hub_class_requests.md`：hub class request 的 control transfer payload
- `specs/hub_interrupt_endpoint.md`：status change 回報的 interrupt endpoint 細節
- `specs/standard_device_requests.md`：SETUP transaction 中承載的 setup packet

## Non-claims

- 本頁不宣告 transaction 序列已針對實體 hub 驗證。
- 本頁不規定完整的 USB 2.0 host controller 排程演算法。
- 本頁不宣告錯誤恢復時序已 implementation-verified。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/usb_transactions.md: English counterpart topic (en).
