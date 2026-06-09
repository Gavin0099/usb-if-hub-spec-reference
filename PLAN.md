> **Last Updated**: 2026-06-09
> **Owner**: USB-IF Hub Spec Reference
> **Freshness**: Sprint (14d)

# PLAN

This repository is a read-only USB hub specification reference layer. It
clarifies USB hub standard semantics for consuming firmware repositories, but it
does not govern firmware behavior and does not override confirmed project facts.

## Current State

- USB 2.0 LLM wiki/reference surface is complete at reviewed-reference depth.
- VitePress static site deployed to GitHub Pages; bilingual zh-TW/English.
- Governed tracked entries: 151.
- Entry-level verified entries: 105.
- Reviewed entries: 46.
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

### Phase 16 - Bucket B Verified Promotion

- Promoted 16 reviewed entries to verified across two tables:
  - `tables/standard_device_request_matrix.yaml`: all 12 entries reviewed → verified
    (GET_STATUS, CLEAR_FEATURE, SET_FEATURE, SET_ADDRESS, GET_DESCRIPTOR,
    GET_CONFIGURATION, SET_CONFIGURATION, GET_INTERFACE, SET_INTERFACE — device,
    interface, and endpoint variants)
  - `tables/hub_interrupt_endpoint_matrix.yaml`: all 4 entries reviewed → verified
    (bEndpointAddress, bmAttributes, wMaxPacketSize, bInterval)
- 16 evidence packets written (one per promoted entry).
- Statistics at completion: tracked=145, verified=100, reviewed=45, inferred=0,
  evidence_packets=100.
- Updated visible surfaces: README.md, PLAN.md, specs/en/index.md,
  verification_status.md (ZH + EN); verified entries table +16 rows.
- Reviewed surface post-promotion: 45 entries = 4 high-bit boundary-only +
  41 reserved bits (permanent boundaries, no semantic promotion pending).

Claim ceiling: entry-level verified gate only; selector-name/value or bit name
and bit position identity scope only.

### Phase WHC-1 - wHubCharacteristics Bit-Group Governed Matrix

- NEW `tables/wHubCharacteristics_bit_matrix.yaml`: 6 entries covering wHubCharacteristics
  bit groups with value_encoding:
  - `usb20_whc_power_switching` (bits[1:0]): Logical Power Switching Mode — verified
  - `usb20_whc_compound_device` (bit[2]): Compound Device flag — verified
  - `usb20_whc_over_current_mode` (bits[4:3]): Over-Current Protection Mode — verified
  - `usb20_whc_tt_think_time` (bits[6:5]): TT Think Time (cross-link to TT matrix) — verified
  - `usb20_whc_port_indicators` (bit[7]): Port Indicators Supported — verified
  - `usb20_whc_reserved_high` (bits[15:8]): Reserved boundary — permanent reviewed
- NEW `scripts/validate_wHubCharacteristics_bit_matrix.py`: structural validator (R1–R10).
- 5 evidence packets written (one per verified entry).
- `scripts/validate_reference_surface_statistics.py`: registered hub_characteristics_bits.
- Updated `specs/hub_descriptor.md` + EN: Governed Linkage → wHubCharacteristics bit matrix.
- Statistics: tracked=151, verified=105, reviewed=46.

Claim ceiling: bit-group name and value-encoding identity only; not descriptor dump
verification, firmware behavior, electrical/power behavior, or hub compliance.

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

### Phase USB3-0 - SuperSpeed Hub Scope Boundary

- NEW `governance/USB3_SCOPE_BOUNDARY.md`: defines candidate scope, spec
  authority, governance separation rules, schema compatibility note, UI namespace
  plan (deferred), and permanent non-claims for USB 3.x governed surface.
- Candidate governed surface identified: SS hub descriptor, SS port status bits,
  SS feature selectors (PORT_U1_TIMEOUT, PORT_U2_TIMEOUT), SS hub class requests
  (SET_HUB_DEPTH, GET_PORT_ERR_COUNT).
- Governance separation: USB 3.x entries will be in separate tables; no
  cross-table claim-level inheritance with USB 2.0; `specs/usb3/` namespace
  reserved; `spec_family: usb3` frontmatter required.
- No governed entries added. No wiki pages added. No UI changes.
- USB 2.0 governed surface freeze is unaffected: tracked=151, verified=105,
  reviewed=46.

Claim ceiling: scope boundary documentation only. No USB 3.x reference surface
is claimed to exist. No USB 3.x entries are tracked.

### Phase USB3-1 - SuperSpeed Hub Wiki Scaffold + UI Namespace Split

- NEW `specs/usb3/` and `specs/en/usb3/` namespace established.
- NEW 3 bilingual wiki page pairs (ZH + EN):
  - `ss_hub_descriptor`: bDescriptorType=0x2A, wHubCharacteristics (no TT Think Time),
    bHubDecLat, wHubDelay; comparison table vs. USB 2.0 descriptor.
  - `ss_port_status_bits`: wPortStatus / wPortChange full bit definitions,
    PORT_LINK_STATE encoding table (U0–Loopback), PORT_SPEED encoding table
    (FS/LS/HS/SS/SS+), wPortChange new bits (C_BH_PORT_RESET, C_PORT_LINK_STATE,
    C_PORT_CONFIG_ERROR); comparison table vs. USB 2.0.
  - `ss_hub_class_requests`: SET_HUB_DEPTH (mandatory), GET_PORT_ERR_COUNT
    (optional), TT-related requests not applicable, SS feature selectors
    (PORT_U1_TIMEOUT, PORT_U2_TIMEOUT, PORT_BH_PORT_RESET).
- NEW `specs/usb3/index.md` and `specs/en/usb3/index.md`: USB 3.x section
  landing pages with coverage table and key USB 2.0 vs USB 3.x differences.
- All USB 3.x pages carry `spec_family: usb3` frontmatter.
- UI namespace split in `.vitepress/config.ts`:
  - Nav Reference dropdown grouped: USB 2.0 Hub / USB 3.x SuperSpeed Hub.
  - Sidebar split into two sections: USB 2.0 Hub / USB 3.x SuperSpeed Hub.
  - ZH and EN label dictionaries extended with USB 3.x keys.
  - Footer updated to version-neutral non-claim (ZH + EN).
