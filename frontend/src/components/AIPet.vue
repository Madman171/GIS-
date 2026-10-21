<template>
  <div
    class="ai-pet-layer"
    :style="{ left: `${position.x}px`, top: `${position.y}px` }"
  >
    <div v-if="suggestion && !muted && !chatOpen" class="pet-suggestion">
      <button
        type="button"
        class="suggestion-close"
        title="关闭建议"
        aria-label="关闭建议"
        @click="dismissSuggestion"
      >
        ×
      </button>
      <p>{{ suggestion.text }}</p>
      <button
        v-if="suggestion.actionLabel"
        type="button"
        class="suggestion-action"
        @click="$emit('suggestion-action', suggestion.action)"
      >
        {{ suggestion.actionLabel }}
      </button>
    </div>

    <div v-if="chatOpen" class="pet-chat-popover">
      <div class="pet-chat-toolbar">
        <span><Sparkles :size="14" /> 图谱小助手</span>
        <button type="button" title="收起问答" aria-label="收起问答" @click="chatOpen = false">
          <X :size="15" />
        </button>
      </div>
      <ChatPanel
        class="compact-chat-panel"
        compact
        :messages="messages"
        :loading="loading"
        :configured="configured"
        @send="$emit('send', $event)"
        @select-reference="$emit('select-reference', $event)"
      />
    </div>

    <button
      ref="petButton"
      type="button"
      class="ai-pet-button"
      :class="{ active: chatOpen }"
      title="打开图谱小助手，可拖动"
      aria-label="打开图谱小助手，可拖动"
      @pointerdown="startDrag"
      @click="toggleChat"
    >
      <Bot :size="25" />
      <span class="pet-sparkle"><Sparkles :size="12" /></span>
    </button>
    <button
      type="button"
      class="pet-mute-button"
      :title="muted ? '开启建议' : '暂时关闭建议'"
      :aria-label="muted ? '开启建议' : '暂时关闭建议'"
      @click="toggleMute"
    >
      {{ muted ? '·' : '✦' }}
    </button>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { Bot, Sparkles, X } from '@lucide/vue'
import ChatPanel from './ChatPanel.vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  configured: { type: Boolean, default: false },
  suggestion: { type: Object, default: null },
})

const emit = defineEmits([
  'send',
  'select-reference',
  'dismiss-suggestion',
  'toggle-mute',
  'suggestion-action',
])

const position = ref({ x: 0, y: 0 })
const chatOpen = ref(false)
const muted = ref(false)
const dragging = ref(false)
const dragMoved = ref(false)
const dragOffset = ref({ x: 0, y: 0 })
const petButton = ref(null)
const STORAGE_KEY = 'gis-knowledge-ai-pet-position'

function clampPosition(x, y) {
  const size = 58
  return {
    x: Math.max(10, Math.min(x, window.innerWidth - size - 10)),
    y: Math.max(72, Math.min(y, window.innerHeight - size - 14)),
  }
}

function savePosition() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(position.value))
}

function startDrag(event) {
  if (event.button !== 0) return
  const rect = petButton.value?.getBoundingClientRect()
  if (!rect) return
  dragging.value = true
  dragMoved.value = false
  dragOffset.value = { x: event.clientX - rect.left, y: event.clientY - rect.top }
  petButton.value.setPointerCapture?.(event.pointerId)
  window.addEventListener('pointermove', moveDrag)
  window.addEventListener('pointerup', stopDrag, { once: true })
}

function moveDrag(event) {
  if (!dragging.value) return
  const next = clampPosition(
    event.clientX - dragOffset.value.x,
    event.clientY - dragOffset.value.y,
  )
  if (Math.abs(next.x - position.value.x) > 2 || Math.abs(next.y - position.value.y) > 2) {
    dragMoved.value = true
  }
  position.value = next
}

function stopDrag() {
  if (!dragging.value) return
  dragging.value = false
  window.removeEventListener('pointermove', moveDrag)
  savePosition()
  window.setTimeout(() => { dragMoved.value = false }, 0)
}

function toggleChat(event) {
  if (dragMoved.value) {
    event.preventDefault()
    return
  }
  chatOpen.value = !chatOpen.value
}

function dismissSuggestion() {
  emit('dismiss-suggestion')
}

function toggleMute() {
  muted.value = !muted.value
  localStorage.setItem('gis-knowledge-ai-pet-muted', String(muted.value))
  emit('toggle-mute', muted.value)
}

