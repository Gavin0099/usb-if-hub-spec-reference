import { defineConfig } from "vitepress";
import { existsSync, readdirSync } from "fs";
import { join } from "path";

const ROOT = join(__dirname, "..");
const SPECS_DIR = join(ROOT, "specs");

type Labels = Record<string, string>;

const ZH_LABELS: Labels = {
  escalation_table: "升級觸發表",
  hub_class_requests: "Hub 類別請求",
  hub_descriptor: "Hub 描述符",
  port_status_bits: "連接埠狀態位元",
  transaction_translator: "Transaction Translator",
  version_source_map: "版本來源對應",
};

const EN_LABELS: Labels = {
  escalation_table: "Escalation Table",
  hub_class_requests: "Hub Class Requests",
  hub_descriptor: "Hub Descriptor",
  port_status_bits: "Port Status Bits",
  transaction_translator: "Transaction Translator",
  version_source_map: "Version Source Map",
};

function buildSidebar(relativeDir: string, labels: Labels, sectionText: string, prefix = "") {
  const dir = join(SPECS_DIR, relativeDir);
  if (!existsSync(dir)) return [];

  const files = readdirSync(dir)
    .filter((file) => file.endsWith(".md") && file !== "index.md")
    .sort()
    .map((file) => {
      const stem = file.replace(/\.md$/, "");
      return {
        text: labels[stem] ?? stem.replace(/_/g, " "),
        link: `${prefix}/${stem}`.replace("//", "/"),
      };
    });

  return [
    {
      text: sectionText,
      collapsed: false,
      items: files,
    },
  ];
}

export default defineConfig({
  title: "USB-IF Hub 規格參考",
  description: "USB Hub 規格參考網站，僅提供標準語意澄清，claim_level: inferred",
  srcDir: "./specs",
  base: process.env.BASE_URL ?? "/",
  head: [["link", { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" }]],

  locales: {
    root: {
      lang: "zh-TW",
      label: "繁體中文",
      themeConfig: {
        nav: [
          { text: "首頁", link: "/" },
          { text: "Hub 類別請求", link: "/hub_class_requests" },
          { text: "連接埠狀態位元", link: "/port_status_bits" },
        ],
        sidebar: buildSidebar(".", ZH_LABELS, "規格參考"),
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
        footer: {
          message:
            "claim_level: inferred，semantic_verification_claimed: false，內容尚未完成 USB 2.0 PDF 逐節驗證",
        },
      },
    },
    en: {
      lang: "en-US",
      label: "English",
      link: "/en/",
      title: "USB-IF Hub Spec Reference",
      description:
        "USB Hub specification reference site for standards clarification only, claim_level: inferred",
      themeConfig: {
        nav: [
          { text: "Home", link: "/en/" },
          { text: "Hub Class Requests", link: "/en/hub_class_requests" },
          { text: "Port Status Bits", link: "/en/port_status_bits" },
        ],
        sidebar: buildSidebar("en", EN_LABELS, "Specification Reference", "/en"),
        search: {
          provider: "local",
        },
        footer: {
          message:
            "claim_level: inferred, semantic_verification_claimed: false, content is not yet section-level verified against the USB 2.0 PDF",
        },
      },
    },
  },

  themeConfig: {
    logo: undefined,
  },

  markdown: {
    lineNumbers: false,
  },
});
