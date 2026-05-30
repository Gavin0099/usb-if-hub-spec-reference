# Enumd Influence (Design-Level Only)

## Purpose

This document records design patterns adopted from Enumd for this repository.
It is a design influence note, not an implementation dependency.

## What We Adopt

1. Observable uncertainty:
   Signals must carry confidence/state fields instead of hiding uncertainty.
2. Evidence-first posture:
   Claims require explicit source, authority, and status metadata.
3. Layer separation:
   Source observation, claim formation, and governance verdict are separate layers.
4. Machine-checkable invariants:
   Key governance assumptions must be testable as explicit rules.
5. Drift-aware governance:
   Source change detection triggers review workflow, not auto-truth promotion.

## What We Explicitly Do Not Adopt

- Notion-specific adapters or APIs.
- Enumd runtime extraction pipeline (`scripts/export.ts` and related runtime flow).
- Pilot ledger/session accounting workflows.
- Full Enumd CI/governance stack in this step.

## Boundary Statement

Enumd is treated as a governance pattern reference.
This repository does not import Enumd as a submodule or runtime dependency.

## First Invariant Candidates

1. `normative_claim_without_normative_source == 0`
2. `usb21_standalone_base_claim == 0`
3. `usb4_hub_equivalence_claim_without_boundary_evidence == 0`
4. `unresolved_source_drift AND claim_level in [normative, verified] == invalid`
5. `total_claims == normative + verified + inferred + provisional + draft + rejected`
6. `verified_claim_with_section_anchor_missing == 0`

## Non-Goals for This Step

- No runtime extraction implementation.
- No monitor-to-validator integration.
- No table extraction expansion.
- No CI enforcement in this change set.
