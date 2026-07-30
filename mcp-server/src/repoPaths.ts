import path from "node:path";
import { fileURLToPath } from "node:url";

// mcp-server/ lives directly under the repo root, so the repo root is one
// level above this package's own directory (dist/ or src/, both one level
// deep from mcp-server/).
const THIS_DIR = path.dirname(fileURLToPath(import.meta.url));

/**
 * Absolute path to the usb-if-hub-spec-reference repo root.
 * Works whether running from src/ (ts-node/tsx) or dist/ (compiled), since
 * both are exactly one directory level under mcp-server/.
 */
export const REPO_ROOT = path.resolve(THIS_DIR, "..", "..");

export function repoPath(...segments: string[]): string {
  return path.join(REPO_ROOT, ...segments);
}

/** Convert an absolute path under REPO_ROOT to a repo-relative, forward-slash path. */
export function toRepoRelative(absolutePath: string): string {
  const rel = path.relative(REPO_ROOT, absolutePath);
  return rel.split(path.sep).join("/");
}
