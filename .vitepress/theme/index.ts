import DefaultTheme from 'vitepress/theme'
import AskAI from './components/AskAI.vue'
import { h } from 'vue'

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'doc-after': () => h(AskAI),
    })
  },
}
