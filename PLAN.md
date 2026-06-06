> **Last Updated**: 2026-06-06
> **Owner**: USB-IF Hub Spec Reference
> **Freshness**: Sprint (14d)

# PLAN

This repository is a read-only USB hub specification reference layer. It
clarifies USB hub standard semantics for consuming firmware repositories, but it
does not govern firmware behavior and does not override confirmed project facts.

## Current State

- USB 2.0 LLM wiki/reference surface is complete at reviewed-reference depth.
- VitePress static site deployed to GitHub Pages; bilingual zh-TW/English.
- Governed tracked entries: 145.
- Entry-level verified entries: 100.
- Reviewed entries: 45.
- Inferred tracked entries: 0.
- Wiki pages (bilingual zh-TW + English): 28 topic pairs covering the full USB 2.0
  specification surface area (Chapters 5, 7, 8, 9, 11).
- Verification scope remains narrow: verified entries are limited to descriptor field
  identity, selector-name/value, or bit name and bit position.
- No page-level, table-level, firmware-behavior, or full USB compliance
  verification is claimed.

## Completed Phases

### Phase 1 - Governance Baseline

- Adopted `ai-governance-framework` baseline.
- Created `contract.yaml`, `AGENTS.md`, and `AGENTS.base.md`.
- Installed repo governance hooks.

Claim ceiling: governance baseline only.

### Phase 2 - USB-IF Spec Reference Tables

- `tables/escalation_trigger_matrix.yaml`: 10 reviewed USB 2.0 standard-side
  escalation trigger-boundary entries.
- `tables/hub_descriptor_matrix.yaml`: 8 verified USB 2.0 hub descriptor field
  identity entries.
- `tables/transaction_translator_matrix.yaml`: 10 reviewed USB 2.0 TT type,
  think-time, and TT request-linkage entries.
- `tables/class_request_matrix.yaml`: 12 entries, 9/9 USB 2.0 hub class request
  families covered.
- `tables/feature_selector_matrix.yaml`: 25 entries, all selector entries are now
  promoted to selector-name/value verified scope.
- `tables/port_status_bit_matrix.yaml`: 23 tracked hub/port status and change
  entries, including 19 verified entries, 0 reviewed defined port
  status/change namespace entries, and 4 reviewed high-bit boundary
  placeholders (wPortStatus, wPortChange, wHubStatus, wHubChange).
- `tables/hub_interrupt_endpoint_matrix.yaml`: 4 reviewed entries for the hub
  status change endpoint descriptor fields (bEndpointAddress, bmAttributes,
  wMaxPacketSize, bInterval).
- Core bilingual spec pages are present under `specs/` and `specs/en/`.

Claim ceiling: structured spec-reference entries only; no firmware behavior.

### Phase 2A - Wiki Frontmatter Bootstrap

- Added required frontmatter to canonical spec pages.
- Established `scripts/validate_wiki_frontmatter.py`.

Claim ceiling: wiki frontmatter structural consistency only.

### Phase 2B - Wiki/Table Consistency Probe

- Added observation-only wiki consistency probe and fixture smoke coverage.
- Real table/page token coverage has been improved through later page deepening.

Claim ceiling: lexical consistency observation only; no semantic proof.

### Phase 3 - Cross-Repo Reference Registration

- Registered this repo as standard-side reference input in the consuming
  firmware contract repo traceability surface.
- Allowed usage: lookup, semantics clarification, escalation support,
  terminology alignment.
- Prohibited usage: overriding project facts, treating inferred/reviewed entries
  as implementation truth.

Claim ceiling: cross-repo reference registered only.

### Phase 4 - Machine-Readable Consumer Access Contract

- Added `exports/usb20_hub_class_request_manifest.yaml`.
- Validators cover class request, feature selector, port status bit, and manifest
  structure.

Claim ceiling: machine-readable namespace and access contract only.

### Phase 5B - Table Fingerprint Drift Observability

- Added `scripts/probe_table_fingerprint.py`.
- Supports `baseline`, `check`, and `compact` modes.
- Current table fingerprint baseline is synchronized: 6 governed tables, 0 drift.

