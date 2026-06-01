---
title: USB 版本來源對應表（Hub 為主）
claim_level: inferred
status: review_required
last_reviewed: "2026-06-01"
usb_versions:
  - usb_2_0
source_refs:
  - usb20_spec
semantic_verification_claimed: false
---

# USB 版本來源對應表（Hub 為主）

> 用途：僅供語意參考層使用。不可用於覆蓋已確認的專案事實。
> 最後確認：2026-05-30

## 適用範圍說明

- 本文件對應 **USB-IF 官方來源的取得位置**，涵蓋 USB 2.0、2.1、3.2、4.0 各版本中
  與 Hub 相關的行為。
- 本文件為來源索引，非韌體需求文件。
- 規範性聲明政策由 `contract/*.yaml` 管理，而非僅憑本文件。

## 權威性與使用規則

依明確的權威邊界使用各來源類型：

| 來源類型 | 主要權威用途 | 說明 |
|---------|------------|------|
| USB-IF 官方規格書 | 是（規範性） | 用於描述符／請求／狀態／欄位定義。 |
| USB-IF ECN／附錄 | 是（規範性更新）| 須標明適用的基礎版本與範圍。 |
| USB-IF 相容性／測試規格 | 輔助用途 | 用於驗證／相容性解讀，不作為唯一基礎定義。 |
| USB-IF 文件庫／搜尋／索引頁面 | 僅供探索 | 用於定位官方文件與追蹤文件系譜。 |
| 社群參考資料（如 OSDev） | 非規範性 | 僅供快速定向與交叉比對。 |
| 鏡像站（如 Archive.org） | 備用來源 | 官方連結無法存取時用於可追溯性。 |

另見：

- `contract/authority_levels.yaml`
- `contract/claim_rules.yaml`
- `contract/evidence_requirements.yaml`
- `contract/version_scope.yaml`

## 版本分類（以 Hub 為主）

| 版本標籤 | 官方來源錨點 | Hub 相關解讀 | 來源類型 |
|---------|-----------|------------|---------|
| USB 2.0 | USB-IF 文件庫：USB 2.0 規格書 | 傳統 Hub 類別語意的主要規範來源（描述符 0x29、連接埠狀態/變更位元、Hub 類別請求、HS Hub 的 TT 行為）。 | 核心基礎規格 + ECN 套件 |
| USB 2.1（業界簡稱）| USB 2.0 頁面包含「USB 2.0 Link Power Management Addendum ECN」及後期 USB 2.0 ECN | USB-IF 文件庫中無獨立的「USB 2.1」基礎規格。比較 Hub 行為時，視為 USB 2.0 + ECN/附錄集合。 | USB 2.0 下的 ECN/附錄集合 |
| USB 3.2 | USB-IF USB 3.2 技術頁面 + USB 3.2 規格文件庫項目 | USB 3.x Hub 行為由 USB 3.2 系列資料涵蓋；USB-IF 說明 USB 3.2 已吸收先前 3.x 規格，並包含 Hub 規格的通道轉換行為更新。 | 3.2 傘形規格 + 相容性/文件 |
| USB4（4.0 命名） | USB-IF USB4 規格頁面（目前為 USB4 v2.0 頁面） | USB4 系統行為由 USB4 文件規範；USB4 拓撲包含 Hub 等效路由實體，向後相容路徑保留 USB 3.2/2.0 通道化情境。 | USB4 基礎規格系列 |

## 實際查閱順序（供未來規格提取參考）

1. 前往 USB-IF 文件庫頁面，找到目標版本。
2. 下載所引用的基礎套件（zip/pdf），並在下游文件中記錄確切章節號。
3. 遇到「USB 2.1」需求時，解析為 USB 2.0 + 特定 ECN/附錄項目名稱
   （不視為獨立基礎版本）。
4. 若 Hub 語意與已確認的韌體事實有差異，依 Standard Escalation Mode
   在 consuming repo 中觸發升級。

## 主要連結

- USB 2.0 規格書（USB-IF）：https://www.usb.org/document-library/usb-20-specification
- USB 3.2 頁面（USB-IF）：https://www.usb.org/usb-32-0
- USB 3.2 相容性/索引頁面（USB-IF）：https://www.usb.org/usb-32
- USB4 規格頁面（USB-IF，重新導向至目前 USB4 v2.0 項目）：https://www.usb.org/document-library/usb4tm-specification
- USB4 v2.0 頁面（USB-IF）：https://www.usb.org/document-library/usb4r-specification-v20

## 次要/探索連結（非規範性）

- USB-IF 文件搜尋入口：https://www.usb.org/documents
- 先前使用者工作流程的探索查詢：https://www.usb.org/documents?search=hub&tid_2%5B0%5D=40&items_per_page=50
- OSDev USB Hubs 頁面（僅供背景參考）：https://wiki.osdev.org/USB_Hubs
- Archive.org USB 2.0 鏡像頁面：https://archive.org/details/USB-2.0
- Archive.org 鏡像 USB 2.0 PDF：https://archive.org/download/USB-2.0/Universal%20Serial%20Bus%20Specification%2C%20Revision%202.0.pdf

## 驗證注意事項

部分 USB-IF 頁面為動態渲染，可能難以透過特定工具開啟。發生此情況時，
請記錄規範的 USB-IF URL，並在一般瀏覽器環境中直接存取以驗證內容。
