<template>
  <aside class="chat-panel">
    <header class="chat-header">
      <div class="chat-heading">
        <div class="bot-icon">
          <Bot :size="18" />
        </div>
        <div>
          <h2>智能问答</h2>
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
          <User v-if="message.role === 'user'" :size="15" />
          <Bot v-else :size="15" />
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
          <Bot :size="15" />
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
        <Send :size="17" />
      </button>
    </form>
  </aside>
</template>

<script setup>
import { nextTick, ref, watch } from 'vue'
import { Bot, Send, User } from '@lucide/vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  configured: { type: Boolean, default: false },
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

<style scoped>
.chat-panel {
  height: 100%;
  min-height: 0;
  border-left: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  overflow: hidden;
}

.chat-header {
  min-height: 70px;
  padding: 14px 16px;
  border-bottom: 1px solid #e7edf5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.chat-heading {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 9px;
}

.bot-icon {
  width: 34px;
  height: 34px;
  border-radius: 7px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  color: #ffffff;
  background: #0f766e;
}

h2 {
  margin: 0 0 2px;
  color: #0f172a;
  font-size: 15px;
}

.chat-heading span {
  display: block;
  color: #64748b;
  font-size: 11px;
}

.status-dot {
  flex: 0 0 auto;
  padding: 4px 7px;
  border-radius: 999px;
  color: #9a3412;
  background: #fff7ed;
  font-size: 10px;
  font-weight: 700;
}

.status-dot.ready {
  color: #166534;
  background: #f0fdf4;
}

.message-list {
  flex: 1;
  min-height: 0;
  padding: 16px;
  overflow-y: auto;
  background: #f8fafc;
}

.message-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.message-row + .message-row {
  margin-top: 14px;
}

.message-row.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  color: #475569;
  background: #e2e8f0;
}

.assistant .message-avatar {
  color: #ffffff;
  background: #0f766e;
}

.message-bubble {
  max-width: calc(100% - 42px);
  padding: 9px 11px;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  color: #334155;
  background: #ffffff;
  font-size: 12px;
  line-height: 1.65;
  white-space: pre-wrap;
}

.message-content {
  min-width: 0;
  max-width: calc(100% - 42px);
}

.message-content .message-bubble {
  max-width: 100%;
}

.user .message-bubble {
  border-color: #bfdbfe;
  color: #1e3a8a;
  background: #eff6ff;
}

.message-references {
  margin-top: 6px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.message-references button {
  max-width: 100%;
  padding: 4px 7px;
  border: 1px solid #bfdbfe;
  border-radius: 5px;
  overflow: hidden;
  color: #1d4ed8;
  background: #eff6ff;
  cursor: pointer;
  font-size: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.message-references button:hover {
  border-color: #60a5fa;
  background: #dbeafe;
}

.typing {
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 48px;
}

.typing span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #64748b;
  animation: bounce 1s infinite ease-in-out;
}

.typing span:nth-child(2) {
  animation-delay: 0.15s;
}

.typing span:nth-child(3) {
  animation-delay: 0.3s;
}

.quick-prompts {
  padding: 10px 12px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.quick-prompts button {
  padding: 5px 8px;
  border: 1px solid #dbe4ef;
  border-radius: 5px;
  color: #475569;
  background: #ffffff;
  cursor: pointer;
  font-size: 10px;
}

.quick-prompts button:hover {
  border-color: #0f766e;
  color: #0f766e;
}

.chat-composer {
  padding: 10px 12px 12px;
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.chat-composer textarea {
  min-width: 0;
  flex: 1;
  padding: 9px 10px;
  border: 1px solid #d7dee8;
  border-radius: 6px;
  outline: 0;
  color: #0f172a;
  resize: none;
  background: #ffffff;
  font-size: 12px;
  line-height: 1.5;
}

.chat-composer textarea:focus {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.1);
}

.send-button {
  width: 38px;
  height: 38px;
  border: 0;
  border-radius: 6px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  color: #ffffff;
  background: #0f766e;
  cursor: pointer;
}

.send-button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

@keyframes bounce {
  0%,
  60%,
  100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-3px);
  }
}
</style>
