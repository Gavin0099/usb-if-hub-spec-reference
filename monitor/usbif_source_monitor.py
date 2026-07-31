#!/usr/bin/env python3
"""Observation-only USB-IF source drift monitor.

Reads monitored_sources.yaml, fetches each URL, compares with previous snapshot,
and appends drift events when hash/status changes.

All outputs carry:
  time_bound: true
  observation_only: true
  does_not_change_claim_level: true

Non-goals: no semantic diff, no claim downgrade, no PDF parsing.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE_METADATA = {
    "time_bound": True,
    "observation_only": True,
    "does_not_change_claim_level": True,
}
NETWORK_TIMEOUT = 20
MAX_CONTENT_BYTES = 10_000_000


def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _snapshot_id(source_id: str, checked_at: str) -> str:
    ts = checked_at.replace(":", "").replace("-", "").replace("+", "").replace(".", "")[:17]
    return f"snap-{source_id}-{ts}"


def _event_id(source_id: str, detected_at: str) -> str:
    ts = detected_at.replace(":", "").replace("-", "").replace("+", "").replace(".", "")[:17]
    return f"drift-{source_id}-{ts}"


def _sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _load_sources(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    return doc.get("sources", [])


def _load_last_snapshots(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    last: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        sid = rec.get("source_id")
        if sid:
            last[sid] = rec
    return last


def _load_mock_responses(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _fetch_live(url: str) -> dict[str, Any]:
    # GET is required for a meaningful content hash. HEAD usually returns no
    # body, which previously left content_hash empty.
    req = Request(url, method="GET", headers={"User-Agent": "usb-hub-spec-monitor/1.0"})
    try:
        with urlopen(req, timeout=NETWORK_TIMEOUT) as resp:
            headers = dict(resp.headers.items())
            data = resp.read(MAX_CONTENT_BYTES + 1)
            body_too_large = len(data) > MAX_CONTENT_BYTES
            if body_too_large:
                data = b""
            return {
                "reachable": True,
                "http_status": getattr(resp, "status", 200),
                "content_hash": _sha256_bytes(data) if data else None,
                "content_length": int(headers.get("Content-Length", 0)) or None,
                "etag": headers.get("ETag"),
                "last_modified": headers.get("Last-Modified"),
                "advisory_note": "response body exceeds hash limit" if body_too_large else None,
            }
    except HTTPError as e:
        reachable = e.code in (200, 301, 302, 403, 405, 429)
        return {"reachable": reachable, "http_status": e.code, "content_hash": None,
                "content_length": None, "etag": None, "last_modified": None,
                "advisory_note": f"HTTP {e.code}"}
    except (URLError, Exception) as e:
        return {"reachable": False, "http_status": None, "content_hash": None,
                "content_length": None, "etag": None, "last_modified": None,
                "advisory_note": str(e)}


def _build_snapshot(source: dict, fetch_result: dict, checked_at: str) -> dict[str, Any]:
    sid = source["id"]
    snap_id = _snapshot_id(sid, checked_at)
    return {
        "snapshot_id": snap_id,
        "source_id": sid,
        "checked_at": checked_at,
        "url": source["url"],
        "authority_level": source.get("authority_level"),
        **fetch_result,
        **GOVERNANCE_METADATA,
    }


def _compare(previous: dict, current: dict, source: dict) -> dict[str, Any] | None:
    prev_hash = previous.get("content_hash")
    curr_hash = current.get("content_hash")
    prev_status = previous.get("http_status")
    curr_status = current.get("http_status")
    prev_etag = previous.get("etag")
    curr_etag = current.get("etag")
    prev_last_modified = previous.get("last_modified")
    curr_last_modified = current.get("last_modified")

    changed = (
        (prev_hash != curr_hash)
        or (prev_status != curr_status)
        or (
            prev_etag is not None
            and curr_etag is not None
            and prev_etag != curr_etag
        )
        or (
            prev_last_modified is not None
            and curr_last_modified is not None
            and prev_last_modified != curr_last_modified
        )
    )
    if not changed:
        return None

    if prev_hash != curr_hash:
        change_type = "content_hash_changed"
    elif prev_status != curr_status:
        change_type = "http_status_changed"
    elif prev_etag is not None and curr_etag is not None and prev_etag != curr_etag:
        change_type = "etag_changed"
    else:
        change_type = "last_modified_changed"
    return {
        "event_id": _event_id(source["id"], current["checked_at"]),
        "source_id": source["id"],
        "detected_at": current["checked_at"],
        "change_type": change_type,
        "previous_snapshot_id": previous.get("snapshot_id"),
        "current_snapshot_id": current["snapshot_id"],
        "previous_hash": prev_hash,
        "current_hash": curr_hash,
        "previous_http_status": prev_status,
        "current_http_status": curr_status,
        "previous_etag": prev_etag,
        "current_etag": curr_etag,
        "previous_last_modified": prev_last_modified,
        "current_last_modified": curr_last_modified,
        "affected_scopes": source.get("scope", []),
        "required_action": "review_required",
        **GOVERNANCE_METADATA,
    }


def _append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default=str(ROOT / "monitor" / "monitored_sources.yaml"))
    parser.add_argument("--snapshots", default=str(ROOT / "evidence" / "source_snapshots.jsonl"))
    parser.add_argument("--drift-events", default=str(ROOT / "evidence" / "drift_events.jsonl"))
    parser.add_argument(
        "--skip-network", action="store_true",
        help="skip live HTTP; requires --mock-responses",
    )
    parser.add_argument(
        "--mock-responses",
        help="JSON file mapping source_id → fetch result (used with --skip-network)",
    )
    parser.add_argument("--receipt-out", help="write run summary JSON")
    args = parser.parse_args()

    sources = _load_sources(Path(args.sources))
    snapshot_path = Path(args.snapshots)
    drift_path = Path(args.drift_events)
    previous = _load_last_snapshots(snapshot_path)

    mock_responses: dict[str, Any] = {}
    if args.skip_network:
        if not args.mock_responses:
            print("ERROR: --skip-network requires --mock-responses")
            return 1
        mock_responses = _load_mock_responses(Path(args.mock_responses))

    checked_at = _utc_now_iso()
    new_snapshots = 0
    new_drift_events = 0
    advisories: list[str] = []

    for source in sources:
        sid = source["id"]

        if args.skip_network:
            fetch_result = mock_responses.get(sid, {
                "reachable": False,
                "http_status": None,
                "content_hash": None,
                "content_length": None,
                "etag": None,
                "last_modified": None,
                "advisory_note": "not in mock_responses",
            })
        else:
            fetch_result = _fetch_live(source["url"])

        if not fetch_result.get("reachable", False):
            note = fetch_result.get("advisory_note", "unreachable")
            advisories.append(f"{sid}: {note} (advisory only, no drift event)")

        snapshot = _build_snapshot(source, fetch_result, checked_at)
        _append_jsonl(snapshot_path, snapshot)
        new_snapshots += 1

        prev = previous.get(sid)
        if prev is not None and fetch_result.get("reachable", False):
            event = _compare(prev, snapshot, source)
            if event:
                _append_jsonl(drift_path, event)
                new_drift_events += 1

    receipt: dict[str, Any] = {
        "monitor": "usbif_source_monitor.py",
        "authority_ceiling": "drift_observation_only",
        "note": (
            "Drift events record observation only. "
            "does_not_change_claim_level=true. Manual review required on drift."
        ),
        "checked_at": checked_at,
        "skip_network": args.skip_network,
        "sources_checked": len(sources),
        "new_snapshots": new_snapshots,
        "new_drift_events": new_drift_events,
        "advisories": advisories,
        **GOVERNANCE_METADATA,
    }

    if args.receipt_out:
        rpath = Path(args.receipt_out)
        rpath.parent.mkdir(parents=True, exist_ok=True)
        rpath.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    print(f"Monitor run complete: {new_snapshots} snapshots, {new_drift_events} drift events")
    if advisories:
        print(f"- {len(advisories)} advisory note(s) (unreachable sources):")
        for a in advisories:
            print(f"  ~ {a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
