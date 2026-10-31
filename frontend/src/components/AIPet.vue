<template>
  <div class="ai-pet-layer" :style="{ left: `${position.x}px`, top: `${position.y}px` }">
    <div v-if="suggestion && !muted && !chatOpen" ref="suggestionElement" class="pet-suggestion" :style="suggestionStyle">
      <button type="button" class="suggestion-close" title="关闭建议" aria-label="关闭建议" @click="dismissSuggestion">×</button>
      <strong class="suggestion-heading">{{ ASSISTANT_NAME }}的学习小提示</strong>
      <p>{{ suggestion.text }}</p>
      <button v-if="suggestion.actionLabel" type="button" class="suggestion-action" @click="$emit('suggestion-action', suggestion.action)">{{ suggestion.actionLabel }}</button>
    </div>

    <div v-if="chatOpen" class="pet-chat-popover" :style="chatStyle" @keydown.esc.stop="closeChat">
      <div class="pet-chat-toolbar">
        <span>{{ ASSISTANT_NAME }} · 图谱小助手</span>
        <button type="button" title="收起问答" aria-label="收起问答" @click="closeChat"><span aria-hidden="true">×</span></button>
      </div>
      <ChatPanel class="compact-chat-panel" compact :messages="messages" :loading="loading" :configured="configured" @send="$emit('send', $event)" @select-reference="$emit('select-reference', $event)" />
    </div>

    <button ref="petButton" type="button" class="ai-pet-button" :class="{ active: chatOpen, dragging }" :title="`打开${ASSISTANT_NAME}，可拖动`" :aria-label="`打开${ASSISTANT_NAME}图谱小助手，可拖动`" :aria-expanded="chatOpen" @pointerdown="startDrag" @click="toggleChat">
      <img v-if="!imageFailed" class="pet-portrait" src="/assets/ai-pet/xiaodi-2d-v1.png" alt="" aria-hidden="true" width="1086" height="1448" draggable="false" decoding="async" @error="imageFailed = true">
      <span v-else class="pet-fallback-name" aria-hidden="true">{{ ASSISTANT_NAME }}</span>
    </button>
    <span class="pet-nameplate">{{ ASSISTANT_NAME }}</span>

    <button type="button" class="pet-mute-button" :title="muted ? '开启建议' : '暂时关闭建议'" :aria-label="muted ? '开启建议' : '暂时关闭建议'" @click="toggleMute"><span>问</span></button>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import ChatPanel from './ChatPanel.vue'
import { ASSISTANT_NAME } from '../constants/assistant'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  configured: { type: Boolean, default: false },
  suggestion: { type: Object, default: null },
})
const emit = defineEmits(['send', 'select-reference', 'dismiss-suggestion', 'toggle-mute', 'suggestion-action'])
const STORAGE_KEY = 'gis-knowledge-ai-pet-position'
const viewport = ref({ width: window.innerWidth, height: window.innerHeight })
const position = ref({ x: 0, y: 0 })
const chatOpen = ref(false)
const muted = ref(false)
const dragging = ref(false)
const dragMoved = ref(false)
const dragOffset = ref({ x: 0, y: 0 })
const dragStart = ref({ x: 0, y: 0 })
const petButton = ref(null)
const suggestionElement = ref(null)
const suggestionHeight = ref(160)
const canvasTop = ref(0)
const imageFailed = ref(false)
const petSize = computed(() => viewport.value.width <= 520 ? { width: 140, height: 204 } : { width: 160, height: 224 })
const headerBottom = computed(() => viewport.value.width <= 520 ? 96 : viewport.value.width <= 1100 ? 72 : 80)
const chatStyle = computed(() => chatOpen.value ? floatingPanelStyle(360, Math.min(560, Math.max(120, viewport.value.height - panelTopLimit() - 16))) : {})
const suggestionStyle = computed(() => props.suggestion ? floatingPanelStyle(viewport.value.width <= 520 ? viewport.value.width - petSize.value.width - 56 : 270, suggestionHeight.value, false) : {})
let dragResetTimer
let canvasObserver
let suggestionObserver

function clamp(value, min, max) { return Math.max(min, Math.min(value, Math.max(min, max))) }

function clampPosition(x, y) {
  return {
    x: clamp(x, 8, viewport.value.width - petSize.value.width - 8),
    y: clamp(y, Math.max(headerBottom.value + 8, canvasTop.value + 8), viewport.value.height - petSize.value.height - 12),
  }
}

function panelTopLimit() {
  return Math.max(headerBottom.value + 12, canvasTop.value + 8)
}

