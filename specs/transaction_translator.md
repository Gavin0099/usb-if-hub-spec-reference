---
title: Transaction Translator
claim_level: inferred
status: review_required
last_reviewed: "2026-06-03"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Transaction Translator

> Source scope: USB 2.0 Specification Rev 2.0, Sections 11.17-11.18.  
> 本頁是 TT behavior summary，不宣告完整 split-transaction verification。

## Core Concept

Transaction Translator（TT）存在於 high-speed hub 內，用來銜接 host 發出的 high-speed split transactions，並把實際流量轉送到 downstream 的 full-speed 或 low-speed devices。

- 沒有 TT 的 hub，不應宣告支援 TT-specific requests。
- Full-speed-only hub 不應出現 TT behavior。
- TT behavior 會綁定 descriptor 中宣告的 TT type 與 TT think time 設定。

## TT Type and Think Time

| Item | Related Field | Summary |
|---|---|---|
| Single TT | `wHubCharacteristics` 中的 TT type | 所有 downstream ports 共用一個 TT |
| Multiple TT | `wHubCharacteristics` 中的 TT type | 每個 port 或每組 ports 有獨立 TT instance |
| TT Think Time = `00` | `wHubCharacteristics[6:5]` | 8 FS bit times |
| TT Think Time = `01` | `wHubCharacteristics[6:5]` | 16 FS bit times |
| TT Think Time = `10` | `wHubCharacteristics[6:5]` | 24 FS bit times |
| TT Think Time = `11` | `wHubCharacteristics[6:5]` | 32 FS bit times |

## TT Requests

- `CLEAR_TT_BUFFER`
- `RESET_TT`
- `GET_TT_STATE`
- `STOP_TT`

這些 requests 只適用於具 embedded TT 的 HS hubs。

## TT Request Opcode Map

| Request | bRequest | Summary |
|---|---:|---|
| `CLEAR_TT_BUFFER` | `0x08` | 清除 TT buffer state（僅適用於 TT-capable HS hub）。 |
| `RESET_TT` | `0x09` | 重置 TT（僅適用於 TT-capable HS hub）。 |
| `GET_TT_STATE` | `0x0A` | 讀取 TT diagnostic state（僅適用於 TT-capable HS hub）。 |
| `STOP_TT` | `0x0B` | 停止 TT split-transaction processing（僅適用於 TT-capable HS hub）。 |

上表只提供 request-level orientation；`wValue`、`wIndex` 與 `wLength` 的 behavioral limits 仍以 matrix 與相關頁面為準。

本 repo 目前的 reviewed request surface 為：

- `CLEAR_TT_BUFFER`：`wValue` 承載 TT buffer selector fields；`wIndex` 選擇 TT port / context
- `RESET_TT`：`wValue = 0x0000`；`wIndex` 選擇 TT port number
- `GET_TT_STATE`：`wValue = 0x0000`；`wIndex` 選擇 TT port / diagnostic context；`wLength` 表示 TT state data length
- `STOP_TT`：`wValue = 0x0000`；`wIndex` 選擇 TT port number

這仍不足以構成完整的 field-level verified encoding，也不代表 TT behavior 已完成 semantic verification。

## Governed Linkage

- `tables/transaction_translator_matrix.yaml`：governed 的 TT type、think-time 與 TT request-linkage surface
- `tables/hub_descriptor_matrix.yaml`：將 TT think-time 回連到 `wHubCharacteristics[6:5]`
- `tables/class_request_matrix.yaml`：將 TT request names 回連到 class request setup surfaces
- `specs/escalation_table.md`：`E-06`、`E-07` 與 `E-10` 定義 TT 相關 escalation triggers

TT table 只是 reviewed reference boundary。它不驗證 split-transaction timing、TT buffer selector encoding、diagnostic payload semantics，或 firmware support。

## Split Transaction Flow

1. Host 對 HS hub 發出 Start Split。
2. Hub 內的 TT 將 request 轉譯給 downstream 的 FS/LS device。
3. Host 之後再發出 Complete Split。
4. Hub / TT 彙整結果後回傳上游。

## Usage Notes

- 本頁不可覆蓋 consuming repo 對 Single TT / Multiple TT 的已確認 project decision。
- 若 TT think time 與 descriptor 宣告設定不一致，應視為 escalation trigger。
- 若本頁內容會導致 firmware behavior 改變，應先進行 architecture review。