function handleResize() {
  position.value = clampPosition(position.value.x, position.value.y)
}

onMounted(() => {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null')
    const savedMuted = localStorage.getItem('gis-knowledge-ai-pet-muted')
    if (saved && Number.isFinite(saved.x) && Number.isFinite(saved.y)) {
      position.value = clampPosition(saved.x, saved.y)
    } else {
      position.value = clampPosition(window.innerWidth - 82, window.innerHeight - 100)
    }
    muted.value = savedMuted === 'true'
  } catch {
    position.value = clampPosition(window.innerWidth - 82, window.innerHeight - 100)
  }
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('pointermove', moveDrag)
  window.removeEventListener('pointerup', stopDrag)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.ai-pet-layer {
  position: fixed;
  z-index: 60;
  width: 58px;
  height: 58px;
  user-select: none;
}

.ai-pet-button {
  width: 58px;
  height: 58px;
  padding: 0;
  border: 3px solid rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  display: grid;
  place-items: center;
  position: relative;
  color: #ffffff;
  background: linear-gradient(145deg, #7c3aed, #0f766e);
  box-shadow: 0 10px 28px rgba(76, 29, 149, 0.32), 0 0 0 5px rgba(124, 58, 237, 0.12);
  cursor: grab;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.ai-pet-button:hover,
.ai-pet-button.active {
  transform: scale(1.06);
  box-shadow: 0 14px 32px rgba(76, 29, 149, 0.4), 0 0 0 6px rgba(124, 58, 237, 0.16);
}

.ai-pet-button:active { cursor: grabbing; }
.pet-sparkle { position: absolute; top: -2px; right: -1px; width: 21px; height: 21px; border-radius: 50%; display: grid; place-items: center; color: #7c3aed; background: #fef3c7; }
.pet-mute-button { position: absolute; right: -8px; bottom: -7px; width: 22px; height: 22px; border: 1px solid #e2e8f0; border-radius: 50%; color: #64748b; background: #ffffff; cursor: pointer; font-size: 11px; }
.pet-chat-popover { position: absolute; right: 0; bottom: 70px; width: 340px; height: min(540px, calc(100vh - 100px)); overflow: hidden; border: 1px solid #dbe4ef; border-radius: 12px; background: #ffffff; box-shadow: 0 20px 60px rgba(15, 23, 42, 0.2); }
.pet-chat-toolbar { height: 38px; padding: 0 10px 0 13px; display: flex; align-items: center; justify-content: space-between; color: #334155; background: #f8fafc; border-bottom: 1px solid #e7edf5; font-size: 12px; font-weight: 700; }
.pet-chat-toolbar span { display: flex; align-items: center; gap: 5px; color: #6d28d9; }
.pet-chat-toolbar button { width: 25px; height: 25px; padding: 0; border: 0; border-radius: 5px; display: grid; place-items: center; color: #64748b; background: transparent; cursor: pointer; }
.pet-chat-toolbar button:hover { background: #e2e8f0; }
:deep(.compact-chat-panel) { height: calc(100% - 38px); border: 0; }
:deep(.compact-chat-panel .chat-header) { display: none; }
:deep(.compact-chat-panel .message-list) { padding: 12px; }
:deep(.compact-chat-panel .quick-prompts) { padding-top: 7px; }
.pet-suggestion { position: absolute; right: 0; bottom: 70px; width: 250px; padding: 11px 12px; border: 1px solid #ddd6fe; border-radius: 11px; color: #4338ca; background: #faf5ff; box-shadow: 0 12px 30px rgba(76, 29, 149, 0.16); transform: translateX(-4px); }
.pet-suggestion p { margin: 0 18px 8px 0; font-size: 12px; line-height: 1.55; }
.suggestion-close { position: absolute; top: 5px; right: 7px; border: 0; color: #8b5cf6; background: transparent; cursor: pointer; font-size: 16px; }
.suggestion-action { padding: 5px 8px; border: 1px solid #c4b5fd; border-radius: 6px; color: #6d28d9; background: #ffffff; cursor: pointer; font-size: 11px; }
@media (max-width: 520px) { .pet-chat-popover { position: fixed; right: 10px; bottom: 76px; width: min(92vw, 360px); height: min(560px, calc(100vh - 92px)); } .pet-suggestion { position: fixed; right: 12px; bottom: 76px; width: min(78vw, 280px); } }
</style>
