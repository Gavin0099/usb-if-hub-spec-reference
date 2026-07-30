import express from "express";
import { randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { apiKeyAuth } from "./auth.js";
import { registerAllTools } from "./tools.js";

const PORT = Number(process.env.MCP_PORT ?? 8787);

function createMcpServer(): McpServer {
  const server = new McpServer({
    name: "usb-if-hub-spec-reference-mcp",
    version: "0.1.0",
  });
  registerAllTools(server);
  return server;
}

async function main() {
  const app = express();
  app.use(express.json());

  // Auth applies to the MCP endpoint only; a plain unauthenticated health
  // check is left open so pilot deployments can be probed by uptime
  // monitors without an API key.
  app.get("/healthz", (_req, res) => {
    res.status(200).json({ status: "ok" });
  });

  app.all("/mcp", apiKeyAuth, async (req, res) => {
    // Stateless mode per SDK docs (sessionIdGenerator: undefined): every
    // request gets a fresh server + transport pair. This matches the
    // proposal's "single-round-trip, read-only, no cross-call state" design
    // (mcp_tool_schema.md) and avoids holding per-session state in memory.
    const server = createMcpServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
    });
    res.on("close", () => {
      transport.close();
      server.close();
    });
    try {
      await server.connect(transport);
      await transport.handleRequest(req, res, req.body);
    } catch (err) {
      if (!res.headersSent) {
        res.status(500).json({
          jsonrpc: "2.0",
          error: { code: -32603, message: "internal_error" },
          id: randomUUID(),
        });
      }
    }
  });

  app.listen(PORT, () => {
    console.log(`usb-if-hub-spec-reference MCP server listening on :${PORT} (Streamable HTTP, stateless)`);
    console.log(`Health check: GET /healthz (no auth). MCP endpoint: ALL /mcp (API key required).`);
  });
}

main().catch((err) => {
  console.error("Fatal startup error:", err);
  process.exitCode = 1;
});