Claim ceiling: table content fingerprint drift only.

### Phase 6 - USB 2.0 Core Reference Deepening

- Deepened core zh-TW and English pages for:
  - hub descriptor
  - hub class requests
  - feature selectors
  - port status bits
  - transaction translator
  - escalation table
  - glossary
- Current core pages are readable reference summaries with explicit non-claims.

Claim ceiling: readable reference surface only; not semantic verification.

### Phase 7 - Section Anchor Metadata

- Added section anchor schema and governance documentation.
- Attached section references to selected pilot entries.
- Clarified that section references are evidence metadata and do not upgrade
  claim level by themselves.

Claim ceiling: section-ref metadata only.

### Phase 8 - Entry-Level Verification Pilot

- Added entry verification packet schema and governance guidance.
- Added promotion gate for a bounded pilot set.
- Current verified entries:
  - `usb20_hub_desc_bDescLength`
  - `usb20_hub_desc_bDescriptorType`
  - `usb20_hub_desc_bNbrPorts`
  - `usb20_hub_desc_wHubCharacteristics`
  - `usb20_hub_desc_bPwrOn2PwrGood`
  - `usb20_hub_desc_bHubContrCurrent`
  - `usb20_hub_desc_DeviceRemovable`
  - `usb20_hub_desc_PortPwrCtrlMask`
  - `wPortStatus.bit0.PORT_CONNECTION`
  - `wPortStatus.bit1.PORT_ENABLE`
  - `wPortStatus.bit2.PORT_SUSPEND`
  - `wPortStatus.bit3.PORT_OVER_CURRENT`
  - `wPortStatus.bit4.PORT_RESET`
  - `wPortStatus.bit8.PORT_POWER`
  - `wPortStatus.bit9.PORT_LOW_SPEED`
  - `wPortStatus.bit10.PORT_HIGH_SPEED`
  - `wPortStatus.bit11.PORT_TEST`
  - `wPortStatus.bit12.PORT_INDICATOR`
  - `wPortChange.bit0.C_PORT_CONNECTION`
  - `wPortChange.bit1.C_PORT_ENABLE`
  - `wHubStatus.bit0.HUB_LOCAL_POWER`
  - `wHubStatus.bit1.HUB_OVER_CURRENT`
  - `wHubChange.bit0.C_HUB_LOCAL_POWER`
  - `wHubChange.bit1.C_HUB_OVER_CURRENT`
  - `usb20_get_status_hub`
  - `usb20_get_status_port`
  - `usb20_set_feature_hub`
  - `usb20_set_feature_port`
  - `usb20_clear_feature_hub`
  - `usb20_clear_feature_port`
  - `usb20_clear_tt_buffer`
  - `usb20_reset_tt`
  - `usb20_get_tt_state`
  - `usb20_stop_tt`
  - `usb20_get_descriptor_hub`
  - `usb20_set_descriptor_hub`
  - Additional 25 verified entries were added from
    `tables/feature_selector_matrix.yaml` at selector-name/value scope.
- Verified scope for the 8 hub descriptor entries: descriptor field identity
  only.
- Verified scope for selector and status-change entries: selector-name/value or
  bit name and bit position only.

Claim ceiling: entry-level verified gate only.

### Phase 9 - LLM Wiki Reference Surface Completion

- Canonical visible wiki surface is under `specs/` and `specs/en/`.
- Legacy `wiki/` pages have been demoted to orientation notes.
- Homepage and verification status surfaces align to 86 tracked entries, 84 verified
  entries, 2 reviewed entries, and 0 inferred tracked entries at Phase 9 completion.
- Added `scripts/validate_reference_surface_statistics.py` to check that visible
  statistics remain aligned with governed tables and evidence packets.

Claim ceiling: LLM reference readability and boundary clarity only.

### Phase 10 - ai-governance Repo-Local Import

- Pulled latest `ai-governance-framework` state at
  `a0d42d15a43cf98be33dc8618deae8153d69ff62`.
- Imported only repo-local reporting and reviewer-facing surfaces:
  - `governance/RESPONSE_ENVELOPE_CONTRACT.md`
  - `governance/TRUST_BOUNDARY_TAXONOMY.md`
