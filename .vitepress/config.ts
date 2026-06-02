import { defineConfig } from "vitepress";
import { readdirSync, existsSync } from "fs";
import { join } from "path";

const ROOT = join(__dirname, "..");
const SPECS_DIR = join(ROOT, "specs");

const PAGE_LABELS: Record<string, string> = {
  hub_class_requests: "Hub 類別請求",
  hub_descriptor: "Hub 描述符",
  port_status_bits: "連接埠狀態位元",
  transaction_translator: "Transaction Translator",
  version_source_map: "版本來源對應",
  escalation_table: "升級觸發表",
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
      text: "規格參考",
      collapsed: false,
      items: files,
    },
  ];
}

export default defineConfig({
  title: "USB-IF Hub 規格參考",
  description: "USB Hub 規格參考網站，僅提供標準語意澄清，claim_level: inferred",
  srcDir: "./specs",
  lang: "zh-TW",
  base: process.env.BASE_URL ?? "/",
  head: [['link', { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" }]],

  themeConfig: {
    search: {
      provider: "local",
      options: {
        translations: {
          button: { buttonText: "搜尋", buttonAriaLabel: "搜尋文件" },
          modal: {
            noResultsText: "找不到對應結果",
            resetButtonTitle: "清除搜尋條件",
            footer: { selectText: "選擇", navigateText: "切換", closeText: "關閉" },
          },
        },
      },
    },

    nav: [
      { text: "首頁", link: "/" },
      { text: "Hub 類別請求", link: "/hub_class_requests" },
      { text: "連接埠狀態位元", link: "/port_status_bits" },
    ],

    sidebar: buildSidebar(),

    footer: {
      message:
        "claim_level: inferred，semantic_verification_claimed: false，內容尚未完成 USB 2.0 PDF 逐節驗證",
    },
  },

  markdown: {
    lineNumbers: false,
  },
});
