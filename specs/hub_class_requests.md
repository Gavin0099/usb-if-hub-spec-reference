---
title: Hub 類別請求
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Hub 類別請求

> 來源範圍：USB 2.0 Specification Rev 2.0，第 11.24.2 節。
> 本頁只提供結構化語意摘要；欄位與 setup packet 的 section-level 驗證仍待 PDF 核對。

## 請求家族總覽

| bRequest | 數值 | 方向 | 接收者 | 摘要 |
|---|---|---|---|---|
| `GET_STATUS` | `0x00` | Device-to-Host | Hub / Port | 讀取 hub 或 port 的 status 與 change 欄位 |
| `CLEAR_FEATURE` | `0x01` | Host-to-Device | Hub / Port | 清除 feature，或清除 change bit 所代表的變更事件紀錄 |
| `SET_FEATURE` | `0x03` | Host-to-Device | Hub / Port | 設定 hub 或 port 的 feature |
| `GET_DESCRIPTOR` | `0x06` | Device-to-Host | Hub | 讀取 hub class-specific descriptor |
| `SET_DESCRIPTOR` | `0x07` | Host-to-Device | Hub | 寫入 hub class-specific descriptor，支援度待個別實作確認 |
| `CLEAR_TT_BUFFER` | `0x08` | Host-to-Device | TT-capable Hub | 清除 TT buffer 狀態 |
| `RESET_TT` | `0x09` | Host-to-Device | TT-capable Hub | 重設 Transaction Translator |
| `GET_TT_STATE` | `0x0A` | Device-to-Host | TT-capable Hub | 讀取 TT 診斷狀態 |
| `STOP_TT` | `0x0B` | Host-to-Device | TT-capable Hub | 停止 TT split transaction 處理 |

## 怎麼理解 `CLEAR_FEATURE`

`CLEAR_FEATURE` 在 hub class 裡不只是「把某個 feature 關掉」而已，也常用來清除 change bit：

- 對 `wPortChange` / `wHubChange` 這類 change 欄位來說，對應的 `CLEAR_FEATURE(...)` 表示 host 已處理這次變更事件
- 例如 `CLEAR_FEATURE(C_PORT_CONNECTION)` 的意思，不是「關閉連接」，而是「清除連接變化事件的紀錄旗標」
- 所以閱讀 `GET_STATUS` 時，通常要把 change bits 與 `CLEAR_FEATURE` 配對理解

## 常見 setup packet 形態

| 請求 | `bmRequestType` | `wValue` | `wIndex` | `wLength` |
|---|---|---|---|---|
| Hub `GET_STATUS` | `0xA0` | `0x0000` | `0x0000` | `4` |
| Port `GET_STATUS` | `0xA3` | `0x0000` | `port_number` | `4` |
| Hub `SET_FEATURE` / `CLEAR_FEATURE` | `0x20` | `feature_selector` | `0x0000` | `0` |
| Port `SET_FEATURE` / `CLEAR_FEATURE` | `0x23` | `feature_selector` | `port_number` | `0` |
| TT family requests | 多為 `0x23` 或 `0xA3` | `spec_defined` 或 `0x0000` | `spec_defined` | 依請求而定 |

## Feature selector 邊界

- Hub recipient 與 Port recipient 的 selector namespace 必須分開理解。
- Port selector 的標準範圍是 `0-22`，vendor selector 不得與這個範圍重疊。
- `GET_STATUS` 回傳的 bit 定義應搭配 `specs/port_status_bits.md` 一起看。
- `SET_FEATURE` / `CLEAR_FEATURE` 的 selector 詳細值應搭配 `tables/feature_selector_matrix.yaml` 一起看。

## TT 請求限制

- `CLEAR_TT_BUFFER`、`RESET_TT`、`GET_TT_STATE`、`STOP_TT` 只適用於內建 TT 的 HS hub。
- 這些請求的 `wValue`、`wIndex`、`wLength` 仍有 `spec_defined` 項，表示目前尚未完成 section-level PDF 驗證。
- consuming repo 若要依此改變 TT 行為，應先進入 Standard Escalation Mode。