- Registered retained files in `governance/AUTHORITY.md`, `contract.yaml`, and
  `governance/framework.lock.json`.
- Excluded framework memory, artifacts, runtime profile validator, fleet
  governance, and new CI workflow surfaces.

Claim ceiling: reporting/reference governance surface only.

### Phase 11 - VitePress Static Site and GitHub Pages Deployment

- Added `.vitepress/config.ts` with zh-TW / English bilingual navigation and
  local search.
- Added `.vitepress/theme/components/AskAI.vue` — browser-side AI Q&A widget
  using `claude-haiku-4-5-20251001`; API key stored in localStorage only.
- Added `.github/workflows/deploy-pages.yml` — auto-deploys to GitHub Pages on
  push to `main` when `specs/` or `.vitepress/` changes.
- `npm run build` passes against the current `specs/` surface.

Claim ceiling: static reference site deployment only; no semantic verification
upgrade and no governance behavior change.

### Phase 14 - Full USB 2.0 Spec Coverage (Chapters 5, 7, 9)

- NEW `tables/standard_device_request_matrix.yaml`: 12 reviewed entries for standard USB 2.0
  device requests applicable to hubs (GET_STATUS device/interface/endpoint, CLEAR_FEATURE,
  SET_FEATURE, SET_ADDRESS, GET_DESCRIPTOR, GET_CONFIGURATION, SET_CONFIGURATION,
  GET_INTERFACE, SET_INTERFACE).
- NEW `scripts/validate_standard_device_request_matrix.py`: structural validator (R1–R9).
- NEW `specs/standard_device_requests.md` + EN: setup packet format, bmRequestType breakdown,
  all 11 hub-relevant standard requests, standard feature selectors.
- NEW `specs/standard_descriptors.md` + EN: device descriptor (18B), Device_Qualifier,
  configuration descriptor (9B), interface descriptor (9B), endpoint descriptor (7B),
  string descriptor — all with hub-specific values.
- NEW `specs/usb_device_states.md` + EN: Chapter 9 §9.1 device states (Attached → Powered →
  Default → Address → Configured → Suspended); comparison table vs. hub port states.
- NEW `specs/usb_transfer_types.md` + EN: Chapter 5 four transfer types; hub uses Control
  (EP0) and Interrupt (status change EP); Bulk and Isochronous not used.
- NEW `specs/usb_signaling.md` + EN: Chapter 7 §7.1 bus states (J/K/SE0/SE1), NRZI encoding,
  bit stuffing, reset/suspend/resume/SOF signaling.
- NEW `specs/hs_detection.md` + EN: Chapter 7 §7.1.7.1 HS chirp handshake sequence, outcome
  matrix, timing reference.
- Updated statistics: tracked=145, verified=84, reviewed=61.
- Updated `.vitepress/config.ts`, `specs/en/index.md`, both verification_status pages.

Claim ceiling: reviewed reference surface only; not semantic verification.

### Phase 15 - USB 2.0 Chapter 8 Coverage + HS Compliance Topics