- USB 2.0 page URLs, labels, and nav order unchanged.
- USB 2.0 freeze unaffected: tracked=151, verified=105, reviewed=46.

Claim ceiling: reference summary only; not semantic verification of USB 3.x
entries. No USB 3.x governed matrix entries tracked. No LTSSM, xHCI, or
electrical compliance claimed.

### Phase USB3-2 - SuperSpeed Governed Matrix Scaffold

- NEW `tables/ss_port_status_bit_matrix.yaml`: 19 entries (15 defined + 4 reserved).
  wPortStatus: PORT_CONNECTION, PORT_ENABLE, PORT_OVER_CURRENT, PORT_RESET,
  PORT_LINK_STATE (bits[8:5] with 12-value encoding), PORT_POWER,
  PORT_SPEED (bits[12:10] with 6-value encoding), PORT_U1_ENABLE, PORT_U2_ENABLE,
  plus reserved boundaries.
  wPortChange: C_PORT_CONNECTION, C_PORT_OVER_CURRENT, C_PORT_RESET,
  C_BH_PORT_RESET, C_PORT_LINK_STATE, C_PORT_CONFIG_ERROR, plus reserved boundaries.
- NEW `tables/ss_hub_class_request_matrix.yaml`: 10 entries.
  Shared with USB 2.0: GET_STATUS, SET_FEATURE, CLEAR_FEATURE, GET_DESCRIPTOR,
  SET_DESCRIPTOR. SS-only mandatory: SET_HUB_DEPTH (0x0C).
  SS-only optional: GET_PORT_ERR_COUNT (0x0D).
  TT requests not included (SS hubs have no TT).
- NEW `tables/ss_hub_descriptor_matrix.yaml`: 9 entries.
  All USB 3.x SS hub descriptor fields including new USB 3.x-only fields:
  bHubDecLat and wHubDelay.
- NEW `scripts/validate_ss_port_status_bit_matrix.py`: R1–R10 structural
  validator; verified gate CLOSED at scaffold.
- NEW `scripts/validate_ss_hub_class_request_matrix.py`: R1–R7 structural
  validator; verified gate CLOSED at scaffold.
- NEW `scripts/validate_ss_hub_descriptor_matrix.py`: R1–R7 structural
  validator; verified gate CLOSED at scaffold.
- All USB 3.x scaffold entries: `claim_level: reviewed`, `evidence_status: reviewed`.
- USB 3.x scaffold statistics (38 entries, 0 verified) are tracked SEPARATELY
  from USB 2.0 surface; USB 2.0 freeze unaffected: tracked=151, verified=105,
  reviewed=46.
- `specs/verification_status.md` + EN: added USB 3.x scaffold surface section
  with independent 38-entry table and explicit non-claims.

Claim ceiling: scaffold_reviewed — bit/field/request name and position identity
only. Verified gate closed. No LTSSM, xHCI, or electrical compliance claimed.

### Phase USB3-3A - SS Hub Descriptor Field Identity Verified Pilot

- `tables/ss_hub_descriptor_matrix.yaml` promoted to version "0.2": all 9
  SS hub descriptor entries promoted from `reviewed` to `verified`.
  Verified scope: descriptor field identity only (field name, offset, size).
- NEW `evidence/entry_verification_packets/usb3/` subdirectory created to
  isolate USB 3.x evidence packets from USB 2.0 surface statistics.
- 9 USB 3.x evidence packets created (one per descriptor field):
  `ss_hub_descriptor_usb3_bLength.yaml`, `ss_hub_descriptor_usb3_bDescriptorType.yaml`,
  `ss_hub_descriptor_usb3_bNbrPorts.yaml`, `ss_hub_descriptor_usb3_wHubCharacteristics.yaml`,
  `ss_hub_descriptor_usb3_bPwrOn2PwrGood.yaml`, `ss_hub_descriptor_usb3_bHubContrCurrent.yaml`,
  `ss_hub_descriptor_usb3_bHubDecLat.yaml`, `ss_hub_descriptor_usb3_wHubDelay.yaml`,
  `ss_hub_descriptor_usb3_DeviceRemovable.yaml`.
- `scripts/validate_ss_hub_descriptor_matrix.py` rewritten from CLOSED gate
  to PARTIAL/allowlist gate (ALLOWLIST_VERIFIED_IDS = 9 field IDs).
- `specs/verification_status.md` + EN: added USB 3.x Scaffold Surface section
  showing independent stats: 38 tracked, 9 verified (SS hub descriptor), 29 reviewed.
  USB 3.x evidence packets tracked at 9, stored in `usb3/` subdirectory,
  not counted in USB 2.0 statistics (105 remains).
- USB 2.0 freeze unaffected: tracked=151, verified=105, reviewed=46, evidence_packets=105.

Claim ceiling: descriptor_field_identity_only — field name, offset, and size
boundary only. Does not claim descriptor dump correctness, firmware behavior, or
electrical compliance. SS port status and SS hub class request matrices remain
with verified gate CLOSED; no USB3-3B/USB3-3C pilot yet started.

### Phase USB3-3B - SS Hub Class Request Evidence Pilot

- `tables/ss_hub_class_request_matrix.yaml` promoted to version "0.2": all 10
  SS hub class request entries promoted from `reviewed` to `verified`.
  Three distinct verified scopes applied:
  - 8 shared requests: `request_linkage_identity_only` (request name, bRequest,
    recipient, bmRequestType identity only)
  - `usb3_set_hub_depth`: `request_identity_requiredness_only` (request name,
    bRequest=0x0C, SS-only mandatory status; not xHCI topology behavior)
  - `usb3_get_port_err_count`: `request_identity_optionality_only` (request
    name, bRequest=0x0D, SS-only optional status; not error counter hardware)
- 10 USB 3.x evidence packets added to `evidence/entry_verification_packets/usb3/`:
  one per SS hub class request entry.
- `scripts/validate_ss_hub_class_request_matrix.py` rewritten from CLOSED gate
  to PARTIAL/allowlist gate (ALLOWLIST_VERIFIED_IDS = 10 request IDs).
- `specs/verification_status.md` + EN: USB 3.x scaffold stats updated to
  38 tracked / 19 verified / 19 reviewed, evidence_packets=19 (usb3/).
- USB 2.0 freeze unaffected: tracked=151, verified=105, reviewed=46,
  evidence_packets=105.

