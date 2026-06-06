"""
Validates tables/standard_device_request_matrix.yaml structure.

Rules:
  R1  matrix_id == usb20_standard_device_request_matrix
  R2  All request_id values are unique
  R3  All entries have request_name
  R4  All entries have recipient
  R5  claim_level in {reviewed, inferred, verified}
  R6  evidence_status in {reviewed, inferred, verified}
  R7  source_refs is a non-empty list
  R8  setup block is present with bmRequestType, bRequest, wValue, wIndex, wLength
  R9  All 12 expected hub-relevant standard requests are present
"""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = ROOT / "tables" / "standard_device_request_matrix.yaml"

VALID_CLAIM_LEVELS = {"reviewed", "inferred", "verified"}
VALID_EVIDENCE_STATUSES = {"reviewed", "inferred", "verified"}
REQUIRED_SETUP_FIELDS = {"bmRequestType", "bRequest", "wValue", "wIndex", "wLength"}

EXPECTED_REQUEST_IDS = {
    "usb20_std_get_status_device",
    "usb20_std_get_status_interface",
    "usb20_std_get_status_endpoint",
    "usb20_std_clear_feature_device",
    "usb20_std_clear_feature_endpoint",
    "usb20_std_set_feature_device",
    "usb20_std_set_address",
    "usb20_std_get_descriptor",
    "usb20_std_get_configuration",
    "usb20_std_set_configuration",
    "usb20_std_get_interface",
    "usb20_std_set_interface",
}


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    if not MATRIX_PATH.exists():
        fail(f"Matrix file not found: {MATRIX_PATH}")

    with open(MATRIX_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # R1
    matrix_id = data.get("matrix_id", "")
    if matrix_id != "usb20_standard_device_request_matrix":
        fail(f"R1: matrix_id mismatch: {matrix_id!r}")

    entries = data.get("entries", [])
    if not entries:
        fail("No entries found")

    # R2
    seen_ids = set()
    for e in entries:
        rid = e.get("request_id", "")
        if rid in seen_ids:
            fail(f"R2: duplicate request_id: {rid!r}")
        seen_ids.add(rid)

    for e in entries:
        rid = e.get("request_id", "<unknown>")

        # R3
        if not e.get("request_name"):
            fail(f"R3: missing request_name on {rid!r}")

        # R4
        if not e.get("recipient"):
            fail(f"R4: missing recipient on {rid!r}")

        # R5
        cl = e.get("claim_level", "")
        if cl not in VALID_CLAIM_LEVELS:
            fail(f"R5: invalid claim_level {cl!r} on {rid!r}")

        # R6
        es = e.get("evidence_status", "")
        if es not in VALID_EVIDENCE_STATUSES:
            fail(f"R6: invalid evidence_status {es!r} on {rid!r}")

        # R7
        refs = e.get("source_refs", [])
        if not refs:
            fail(f"R7: missing source_refs on {rid!r}")

        # R8
        setup = e.get("setup", {})
        missing = REQUIRED_SETUP_FIELDS - set(setup.keys())
        if missing:
            fail(f"R8: setup block missing fields {missing} on {rid!r}")

    # R9
    missing_ids = EXPECTED_REQUEST_IDS - seen_ids
    if missing_ids:
        fail(f"R9: missing expected request_ids: {missing_ids}")

    print("Standard device request matrix validation PASSED")
    print(f"- matrix_id: {matrix_id}")
    print(f"- entries: {len(entries)}")
    print(f"- all {len(EXPECTED_REQUEST_IDS)} expected request entries present")


if __name__ == "__main__":
    main()
