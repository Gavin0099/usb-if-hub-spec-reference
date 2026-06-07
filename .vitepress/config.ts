import { defineConfig } from "vitepress";
import { existsSync, readdirSync } from "fs";
import { join } from "path";

const ROOT = join(__dirname, "..");
const SPECS_DIR = join(ROOT, "specs");

type Labels = Record<string, string>;

const ZH_LABELS: Labels = {
  escalation_table: "Escalation Table",
  feature_selectors: "Feature Selectors",
  glossary: "Glossary",
  hs_detection: "HS Detection",
  hub_class_requests: "Hub Class Requests",
  hub_compound_device: "Hub Compound Device",
  hub_configuration: "Hub Configuration Descriptors",
  hub_descriptor: "Hub Descriptor",
  hub_device_class: "Hub Device Class Codes",
  hub_enumeration: "Hub Enumeration Sequence",
  hub_interrupt_endpoint: "Hub Interrupt Endpoint",
  hub_power_management: "Hub Power Management",
  port_state_machine: "Port State Machine",
  port_status_bits: "Port Status Bits",
  standard_descriptors: "Standard USB Descriptors",
  standard_device_requests: "Standard Device Requests",
  transaction_translator: "Transaction Translator",
  usb_device_states: "USB Device States",
  usb_signaling: "USB Signaling",
  usb_transfer_types: "USB Transfer Types",
  verification_status: "Verification Status",
  version_source_map: "Version Source Map",
  usb_packet_types: "USB Packet Types",
  usb_transactions: "USB Transactions",
  split_transaction_packets: "Split Transaction Packets",
  usb_test_modes: "USB Test Modes",
  port_indicators: "Port Indicators",
  hub_power_budget: "Hub Power Budget",
  // USB 3.x / SuperSpeed Hub
  ss_hub_descriptor: "SuperSpeed Hub Descriptor",
  ss_port_status_bits: "SS Port Status Bits",
  ss_hub_class_requests: "SS Hub Class Requests",
};

