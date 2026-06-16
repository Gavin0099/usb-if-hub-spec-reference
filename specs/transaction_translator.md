---
title: Transaction Translator
claim_level: inferred
status: review_required
last_reviewed: "2026-06-05"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Transaction Translator

> Source scope: USB 2.0 Specification Rev 2.0, Sections 11.17-11.18.
> 這個頁面是 TT 行為摘要，不是完整 split-transaction 的 correctness 驗證。

## 核心概念

Transaction Translator (TT) 位於 high-speed hub 內，用來協助 host 的高速度 split transaction 與實際對下游 full-speed / low-speed 裝置的傳輸對接。

- 不支援 TT 的 hub 不應聲稱 TT-specific request 支援。
- TT 行為不應出現在僅支援 full-speed 的 hub 上。
- TT 行為應與 descriptor 宣告的 TT type 及 TT think time 設定保持一致。

## TT Type 與 Think Time

| 項目 | 相關欄位 | 摘要 |
|---|---|---|
| Single TT | `wHubCharacteristics` 中的 TT type | 全域共用一個 TT，供所有下游 port 共用 |
| Multiple TT | `wHubCharacteristics` 中的 TT type | 每個 port 或一群 port 可能有獨立 TT 實例 |
| TT Think Time = `00` | `wHubCharacteristics[6:5]` | 8 FS bit times |
| TT Think Time = `01` | `wHubCharacteristics[6:5]` | 16 FS bit times |
| TT Think Time = `10` | `wHubCharacteristics[6:5]` | 24 FS bit times |
| TT Think Time = `11` | `wHubCharacteristics[6:5]` | 32 FS bit times |

## TT Requests

- `CLEAR_TT_BUFFER`
- `RESET_TT`
- `GET_TT_STATE`
- `STOP_TT`

以上 request 僅適用於具備 embedded TT 的 HS hub。

## TT Request Opcode Map

| Request | bRequest | 摘要 |
|---|---:|---|
| `CLEAR_TT_BUFFER` | `0x08` | Clears TT buffer state（僅 TT-capable HS hub）。 |
| `RESET_TT` | `0x09` | Resets the TT（僅 TT-capable HS hub）。 |
| `GET_TT_STATE` | `0x0A` | Reads TT diagnostic state（僅 TT-capable HS hub）。 |
| `STOP_TT` | `0x0B` | Stops TT split-transaction processing（僅 TT-capable HS hub）。 |

以上為 request-level 導向；`wValue`、`wIndex`、`wLength` 的行為限制仍以 matrix 與相關頁面為主。

本 repo 的目前 reviewed surface 為：

- `CLEAR_TT_BUFFER`：`wValue` 持有 TT buffer selector 欄位；`wIndex` 選擇 TT port / context
- `RESET_TT`：`wValue = 0x0000`；`wIndex` 選擇 TT port number
- `GET_TT_STATE`：`wValue = 0x0000`；`wIndex` 選擇 TT port / diagnostic context；`wLength` 為 TT state data 長度
- `STOP_TT`：`wValue = 0x0000`；`wIndex` 選擇 TT port number

這仍不足以構成完整欄位層級 verified encoding，也不表示 TT 行為已完成語義驗證。

## Governed Linkage

- `tables/transaction_translator_matrix.yaml`：管控 TT type / think-time / TT request linkage 的主要來源。
- `tables/hub_descriptor_matrix.yaml`：連結 TT think-time 到 `wHubCharacteristics[6:5]`。
- `tables/class_request_matrix.yaml`：連結 TT request name 到 class request setup surface。
- `specs/escalation_table.md`：`E-06`、`E-07`、`E-10` 釐清 TT 相關 escalate trigger。

TT table 僅為 reviewed reference boundary。未覆蓋 split-transaction timing、TT buffer selector encoding、diagnostic payload semantics，也未驗證 firmware support 的完整性。

## Split Transaction 流程

1. host 發送 Start Split 至 HS hub。
2. hub 的 TT 將請求轉換後送到下游 FS/LS 裝置。
3. host 後續發送 Complete Split。
4. hub / TT 聚合結果並向上回報。

## 使用注意

- 本頁不應覆蓋 consuming repo 對 Single TT / Multiple TT 的既有決策。
- TT think time 與 descriptor 聲明不一致，應視為 escalation trigger。
- 若有行為變更需求，需先經架構層級審核後再套用到實作。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/transaction_translator.md: English counterpart topic (en).