Non-claims (written into evidence packets):
- SET_HUB_DEPTH verified scope does not cover xHCI topology runtime behavior
  or hub depth assignment algorithm.
- GET_PORT_ERR_COUNT verified scope does not cover error counter hardware
  behavior or link quality measurement accuracy.
- No TT request behavior claimed (TT requests absent from SS matrix by design).
- No xHCI, LTSSM, or firmware compliance claimed.

Claim ceiling: per-entry scoped — request_linkage_identity_only (shared),
request_identity_requiredness_only (SET_HUB_DEPTH),
request_identity_optionality_only (GET_PORT_ERR_COUNT).
SS port status bit matrix verified gate CLOSED → OPEN in USB3-3C.

### Phase USB3-3C - SS Port Status Bit Matrix Verified Pilot

- `tables/ss_port_status_bit_matrix.yaml` promoted to version "0.2": 15 defined
  SS port status bit entries promoted from `reviewed` to `verified`.
  Two distinct verified scopes applied:
  - 13 single-bit defined entries: `bit_name_and_position_only`
    (PORT_CONNECTION, PORT_ENABLE, PORT_OVER_CURRENT, PORT_RESET, PORT_POWER,
    PORT_U1_ENABLE, PORT_U2_ENABLE in wPortStatus; C_PORT_CONNECTION,
    C_PORT_OVER_CURRENT, C_PORT_RESET, C_BH_PORT_RESET, C_PORT_LINK_STATE,
    C_PORT_CONFIG_ERROR in wPortChange)
  - 2 multi-bit defined entries: `bit_name_range_and_encoding_identity_only`
    (PORT_LINK_STATE bits[8:5] with 12-value encoding; PORT_SPEED bits[12:10]
    with 6-value encoding)
  - 4 reserved entries remain `reviewed` (permanent boundaries, not promotable):
    wPortStatus bit4, bit15; wPortChange bit1, bits[15:7]
- 15 USB 3.x evidence packets added to `evidence/entry_verification_packets/usb3/`:
  one per SS port status bit defined entry.
- `scripts/validate_ss_port_status_bit_matrix.py` rewritten from CLOSED gate to
  PARTIAL/allowlist gate (ALLOWLIST_VERIFIED_IDS = 15 defined entry IDs).
- `specs/verification_status.md` + EN: USB 3.x stats updated to
  38 tracked / 34 verified / 4 reviewed, evidence_packets=34.
  Second scaffold table updated to reflect all three gates OPEN.
- USB 2.0 freeze unaffected: tracked=151, verified=105, reviewed=46,
  evidence_packets=105.

Non-claims (written into evidence packets):
- PORT_LINK_STATE verified scope does not cover LTSSM state transitions,
  U1/U2/U3 entry/exit timing, or xHCI link state management.
- PORT_SPEED verified scope does not cover speed detection hardware or
  LTSSM training outcome.
- C_BH_PORT_RESET verified scope does not cover BH Reset timing or LFPS signaling.
- C_PORT_LINK_STATE verified scope does not cover LTSSM transition conditions.
- C_PORT_CONFIG_ERROR verified scope does not cover configuration failure
  conditions or xHCI enumeration error handling.
- No LTSSM, xHCI, LPM, or firmware compliance claimed.

Claim ceiling: per-entry scoped — bit_name_and_position_only (single-bit),
bit_name_range_and_encoding_identity_only (PORT_LINK_STATE, PORT_SPEED).
All three USB 3.x governed matrices are now at verified status for their
defined entries. USB 3.x surface: 38 tracked / 34 verified / 4 reviewed.

### Phase USB3-FS-1 - SS Feature Selector Matrix Scaffold

- NEW `tables/ss_feature_selector_matrix.yaml`: 6 SS-only port feature selector
  entries (scaffold phase, verified gate CLOSED).
  All entries: `claim_level: reviewed`, `evidence_status: reviewed`.
  Entries: PORT_U1_ENABLE (17), PORT_U2_ENABLE (18), PORT_U1_TIMEOUT (23),
  PORT_U2_TIMEOUT (24), PORT_REMOTE_WAKE_MASK (27), BH_PORT_RESET (28).
  Each entry carries an explicit `non_claims` block covering U-state behavior,
  LTSSM, xHCI policy, reset sequence, wake policy, and firmware compliance.
- NEW `scripts/validate_ss_feature_selector_matrix.py`: CLOSED gate validator
  (R1–R8); `claim_level: verified` is blocked until USB3-FS-2.
- `specs/verification_status.md` + EN: added "USB 3.x Feature Selector
  Expansion Scaffold" section with independent 6-entry table, gate CLOSED.
  This section is explicitly separate from the 38/34/4 matrix-level closeout
  baseline; USB 3.x closeout numbers unchanged.
- PLAN.md: Active Validators updated; USB 3.x state section updated.
- USB 2.0 freeze unaffected: tracked=151, verified=105, reviewed=46.
- USB 3.x matrix-level closeout unaffected: tracked=38, verified=34, reviewed=4.
- Expansion scaffold does not enter the unified manifest or fingerprint baseline
  (those remain at EXPORT-CONTRACT-1.0 state).

Claim ceiling: selector name/value/applicability/recipient identity only.
Verified gate: CLOSED. U1/U2 behavior, LTSSM, xHCI, reset timing, and wake
policy are outside scope permanently at this level.

### Phase USB3-FS-2 - SS Feature Selector Verified Promotion

- `tables/ss_feature_selector_matrix.yaml` promoted to version "0.2": all 6
  SS-only port feature selector entries promoted from `reviewed` to `verified`.
  Verified scope: `selector_name_value_applicability_recipient_identity_only`.
  All 6 entries carry an explicit `evidence.verification_packet` reference
  and per-entry `non_claims` blocks.
- 6 USB 3.x evidence packets created in `evidence/entry_verification_packets/usb3/`:
  `ss_feature_selector_usb3_port_u1_enable.yaml`,
  `ss_feature_selector_usb3_port_u2_enable.yaml`,
  `ss_feature_selector_usb3_port_u1_timeout.yaml`,
  `ss_feature_selector_usb3_port_u2_timeout.yaml`,
  `ss_feature_selector_usb3_port_remote_wake_mask.yaml`,
  `ss_feature_selector_usb3_port_bh_port_reset.yaml`.
