<template>
  <aside class="chat-panel" :class="{ compact }">
    <header class="chat-header">
      <div class="chat-heading">
        <div class="bot-icon">
          <span>AI</span>
        </div>
        <div>
          <h2>{{ ASSISTANT_NAME }} · 智能问答</h2>
          <span>基于知识图谱的课程助手</span>
        </div>
      </div>
      <span
        class="status-dot"
        :class="{ ready: configured }"
      >
        {{ configured ? '已连接' : '待配置' }}
      </span>
    </header>

    <div ref="messageList" class="message-list">
      <div
        v-for="(message, index) in messages"
        :key="`${message.role}-${index}`"
        class="message-row"
        :class="message.role"
      >
        <div class="message-avatar">
          <span v-if="message.role === 'user'">我</span>
          <span v-else>{{ ASSISTANT_NAME }}</span>
        </div>
        <div class="message-content">
          <div class="message-bubble">{{ message.content }}</div>
          <div
            v-if="message.role === 'assistant' && message.references?.length"
            class="message-references"
          >
            <button
              v-for="reference in message.references"
              :key="reference.id"
              type="button"
              @click="$emit('select-reference', reference)"
            >
              {{ reference.name }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="message-row assistant">
        <div class="message-avatar">
          <span>{{ ASSISTANT_NAME }}</span>
        </div>
        <div class="message-bubble typing">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <div class="quick-prompts">
      <button
        v-for="prompt in quickPrompts"
        :key="prompt"
        type="button"
        @click="sendPrompt(prompt)"
      >
        {{ prompt }}
      </button>
    </div>

    <form class="chat-composer" @submit.prevent="submit">
      <textarea
        v-model.trim="draft"
        rows="3"
        placeholder="输入关于知识图谱的问题"
        aria-label="智能问答输入框"
        @keydown.enter.exact.prevent="submit"
      ></textarea>
      <button
        type="submit"
        class="send-button"
        :disabled="!draft || loading"
        title="发送问题"
        aria-label="发送问题"
      >
        <span>发送</span>
      </button>
    </form>
  </aside>
</template>

<script setup>
import { nextTick, ref, watch } from 'vue'
import { ASSISTANT_NAME } from '../constants/assistant'


const props = defineProps({
  messages: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  configured: { type: Boolean, default: false },
  compact: { type: Boolean, default: false },
})

const emit = defineEmits(['send', 'select-reference'])

const draft = ref('')
const messageList = ref(null)
const quickPrompts = [
  '什么是交通路网数据模型？',
  '轨迹数据有哪些关键技术？',
  '推荐一条学习路径',
]

watch(
  () => props.messages.length,
  async () => {
    await nextTick()
    if (messageList.value) {
      messageList.value.scrollTop = messageList.value.scrollHeight
    }
  },
)

function submit() {
  sendPrompt(draft.value)
}

function sendPrompt(value) {
  const question = value.trim()
  if (!question || props.loading) return
  emit('send', question)
  draft.value = ''
}
</script>
