---
title: Redirecting to English
titleTemplate: false
layout: doc
---

<script setup>
import { onMounted } from "vue";

onMounted(() => {
  if (typeof window === "undefined") return;
  window.location.replace(new URL("./en/", window.location.href).toString());
});
</script>

# Redirecting to English

The default entry point now opens the English homepage.

If you are not redirected automatically, continue to [English Home](./en/).

如果沒有自動跳轉，請改用 [English Home](./en/)。
