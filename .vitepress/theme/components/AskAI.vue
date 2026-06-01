<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isMounted = ref(false)
const isOpen = ref(false)
const question = ref('')
const answer = ref('')
const loading = ref(false)
const apiKey = ref('')
const showKeyInput = ref(false)
const tempKey = ref('')
const errorMsg = ref('')

onMounted(() => {
  isMounted.value = true
  apiKey.value = localStorage.getItem('anthropic_api_key') || ''
})

function saveKey() {
  const k = tempKey.value.trim()
  if (!k.startsWith('sk-')) {
    errorMsg.value = 'API Key 格式錯誤（應以 sk- 開頭）'
    return
  }
  apiKey.value = k
  localStorage.setItem('anthropic_api_key', k)
  showKeyInput.value = false
  tempKey.value = ''
  errorMsg.value = ''
}

function clearKey() {
  apiKey.value = ''
  localStorage.removeItem('anthropic_api_key')
  answer.value = ''
  question.value = ''
}

function getPageText(): string {
  const el = document.querySelector('.vp-doc')
  return el ? (el.textContent || '').slice(0, 8000) : ''
}

async function askAI() {
  if (!question.value.trim() || !apiKey.value || loading.value) return
  loading.value = true
  answer.value = ''
  errorMsg.value = ''

  const pageText = getPageText()
  const system = [
    '你是 USB 規格文件技術助手，使用繁體中文回答。',
    '請根據以下頁面內容回答問題。如果答案不在頁面中，請明確說明。',
    '不要主張 USB 2.0 語意正確性。回答請簡潔。',
  ].join('\n')

  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': apiKey.value,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
        'anthropic-dangerous-direct-browser-access': 'true',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 512,
        system,
        messages: [{
          role: 'user',
          content: `頁面內容：\n\n${pageText}\n\n---\n\n問題：${question.value}`,
        }],
      }),
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error((err as any).error?.message || `API 錯誤 ${res.status}`)
    }

    const data = await res.json() as any
    answer.value = data.content?.[0]?.text || '（無回應）'
  } catch (e: any) {
    errorMsg.value = `錯誤：${e.message}`
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div v-if="isMounted" class="ask-ai-wrapper">
    <div class="ask-ai-toggle" @click="isOpen = !isOpen">
      <span>🤖 詢問 AI</span>
      <span class="toggle-icon">{{ isOpen ? '▲' : '▼' }}</span>
    </div>

    <div v-if="isOpen" class="ask-ai-panel">
      <p class="governance-note">
        基於本頁內容回答 ·
        <code>claim_level: inferred</code> ·
        不主張 USB 2.0 語意正確性
      </p>

      <!-- API Key 設定 -->
      <div v-if="!apiKey || showKeyInput" class="key-section">
        <label>Anthropic API Key：</label>
        <div class="key-row">
          <input
            v-model="tempKey"
            type="password"
            placeholder="sk-ant-..."
            @keyup.enter="saveKey"
          />
          <button @click="saveKey">儲存</button>
          <button v-if="apiKey" class="secondary" @click="showKeyInput = false">取消</button>
        </div>
        <small>Key 僅存於瀏覽器 localStorage，不會傳送至任何伺服器。</small>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
      </div>

      <!-- 問答區 -->
      <div v-if="apiKey && !showKeyInput" class="query-section">
        <textarea
          v-model="question"
          placeholder="輸入問題，例如：GET_STATUS 用來做什麼？"
          rows="3"
          @keyup.ctrl.enter="askAI"
        />
        <div class="query-actions">
          <button @click="askAI" :disabled="loading || !question.trim()">
            {{ loading ? '回答中…' : '送出（Ctrl+Enter）' }}
          </button>
          <button class="secondary" @click="showKeyInput = true">更換 Key</button>
          <button class="secondary danger" @click="clearKey">清除</button>
        </div>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

        <div v-if="answer" class="answer-box">
          <div class="answer-header">
            AI 回答 <span class="caution">（非語意驗證 · inferred only）</span>
          </div>
          <div class="answer-content">{{ answer }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ask-ai-wrapper {
  margin-top: 2rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  overflow: hidden;
}

.ask-ai-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--vp-c-bg-soft);
  cursor: pointer;
  user-select: none;
  font-weight: 500;
}

.ask-ai-toggle:hover {
  background: var(--vp-c-bg-mute);
}

.ask-ai-panel {
  padding: 1rem;
}

.governance-note {
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.75rem;
}

.key-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.key-row {
  display: flex;
  gap: 0.5rem;
}

.key-row input {
  flex: 1;
  padding: 0.4rem 0.6rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.9rem;
}

.key-section small {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.query-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 4px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.9rem;
  resize: vertical;
  box-sizing: border-box;
}

.query-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

button {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  background: var(--vp-c-brand-1);
  color: white;
  cursor: pointer;
  font-size: 0.85rem;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button.secondary {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  border: 1px solid var(--vp-c-divider);
}

button.danger {
  background: var(--vp-c-danger-soft);
  color: var(--vp-c-danger-1);
}

.answer-box {
  margin-top: 0.75rem;
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 6px;
  overflow: hidden;
}

.answer-header {
  padding: 0.4rem 0.75rem;
  background: var(--vp-c-brand-soft);
  font-size: 0.8rem;
  font-weight: 600;
}

.caution {
  font-weight: normal;
  color: var(--vp-c-text-2);
}

.answer-content {
  padding: 0.75rem;
  white-space: pre-wrap;
  font-size: 0.9rem;
  line-height: 1.6;
}

.error-msg {
  color: var(--vp-c-danger-1);
  font-size: 0.85rem;
}
</style>
