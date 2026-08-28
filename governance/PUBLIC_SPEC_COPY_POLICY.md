# Public Spec Copy Policy

Status: active repository governance gate.

This policy defines how this repository may publish an independently authored
engineering reference based on USB specifications. It is a content-process
boundary, not a legal opinion and not a substitute for review by the rights
holder or qualified counsel.

## Boundary

The repository may organize protocol names, constants, field names, bit
positions, request identifiers, and independently written engineering
summaries. The official USB specifications remain the authoritative source for
normative requirements. This repository must not become a sequential or
substitutive HTML reproduction of an official specification.

## MUST NOT

- reproduce full specification sections;
- copy specification paragraphs verbatim;
- reproduce original figures;
- reproduce original diagrams;
- reproduce large original tables;
- reconstruct the complete specification sequentially;
- describe this repository as issued, affiliated with, endorsed by, or
  certified by USB Implementers Forum, Inc.;
- use a repository-wide license statement that purports to license third-party
  standards, trademarks, or other rights held by their owners.

## MAY

- state protocol constants;
- state field names;
- state bit positions;
- state request IDs;
- summarize semantics in original wording;
- create independently designed comparison tables;
- cite specification section or table anchors;
- explain engineering implications while preserving the reference claim
  boundary.

## Attribution and authority

Public pages must identify the site as an independent, unofficial engineering
reference and state that it is not affiliated with or endorsed by USB
Implementers Forum, Inc. Page-level source scope should identify the relevant
specification and section where a normative-looking claim is made. Public
pages must link users to the official USB-IF source for normative requirements.

Official entry points:

- [USB 2.0 Specification — USB-IF Document Library](https://www.usb.org/document-library/usb-20-specification)
- [USB-IF Document Library](https://www.usb.org/document-library)

Specification names, trademarks, and associated rights remain with their
respective rights holders. A disclaimer clarifies affiliation and authority;
it does not grant permission to reproduce protected material.

## Licensing boundary

Only repository-authored material for which the owner has chosen a license may
be licensed by this repository. Third-party standards and trademarks are not
licensed by this repository. Do not add a blanket statement such as “MIT
License — everything in this repository”. When a file-specific license is
chosen later, it must identify the covered material and preserve this
third-party-rights boundary.

## Review gate

Before merging a new or materially expanded public reference page, the author
must confirm:

1. the page is an independently authored summary or structure, not a copied
   section, figure, diagram, or large table;
2. the page includes a source scope or source-map link appropriate to its
   claims;
3. the page does not imply USB-IF affiliation, endorsement, certification, or
   authority for project-specific firmware behavior;
4. any uncertain boundary is marked for review and is not promoted by the
   structural validator into a legal or semantic approval.

`validate_public_spec_copy_policy.py` verifies that this policy and its public
authority anchors remain structurally present. It does not detect plagiarism,
decide copyrightability, or prove legal compliance.
