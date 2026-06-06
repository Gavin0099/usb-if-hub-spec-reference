---
title: Split Transaction Packets
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Split Transaction Packets

> 來源範圍：USB 2.0 Specification Rev 2.0，§8.4.2 和 §11.17。  
> 本頁涵蓋 HS hub 嵌入式 Transaction Translator 使用的 SPLIT 封包結構與 SSPLIT/CSPLIT transaction 流程。TT 高階語意請見 `specs/transaction_translator.md`。

## 頁面目的

本頁回答：

- SPLIT 封包在 byte/欄位層級的結構。
- SSPLIT 和 CSPLIT token 如何編碼。
- 完整的 split transaction 時序序列。

## 為何需要 Split Transactions

HS hub 的上行 port 以 480 Mbps 運作，但下行 port 可能是 FS（12 Mbps）或 LS（1.5 Mbps）。Host controller 使用 HS split transaction 與 hub 的 Transaction Translator（TT）通訊；TT 獨立處理 FS/LS 段。

若沒有 split transaction，host 就必須直接計時 FS/LS bus 段，這與 HS frame 排程不相容。

## SPLIT 封包結構

SPLIT 封包位於 split transaction 中 token 之前。PID = `0x78`。

**SPLIT token 欄位**（4 bytes 總計：PID + 3 payload bytes）：

| Bits | 欄位 | 說明 |
|---|---|---|
| `[6:0]` | Hub Address | TT hub 的 7-bit USB 位址 |
| `[7]` | SC | 0 = Start-Split（SSPLIT）；1 = Complete-Split（CSPLIT）|
| `[14:8]` | Port | TT hub 上的 7-bit port 編號 |
| `[15]` | S | 速度指示：0 = FS；1 = LS（isochronous：payload 開始指示）|
| `[16]` | E/U | SSPLIT isochronous end 指示 / CSPLIT 未使用 |
| `[18:17]` | ET | Endpoint type：00=Control，01=Isochronous，10=Bulk，11=Interrupt |
| `[23:19]` | CRC5 | 覆蓋 Hub Addr + SC + Port + S + E/U + ET 的 5-bit CRC |

## SSPLIT Transaction（Start Split）

Host 透過向 TT hub 發送 SSPLIT 來發起 split transaction：

```
HS 段（host → TT hub）：
  SPLIT(SC=0) + token (IN/OUT/SETUP) + [OUT/SETUP 的資料] + [handshake]
```

TT hub 收到 SSPLIT + token 後：
1. 向 host 發 ACK（transaction 已交給 TT）。
2. 排隊並在下行 port 執行完整的 FS/LS transaction。

## CSPLIT Transaction（Complete Split）

Host 透過發送 CSPLIT 從 TT 取回結果：

```
HS 段（host → TT hub）：
  SPLIT(SC=1) + token (IN 或 OUT)
TT hub → host：
  DATA（IN 時）或 ACK/NAK/STALL（OUT 時）— 或 NYET（結果尚未就緒）
```

若 TT 尚未完成下行 FS/LS transaction：hub 回傳 `NYET`，host 在下一個 micro-frame 重試 CSPLIT。

## Split Transaction 流程：Control Transfer 範例

```
Micro-frame 0：Host → Hub：SSPLIT(SETUP) + SETUP token + DATA0(8B) + Hub 回 ACK
              Hub → FS device：SETUP token + DATA0(8B) + FS device 回 ACK

Micro-frame 2+：Host → Hub：CSPLIT(IN) + IN token
               Hub → Host：NYET（仍在執行 FS DATA 階段）

Micro-frame 3+：Host → Hub：CSPLIT(IN) + IN token
               Hub → Host：DATA1(payload)（FS device 已回覆）
               Host → Hub：ACK
```

## SSPLIT/CSPLIT 時序限制

| 階段 | 限制 |
|---|---|
| SSPLIT 發出時機 | 任意 micro-frame |
| CSPLIT 最早發出 | Micro-frame `start + 2`（最少）|
| Hub NYET 回應 | TT 仍在執行下行 segment；host 下一個 micro-frame 重試 |
| Hub ERR 回應 | FS/LS 段上發生錯誤；host 端錯誤恢復 |

## Endpoint Type 與 Split 行為

| ET（Endpoint Type）| SSPLIT 行為 | CSPLIT 行為 |
|---|---|---|
| `00` Control | 完整 SETUP/DATA/STATUS | HOST 為每個結果階段發 CSPLIT |
| `01` Isochronous | S/E bits 指示 payload 段 | 無 CSPLIT（ISO 不重試）|
| `10` Bulk | 標準開始 | CSPLIT 取回 ACK/NAK/STALL |
| `11` Interrupt | 標準開始 | CSPLIT 取回 DATA/NAK/STALL |

Isochronous split transaction 不使用 CSPLIT；若無 CSPLIT，hub 丟棄結果（與 ISO 不重試語意一致）。

## Governed Linkage

- `specs/transaction_translator.md`：TT 高階語意、think-time、TT request families
- `specs/usb_packet_types.md`：SPLIT PID 值與封包框架
- `specs/usb_transactions.md`：transaction 層級控制流程（SSPLIT/CSPLIT 建立在 IN/OUT/SETUP 之上）
- `specs/hub_class_requests.md`：`CLEAR_TT_BUFFER`、`RESET_TT`、`GET_TT_STATE`、`STOP_TT`

## Non-claims

- 本頁不宣告 split transaction 欄位編碼已針對 USB 2.0 PDF 驗證。
- 本頁不宣告 isochronous split transaction 行為已 correctness-verified。
- 本頁不定義完整的 TT 排程模型。
- 本頁不覆蓋 consuming repo 已確認的 project facts。
