---
title: USB Test Modes
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB Test Modes

> 來源範圍：USB 2.0 Specification Rev 2.0，§7.1.20 和 §9.4.9。  
> 本頁是 USB 2.0 高速 test modes 的 reviewed reference summary。Test modes 用於 HS 電氣合規測試，透過標準 `SET_FEATURE(TEST_MODE)` 請求進入。

## 頁面目的

本頁回答：

- USB 2.0 有哪些 test modes，各自的用途是什麼。
- Host 如何在 hub 或下行設備上進入 test mode。
- 如何退出 test mode。

## 概覽

USB 2.0 定義了五種 **Test Mode** selectors 用於 HS 電氣合規測試。Test modes 讓設備或 hub 在匯流排上發送特定的固定信號 pattern，配合 USB 2.0 合規測試設備使用，不應在正常操作中進入。

Test modes 僅適用於 **HS-capable 設備和 hub**（`bDeviceProtocol = 0x01` 或 `0x02`）。

## Test Mode Feature Selectors

透過 `SET_FEATURE(TEST_MODE)`，`wIndex[15:8]` = test mode 編號來進入：

| Test Mode | `wIndex[15:8]` | 信號 Pattern | 用途 |
|---|---|---|---|
| `TEST_J` | `0x01` | 持續 J 狀態 | 測試差分 `1` 信號位準 |
| `TEST_K` | `0x02` | 持續 K 狀態 | 測試差分 `0` 信號位準 |
| `TEST_SE0_NAK` | `0x03` | SE0（對 IN token 回 NAK）| 測試 single-ended zero 和靜態位準 |
| `TEST_PACKET` | `0x04` | 特定測試資料封包（重複發送）| 測試全資料 pattern 下的信號品質 |
| `TEST_FORCE_ENABLE` | `0x05` | 正常 HS 信號啟用 | 強制啟用 HS 上行 port |

`wIndex[7:0]` = `0x00`（保留）。

## `SET_FEATURE(TEST_MODE)` 請求

```
bmRequestType: 0x00  (Host→Device, Standard, Device recipient)
bRequest:      0x03  (SET_FEATURE)
wValue:        0x0002  (TEST_MODE feature selector)
wIndex:        [test_mode_number << 8]  (test mode 在高 byte)
wLength:       0
```

設備必須在 `SET_FEATURE` 請求的 status 階段完成後進入 test mode。

## Test Mode 進入規則

- 只有處於 `Address` 或 `Configured` 狀態的設備才能收到 `SET_FEATURE(TEST_MODE)`。
- 進入後，設備發送指定 pattern，**不再回應任何 USB 通訊**。
- Host 不得在 `SET_FEATURE` status 階段後發出任何附加請求。

## 退出 Test Mode

**Test modes 只能透過以下方式退出：**
- 硬體電源循環（移除並重新施加 VBUS），或
- 硬體 reset（實體 reset 按鈕，如有）。

軟體 reset（`SET_FEATURE(PORT_RESET)`）或 USB bus reset **不足以**退出 test mode。

## Hub Port Test Mode（`wIndex[7:0]` = port 編號）

Hub 上行 port 測試：`wIndex[7:0] = 0x00`。  
Hub 下行 port 測試：`wIndex[7:0]` = port 編號（1-based）。

這允許 host 獨立對特定下行 port 設置 test mode。

## `TEST_PACKET` 資料

`TEST_PACKET` mode 重複發送一個特定的 53-byte 封包，定義於 USB 2.0 §7.1.20，包含各種資料 pattern 組合以對信號完整性進行壓力測試。

## Hub 在 Test Mode 中的角色

- 對 hub 執行 `TEST_FORCE_ENABLE` 使 hub 無論正常枚舉狀態如何都啟用上行 HS port。
- 對下行 port 設置 test mode 時，hub 僅對該 port 傳播測試信號。
- Hub 的 TT 不參與下行 port test modes。

## Governed Linkage

- `specs/standard_device_requests.md`：`SET_FEATURE` 標準請求編碼
- `specs/hs_detection.md`：識別 HS-capable hub 的 `bDeviceProtocol`
- `specs/usb_signaling.md`：test mode 信號 pattern 引用的 J/K/SE0 bus 狀態
- `specs/hub_device_class.md`：識別 HS hub 的 `bDeviceProtocol` 值

## Non-claims

- 本頁不宣告 test mode 信號位準或 pattern 已針對測試設備驗證。
- 本頁不規定 USB 2.0 合規測試程序。
- 本頁不宣告 53-byte TEST_PACKET 內容已在此完整重現。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/usb_test_modes.md: English counterpart topic (en).
