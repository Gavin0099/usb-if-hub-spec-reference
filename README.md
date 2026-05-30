# USB-IF Hub Spec Reference

Governed USB hub specification reference and LLM wiki scaffold.

## Purpose

This repository provides controlled reference content from USB-IF hub-related specifications
for consumption by firmware governance contracts.

It does **not** govern firmware behavior. It clarifies standard semantics only.

## Contents

| Document | Spec Section | Description |
|----------|-------------|-------------|
| [specs/hub_descriptor.md](specs/hub_descriptor.md) | 11.23.2.1 | Hub descriptor field definitions |
| [specs/port_status_bits.md](specs/port_status_bits.md) | 11.24.2.7 | Port status and change bit definitions |
| [specs/hub_class_requests.md](specs/hub_class_requests.md) | 11.24.2 | Hub class request semantics |
| [specs/transaction_translator.md](specs/transaction_translator.md) | 11.17–11.18 | TT rules summary |
| [specs/escalation_table.md](specs/escalation_table.md) | — | Standard Escalation trigger table for consuming repos |
| [specs/version_source_map.md](specs/version_source_map.md) | Multi-version | USB 2.0 / 2.1 / 3.2 / 4.0 hub-focused source map |

## Governance Layers

- `contract/`: machine-readable authority, claim, evidence, version, and staleness rules
- `wiki/`: human/LLM knowledge layer with version-scoped pages
- `tables/`: machine-readable structured topic matrices
- `evidence/`: source registry and drift/snapshot logs
- `monitor/`: USB-IF source drift detection scripts/config

## Source Drift Principle

Source monitoring detects **staleness risk** and triggers review.
It does **not** automatically validate semantic correctness or auto-upgrade claims.

## Usage Boundary

This repo may be used to **clarify semantics**. It may **not** be used to override
confirmed project facts in consuming firmware repos.

When a conflict is detected between this spec and a confirmed project fact, the consuming
repo's **Standard Escalation Mode** (AGENTS.md Section 10) must be activated.

## Governance

Adopted from [ai-governance-framework](https://github.com/Gavin0099/ai-governance-framework) v1.2.0.

## Source

Primary source set currently anchors on USB-IF documents, starting from USB 2.0 and expanding to USB 3.2 and USB4 source mapping.
