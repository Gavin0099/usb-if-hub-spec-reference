---
title: Port Indicators and Test Mode
claim_level: inferred
status: review_required
last_reviewed: "2026-06-06"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# Port Indicators and Test Mode

> 來源範圍：USB 2.0 Specification Rev 2.0，§11.5.3 和 §11.24.2.7。  
> 本頁涵蓋選用的 USB 2.0 hub port 指示燈（LED）控制功能與 PORT_TEST feature selector 行為。

## 頁面目的

本頁回答：

- `PORT_INDICATOR` feature 控制如何運作，定義了哪些 LED 狀態。
- `PORT_TEST` 的作用，及其與電氣 test modes 的關係。
- `wHubCharacteristics bit 7` 如何指示指示燈支援。

## Port 指示燈

USB 2.0 hub 可選配每 port LED，顏色可由 host 控制。這是選用硬體；支援與否由 `wHubCharacteristics bit 7` 指示。

| `wHubCharacteristics bit 7` | 含義 |
|---|---|
| `0` | Port 指示燈**不支援** |
| `1` | Port 指示燈支援；host 可使用 `SET_FEATURE(PORT_INDICATOR)` |

### `SET_FEATURE(PORT_INDICATOR)` 編碼

```
bmRequestType: 0x23  (Host→Device, Class, Other recipient)
bRequest:      0x03  (SET_FEATURE)
wValue:        port_indicator_selector（見下表）
wIndex:        port_number（1-based）
wLength:       0
```

Feature selector 值編碼所需的 LED 狀態：

| Selector 值 | LED 狀態 | 含義 |
|---|---|---|
| `0` | Automatic | Hub 控制指示燈（預設行為）|
| `1` | Amber | Host 強制顯示琥珀色（例如：需要注意）|
| `2` | Green | Host 強制顯示綠色（例如：設備活躍）|
| `3` | Off | Host 關閉指示燈 |

Hub 上電時，所有指示燈預設為 **Automatic** 模式。在 automatic 模式下，hub 套用自己的邏輯（通常是連接且 enabled 時綠色，錯誤狀態時琥珀色）。

### 指示燈狀態 vs. Port 狀態（Automatic 模式）

Automatic 模式下，hub 通常顯示：

| Port 狀態 | 典型自動顏色 |
|---|---|
| Powered-off | 關閉 |
| Disconnected（已上電）| 關閉或暗 |
| Disabled | 琥珀色 |
| Enabled | 綠色 |
| Suspended | 琥珀色 |
| Port Error | 琥珀色 |

此對應是 hub 實作定義的；規格未強制要求特定的自動顏色行為。

## PORT_TEST Feature

`PORT_TEST` 將特定下行 port 置入 USB 2.0 電氣 test mode，與 `specs/usb_test_modes.md` 中描述的設備層級 `TEST_MODE` 不同。

```
bmRequestType: 0x23  (Host→Device, Class, Other recipient)
bRequest:      0x03  (SET_FEATURE)
wValue:        PORT_TEST（feature selector = 21 / 0x15）
wIndex[15:8]:  test_selector（1=TEST_J, 2=TEST_K, 3=TEST_SE0_NAK, 4=TEST_PACKET, 5=TEST_FORCE_ENABLE）
wIndex[7:0]:   port_number（1-based）
wLength:       0
```

`SET_FEATURE(PORT_TEST)` 後，hub 將指定下行 port 置入 test mode。該 port 不再參與正常 USB 通訊。

退出 `PORT_TEST` 需要電源循環；USB bus reset 不足以退出。

## Feature Selector 參考

| Feature Selector | 值 | 適用 | 說明 |
|---|---|---|---|
| `PORT_INDICATOR` | `22`（0x16）| Port | 控制 LED 顏色；需 wHubCharacteristics bit 7 = 1 |
| `PORT_TEST` | `21`（0x15）| Port | 將 port 置入電氣 test mode |

`PORT_INDICATOR` 和 `PORT_TEST` 均使用 `bmRequestType=0x23`（class，other recipient）。

## Governed Linkage

- `specs/hub_descriptor.md`：指示燈支援旗標 `wHubCharacteristics bit 7`
- `specs/feature_selectors.md`：feature selector 值表（PORT_TEST=21，PORT_INDICATOR=22）
- `specs/usb_test_modes.md`：HS 電氣合規的設備層級 `SET_FEATURE(TEST_MODE)`
- `specs/hub_class_requests.md`：port-recipient `SET_FEATURE` 請求結構

## Non-claims

- 本頁不宣告任何特定 hub 實作的 port 指示燈 LED 顏色已驗證。
- 本頁不宣告 PORT_TEST 行為已 implementation-verified。
- 本頁不為任何特定 hub 定義完整的 automatic 指示燈顏色邏輯。
- 本頁不覆蓋 consuming repo 已確認的 project facts。

## Reference Navigation

- specs/usb2.md: USB 2.0 topic index (zh).
- specs/en/port_indicators.md: English counterpart topic (en).