- `scripts/validate_ss_feature_selector_matrix.py` rewritten from CLOSED gate
  to PARTIAL/allowlist gate (ALLOWLIST_VERIFIED_IDS = 6 selector IDs, R1–R8).
- `specs/verification_status.md` + EN: "USB 3.x Feature Selector Expansion Scaffold"
  section updated to "USB3-FS-2" with 6 verified entries table and evidence
  packet listing. Gate updated from CLOSED to PARTIAL/allowlist.
- USB 2.0 freeze unaffected: tracked=151, verified=105, reviewed=46.
- USB 3.x matrix-level closeout unaffected: tracked=38, verified=34, reviewed=4.
- Feature selector expansion: tracked=6, verified=6, reviewed=0.
- Feature selector evidence packets: 6 (separate from USB 3.x matrix 34-packet count).
- Manifest/baseline inclusion deferred to EXPORT-CONTRACT-1.1.

Non-claims:
- U1/U2 power state entry or exit behavior not verified.
- LTSSM transition behavior not verified.
- xHCI port power policy or xHCI warm reset behavior not verified.
- U1/U2 timeout encoding semantics or wValue field behavior not verified.
- Remote wake event routing, platform wake policy, OS power management not verified.
- BH/warm reset sequence timing, LFPS signaling, link recovery outcome not verified.

Claim ceiling: selector_name_value_applicability_recipient_identity_only.
Verified gate: PARTIAL / allowlist-only (6 entries, USB3-FS-2 pilot complete).

### Phase RELEASE-1 - Hub Governed Surface Export Contract Release Note

- NEW `docs/RELEASE_NOTES_EXPORT_CONTRACT.md`: stable checkpoint release note
  covering the full export contract surface at EXPORT-CONTRACT-1.0.
  Sections: governed surface state at release (USB 2.0 freeze + USB 3.x
  matrix-level closeout with per-table breakdown), export contract components
  (six components with paths and roles), consuming repo usage guide (entry
  point, two-step CI gate, allowed usage, re-baseline procedure), non-claims
  (fixed boundaries: LTSSM, xHCI, firmware compliance, electrical, USB-IF,
  USB 3.x depth parity), public navigation chain, phases included in release.
- PLAN.md: add RELEASE-1 phase entry.
- No table changes. No statistic changes.

### Phase DOC-LINK-1 - Consumer Contract Visibility Sync

- `README.md`: restructured "Current USB 2.0 Status" into "Governed Surface
  Status" with separate USB 2.0 (Freeze) and USB 3.x (Matrix-Level Closeout)
  subsections. Updated "Machine-Readable Surfaces" to reference the unified
  manifest and all 34+105 evidence packets. Added "Consumer Integration"
  section with two-step CI gate commands and link to contract doc. Updated
  "Validation" commands to use new manifest + consumer smoke. Added USB3/export
  non-claims to "Non-Claims" block.
- `specs/verification_status.md` + EN: added "Export Contract Surface" section
  listing the six export contract components (manifest, fingerprint baseline,
  contract doc, manifest validator, fingerprint probe, consumer smoke) with
  component roles, two-step CI gate commands, and export contract non-claims.
- `specs/en/index.md`: added "Consumer Integration Contract" feature card
  above Verification Status; updated Verification Status card details to show
  both USB 2.0 and USB 3.x stats; updated footer boundary note to name
  manifest and contract doc.
- No table changes. No statistic changes.
- All validators, consumer smoke, and build PASS.

### Phase CONSUMER-SMOKE-1 - Consumer Integration Contract Smoke Fixture

- NEW `scripts/smoke_consumer_integration_fixtures.py`: smoke test covering
  three consumer integration contract cases using the real governed surface:
  - `manifest_integrity_pass`: `validate_hub_governed_surface_manifest.py`
    against the real manifest — expect exit 0, PASS in output.
  - `fingerprint_no_drift`: `probe_table_fingerprint.py --mode check` against
    the real manifest + real baseline — expect exit 0, 12 tables checked, 0 drift.
  - `fingerprint_drift_detected`: programmatically corrupt the hash for
    `usb20_hub_descriptor_field_matrix` in a temp baseline copy, run check —
    expect exit 1, drift_count=1, table id named in stdout.
- The drift case validates that the failure message specifically identifies the
  drifted table — not just that the check failed.
- All three cases PASS.
- Active Validators updated to include `smoke_consumer_integration_fixtures.py`.
- No table changes. No statistic changes.

Authority ceiling: consumer_integration_contract_smoke_only.
Claim ceiling: does not validate table semantics or promote claim levels.

### Phase EXPORT-2 - Consumer Integration Contract

- NEW `docs/CONSUMER_INTEGRATION_CONTRACT.md`: formal consumer-facing contract
  for the governed surface export. Defines:
  - **Entry point**: `exports/hub_governed_surface_manifest.yaml` as the
    canonical governed truth index; consuming repos must not read individual
    YAML tables directly as primary source of truth.
  - **Two-step integration check**: Step 1 = manifest structural integrity
    (`validate_hub_governed_surface_manifest.py`); Step 2 = table content
    drift detection (`probe_table_fingerprint.py --mode check`).
  - **Allowed usage** (6 categories): table drift detection, selector/request/
    bit identity reference, reserved boundary guard, USB 2.0/USB 3.x family
    separation, verified scope lookup, reviewed meaning lookup.
  - **Forbidden usage** (7 categories): firmware compliance truth,
    LTSSM runtime behavior, xHCI port state management, electrical/timing
    compliance, USB-IF certification, treating reviewed entries as
    implementation truth, overriding consuming repo project facts.
  - **Failure interpretation**: Manifest validator FAIL = export contract
    broken (stop using governed surface); Fingerprint drift FAIL = governed
    table changed (investigate then re-baseline if authorized).
  - **Governance layer model**: L1–L3 confirmed; L4 (framework runtime) and
    L5 (consumer enforcement) left to the consuming repo's decision.
  - Explicit non-claims: PORT_LINK_STATE/LTSSM, xHCI behavior, USB-IF
    certification, USB 3.x depth ≠ USB 2.0 depth.
- Supersedes `docs/phase4_consumer_access_closeout.md` (partial Phase 4 contract).
- No table changes. No statistic changes.

Claim ceiling: governed_matrix_identity_and_boundary_reference_only.

