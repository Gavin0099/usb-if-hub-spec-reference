import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { REPO_ROOT } from "./repoPaths.js";

export type DriftStatus = "clean" | "drift_detected" | "unknown";

interface FingerprintCache {
  driftStatus: DriftStatus;
  checkedAt: string;
  cachedAt: number; // Date.now() in ms
  detail?: string;
}

const PYTHON_BIN = process.env.MCP_PYTHON_BIN ?? "python";
// Must never exceed this server's own re-check interval for
// scripts/probe_table_fingerprint.py (see mcp_tool_schema.md, Tool 9), so a
// cached "clean" result cannot outlive the check that justified it.
const CHECK_INTERVAL_MS = Number(process.env.MCP_FINGERPRINT_CHECK_INTERVAL_MS ?? 60_000);

let cache: FingerprintCache | undefined;

function runProbe(): FingerprintCache {
  const tmpDir = mkdtempSync(path.join(tmpdir(), "usbif-fp-"));
  const receiptPath = path.join(tmpDir, "receipt.json");
  try {
    const result = spawnSync(
      PYTHON_BIN,
      ["scripts/probe_table_fingerprint.py", "--mode", "check", "--receipt-out", receiptPath],
      { cwd: REPO_ROOT, encoding: "utf-8" }
    );

    if (result.error) {
      return {
        driftStatus: "unknown",
        checkedAt: new Date().toISOString(),
        cachedAt: Date.now(),
        detail: `probe_execution_failed: ${result.error.message}`,
      };
    }

    let receipt: Record<string, unknown>;
    try {
      receipt = JSON.parse(readFileSync(receiptPath, "utf-8"));
    } catch {
      return {
        driftStatus: "unknown",
        checkedAt: new Date().toISOString(),
        cachedAt: Date.now(),
        detail: "probe_receipt_unreadable",
      };
    }

    const resultField = receipt["result"];
    const driftStatus: DriftStatus =
      resultField === "PASS"
        ? "clean"
        : resultField === "DRIFT_DETECTED"
          ? "drift_detected"
          : "unknown";

    return {
      driftStatus,
      checkedAt: typeof receipt["checked_at"] === "string" ? receipt["checked_at"] : new Date().toISOString(),
      cachedAt: Date.now(),
      detail: typeof resultField === "string" ? resultField : undefined,
    };
  } finally {
    rmSync(tmpDir, { recursive: true, force: true });
  }
}

/**
 * Returns the current drift status against
 * evidence/table_fingerprint_baseline.jsonl. Never fabricates "clean" — if
 * the probe has never run within CHECK_INTERVAL_MS or fails to execute, this
 * returns "unknown".
 */
export function getDriftStatus(): { driftStatus: DriftStatus; checkedAt: string } {
  const now = Date.now();
  if (!cache || now - cache.cachedAt > CHECK_INTERVAL_MS) {
    cache = runProbe();
  }
  return { driftStatus: cache.driftStatus, checkedAt: cache.checkedAt };
}
