# Public Spec Boundary Review Receipt

Status: active repository governance contract.

This document defines the structural integrity boundary for a page that is
marked `reviewed` or `cleared` in the public specification inventory. A receipt
can prove that a structured review record is present and that it is bound to
the current page bytes. It cannot prove the reviewer's real-world identity,
the quality of the review, copyrightability, or legal permission to publish.

## Inventory contract

An inventory entry with `review_status: pending` or `review_status: blocked`
does not need a receipt. An entry with `review_status: reviewed` or
`review_status: cleared` must contain only a structured receipt reference:

```yaml
review_receipt:
  path: governance/reviews/example.yaml
```

Inline `review_evidence` text is not an accepted approval surface.

## Receipt schema

The referenced YAML mapping must contain:

```yaml
schema_version: 1
page: specs/en/example.md
decision: approved
review_type: human_boundary_review
reviewer: reviewer-identifier
reviewed_at: "2026-08-28"
content_sha256: <64 lowercase hexadecimal characters>
source_commit: <40 hexadecimal commit SHA>
```

Receipts must live under `governance/reviews/`. The validator checks that the
receipt page exactly matches the inventory page, `decision` is `approved`, the
review type is allowed, the date and identifiers have the expected shape, and
`content_sha256` matches the current page bytes. Editing one byte of the page
invalidates the prior receipt.

`source_commit` records the commit context named by the receipt. This
repository validator does not authenticate the reviewer or independently
verify that commit's authorship.

The current public inventory intentionally keeps all 118 pages at `pending`;
this phase does not create 118 review receipts or mark any page legally clear.