// Panels follow the companion but stay on screen when it is dragged to an edge.
function floatingPanelStyle(preferredWidth, height, fixedHeight = true) {
  const { width: screenWidth, height: screenHeight } = viewport.value
  const width = Math.min(preferredWidth, screenWidth - 32)
  const topLimit = panelTopLimit()
  let left = position.value.x + petSize.value.width - width
  let top = position.value.y - height - 12
  if (top < topLimit) {
    if (position.value.x - width - 12 >= 16) {
      left = position.value.x - width - 12
      top = position.value.y + petSize.value.height - height
    } else if (position.value.x + petSize.value.width + width + 12 <= screenWidth - 16) {
      left = position.value.x + petSize.value.width + 12
      top = position.value.y + petSize.value.height - height
    } else if (!fixedHeight && position.value.y + petSize.value.height + height + 28 <= screenHeight) {
      top = position.value.y + petSize.value.height + 12
    } else {
      top = position.value.y + petSize.value.height - height
    }
  }
  return {
    left: `${clamp(left, 16, screenWidth - width - 16)}px`,
    top: `${clamp(top, topLimit, screenHeight - height - 16)}px`,
    width: `${width}px`,
    ...(fixedHeight ? { height: `${height}px` } : { maxHeight: `${Math.max(100, screenHeight - topLimit - 16)}px` }),
  }
}

function savePosition() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(position.value)) } catch { /* Keep dragging usable when storage is unavailable. */ }
}

function startDrag(event) {
  if (event.button !== 0) return
  const rect = petButton.value?.getBoundingClientRect()
  if (!rect) return
  event.preventDefault()
  clearTimeout(dragResetTimer)
  dragging.value = true
  dragMoved.value = false
  dragOffset.value = { x: event.clientX - rect.left, y: event.clientY - rect.top }
  dragStart.value = { x: event.clientX, y: event.clientY }
  petButton.value.setPointerCapture?.(event.pointerId)
  window.addEventListener('pointermove', moveDrag)
  window.addEventListener('pointerup', stopDrag, { once: true })
  window.addEventListener('pointercancel', stopDrag, { once: true })
}

function moveDrag(event) {
  if (!dragging.value) return
  if (Math.hypot(event.clientX - dragStart.value.x, event.clientY - dragStart.value.y) < 4 && !dragMoved.value) return
  dragMoved.value = true
  position.value = clampPosition(event.clientX - dragOffset.value.x, event.clientY - dragOffset.value.y)
}

function stopDrag() {
  if (!dragging.value) return
  dragging.value = false
  window.removeEventListener('pointermove', moveDrag)
  window.removeEventListener('pointerup', stopDrag)
  window.removeEventListener('pointercancel', stopDrag)
  if (dragMoved.value) savePosition()
  dragResetTimer = window.setTimeout(() => { dragMoved.value = false }, 0)
}

function toggleChat(event) {
  if (dragMoved.value) { event.preventDefault(); return }
  chatOpen.value = !chatOpen.value
}

function closeChat() {
  chatOpen.value = false
  petButton.value?.focus({ preventScroll: true })
}

function dismissSuggestion() { emit('dismiss-suggestion') }
function toggleMute() {
  muted.value = !muted.value
  try { localStorage.setItem('gis-knowledge-ai-pet-muted', String(muted.value)) } catch { /* Session state still works. */ }
  emit('toggle-mute', muted.value)
}

function handleResize() {
  viewport.value = { width: window.innerWidth, height: window.innerHeight }
  position.value = clampPosition(position.value.x, position.value.y)
}

watch(suggestionElement, element => {
  suggestionObserver?.disconnect()
  if (!element) return
  suggestionObserver = new ResizeObserver(() => { suggestionHeight.value = element.getBoundingClientRect().height })
  suggestionObserver.observe(element)
})

onMounted(() => {
  // Start clear of the directory and bottom legend/minimap, preserving saved positions.
  const compactShortScreen = viewport.value.width <= 520 && viewport.value.height < 720
  position.value = clampPosition(compactShortScreen ? 16 : viewport.value.width - petSize.value.width - 24, viewport.value.height - 440)
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null')
    if (saved && Number.isFinite(saved.x) && Number.isFinite(saved.y)) position.value = clampPosition(saved.x, saved.y)
    muted.value = localStorage.getItem('gis-knowledge-ai-pet-muted') === 'true'
  } catch { /* Use the on-screen default position. */ }
  const canvas = document.querySelector('.canvas-shell')
  if (canvas) {
    canvasObserver = new ResizeObserver(() => {
      canvasTop.value = canvas.getBoundingClientRect().top
      position.value = clampPosition(position.value.x, position.value.y)
    })
    canvasObserver.observe(canvas)
  }
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  clearTimeout(dragResetTimer)
  canvasObserver?.disconnect()
  suggestionObserver?.disconnect()
  window.removeEventListener('pointermove', moveDrag)
  window.removeEventListener('pointerup', stopDrag)
  window.removeEventListener('pointercancel', stopDrag)
  window.removeEventListener('resize', handleResize)
})
</script>
