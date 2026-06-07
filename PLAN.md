> **Last Updated**: 2026-06-07
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
- `python scripts\probe_table_fingerprint.py --mode check --manifest exports\usb20_hub_class_request_manifest.yaml --baseline-in evidence\table_fingerprint_baseline.jsonl`
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
