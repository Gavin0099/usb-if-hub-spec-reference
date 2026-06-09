# Review Log

## 2026-06-02 Repo Audit

### Review Inputs Checked
- governance/REVIEW_CRITERIA.md
- specs/escalation_table.md
- specs/index.md
- specs/en/index.md
- .vitepress/config.ts
- .vitepress/theme/index.ts
- scripts/probe_table_fingerprint.py

### [Decision Summary]
**Verdict**: CHANGES_REQUESTED
**Risk Level**: Low

### Governance Audit
- Architecture: APPROVED (符合唯讀標準規格澄清層邊界限制，未引入韌體行為)
- Native Safety: N/A
- Test Integrity: APPROVED (內建豐富的驗證腳本與 smoke tests 確保 table 一致性與結構完整性)
- Thread Safety: N/A
- Baseline Status: Stable

### Technical Findings

1. [WARNING] 多語言 (Locales) 未在 VitePress 配置中啟用
   - Location: `.vitepress/config.ts`
   - Evidence: 專案內已完整建立 `specs/en/` 目錄，但 `.vitepress/config.ts` 的 `themeConfig` 完全沒有 locales 配置，使得英文版 sidebar 與導覽列無法渲染，讀者亦無法於 UI 上進行切換。
   - Rule Reference: `governance/REVIEW_CRITERIA.md` 3.3 Quality and Verification
   - Fix Required / Reasoning: 在 `defineConfig` 中加入 `locales` 屬性，為 `root` (zh-TW) 與 `en` 分別配置 sidebar 和 nav，以整合現有英文規格 Wiki。

2. [WARNING] `probe_table_fingerprint.py` 缺乏 Compaction 收縮機制
   - Location: `scripts/probe_table_fingerprint.py`
   - Evidence: `run_baseline()` 在執行 `--mode baseline` 時採用 pure-append 模式，不斷追加新 entry 到 `evidence/table_fingerprint_baseline.jsonl`，在長時間開發演進中會導致檔案累積無效 entry。
   - Rule Reference: `governance/REVIEW_CRITERIA.md` 3.3 Quality and Verification
   - Fix Required / Reasoning: 建議增加 `--compact` 或 `--clean` 參數，以便在寫入新雜湊前對檔案進行收縮或重新整理，清除 stale entries。

3. [WARNING] `tables/port_status_bit_matrix.yaml` 缺乏全面的 PDF 節區驗證
   - Location: `tables/port_status_bit_matrix.yaml`
   - Evidence: 除少數 pilot 項目（如 `PORT_CONNECTION`、`PORT_ENABLE` 等）外，大多數連接埠狀態位元項目仍缺乏 `section_refs`，且此表格與核心 specs 頁面的 `claim_level` 依然是 `inferred`。
   - Rule Reference: `governance/REVIEW_CRITERIA.md` 3.3 Quality and Verification
   - Fix Required / Reasoning: 應逐步推進 Phase 8 計畫，將更多 bit 與 USB 2.0 Spec PDF 的具體節區進行 bit-by-bit 對照，補全 `section_refs`，從而提高 spec 信心。

4. [SUGGESTION] specs 靜態網站 UI 樣式與 Favicon 遺失問題
   - Location: `specs/escalation_table.md`（包括中文與英文版）
   - Evidence:
     - 觸發條件表格首欄（編號欄位）因連字號 `-` 而被非預期折行。
     - 範例程式碼區塊在預設載入寬度下發生文字被截斷且出現灰色水平滾動條。
     - Console 拋出 `Failed to load resource: the server responded with a status of 404 (Not Found) - favicon.ico`。
   - Rule Reference: `governance/REVIEW_CRITERIA.md` 3.3 Quality and Verification
   - Fix Required / Reasoning: 建議於 `.vitepress/theme/` 中新增 custom CSS，加入 `white-space: nowrap !important;` (表格首欄) 與 `white-space: pre-wrap !important;` (pre/code) 的設定，並於 `specs/public/` 中放置 `favicon.ico` 解決錯誤。

### Knowledge Base Alignment
- Anti-patterns checked: 0
- Regression notes checked: 0
- Result: Pass

---

## 2026-06-09 Hub PM Review — Yihsun (State Transition Readability)

### Review Type
External functional review — Hub PM user perspective.

### Reviewer
Yihsun (Hub PM). Context: shared site URL after HOME-IA-1 cleanup.

### Initial Feedback
> 看得懂，很清楚。

Positive reception after HOME-IA-1 homepage redesign (categorical cards replacing flat 28-topic list).

### Gap Identified
Follow-up question: "有沒有你最常需要查但這裡找不到的東西？"

Reviewer response:
> 就是某些state只能從哪裡跳到哪裡，不能跳到那裏。USB3就像是SS.disable state, Rx.detect state, recovery state…很多state, 不能隨便跳到哪。U2也有。那種要用流程圖比較看得懂。

### Root Cause Analysis

Two distinct gaps were identified:

1. **Hub-class port state transitions** (USB 2.0 and USB 3.x U-states): which transitions require intermediate states; no direct path rules.
2. **LTSSM physical-layer states** (USB 3.x SS.Disabled, Rx.Detect, Polling, Recovery, etc.): orientation of how these states relate to each other.

### Response

| Gap | Response | Claim ceiling |
|---|---|---|
| USB 2.0 hub port transition constraints | Added "Transition Constraints" table to `port_state_machine.md` (ZH+EN) | `claim_level: inferred` |
| USB 3.x U-state transition constraints | Added "U-State Transition Rules" to `ss_port_state_machine.md` (ZH+EN) | `claim_level: inferred` |
| LTSSM state orientation | New `ss_ltssm.md` (ZH+EN): state groups + high-level transition orientation | `claim_level: inferred`, `governed_surface: false` |

### Governance Decision

LTSSM was incorporated as **orientation reference only**. It was not added to the governed/verified surface.

- `governed_surface: false`
- `verified_count_delta: 0`
- LTSSM governed matrix: not created

Rationale: LTSSM behavior (LFPS, equalization, timing, compliance mode) is physical-layer scope far outside the hub class descriptor / request / status bit surface this repo governs. Incorporating it as orientation reference addresses the reviewer's readability need without expanding the governed claim boundary.

### Mermaid Diagram Request

Reviewer noted: "那種要用流程圖比較看得懂."

Decision: deferred as LTSSM-0 Phase B. Requires:
1. Mermaid plugin installation (`vitepress-plugin-mermaid` or equivalent)
2. Diagram title locked to "Simplified LTSSM Orientation Diagram" (not "USB3 LTSSM State Machine")
3. Diagram scope limited to orientation — not a normative transition matrix

### Status
CLOSED. Readability gap addressed. Governed surface unchanged.
