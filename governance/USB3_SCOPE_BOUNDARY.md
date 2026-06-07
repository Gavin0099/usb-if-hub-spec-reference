# USB 3.x SuperSpeed Hub Scope Boundary

**Phase**: USB3-0
**Status**: scope boundary only — no governed entries, no wiki pages, no UI changes
**Date established**: 2026-06-07

---

## Purpose

This document defines the candidate scope for a future USB 3.x / SuperSpeed hub
governed reference surface. It does not add any governed entries, evidence
packets, or wiki pages. It establishes the namespace, spec authority, and
non-claim boundaries before any USB 3.x content is authored.

USB 2.0 governed surface remains closed at this boundary point.
See PLAN.md §USB 2.0 Governed Surface Freeze.

---

## Candidate Spec Authority

| Document | Scope |
|---|---|
| USB 3.2 Specification Rev 1.0 (September 2017) | Core SS/SS+ bus protocol, Chapter 10 (Hub Class) |
| USB Hub Class Specification for USB 3.x | Hub descriptor, class requests, port status bits |

No other spec document is in scope for the initial USB 3.x governed surface.

---

## Candidate Governed Surface

The following are **candidates only**; none are tracked entries until USB3-1 or
later phases formally add and gate them.

### SuperSpeed Hub Descriptor

- `bDescLength`, `bDescriptorType` (0x2A), `bNbrPorts`, `wHubCharacteristics`
- `bPwrOn2PwrGood`, `bHubContrCurrent`, `bHubDecLat`
- `wHubDelay`, `DeviceRemovable`

### SS Port Status Bits (wPortStatus / wPortChange)

- `PORT_CONNECTION` (bit 0), `PORT_ENABLE` (bit 1), `PORT_OVER_CURRENT` (bit 3),
  `PORT_RESET` (bit 4), `PORT_LINK_STATE` (bits[8:5]), `PORT_POWER` (bit 9),
  `PORT_SPEED` (bits[12:10]), `PORT_U1_ENABLE` (bit 16), `PORT_U2_ENABLE` (bit 17)
- Change bits: `C_PORT_CONNECTION`, `C_PORT_RESET`, `C_PORT_LINK_STATE`,
  `C_PORT_CONFIG_ERROR`

### SS Feature Selectors (hub-relevant)

- `PORT_U1_TIMEOUT` (0x23), `PORT_U2_TIMEOUT` (0x24)
- `C_PORT_LINK_STATE` (0x19), `C_PORT_CONFIG_ERROR` (0x1E)

### SS Hub Class Requests

- Mostly shared with USB 2.0 family; SS-specific: `SET_HUB_DEPTH` (0x0C),
  `GET_PORT_ERR_COUNT` (0x0D)

---

## Governance Separation Rules

1. USB 3.x governed entries will live in separate tables from USB 2.0 entries.
   No cross-table claim-level inheritance.
2. `claim_level` semantics remain identical to USB 2.0: `verified` requires an
   evidence packet scoped to name/value/position identity only.
3. USB 3.x wiki pages will live under `specs/usb3/` and `specs/en/usb3/`
   (deferred to USB3-1).
4. USB 3.x pages must carry `spec_family: usb3` in frontmatter.
5. USB 2.0 page URLs, labels, sidebar sections, and nav items are not modified
   during USB3-0.

---

## Schema Compatibility

Existing YAML table schemas (`bit_range`, `value_encoding`, `evidence_status`,
`claim_level`) are compatible with USB 3.x entries without modification.
The `wPortStatus` SS bit layout uses wider fields (e.g., bits[8:5] for
PORT_LINK_STATE) which the existing `bit_range` schema already supports.

---

## UI Namespace Plan (deferred to USB3-1)

The following UI changes are **explicitly deferred** and must not be made during
USB3-0:

- Nav Reference dropdown grouping (USB 2.0 Hub / USB 3.x SuperSpeed Hub)
- Sidebar two-section split (USB 2.0 Hub / USB 3.x SuperSpeed Hub)
- Footer version-neutral rewrite
- USB 3.x label dictionary entries

These will be implemented atomically in USB3-1 when the first USB 3.x wiki pages
are ready to ship.

---

## Non-Claims (permanent)

This scope boundary does not and will never claim:

- Full LTSSM (Link Training and Status State Machine) behavioral model
- xHCI host controller interaction or behavior
- USB 3.x electrical, timing, or signal integrity compliance
- USB4 or Thunderbolt hub semantics
- SS+ (USB 3.2 Gen 2) electrical behavior beyond hub descriptor semantics
- USB-IF certification completeness for any USB 3.x device
- Firmware behavior or implementation truth

---

## What Happens Next

USB3-1 will:
1. Create `specs/usb3/` and `specs/en/usb3/`
2. Add the first USB 3.x wiki pages (SS hub descriptor, SS port status bits)
3. Add USB 3.x label dictionary entries to config.ts
4. Split nav and sidebar into USB 2.0 / USB 3.x groups
5. Update footer to version-neutral non-claim
6. Add `scripts/validate_ss_hub_descriptor_matrix.py` if a new governed table is introduced
