---
title: USB Packet Types
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Packet Types

> 來源範圍：USB 2.0 Specification Rev 2.0，§8.3。  
> 本頁是 USB 2.0 封包類型、PID 編碼與封包結構的 reviewed reference summary。理解封包類型是理解 transaction、錯誤處理與 split transaction 的前提。

## 頁面目的

本頁回答：

- USB 2.0 有哪些封包類型，如何識別。
- 每種封包類型包含哪些欄位。
- 哪些封包與 hub 和 hub-port 操作相關。

## PID（Packet Identifier）

每個 USB 封包都以 **PID byte** 開頭，用於識別封包類型：

- Bits `[3:0]`：PID 類型代碼。
- Bits `[7:4]`：bits `[3:0]` 的一補數（check 欄位——確保至少 4 個信號轉換）。

若接收到的 check bits 不匹配，則靜默丟棄該封包。

## Token Packets

Token packets 發起一個 transaction，識別目標設備與 endpoint。

**結構**：`PID`（1B）+ `ADDR[6:0] + ENDP[3:0]`（2B）+ `CRC5`（在 2B 中）

| 封包 | PID | 發起者 | 用途 |
|---|---|---|---|
| `OUT` | `0xE1` | Host | Host 將向設備 endpoint 傳送資料 |
| `IN` | `0x69` | Host | Host 向設備 endpoint 請求資料 |
| `SOF` | `0xA5` | Host | 幀開始標記；每 1ms（FS）或 125µs（HS）發送一次 |
| `SETUP` | `0x2D` | Host | 發起 control transfer SETUP 階段（僅限 EP0）|

**SOF 封包** 攜帶 11-bit `Frame Number` 欄位而非 `ADDR+ENDP`，加上 `CRC5`。

Token packets 由 host 發出；設備永遠不發送 token packets。

## Data Packets

Data packets 攜帶 payload bytes，緊跟在 token packet 之後。

**結構**：`PID`（1B）+ `DATA[0..N]`（0 到 1024B）+ `CRC16`（2B）

| 封包 | PID | 速度 | 說明 |
|---|---|---|---|
| `DATA0` | `0xC3` | FS / LS / HS | 與 DATA1 交替用於錯誤偵測 |
| `DATA1` | `0x4B` | FS / LS / HS | 與 DATA0 交替 |
| `DATA2` | `0x87` | 僅 HS | 用於高頻寬 isochronous transaction |
| `MDATA` | `0x0F` | 僅 HS | 用於 split transaction 和高頻寬 ISO |

**Data toggle**（DATA0↔DATA1）：傳送方和接收方維持相同的 toggle bit。不匹配表示重傳或遺失 ACK；接收方丟棄重複資料。

## Handshake Packets

Handshake packets 確認或拒絕資料 transaction，**僅 1 byte**（只有 PID）。

| 封包 | PID | 發送者 | 含義 |
|---|---|---|---|
| `ACK` | `0xD2` | 接收方 | 資料已接受；toggle 前進 |
| `NAK` | `0x5A` | 設備 | 忙碌——無法接受/傳送資料；host 應重試 |
| `STALL` | `0x1E` | 設備 | Endpoint 已停用；需 `CLEAR_FEATURE(ENDPOINT_HALT)` 恢復 |
| `NYET` | `0x96` | 設備 | 僅限 HS：尚未就緒（用於 split transaction）|
| `ERR` | `0x3C` | Hub（TT）| 僅限 HS：FS/LS 段上的 split transaction 錯誤 |

`NAK` 是**暫時**狀態（設備忙碌）；host 自動重試。  
`STALL` 是**持久**停用狀態；需要 host 顯式操作才能清除。

## 特殊封包

| 封包 | PID | 說明 |
|---|---|---|
| `PRE`（Preamble）| `0x3C` | FS hub 在 LS 下行 token 前發出 LS preamble |
| `PING` | `0xB4` | 僅限 HS：host 在傳送 OUT 資料前詢問設備是否就緒 |
| `SPLIT` | `0x78` | 僅限 HS：引入 split transaction（SSPLIT 或 CSPLIT）|
| `EXT` | `0xF0` | 擴展 token（保留供未來使用）|

注意：`PRE` 和 `ERR` 共用 PID `0x3C`，解讀依情境而定（PRE 出現在 LS token 前的獨立封包；ERR 出現為 TT hub 的 handshake 回應）。

## 封包類型與 Hub 操作

| Hub 活動 | 涉及的封包 |
|---|---|
| Host 枚舉 hub | SETUP token + DATA0（setup packet）+ ACK → hub 回應 ACK/NAK/STALL |
| Hub 回報狀態變化 | Host 向 interrupt endpoint 發 IN token；hub 回應 DATA0/DATA1 bitmap 或 NAK |
| Host 發出 hub class request | SETUP + DATA0（8B setup）+ ACK；可選 IN 資料階段；STATUS 階段 |
| HS hub 轉發 FS/LS transaction | SPLIT + SSPLIT token → hub 執行下行 → host 發 CSPLIT 取得結果 |
| Hub 停用 endpoint | Hub 發 STALL；host 必須發 `CLEAR_FEATURE(ENDPOINT_HALT)` 恢復 |

## Governed Linkage

- `specs/usb_transactions.md`：封包如何組合成 SETUP、IN、OUT transaction
- `specs/split_transaction_packets.md`：SPLIT 封包結構與 SSPLIT/CSPLIT 欄位
- `specs/usb_signaling.md`：承載這些封包的匯流排信號編碼（NRZI、bit stuffing）
- `specs/standard_device_requests.md`：DATA0 封包中承載的 control transfer 內容
- `specs/transaction_translator.md`：TT hub 如何將 HS split transaction 轉換為 FS/LS

## Non-claims

- 本頁不宣告 PID 值或封包結構已針對 USB 2.0 PDF 驗證。
- 本頁不宣告 CRC 計算演算法已 correctness-verified。
- 本頁不建立完整的 USB protocol layer 實作規格。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/usb_packet_types.md: English counterpart topic (en).