const EN_LABELS: Labels = {
  escalation_table: "Escalation Table",
  feature_selectors: "Feature Selectors",
  glossary: "Glossary",
  hs_detection: "HS Detection",
  hub_class_requests: "Hub Class Requests",
  hub_compound_device: "Hub Compound Device",
  hub_configuration: "Hub Configuration Descriptors",
  hub_descriptor: "Hub Descriptor",
  hub_device_class: "Hub Device Class Codes",
  hub_enumeration: "Hub Enumeration Sequence",
  hub_interrupt_endpoint: "Hub Interrupt Endpoint",
  hub_power_management: "Hub Power Management",
  port_state_machine: "Port State Machine",
  port_status_bits: "Port Status Bits",
  standard_descriptors: "Standard USB Descriptors",
  standard_device_requests: "Standard Device Requests",
  transaction_translator: "Transaction Translator",
  usb_device_states: "USB Device States",
  usb_signaling: "USB Signaling",
  usb_transfer_types: "USB Transfer Types",
  verification_status: "Verification Status",
  version_source_map: "Version Source Map",
  usb_packet_types: "USB Packet Types",
  usb_transactions: "USB Transactions",
  split_transaction_packets: "Split Transaction Packets",
  usb_test_modes: "USB Test Modes",
  port_indicators: "Port Indicators",
  hub_power_budget: "Hub Power Budget",
  // USB 3.x / SuperSpeed Hub
  ss_hub_descriptor: "SuperSpeed Hub Descriptor",
  ss_port_status_bits: "SS Port Status Bits",
  ss_hub_class_requests: "SS Hub Class Requests",
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

const zhUsb2Items = [
  { text: "Hub Class Requests", link: "/hub_class_requests" },
  { text: "Feature Selectors", link: "/feature_selectors" },
  { text: "Port Status Bits", link: "/port_status_bits" },
  { text: "Port State Machine", link: "/port_state_machine" },
  { text: "Hub Descriptor", link: "/hub_descriptor" },
  { text: "Hub Device Class Codes", link: "/hub_device_class" },
  { text: "Hub Interrupt Endpoint", link: "/hub_interrupt_endpoint" },
  { text: "Hub Power Management", link: "/hub_power_management" },
  { text: "Hub Configuration Descriptors", link: "/hub_configuration" },
  { text: "Hub Enumeration Sequence", link: "/hub_enumeration" },
  { text: "Hub Compound Device", link: "/hub_compound_device" },
  { text: "Standard Device Requests", link: "/standard_device_requests" },
  { text: "Standard USB Descriptors", link: "/standard_descriptors" },
  { text: "USB Device States", link: "/usb_device_states" },
  { text: "USB Transfer Types", link: "/usb_transfer_types" },
  { text: "USB Signaling", link: "/usb_signaling" },
  { text: "HS Detection", link: "/hs_detection" },
  { text: "Transaction Translator", link: "/transaction_translator" },
  { text: "USB Packet Types", link: "/usb_packet_types" },
  { text: "USB Transactions", link: "/usb_transactions" },
  { text: "Split Transaction Packets", link: "/split_transaction_packets" },
  { text: "USB Test Modes", link: "/usb_test_modes" },
  { text: "Port Indicators", link: "/port_indicators" },
  { text: "Hub Power Budget", link: "/hub_power_budget" },
  { text: "Escalation Table", link: "/escalation_table" },
  { text: "Version Source Map", link: "/version_source_map" },
  { text: "Verification Status", link: "/verification_status" },
  { text: "Glossary", link: "/glossary" },
];

const zhUsb3Items = [
  { text: "SuperSpeed Hub Descriptor", link: "/usb3/ss_hub_descriptor" },
  { text: "SS Port Status Bits", link: "/usb3/ss_port_status_bits" },
  { text: "SS Hub Class Requests", link: "/usb3/ss_hub_class_requests" },
];

const enUsb2Items = [
  { text: "Hub Class Requests", link: "/en/hub_class_requests" },
  { text: "Feature Selectors", link: "/en/feature_selectors" },
  { text: "Port Status Bits", link: "/en/port_status_bits" },
  { text: "Port State Machine", link: "/en/port_state_machine" },
  { text: "Hub Descriptor", link: "/en/hub_descriptor" },
  { text: "Hub Device Class Codes", link: "/en/hub_device_class" },
  { text: "Hub Interrupt Endpoint", link: "/en/hub_interrupt_endpoint" },
  { text: "Hub Power Management", link: "/en/hub_power_management" },
  { text: "Hub Configuration Descriptors", link: "/en/hub_configuration" },
  { text: "Hub Enumeration Sequence", link: "/en/hub_enumeration" },
  { text: "Hub Compound Device", link: "/en/hub_compound_device" },
  { text: "Standard Device Requests", link: "/en/standard_device_requests" },
  { text: "Standard USB Descriptors", link: "/en/standard_descriptors" },
  { text: "USB Device States", link: "/en/usb_device_states" },
  { text: "USB Transfer Types", link: "/en/usb_transfer_types" },
  { text: "USB Signaling", link: "/en/usb_signaling" },
  { text: "HS Detection", link: "/en/hs_detection" },
  { text: "Transaction Translator", link: "/en/transaction_translator" },
  { text: "USB Packet Types", link: "/en/usb_packet_types" },
  { text: "USB Transactions", link: "/en/usb_transactions" },
  { text: "Split Transaction Packets", link: "/en/split_transaction_packets" },
  { text: "USB Test Modes", link: "/en/usb_test_modes" },
  { text: "Port Indicators", link: "/en/port_indicators" },
  { text: "Hub Power Budget", link: "/en/hub_power_budget" },
  { text: "Escalation Table", link: "/en/escalation_table" },
  { text: "Version Source Map", link: "/en/version_source_map" },
  { text: "Verification Status", link: "/en/verification_status" },
  { text: "Glossary", link: "/en/glossary" },
];

const enUsb3Items = [
  { text: "SuperSpeed Hub Descriptor", link: "/en/usb3/ss_hub_descriptor" },
  { text: "SS Port Status Bits", link: "/en/usb3/ss_port_status_bits" },
  { text: "SS Hub Class Requests", link: "/en/usb3/ss_hub_class_requests" },
];

const zhReferenceItems = [
  { text: "USB 2.0 Hub", items: zhUsb2Items },
  { text: "USB 3.x / SuperSpeed Hub", items: zhUsb3Items },
];

const enReferenceItems = [
  { text: "USB 2.0 Hub", items: enUsb2Items },
  { text: "USB 3.x / SuperSpeed Hub", items: enUsb3Items },
];

export default defineConfig({
  title: "USB-IF Hub Spec Reference",
  description:
    "USB Hub specification reference site for standards clarification only, claim_level: inferred",
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
          { text: "Reference", items: zhReferenceItems },
        ],
        sidebar: [
          ...buildSidebar(".", ZH_LABELS, "USB 2.0 Hub"),
          ...buildSidebar("usb3", ZH_LABELS, "USB 3.x / SuperSpeed Hub", "/usb3"),
        ],
        search: {
          provider: "local",
          options: {
            translations: {
              button: { buttonText: "搜尋", buttonAriaLabel: "搜尋文件" },
              modal: {
                noResultsText: "找不到結果",
                resetButtonTitle: "清除查詢條件",
                footer: {
                  selectText: "選取",
                  navigateText: "切換",
                  closeText: "關閉",
                },
              },
            },
          },
        },
        footer: {
          message:
            "本參考站是受治理的規格澄清層；不宣告完整 PDF section-level verification、runtime behavior model、firmware compliance truth，亦不宣告 USB-IF certification completeness。",
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
          { text: "Reference", items: enReferenceItems },
        ],
        sidebar: [
          ...buildSidebar("en", EN_LABELS, "USB 2.0 Hub", "/en"),
          ...buildSidebar("en/usb3", EN_LABELS, "USB 3.x / SuperSpeed Hub", "/en/usb3"),
        ],
        search: {
          provider: "local",
        },
        footer: {
          message:
            "This reference is a governed standards-clarification layer. It does not claim full PDF section-level verification, runtime behavior modeling, firmware compliance truth, or USB-IF certification completeness.",
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