### Phase EXPORT-1 - Unified Hub Governed Surface Manifest

- NEW `exports/hub_governed_surface_manifest.yaml`: unified machine-readable
  manifest covering all 12 governed tables (9 USB 2.0 + 3 USB 3.x).
  - `authority_surface` block declares per-family state, tracked/verified/reviewed
    counts, reviewed_meaning, and pending_semantic_promotion.
  - `claim_ceiling` block lists all cannot-establish domains (firmware behavior,
    LTSSM, xHCI, electrical compliance, USB-IF certification).
  - `consumer_usage` block specifies intended uses and must-not constraints.
  - Each `governed_tables` entry carries: id, spec_family, path, validator,
    state, verified, reviewed, verified_scope, reviewed_meaning (where applicable).
- NEW `scripts/validate_hub_governed_surface_manifest.py`: structural validator
  (R1–R8) checking manifest_id, entry completeness, path existence, spec_family
  and state validity, id uniqueness, and per-family verified/reviewed sum
  cross-check against authority_surface summary.
- Updated `evidence/table_fingerprint_baseline.jsonl`: re-baselined with all
  12 tables (was 6 USB 2.0 only); compact pass retained 12 latest entries.
  Fingerprint check PASSES: 12 tables, 0 drift.
- `exports/usb20_hub_class_request_manifest.yaml`: marked deprecated; retained
  for backward compatibility; consumers directed to new manifest.
- Active Validators updated: `validate_hub_governed_surface_manifest.py` added;
  fingerprint probe updated to use `hub_governed_surface_manifest.yaml`.

USB 2.0 freeze unaffected: tracked=151, verified=105, reviewed=46.
USB 3.x surface unaffected: tracked=38, verified=34, reviewed=4.

Claim ceiling: manifest_structural_integrity_only; does not re-verify table contents.

### Phase USB3-WHC-1 - SS Hub Characteristics Bit Matrix

- NEW `tables/ss_hub_characteristics_bit_matrix.yaml`: 5 entries covering USB 3.x
  wHubCharacteristics bit groups (version 0.1, spec_family: usb3, verified_gate: PARTIAL).
  - `usb3_ss_whc_power_switching` (bits[1:0]): Logical Power Switching Mode — verified
  - `usb3_ss_whc_compound_device` (bit[2]): Compound Device flag — verified
  - `usb3_ss_whc_over_current_mode` (bits[4:3]): Over-Current Protection Mode — verified
  - `usb3_ss_whc_port_indicators` (bit[5]): Port Indicators Supported — verified
  - `usb3_ss_whc_reserved_high` (bits[15:6]): Reserved boundary — permanent reviewed
  Key USB 3.x difference: NO TT Think Time bits (USB 3.x hubs have no Transaction Translator);
  Port Indicators at bit[5] (not bit[7] as in USB 2.0); reserved range bits[15:6] (not bits[15:8]).
  Source: USB 3.2 §10.14.2 Table 10-10 (wHubCharacteristics for SuperSpeed Hub).
- NEW `scripts/validate_ss_hub_characteristics_bit_matrix.py`: R1–R8 structural validator;
  ALLOWLIST_VERIFIED_IDS = 4 ids; EXPECTED_ENTRY_IDS = 5 ids.
- 4 evidence packets in `evidence/entry_verification_packets/usb3/` (ss_whc_*.yaml):
  `verification_scope.claim: bit_group_name_value_encoding_identity_only`.
- USB 3.x authority_surface: tracked=53, verified=48, reviewed=5, evidence_packets=48
  (WHC adds 5 tracked entries: 4 verified + 1 reviewed, 4 new evidence packets).

Claim ceiling: bit_group_name_value_encoding_identity_only. Does not claim wHubCharacteristics
runtime behavior, power switching firmware implementation, or OCP hardware behavior.

### Phase USB3-IEP-1 - SS Hub Interrupt Endpoint Matrix

- NEW `tables/ss_hub_interrupt_endpoint_matrix.yaml`: 4 entries covering USB 3.x SuperSpeed
  hub interrupt endpoint descriptor fields (version 0.1, spec_family: usb3, verified_gate: PARTIAL).
  All 4 entries: `claim_level: verified`.
  - `usb3_ss_hub_ep_bEndpointAddress`: 0x81 (IN, endpoint 1) — verified
  - `usb3_ss_hub_ep_bmAttributes`: 0x03 (Interrupt transfer type) — verified
  - `usb3_ss_hub_ep_wMaxPacketSize`: 1 byte (1 bit per port + hub status) — verified
  - `usb3_ss_hub_ep_bInterval`: 2^(bInterval-1) × 125 μs; bInterval range 1–16 — verified
  USB 3.x bInterval encoding: microframe-based (same as USB 2.0 HS), NOT direct ms.
  Source: USB 3.2 §10.14.2 and §10.15.1.
- NEW `scripts/validate_ss_hub_interrupt_endpoint_matrix.py`: R1–R8 structural validator;
  ALLOWLIST_VERIFIED_IDS = all 4 field ids; uses field_id as key.
- 4 evidence packets in `evidence/entry_verification_packets/usb3/` (ss_iep_*.yaml):
  `verification_scope.claim: field_identity_constraint_encoding_only`.

Claim ceiling: field_identity_constraint_encoding_only. Does not claim interrupt endpoint
runtime behavior, xHCI interrupt scheduling, or hub status change reporting behavior.

### Phase MANIFEST-UPDATE-2 - Manifest v0.3 + 15-Table Re-baseline

- `exports/hub_governed_surface_manifest.yaml` → v0.3: added entries 14 and 15
  (usb3_ss_hub_characteristics_bit_matrix, usb3_ss_hub_interrupt_endpoint_matrix).
  `authority_surface.usb3` updated: tracked=44→53, verified=40→48, reviewed=4→5,
  evidence_packets=40→48. USB3 section comment updated to "(6 tables)".
- `evidence/table_fingerprint_baseline.jsonl`: re-baselined for all 15 tables.
  Fingerprint check PASSES: 15 tables, 0 drift.
- `scripts/smoke_consumer_integration_fixtures.py`: updated `fingerprint_no_drift`
  case to expect 15 tables (was 13). Consumer smoke PASSES: 3/3 cases.
