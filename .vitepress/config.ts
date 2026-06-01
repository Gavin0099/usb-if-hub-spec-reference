import { defineConfig } from "vitepress";
import { readdirSync, existsSync } from "fs";
import { join } from "path";

const ROOT = join(__dirname, "..");
const SPECS_DIR = join(ROOT, "specs");

const PAGE_LABELS: Record<string, string> = {
  hub_class_requests: "Hub Class Requests",
  hub_descriptor: "Hub Descriptor",
  port_status_bits: "Port Status Bits",
  transaction_translator: "Transaction Translator",
  version_source_map: "Version Source Map",
  escalation_table: "Escalation Table",
};

function buildSidebar() {
  if (!existsSync(SPECS_DIR)) return [];

  const files = readdirSync(SPECS_DIR)
    .filter((f) => f.endsWith(".md") && f !== "index.md")
    .sort()
    .map((f) => {
      const stem = f.replace(/\.md$/, "");
      return {
        text: PAGE_LABELS[stem] ?? stem.replace(/_/g, " "),
        link: `/${stem}`,
      };
    });

  return [
    {
      text: "Spec Reference",
      collapsed: false,
      items: files,
    },
  ];
}

export default defineConfig({
  title: "USB-IF Hub Spec Reference",
  description: "Governed USB hub specification reference — claim_level: inferred",
  srcDir: "./specs",

  themeConfig: {
    search: { provider: "local" },

    nav: [
      { text: "Home", link: "/" },
      { text: "Hub Class Requests", link: "/hub_class_requests" },
      { text: "Port Status Bits", link: "/port_status_bits" },
    ],

    sidebar: buildSidebar(),

    footer: {
      message:
        "claim_level: inferred · semantic_verification_claimed: false · USB 2.0 semantic correctness not claimed",
    },
  },

  markdown: {
    lineNumbers: false,
  },
});
