<template>
  <dialog
    ref="dialogElement"
    class="detail-panel"
    aria-label="知识点详情"
    @cancel.prevent="$emit('close')"
    @pointerdown="rememberBackdropPress"
    @click="dismissOnBackdrop"
  >
    <div v-if="loading" class="detail-state">
      <button type="button" class="icon-button detail-loading-close" aria-label="关闭详情" autofocus @click="$emit('close')">×</button>
      <LoaderCircle class="spin" :size="22" />
      <span>正在加载知识点</span>
    </div>

    <template v-else-if="detail">
      <header class="detail-header">
        <div class="title-wrap">
          <span class="type-badge">知识点</span>
          <h2>{{ nodeName }}</h2>
        </div>
        <div class="detail-header-actions">
          <button
            v-if="canGoBack"
            type="button"
            class="back-detail-button"
            title="返回上一个知识点"
            aria-label="返回上一个知识点"
            @click="$emit('go-back')"
          >

            返回
          </button>
          <button
            type="button"
            class="icon-button"
            title="关闭详情"
            aria-label="关闭详情"
            ref="closeButton"
            autofocus
            @click="$emit('close')"
          >
            <span aria-hidden="true">×</span>
          </button>
        </div>
      </header>

      <div ref="detailContent" class="detail-content">
        <div class="meta-grid">
          <div class="meta-item">

            <span>难度</span>
            <strong>{{ properties.difficulty || '未标注' }}</strong>
          </div>
          <div class="meta-item">

            <span>重要性</span>
            <strong>{{ properties.importance || '未标注' }}</strong>
          </div>
          <div class="meta-item">

            <span>分类</span>
            <strong>{{ properties.subcategory || '未分类' }}</strong>
          </div>
          <div class="meta-item">

            <span>所属模块</span>
            <strong>{{ moduleName }}</strong>
          </div>
        </div>

        <section class="content-section">
          <h3>知识点说明</h3>
          <p>{{ properties.description || '暂无详细说明。' }}</p>
        </section>

        <section class="content-section learning-path-section">
          <h3>前置学习路径</h3>

          <div v-if="learningPathLoading" class="path-state">
            <LoaderCircle class="spin" :size="17" />
            <span>正在整理学习顺序</span>
          </div>

          <div v-else-if="learningPathError" class="path-empty">
            <strong>学习路径暂时不可用</strong>
            <span>{{ learningPathError }}</span>
          </div>

          <template v-else>
            <div v-if="hasCycle" class="path-warning">

              <span>检测到前置关系循环，以下路径仅供参考。</span>
            </div>

            <div v-if="pathItems.length" class="learning-path-list">
              <button
                v-for="(item, index) in pathItems"
                :key="`${item.id}-${item.depth}`"
                type="button"
                class="path-item"
                @click="navigateToNode(item, { path: true })"
              >
                <span class="path-index">{{ index + 1 }}</span>
                <span class="path-copy">
                  <strong>{{ item.name }}</strong>
                  <small>
                    前置知识 · {{ item.difficulty || '未标注' }}
                  </small>
                </span>
                <span class="row-chevron" aria-hidden="true">›</span>
              </button>
            </div>

            <div v-else class="path-empty">
              <strong>暂无已配置的前置知识</strong>
              <span>当前知识点可以直接开始学习。</span>
            </div>
          </template>
        </section>

        <section
          v-if="relationGroups.length"
          class="content-section"
        >
          <h3><Link2 :size="15" />关联知识</h3>
          <div
            v-for="group in relationGroups"
            :key="group.type"
            class="relation-group"
          >
            <span class="relation-label">{{ group.label }}</span>
            <button
              v-for="item in group.items"
              :key="item.node.id"
              type="button"
              class="related-row"
              @click="navigateToNode(item.node)"
            >
              <span>{{ getNodeName(item.node) }}</span>
              <ChevronRight :size="14" />
            </button>
          </div>
        </section>

        <section class="content-section">
          <h3><PlayCircle :size="15" />教学资源</h3>

          <div v-if="videos.length" class="media-list">
            <article
              v-for="video in videos"
              :key="video.id"
              class="media-card"
            >
              <div class="media-title">
                <Film :size="16" />
                <strong>{{ video.title }}</strong>
              </div>
              <video
                v-if="video.url"
                class="video-player"
                controls
                preload="metadata"
                :poster="video.coverUrl || undefined"
                :src="video.url"
              >
                当前浏览器不支持视频播放。
              </video>
            </article>
          </div>

          <div v-else class="resource-placeholder">
            <Film :size="20" />
            <div>
              <strong>暂无视频资源</strong>
              <span>后续可在媒体清单中添加 MP4 或 WebM 文件。</span>
            </div>
          </div>

          <div v-if="slides.length" class="media-list">
            <a
              v-for="slide in slides"
              :key="slide.id"
              class="media-link"
              :href="slide.url"
              target="_blank"
              rel="noopener"
            >
              <Presentation :size="17" />
              <span>
                <strong>{{ slide.title }}</strong>
                <small>{{ slide.format || '课件' }}</small>
              </span>
              <ExternalLink :size="14" />
            </a>
          </div>

          <div v-else class="resource-placeholder">
            <Presentation :size="20" />
            <div>
              <strong>暂无课件资源</strong>
              <span>后续可添加 PDF、PPT 或 PPTX 文件。</span>
            </div>
          </div>
        </section>

        <nav
          v-if="previous || next"
          class="detail-navigation"
          aria-label="相邻知识点"
        >
          <button
            type="button"
            :disabled="!previous"
            @click="$emit('previous')"
          >
            <ChevronLeft :size="15" />
            <span>
              <small>上一个</small>
              <strong>{{ previous?.name || '已经是第一个' }}</strong>
            </span>
          </button>
          <button
            type="button"
            :disabled="!next"
            @click="$emit('next')"
          >
            <span>
              <small>下一个</small>
              <strong>{{ next?.name || '已经是最后一个' }}</strong>
            </span>
            <ChevronRight :size="15" />
          </button>
        </nav>
      </div>
    </template>
  </dialog>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { LoaderCircle } from '@lucide/vue'