- `specs/verification_status.md` + EN: added USB3-WHC-1 and USB3-IEP-1 rows to
  USB 3.x stats table; totals updated to tracked=53, verified=48, reviewed=5;
  evidence packets updated to 48; added new sections for each matrix.
  CI gate example updated (12→15 tables). Export Contract table updated (12→15).
- `README.md`: updated USB3 stats (tracked 44→53, verified 40→48, tables 13→15,
  evidence packets 40→48).

Claim ceiling: manifest_structural_integrity_only; does not re-verify table contents.

### Phase USB3-WIKI-CORE - SS Hub Core Wiki Pages (6 Topic Pairs ZH+EN)

All pages: `claim_level: inferred`, `semantic_verification_claimed: false`,
`spec_family: usb3`, `last_reviewed: 2026-06-08`.

- NEW `specs/usb3/ss_feature_selectors.md` + EN: 6 SS-only port feature selectors table
  (PORT_U1_ENABLE/U2_ENABLE/U1_TIMEOUT/U2_TIMEOUT/REMOTE_WAKE_MASK/BH_PORT_RESET),
  U1/U2 LPM explanations, Verified Gate note linking to ss_feature_selector_matrix.
- NEW `specs/usb3/ss_hub_characteristics.md` + EN: wHubCharacteristics bit layout table,
  USB3 vs USB2 diff table (NO TT Think Time bits, Port Indicators at bit[5]).
  Cross-link to governed ss_hub_characteristics_bit_matrix.
- NEW `specs/usb3/ss_hub_interrupt_endpoint.md` + EN: 4 descriptor fields,
  bInterval microframe encoding table, wMaxPacketSize formula.
  Cross-link to governed ss_hub_interrupt_endpoint_matrix.
- NEW `specs/usb3/ss_hub_power.md` + EN: power control modes, U1/U2/U3 states,
  bPwrOn2PwrGood, OC protection, USB3 vs USB2 diff table.
- NEW `specs/usb3/ss_hub_enumeration.md` + EN: 8-step enumeration sequence,
  SET_HUB_DEPTH mandatory, USB3 vs USB2 diff table.
- NEW `specs/usb3/ss_port_state_machine.md` + EN: port states table, Warm/Hot Reset types,
  PORT_LINK_STATE 12-value encoding table, PORT_SPEED table.

No new governed matrix entries. No new verified claims beyond existing matrices.

Claim ceiling: reviewed reference summary only; inferred from spec reading.

### Phase USB3-WIKI-EXT - SS Hub Extended Wiki Pages (7 Topic Pairs ZH+EN)

All pages: `claim_level: inferred`, `semantic_verification_claimed: false`,
`spec_family: usb3`, `last_reviewed: 2026-06-08`.

- NEW `specs/usb3/ss_lpm.md` + EN: U0-U3 states table, U1/U2 entry/exit, timeout selectors,
  U3 suspend, wPortStatus LPM bits.
- NEW `specs/usb3/ss_signaling.md` + EN: SS differential serial (TX+/TX-/RX+/RX-),
  LFPS uses, Gen1 (5 Gbps, 8b10b) vs Gen2 (10 Gbps, 128b132b) diff table.
- NEW `specs/usb3/ss_standard_device_requests.md` + EN: retained USB2 requests table,
  U1/U2/LTM feature selectors, new descriptor types (BOS 0x0F, SSP 0x10, SS Hub 0x2A).
- NEW `specs/usb3/ss_hub_compound_device.md` + EN: wHubCharacteristics bit[2],
  compound device definition, USB3 vs USB2 encoding diff.
- NEW `specs/usb3/ss_packet_types.md` + EN: LMP/TP/DP/ITP overview table,
  TP subtypes (ACK/NRDY/ERDY/STATUS/STALL/DEV_NOTIFICATION/PING/PING_RESPONSE).
- NEW `specs/usb3/ss_transactions.md` + EN: point-to-point full-duplex model,
  NRDY/ERDY flow control, no TT, hub packet routing role.
- NEW `specs/usb3/ss_test_modes.md` + EN: Compliance Mode (PORT_LINK_STATE=0xA),
  Loopback (0xB), PORT_LINK_STATE mapping table, USB2 vs USB3 test mode diff table.

No new governed matrix entries. No new verified claims.

Claim ceiling: reviewed reference summary only; inferred from spec reading.

### Phase EXPORT-CONTRACT-1.1 - Feature Selector Expansion Manifest + Fingerprint Re-baseline

- `exports/hub_governed_surface_manifest.yaml` v0.2: added 13th governed table
  (`usb3_ss_feature_selector_matrix`, state=partial_verified, verified=6, reviewed=0,
  verified_scope=selector_name_value_applicability_recipient_identity_only).
  `authority_surface.usb3` updated: state=partial_verified_expansion,
  tracked=44 (was 38), verified=40 (was 34), reviewed=4, evidence_packets=40 (was 34).
  `manifest_version` bumped to "0.2".
- `scripts/validate_hub_governed_surface_manifest.py`: added `partial_verified`
  to VALID_STATES (previously only freeze and matrix_level_closeout).
- `evidence/table_fingerprint_baseline.jsonl`: re-baselined for all 13 tables.
  Fixed 5 stale USB 2.0 table hashes (class_request, feature_selector,
  port_status_bit, interrupt_endpoint, standard_device_request) that had
  accumulated since EXPORT-CONTRACT-1.0.
  Fingerprint check PASSES: 13 tables, 0 drift.
- `scripts/smoke_consumer_integration_fixtures.py`: updated `fingerprint_no_drift`
  case to expect 13 tables (was 12). Consumer smoke PASSES: 3/3 cases.
- No USB 2.0 table changes. USB 2.0 freeze unaffected: tracked=151, verified=105,
  reviewed=46.
- USB 3.x matrix-level closeout unaffected: tracked=38, verified=34, reviewed=4.
- Feature selector expansion now included in export contract surface.

Claim ceiling: manifest_structural_integrity_only; does not re-verify table contents.
Authority ceiling: governed_matrix_identity_and_boundary_reference_only.

### Phase REFERENCE-CONSUMER-SMOKE-1 - Manifest v0.3 Consumer Reference Smoke

