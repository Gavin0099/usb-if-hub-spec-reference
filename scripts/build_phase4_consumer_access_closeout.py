#!/usr/bin/env python3
"""Build Phase 4 consumer access closeout artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "exports" / "usb20_hub_class_request_manifest.yaml"
OUT_JSON = ROOT / "evidence" / "validation_receipt_phase4_consumer_access_closeout.json"
OUT_MD = ROOT / "docs" / "phase4_consumer_access_closeout.md"


def run_validator(cmd: list[str]) -> str:
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return "pass" if result.returncode == 0 else "fail"


def run_validators(cmds: list[list[str]]) -> str:
    return "pass" if all(run_validator(cmd) == "pass" for cmd in cmds) else "fail"


def main() -> int:
    manifest_doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    governed_tables = manifest_doc.get("governed_tables", [])

    table_validators = {
        "usb_hub_class_request_matrix": [
            ["python", "scripts/validate_class_request_coverage.py", "--matrix", "tables/class_request_matrix.yaml"]
        ],
        "usb_hub_feature_selector_matrix": [
            ["python", "scripts/validate_feature_selector_matrix.py", "--matrix", "tables/feature_selector_matrix.yaml"]
        ],
        "usb20_hub_port_status_bit_matrix": [
            ["python", "scripts/validate_port_status_bit_matrix.py", "--matrix", "tables/port_status_bit_matrix.yaml"],
            [
                "python",
                "scripts/validate_entry_verification_gate.py",
                "--matrix",
                "tables/port_status_bit_matrix.yaml",
                "--packet-dir",
                "evidence/entry_verification_packets",
            ],
        ],
    }

    table_rows = []
    for entry in governed_tables:
        table_id = entry.get("id", "")
        table_path = entry.get("path", "")
        cmd = table_validators.get(table_id)
        status = run_validators(cmd) if cmd else "unknown"
        table_rows.append(
            {
                "id": table_id,
                "path": table_path,
                "validator": (", ".join(cmd_item[1] for cmd_item in cmd) if cmd else "unknown"),
                "status": status,
            }
        )

    manifest_status = run_validator(
        [
            "python",
            "scripts/validate_usb20_hub_class_request_manifest.py",
            "--manifest",
            "exports/usb20_hub_class_request_manifest.yaml",
        ]
    )

    closeout = {
        "phase": "Phase 4",
        "status": "done",
        "claim": "consumer_discovered_governed_table_access_gaps_closed",
        "claim_ceiling": "machine_readable_namespace_and_access_contract_only",
        "semantic_verification_claimed": False,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "governed_tables": table_rows,
        "manifest_contract": {
            "path": "exports/usb20_hub_class_request_manifest.yaml",
            "validator": "scripts/validate_usb20_hub_class_request_manifest.py",
            "status": manifest_status,
        },
        "non_claims": [
            "USB 2.0 semantic behavior verification",
            "PDF page-level extraction completeness",
            "SET_FEATURE/CLEAR_FEATURE behavioral transition validation",
            "GET_STATUS response semantic completeness",
            "full USB 2.0 hub compliance",
        ],
    }

    OUT_JSON.write_text(json.dumps(closeout, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    md_lines = [
        "# Phase 4 Consumer Access Closeout",
        "",
        "- Status: DONE",
        "- Claim: consumer_discovered_governed_table_access_gaps_closed",
        "- Claim ceiling: machine_readable_namespace_and_access_contract_only",
        "- Semantic verification claimed: false",
        "",
        "## Governed Tables",
    ]
    for row in table_rows:
        md_lines.append(f"- `{row['id']}` -> `{row['path']}` | validator `{row['validator']}` | status `{row['status']}`")
    md_lines.extend(
        [
            "",
            "## Manifest Contract",
            f"- `exports/usb20_hub_class_request_manifest.yaml` | validator `scripts/validate_usb20_hub_class_request_manifest.py` | status `{manifest_status}`",
            "",
            "## Non-Claims",
        ]
    )
    md_lines.extend([f"- {n}" for n in closeout["non_claims"]])
    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    all_pass = manifest_status == "pass" and all(r["status"] == "pass" for r in table_rows)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