- NEW `specs/usb_packet_types.md` + EN: PID encoding (4-bit type + 4-bit one's complement),
  all token packets (OUT=0xE1, IN=0x69, SOF=0xA5, SETUP=0x2D), data packets (DATA0/1/2/MDATA),
  handshake (ACK/NAK/STALL/NYET/ERR), special (SPLIT=0x78), hub operation packet table.
- NEW `specs/usb_transactions.md` + EN: SETUP/IN/OUT transaction structure, control transfer
  3-phase (SETUP+DATA+STATUS), interrupt polling, data toggle mechanism, error response table.
- NEW `specs/split_transaction_packets.md` + EN: SPLIT PID=0x78, 4-byte structure with bit
  layout (Hub Addr[6:0]+SC[7]+Port[14:8]+S[15]+E/U[16]+ET[18:17]+CRC5[23:19]), SSPLIT/CSPLIT
  flows with NYET handling, control transfer micro-frame example, endpoint type behavior table.
- NEW `specs/usb_test_modes.md` + EN: TEST_J/K/SE0_NAK/PACKET/FORCE_ENABLE selectors,
  SET_FEATURE(TEST_MODE) encoding (bmRequestType=0x00, wValue=0x0002, wIndex=[mode<<8]),
  power-cycle-only exit rule, hub port test mode wIndex encoding.
- NEW `specs/port_indicators.md` + EN: wHubCharacteristics bit 7 indicator support,
  SET_FEATURE(PORT_INDICATOR) with selector values 0=Auto/1=Amber/2=Green/3=Off,
  PORT_TEST feature selector (value=21/0x15), both use bmRequestType=0x23.
- NEW `specs/hub_power_budget.md` + EN: self-powered vs. bus-powered rules (bmAttributes bit 6),
  per-port limits (500 mA vs. 100 mA), bHubContrCurrent (direct mA) vs. bMaxPower (×2),
  power budget example, overcurrent interaction.
- Updated `.vitepress/config.ts`: 6 new labels in ZH_LABELS/EN_LABELS, 6 new nav items
  in zhReferenceItems and enReferenceItems.
- Updated `specs/en/index.md`: 6 new feature cards.
- Statistics unchanged (all new pages are wiki only, no new matrix entries).

Claim ceiling: reviewed reference surface only; not semantic verification.

### Phase 13 - USB 2.0 Complete Coverage Expansion

- NEW `specs/hub_enumeration.md` + `specs/en/hub_enumeration.md`:
  - Hub enumeration 3-phase sequence (standard device enum → hub init → port monitoring).
  - `GET_STATUS` 4-byte response format (wStatus[1:0] + wChange[3:2]).
  - Speed detection table (PORT_LOW_SPEED / PORT_HIGH_SPEED after port reset).
  - Port timing reference (10ms minimum reset, bPwrOn2PwrGood × 2ms).
- NEW `specs/hub_compound_device.md` + `specs/en/hub_compound_device.md`:
  - `wHubCharacteristics bit 2` compound device indicator.
  - `DeviceRemovable` bitmap layout and non-removable port interpretation.
  - `PortPwrCtrlMask` USB 2.0 semantics (all bits = 0xFF, no actionable meaning).
  - `wHubCharacteristics` bit layout cross-reference table.
- ENHANCED `specs/port_state_machine.md` + EN:
  - Added Port Reset Timing section (10ms minimum, 20ms cycle).
  - Added Speed Detection After Reset section.
- ENHANCED `specs/hub_class_requests.md` + EN:
  - Added `GET_STATUS` response format table (4-byte layout).
- `.vitepress/config.ts`: registered hub_enumeration and hub_compound_device.
- `specs/en/index.md`: added feature cards for new pages.

Claim ceiling: reviewed reference surface only; not semantic verification.

## Active Validators

- `python scripts\validate_wiki_frontmatter.py`
- `python scripts\validate_wiki_source_coverage.py`
- `python scripts\validate_reference_surface_statistics.py`
- `python scripts\validate_escalation_trigger_matrix.py`
- `python scripts\validate_hub_descriptor_matrix.py`
- `python scripts\validate_transaction_translator_matrix.py`
- `python scripts\validate_feature_selector_matrix.py`
- `python scripts\validate_port_status_bit_matrix.py`
- `python scripts\validate_class_request_matrix.py`
- `python scripts\validate_class_request_coverage.py --matrix tables\class_request_matrix.yaml`
- `python scripts\probe_table_fingerprint.py --mode check --manifest exports\usb20_hub_class_request_manifest.yaml --baseline-in evidence\table_fingerprint_baseline.jsonl`
- `npm.cmd run build`

## Open Work

1. Continue entry-level verification only when narrow evidence packets and gate
   scope are explicit.
2. Keep consuming-repo integration as reference-only; any firmware behavior
   change still belongs in the consuming repo's Standard Escalation Mode.

## Cannot Claim

- USB 2.0 hub behavior is fully verified.
- All entries are PDF-semantically verified.
- Reviewed coverage is the same as verified coverage.
- This repo can override consuming firmware project facts.
- Fleet governance is enabled.
- Runtime profile validation or response envelope enforcement is active.