- NEW `scripts/smoke_manifest_consumer_reference.py`: standalone consumer smoke
  template for downstream repos adopting manifest v0.3.
  Asserts 5 cases (pure YAML read, no subprocess):
  1. `manifest_version_check`: manifest_version == "0.3"
  2. `table_count_check`: governed_tables count == 15
  3. `usb2_stats_check`: USB2 tracked=151 / verified=105 / reviewed=46
  4. `usb3_stats_check`: USB3 tracked=53 / verified=48 / reviewed=5
  5. `table_paths_exist_check`: all 15 governed table paths exist on disk
  All 5 cases PASS against the live repo.
- Accepts `--repo-root` argument: consuming repos pass their pinned checkout path.
- Auto-detects repo root from script location for in-repo use.
- Outputs JSON receipt to `evidence/validation_receipts/consumer_reference_smoke/`.
- Docstring documents the adaptation workflow for consuming repos
  (pin commit 537319e, copy script, adapt path, assert exit 0).

Claim ceiling:
- CAN establish: reference manifest v0.3 is structurally present and passes
  boundary assertions at the pinned checkout.
- CANNOT establish: consuming repo CI integrated, firmware behavior compliance,
  USB-IF certification readiness, LTSSM/xHCI/electrical validation, or
  reviewed entries as equivalent to verified.

Note: This is a reference template. CONSUMER-CI-2 (actual consuming repo
adoption) is a separate phase that requires naming a specific consuming repo
and running smoke from within that repo's CI context.

### Phase USB3-WIKI-FULL-1 - SS Direct Parity Wiki Pages (7 Topic Pairs ZH+EN)

All pages: `claim_level: inferred`, `semantic_verification_claimed: false`,
`spec_family: usb3`, `last_reviewed: 2026-06-08`.

New pages (7 ZH in `specs/usb3/`, 7 EN in `specs/en/usb3/`):
- `ss_hub_device_class`: bDeviceProtocol=0x03 (SS hub, no TT), bcdUSB, protocol values table
- `ss_hub_configuration`: BOS required, SS Endpoint Companion required, no alternate settings
- `ss_standard_descriptors`: Descriptor types table (0x0F BOS, 0x2A SS Hub, 0x30 SS Endpoint Companion), bMaxPacketSize0=9 (exponent encoding)
- `ss_usb_device_states`: Same 6 §9.1 states; U0–U3 overlay; SET_HUB_DEPTH mandatory; >2ms suspend threshold
- `ss_usb_transfer_types`: Same 4 types; NRDY/ERDY flow control; Control=512B; Bulk max=1024B; ITP; no split transactions
- `ss_port_indicators`: wHubCharacteristics bit[5] (not bit[7]); same 4 LED states; governed linkage to WHC matrix
- `ss_hub_power_budget`: 900mA/port self-powered (vs 500mA USB 2.0); 150mA bus-powered (vs 100mA); bHubContrCurrent/bMaxPower/bPwrOn2PwrGood same encoding

Updated `.vitepress/config.ts`:
- Added 7 labels to ZH_LABELS and EN_LABELS
- `zhUsb3Items`: 16 → 23 items
- `enUsb3Items`: 16 → 23 items

Claim ceiling: reviewed reference summary only; inferred from spec reading.
No new governed matrices. No new evidence packets. No new verified claims.
Does not claim USB 3.x wiki parity with USB 2.0 is complete.

### Phase USB3-WIKI-FULL-2 - SS Difference and Shared Reference Pages

All pages: `claim_level: inferred`, `semantic_verification_claimed: false`,
`spec_family: usb3` (where applicable), `last_reviewed: 2026-06-08`.

New pages (2 × ZH+EN = 4 new files):
- `ss_no_transaction_translator`: SS hub has no TT; bounded contrast with USB 2.0 TT architecture;
  `bDeviceProtocol=0x03` vs 0x01/0x02; SS Hub Descriptor type 0x2A vs 0x29; wHubCharacteristics diff
- `ss_speed_detection`: LFPS + TSEQ vs USB 2.0 HS Chirp; LTSSM scope boundary explicit;
  no LFPS runtime timing or electrical claims

Updated existing pages:
- `ss_transactions` (ZH+EN): added "Split Transaction Does Not Apply in SS Context" section
  with cross-link to ss_no_transaction_translator
- `glossary` (ZH+EN): added "USB 3.x / SuperSpeed Terms" section (SS/SSP/BOS/LPM/U0-U3/LFPS/TSEQ/ITP/NRDY-ERDY/SET_HUB_DEPTH);
  updated frontmatter usb_versions/source_refs to include usb_3_2
- `version_source_map` (ZH+EN): updated USB 3.2 row to reflect governed surface present;
  added "USB 3.2 Governed Surface Summary" table; updated frontmatter
- `escalation_table` (ZH+EN): renamed trigger section to "USB 2.0 Trigger Conditions";
  added "SS (USB 3.x) Trigger Conditions" (SE-01 through SE-05);
  updated Governed Linkage with SS table references; updated frontmatter

Updated `.vitepress/config.ts`:
- Added 2 labels to ZH_LABELS and EN_LABELS
- `zhUsb3Items`: 23 → 25 items
- `enUsb3Items`: 23 → 25 items

Claim ceiling: reviewed reference summary only; inferred from spec reading.
No new governed matrices. No new evidence packets. No new verified claims.
Does not claim USB 3.x wiki surface is complete.

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
- `python scripts\validate_hub_interrupt_endpoint_matrix.py`
- `python scripts\validate_standard_device_request_matrix.py`
- `python scripts\validate_wHubCharacteristics_bit_matrix.py`
- `python scripts\validate_ss_port_status_bit_matrix.py`
- `python scripts\validate_ss_hub_class_request_matrix.py`
- `python scripts\validate_ss_hub_descriptor_matrix.py`
- `python scripts\validate_ss_feature_selector_matrix.py`
- `python scripts\validate_ss_hub_characteristics_bit_matrix.py`
- `python scripts\validate_ss_hub_interrupt_endpoint_matrix.py`
- `python scripts\validate_hub_governed_surface_manifest.py`
- `python scripts\probe_table_fingerprint.py --mode check --manifest exports\hub_governed_surface_manifest.yaml --baseline-in evidence\table_fingerprint_baseline.jsonl`
- `python scripts\smoke_consumer_integration_fixtures.py`
- `python scripts\smoke_manifest_consumer_reference.py`
- `npm.cmd run build`