import {
  getNodeName,
  getNodeType,
  RELATION_LABELS,
} from '../constants/graph'

const props = defineProps({
  detail: { type: Object, default: null },
  loading: { type: Boolean, default: false },
  learningPath: { type: Array, default: () => [] },
  learningPathCycle: { type: Boolean, default: false },
  learningPathLoading: { type: Boolean, default: false },
  learningPathError: { type: String, default: '' },
  canGoBack: { type: Boolean, default: false },
  previous: { type: Object, default: null },
  next: { type: Object, default: null },
})

const emit = defineEmits([
  'close',
  'navigate',
  'go-back',
  'previous',
  'next',
])

const dialogElement = ref(null)
const closeButton = ref(null)
const detailContent = ref(null)
let backdropPressed = false
function outsideDialog(event) {
  const bounds = dialogElement.value.getBoundingClientRect()
  return event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom
}
function rememberBackdropPress(event) {
  backdropPressed = event.target === dialogElement.value && outsideDialog(event)
}
function dismissOnBackdrop(event) {
  if (backdropPressed && event.target === dialogElement.value && outsideDialog(event)) emit('close')
  backdropPressed = false
}
onMounted(() => dialogElement.value.showModal())
onBeforeUnmount(() => dialogElement.value?.close())
watch(() => [props.loading, props.detail?.node?.id], async () => {
  await nextTick()
  if (detailContent.value) detailContent.value.scrollTop = 0
  if (!props.loading) closeButton.value?.focus({ preventScroll: true })
})

const properties = computed(() => props.detail?.node?.properties || {})
const nodeName = computed(() => getNodeName(props.detail?.node))
const moduleName = computed(() =>
  props.detail?.module ? getNodeName(props.detail.module) : '未关联模块',
)
const videos = computed(() => props.detail?.materials?.videos || [])
const slides = computed(() => props.detail?.materials?.slides || [])
const pathItems = computed(() =>
  props.learningPath.filter(
    (item) => item.id !== props.detail?.node?.id,
  ),
)
const hasCycle = computed(() =>
  props.learningPathCycle ||
  props.learningPath.some((item) => item.id === props.detail?.node?.id),
)

const relationGroups = computed(() => {
  const groups = new Map()
  for (const relation of props.detail?.relations || []) {
    if (!groups.has(relation.type)) {
      groups.set(relation.type, {
        type: relation.type,
        label: RELATION_LABELS[relation.type] || relation.type,
        items: [],
      })
    }
    groups.get(relation.type).items.push(relation)
  }
  return Array.from(groups.values())
})

function navigateToNode(node, options = {}) {
  const type = node.labels ? getNodeType(node.labels) : 'KnowledgePoint'
  if (type === 'Module') {
    emit('navigate', {
      type,
      id: node.id,
      viewMode: options.path ? 'path' : null,
    })
  } else if (type === 'KnowledgePoint') {
    emit('navigate', {
      type,
      id: node.id,
      moduleId: node.properties?.module_id || node.moduleId,
      viewMode: options.path ? 'path' : null,
    })
  }
}
</script>
