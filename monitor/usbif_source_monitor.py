#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Dict, Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import yaml


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load_sources(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=True) + "\n")


def load_last_snapshot_by_source(path: Path) -> Dict[str, Dict[str, Any]]:
    if not path.exists():
        return {}
    last: Dict[str, Dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        sid = rec.get("source_id")
        if sid:
            last[sid] = rec
    return last


def fetch(url: str, timeout_sec: int = 30) -> Dict[str, Any]:
    req = Request(url, headers={"User-Agent": "usb-hub-spec-monitor/1.0"})
    try:
        with urlopen(req, timeout=timeout_sec) as resp:
            data = resp.read()
            headers = dict(resp.headers.items())
            return {
                "ok": True,
                "status": getattr(resp, "status", 200),
                "body_hash": sha256_bytes(data),
                "content_length": len(data),
                "etag": headers.get("ETag"),
                "last_modified": headers.get("Last-Modified"),
            }
    except HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e)}
    except URLError as e:
        return {"ok": False, "status": None, "error": str(e)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", required=True)
    parser.add_argument("--snapshots", required=True)
    parser.add_argument("--drift-events", required=True)
    args = parser.parse_args()

    sources_doc = load_sources(Path(args.sources))
    sources = sources_doc.get("sources", [])
    snapshot_path = Path(args.snapshots)
    drift_path = Path(args.drift_events)
    previous = load_last_snapshot_by_source(snapshot_path)
    checked_at = utc_now_iso()

    for src in sources:
        sid = src["id"]
        result = fetch(src["url"])
        rec = {
            "source_id": sid,
            "title": src.get("title"),
            "checked_at": checked_at,
            "url": src["url"],
            "authority_level": src.get("authority_level"),
            "scope": src.get("scope", []),
            "result": "unchanged",
            **result,
        }

        prev = previous.get(sid)
        if prev is not None:
            if (prev.get("status") != rec.get("status")) or (prev.get("body_hash") != rec.get("body_hash")):
                rec["result"] = "changed"
                event = {
                    "event_id": f"drift-{sid}-{checked_at}",
                    "source_id": sid,
                    "detected_at": checked_at,
                    "change_type": "status_or_hash_changed",
                    "previous_status": prev.get("status"),
                    "current_status": rec.get("status"),
                    "previous_hash": prev.get("body_hash"),
                    "current_hash": rec.get("body_hash"),
                    "affected_scopes": src.get("scope", []),
                    "required_action": "review_required",
                }
                append_jsonl(drift_path, event)
        append_jsonl(snapshot_path, rec)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