## USB 2.0 Governed Surface Freeze

USB 2.0 governed reference surface is closed.

The governed matrix scope now tracks 151 entries:
- 105 entry-level verified semantic entries
- 46 reviewed permanent-boundary entries

All remaining reviewed entries are reserved bits or boundary-only placeholders.
No reviewed entry is pending semantic promotion.

Active validators and completed phase history are aligned with the final USB 2.0
governed surface.

## USB 3.x Governed Matrix State

USB 3.x governed matrix and wiki surface has reached Wiki Parity state (Phase USB3-WIKI-EXT).

The six USB 3.x governed tables now track 53 entries across 6 matrices:
- 48 entry-level verified entries (all defined entries across all six matrices)
- 5 reviewed permanent-boundary entries (reserved bits only, not pending promotion)

Governed matrices (6 total):
- SS hub descriptor fields: 9 / 9 verified
- SS hub class requests: 10 / 10 verified
- SS port status/change bits: 15 defined entries verified, 4 reserved boundary reviewed
- SS feature selectors: 6 / 6 verified
- SS wHubCharacteristics bit groups: 4 / 5 entries verified (1 reserved boundary reviewed)
- SS hub interrupt endpoint fields: 4 / 4 verified

Wiki surface (22 topic pairs, ZH + EN):
- CORE topics (6): ss_feature_selectors, ss_hub_characteristics, ss_hub_interrupt_endpoint,
  ss_hub_power, ss_hub_enumeration, ss_port_state_machine
- EXT topics (7): ss_lpm, ss_signaling, ss_standard_device_requests, ss_hub_compound_device,
  ss_packet_types, ss_transactions, ss_test_modes
- FULL-1 direct parity topics (7): ss_hub_device_class, ss_hub_configuration,
  ss_standard_descriptors, ss_usb_device_states, ss_usb_transfer_types,
  ss_port_indicators, ss_hub_power_budget
- FULL-2 difference topics (2): ss_no_transaction_translator, ss_speed_detection

Plus 3 earlier pages (ss_hub_descriptor, ss_port_status_bits, ss_hub_class_requests)
= 25 pages per locale (50 total), exceeding USB 2.0's 28-topic pair depth.

USB 3.x authority_surface: tracked=53, verified=48, reviewed=5, evidence_packets=48.
USB 3.x manifest: 15 governed tables (manifest v0.3).

USB 2.0 freeze remains unchanged at 151 / 105 / 46.

## USB 3.x Feature Selector Expansion (USB3-FS-2 + EXPORT-CONTRACT-1.1 Complete)

Phase USB3-FS-2 and EXPORT-CONTRACT-1.1 are both complete:
- `tables/ss_feature_selector_matrix.yaml` v0.2: 6 SS-only port feature selector
  entries (PORT_U1_ENABLE, PORT_U2_ENABLE, PORT_U1_TIMEOUT, PORT_U2_TIMEOUT,
  PORT_REMOTE_WAKE_MASK, BH_PORT_RESET).
- All 6 entries: `claim_level: verified`, verified gate PARTIAL/allowlist.
- 6 evidence packets in `evidence/entry_verification_packets/usb3/`.
- Included in the unified manifest (13th governed table) and fingerprint baseline.
- Now included in the MANIFEST-UPDATE-2 (v0.3) re-baseline (15 tables total).

### Phase LTSSM-0 — LTSSM Orientation Reference (orientation only, not governed)

**Status:** Phase A complete (2026-06-09).

Added `ss_ltssm.md` (ZH + EN) as an orientation reference for LTSSM state names,
state groups, and high-level transition paths. This is a readability / orientation
layer only.

Also added U-state transition rules to SS port_state_machine.md (ZH + EN), and
Transition Constraints table to USB 2.0 port_state_machine.md (ZH + EN).
Triggered by Hub PM (Yihsun) review gap: "某些state只能從哪裡跳到哪裡，不能跳到那裏".

Claim ceiling: `claim_level: inferred`, `semantic_verification_claimed: false`.
LTSSM-0 does not expand USB 3.x governed matrix statistics.

Included:
- LTSSM state group overview (7 groups)
- High-level transition orientation table (common next-state paths; not normative)
- Hub PORT_LINK_STATE relationship table

Not included (permanent boundaries):
- Complete normative LTSSM transition matrix
- LFPS timing, PHY electrical, equalization behavior
- xHCI/firmware interaction with LTSSM
- USB-IF compliance or interoperability behavior

**Phase B** (Mermaid simplified orientation diagram): deferred. Requires Mermaid
plugin installation. Diagram must be titled "Simplified LTSSM Orientation Diagram",
not "USB3 LTSSM State Machine", to maintain correct claim framing.

---

## Open Work

1. Continue entry-level verification only when narrow evidence packets and gate
   scope are explicit.
2. Keep consuming-repo integration as reference-only; any firmware behavior
   change still belongs in the consuming repo's Standard Escalation Mode.
3. USB 3.x wiki surface has reached 25 pages per locale (50 total), exceeding
   USB 2.0's 28-topic depth. Any further expansion requires explicit scope definition
   and governance approval.
4. CONSUMER-CI-2 (actual consuming repo adoption of manifest v0.3) is deferred
   until a specific consuming firmware repo is identified. Use
   `scripts/smoke_manifest_consumer_reference.py` as the starting template.
5. LTSSM-0 Phase B (Mermaid diagram) deferred. Install `vitepress-plugin-mermaid`
   or equivalent, then create simplified orientation diagram with correct title.
   Do not proceed until claim ceiling and diagram naming policy are confirmed.

## Cannot Claim

- USB 2.0 hub behavior is fully verified.
- All entries are PDF-semantically verified.
- Reviewed coverage is the same as verified coverage.
- This repo can override consuming firmware project facts.
- Fleet governance is enabled.
- Runtime profile validation or response envelope enforcement is active.
- USB 3.x governed matrix surface is equivalent to full USB 3.x spec coverage.
- USB 3.x wiki surface covers the full USB 3.2 specification (it covers reference depth only).
- LTSSM runtime state transitions are verified.
- xHCI port state management or xHCI enumeration behavior is verified.
- SuperSpeed hub firmware compliance truth is established.
- PORT_LINK_STATE or PORT_SPEED verified scope covers any behavioral semantics
  beyond bit range and encoding table identity.
