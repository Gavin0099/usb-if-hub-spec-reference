---
title: USB 3.2 Version Scope
topic: version_scope
usb_versions:
  - usb_3_2
authority_required: official_index
claim_level: inferred
source_refs:
  - usb32_spec_page
status: review_required
last_reviewed: 2026-06-03
---

# USB 3.2

This legacy version page is an orientation note only.

Use the canonical version-scope surface for current repo-local boundaries:

- `specs/version_source_map.md`
- `specs/en/version_source_map.md`

## Claim Boundary

- USB 3.2 is treated as SuperSpeed generation context, not as a direct replacement for USB 2.0 hub semantics.
- Do not let compliance/test procedures replace base normative field definitions.
- Preserve separation between USB 2.0 hub function semantics and SuperSpeed hub deltas unless section-level evidence connects them.
- This legacy page must not be used to override `specs/` pages, governed YAML tables, or consuming-repo project facts.
