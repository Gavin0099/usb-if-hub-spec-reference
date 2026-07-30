import type { NextFunction, Request, Response } from "express";
import { timingSafeEqual } from "node:crypto";

/**
 * Reads allowed API keys from the MCP_API_KEYS env var (comma-separated).
 * Fails closed: if MCP_API_KEYS is unset or empty, every request is
 * rejected rather than silently allowed, so a misconfigured deployment
 * cannot accidentally expose this server unauthenticated.
 */
function loadAllowedKeys(): string[] {
  const raw = process.env.MCP_API_KEYS ?? "";
  return raw
    .split(",")
    .map((k) => k.trim())
    .filter((k) => k.length > 0);
}

function constantTimeIncludes(candidate: string, allowed: string[]): boolean {
  const candidateBuf = Buffer.from(candidate, "utf-8");
  let matched = false;
  for (const key of allowed) {
    const keyBuf = Buffer.from(key, "utf-8");
    // timingSafeEqual requires equal-length buffers; comparing against every
    // configured key (rather than short-circuiting) avoids leaking which
    // key length matched via timing.
    if (keyBuf.length === candidateBuf.length && timingSafeEqual(candidateBuf, keyBuf)) {
      matched = true;
    }
  }
  return matched;
}

function extractApiKey(req: Request): string | undefined {
  const header = req.header("authorization");
  if (header?.startsWith("Bearer ")) {
    return header.slice("Bearer ".length).trim();
  }
  const apiKeyHeader = req.header("x-mcp-api-key");
  if (apiKeyHeader) {
    return apiKeyHeader.trim();
  }
  return undefined;
}

/**
 * Express middleware enforcing the pilot auth model (API key). Rejects with
 * 401 and a generic message on any missing/invalid key — never echoes the
 * submitted key back, and never distinguishes "missing" from "wrong" in the
 * response body, to avoid leaking auth-probing signal.
 */
export function apiKeyAuth(req: Request, res: Response, next: NextFunction): void {
  const allowedKeys = loadAllowedKeys();
  if (allowedKeys.length === 0) {
    res.status(503).json({
      error: "server_misconfigured",
      message: "MCP_API_KEYS is not configured; refusing all requests (fail closed).",
    });
    return;
  }

  const submitted = extractApiKey(req);
  if (!submitted || !constantTimeIncludes(submitted, allowedKeys)) {
    res.status(401).json({ error: "unauthorized" });
    return;
  }

  next();
}
