#!/usr/bin/env python3
"""LLM wiki QA probe — observation-only.

Authority ceiling: hub_class_request_wiki_qa_observation_only

Reads a wiki page and a QA spec (YAML), sends each question to an LLM
with the page content as context, and checks whether expected keywords
appear in each answer. Emits observation-only receipts.

This probe:
  - does NOT claim USB 2.0 semantic correctness
  - does NOT upgrade claim_level on any page or table
  - is NOT a required CI gate (advisory only)
  - exits 0 even if all answers miss expected keywords (observation only)
  - exits 0 (SKIPPED) if ANTHROPIC_API_KEY is not set or anthropic package
    is not installed

Rules (hard errors — cause exit 1):
  E1  wiki page file must exist
  E2  QA spec file must exist and be parseable

QA result codes (advisory — never cause exit 1):
  MATCH   all expected keywords found in LLM response (or any, if match_any=true)
  MISS    expected keywords not satisfied
  ERROR   LLM call failed for this question
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]

GOVERNANCE_METADATA = {
    "time_bound": True,
    "observation_only": True,
    "does_not_change_claim_level": True,
}

SYSTEM_PROMPT = (
    "You are a technical documentation assistant. "
    "Answer questions based only on the provided wiki page content. "
    "Be concise. If the answer is not in the page, say so explicitly."
)


def _call_llm(client: Any, model: str, page_text: str, question: str) -> str:
    """Send question + page context to LLM and return response text."""
    response = client.messages.create(
        model=model,
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Wiki page content:\n\n{page_text}\n\n"
                    f"---\n\nQuestion: {question}"
                ),
            }
        ],
    )
    return response.content[0].text


def _check_keywords(
    response: str, keywords: list[str], match_any: bool
) -> tuple[bool, list[str], list[str]]:
    lower = response.lower()
    found = [k for k in keywords if k.lower() in lower]
    missing = [k for k in keywords if k.lower() not in lower]
    matched = (len(found) > 0) if match_any else (len(missing) == 0)
    return matched, found, missing


def _load_qa_spec(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _write_receipt(receipt_out: str | None, receipt: dict) -> None:
    if not receipt_out:
        return
    rp = Path(receipt_out) if Path(receipt_out).is_absolute() else ROOT / receipt_out
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="LLM wiki QA probe (observation-only)."
    )
    parser.add_argument("--page", required=True, help="Wiki page markdown file")
    parser.add_argument("--qa-spec", required=True, help="QA spec YAML file")
    parser.add_argument(
        "--model", default="claude-haiku-4-5-20251001",
        help="Anthropic model ID (default: claude-haiku-4-5-20251001)"
    )
    parser.add_argument("--receipt-out", help="Write receipt JSON to this path")
    args = parser.parse_args()

    page_path = Path(args.page) if Path(args.page).is_absolute() else ROOT / args.page
    qa_path = Path(args.qa_spec) if Path(args.qa_spec).is_absolute() else ROOT / args.qa_spec

    errors: list[dict] = []
    if not page_path.exists():
        errors.append({"code": "E1_PAGE_NOT_FOUND", "message": f"page not found: {page_path}"})
    if not qa_path.exists():
        errors.append({"code": "E2_QA_SPEC_NOT_FOUND", "message": f"QA spec not found: {qa_path}"})

    if errors:
        receipt = {
            "probe": "probe_wiki_qa.py",
            "authority_ceiling": "hub_class_request_wiki_qa_observation_only",
            "result": "ERROR",
            "wiki_page": str(page_path),
            "errors": errors,
            **GOVERNANCE_METADATA,
        }
        _write_receipt(args.receipt_out, receipt)
        for e in errors:
            print(f"[ERROR] {e['code']}: {e['message']}")
        return 1

    page_text = page_path.read_text(encoding="utf-8")
    try:
        qa_spec = _load_qa_spec(qa_path)
    except Exception as exc:
        print(f"[ERROR] E2_QA_SPEC_PARSE_ERROR: {exc}")
        return 1

    # Check for API key and package
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    try:
        import anthropic as _anthropic
        anthropic_available = True
    except ImportError:
        anthropic_available = False

    if not api_key or not anthropic_available:
        skip_reasons = []
        if not api_key:
            skip_reasons.append("ANTHROPIC_API_KEY env var not set")
        if not anthropic_available:
            skip_reasons.append("anthropic package not installed (pip install anthropic)")
        skip_msg = "; ".join(skip_reasons)
        receipt = {
            "probe": "probe_wiki_qa.py",
            "authority_ceiling": "hub_class_request_wiki_qa_observation_only",
            "result": "SKIPPED",
            "skip_reason": skip_msg,
            "wiki_page": str(
                page_path.relative_to(ROOT) if page_path.is_relative_to(ROOT) else page_path
            ),
            "qa_spec": str(
                qa_path.relative_to(ROOT) if qa_path.is_relative_to(ROOT) else qa_path
            ),
            "model": args.model,
            **GOVERNANCE_METADATA,
        }
        _write_receipt(args.receipt_out, receipt)
        print(f"Wiki QA probe SKIPPED: {skip_msg}")
        return 0

    client = _anthropic.Anthropic(api_key=api_key)
    questions = qa_spec.get("questions", [])
    results: list[dict] = []

    for q in questions:
        qid = q.get("id", "?")
        question_text = q.get("question", "").strip()
        expected_keywords = q.get("expected_keywords", [])
        match_any = q.get("match_any", False)

        try:
            response_text = _call_llm(client, args.model, page_text, question_text)
        except Exception as exc:
            results.append({
                "id": qid,
                "question": question_text,
                "result": "ERROR",
                "error": str(exc)[:200],
                "response_excerpt": "",
            })
            continue

        matched, found, missing = _check_keywords(response_text, expected_keywords, match_any)
        results.append({
            "id": qid,
            "question": question_text,
            "result": "MATCH" if matched else "MISS",
            "response_excerpt": response_text[:300],
            "expected_keywords": expected_keywords,
            "match_any": match_any,
            "found_keywords": found,
            "missing_keywords": missing,
        })

    match_count = sum(1 for r in results if r["result"] == "MATCH")
    miss_count = sum(1 for r in results if r["result"] == "MISS")
    error_count = sum(1 for r in results if r["result"] == "ERROR")
    total = len(questions)

    receipt = {
        "probe": "probe_wiki_qa.py",
        "authority_ceiling": "hub_class_request_wiki_qa_observation_only",
        "wiki_page": str(
            page_path.relative_to(ROOT) if page_path.is_relative_to(ROOT) else page_path
        ),
        "qa_spec": str(
            qa_path.relative_to(ROOT) if qa_path.is_relative_to(ROOT) else qa_path
        ),
        "model": args.model,
        "result": "PASS",
        "total_questions": total,
        "match_count": match_count,
        "miss_count": miss_count,
        "error_count": error_count,
        "note": (
            "PASS does not imply USB 2.0 semantic correctness. "
            "MATCH means expected keywords found in LLM response only. "
            "MISS is advisory — does not indicate spec incorrectness."
        ),
        "questions": results,
        **GOVERNANCE_METADATA,
    }
    _write_receipt(args.receipt_out, receipt)

    print(
        f"Wiki QA probe PASS (observation-only): "
        f"{match_count}/{total} MATCH, {miss_count} advisory MISS, {error_count} ERROR"
    )
    for r in results:
        marker = "+" if r["result"] == "MATCH" else ("~" if r["result"] == "MISS" else "!")
        print(f"  [{marker}] {r['id']}: {r['result']}")
        if r["result"] == "MISS":
            print(f"       missing keywords: {r.get('missing_keywords', [])}")
        if r["result"] == "ERROR":
            print(f"       error: {r.get('error', '')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
