<template>
  <aside
    class="detail-panel"
    :class="{ docked }"
    aria-label="知识点详情"
  >
    <div v-if="loading" class="detail-state">
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
            <ArrowLeft :size="15" />
            返回
          </button>
          <button
            type="button"
            class="icon-button"
            title="关闭详情"
            aria-label="关闭详情"
            @click="$emit('close')"
          >
            <X :size="18" />
          </button>
        </div>
      </header>

      <div class="detail-content">
        <div class="meta-grid">
          <div class="meta-item">
            <Gauge :size="16" />
            <span>难度</span>
            <strong>{{ properties.difficulty || '未标注' }}</strong>
          </div>
          <div class="meta-item">
            <Star :size="16" />
            <span>重要性</span>
            <strong>{{ properties.importance || '未标注' }}</strong>
          </div>
          <div class="meta-item">
            <Tags :size="16" />
            <span>分类</span>
            <strong>{{ properties.subcategory || '未分类' }}</strong>
          </div>
          <div class="meta-item">
            <Network :size="16" />
            <span>所属模块</span>
            <strong>{{ moduleName }}</strong>
          </div>
        </div>

        <section class="content-section">
          <h3><Info :size="15" />知识点说明</h3>
          <p>{{ properties.description || '暂无详细说明。' }}</p>
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
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  ExternalLink,
  Film,
  Gauge,
  Info,
  Link2,
  LoaderCircle,
  Network,
  PlayCircle,
  Presentation,
  Star,
  Tags,
  X,
} from '@lucide/vue'
import {
  getNodeName,
  getNodeType,
  RELATION_LABELS,
} from '../constants/graph'

const props = defineProps({
  detail: { type: Object, default: null },
  loading: { type: Boolean, default: false },
  docked: { type: Boolean, default: false },
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

const properties = computed(() => props.detail?.node?.properties || {})
const nodeName = computed(() => getNodeName(props.detail?.node))
const moduleName = computed(() =>
  props.detail?.module ? getNodeName(props.detail.module) : '未关联模块',
)
const videos = computed(() => props.detail?.materials?.videos || [])
const slides = computed(() => props.detail?.materials?.slides || [])

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

function navigateToNode(node) {
  const type = getNodeType(node.labels)
  if (type === 'Module') {
    emit('navigate', { type, id: node.id })
  } else if (type === 'KnowledgePoint') {
    emit('navigate', {
      type,
      id: node.id,
      moduleId: node.properties.module_id,
    })
  }
}
</script>

<style scoped>
.detail-panel {
  position: absolute;
  z-index: 8;
  top: 14px;
  right: 14px;
  bottom: 14px;
  width: min(410px, calc(100% - 28px));
  border: 1px solid #dfe7f1;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.16);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.detail-panel.docked {
  position: relative;
  z-index: 1;
  top: auto;
  right: auto;
  bottom: auto;
  width: 100%;
  height: 100%;
  border-top: 0;
  border-right: 0;
  border-bottom: 0;
  border-radius: 0;
  box-shadow: none;
}

.detail-header {
  padding: 18px 18px 14px;
  border-bottom: 1px solid #e7edf5;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.detail-header-actions {
  display: flex;
  flex: 0 0 auto;
  align-items: center;
  gap: 6px;
}

.back-detail-button {
  height: 32px;
  padding: 0 8px;
  border: 1px solid #dbe4ef;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 5px;
  color: #475569;
  background: #ffffff;
  cursor: pointer;
  font-size: 10px;
}

.back-detail-button:hover {
  border-color: #93c5fd;
  color: #1d4ed8;
  background: #eff6ff;
}

.title-wrap {
  min-width: 0;
}

.type-badge {
  display: inline-flex;
  padding: 3px 7px;
  border-radius: 4px;
  color: #1d4ed8;
  background: #eff6ff;
  font-size: 11px;
  font-weight: 700;
}

h2 {
  margin: 8px 0 0;
  color: #0f172a;
  font-size: 17px;
  line-height: 1.45;
}

.icon-button {
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 6px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  color: #475569;
  background: #f8fafc;
  cursor: pointer;
}

.icon-button:hover {
  color: #0f172a;
  background: #eef2f7;
}

.detail-content {
  min-height: 0;
  padding: 16px 18px 24px;
  overflow-y: auto;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.meta-item {
  min-width: 0;
  padding: 10px;
  border: 1px solid #e7edf5;
  border-radius: 6px;
  display: grid;
  grid-template-columns: 18px 1fr;
  column-gap: 6px;
  color: #64748b;
  background: #f8fafc;
  font-size: 11px;
}

.meta-item svg {
  grid-row: span 2;
  margin-top: 2px;
  color: #2563eb;
}

.meta-item strong {
  min-width: 0;
  overflow: hidden;
  color: #1e293b;
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.content-section + .content-section {
  margin-top: 20px;
}

.content-section h3 {
  margin: 0 0 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #0f172a;
  font-size: 13px;
}

.content-section p {
  margin: 0;
  color: #475569;
  font-size: 13px;
  line-height: 1.75;
}

.relation-group + .relation-group {
  margin-top: 12px;
}

.relation-label {
  display: block;
  margin-bottom: 5px;
  color: #64748b;
  font-size: 11px;
}

.related-row {
  width: 100%;
  padding: 8px 9px;
  border: 0;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  color: #334155;
  background: #f8fafc;
  cursor: pointer;
  text-align: left;
  font-size: 12px;
}

.related-row + .related-row {
  margin-top: 4px;
}

.related-row:hover {
  color: #1d4ed8;
  background: #eff6ff;
}

.related-row span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.resource-placeholder {
  padding: 11px;
  border: 1px dashed #cbd5e1;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #64748b;
  background: #fbfdff;
}

.resource-placeholder + .resource-placeholder {
  margin-top: 8px;
}

.media-list + .media-list,
.resource-placeholder + .media-list,
.media-list + .resource-placeholder {
  margin-top: 8px;
}

.media-card {
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: #f8fafc;
}

.media-card + .media-card {
  margin-top: 8px;
}

.media-title {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 7px;
  color: #334155;
  font-size: 12px;
}

.media-title svg {
  color: #7c3aed;
}

.video-player {
  display: block;
  width: 100%;
  max-height: 220px;
  border-radius: 5px;
  background: #0f172a;
}

.media-link {
  padding: 10px;
  border: 1px solid #dbe4ef;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 9px;
  color: #334155;
  background: #ffffff;
  text-decoration: none;
}

.media-link + .media-link {
  margin-top: 6px;
}

.media-link:hover {
  border-color: #93c5fd;
  color: #1d4ed8;
  background: #eff6ff;
}

.media-link > svg:first-child {
  flex: 0 0 auto;
  color: #7c3aed;
}

.media-link > svg:last-child {
  flex: 0 0 auto;
  color: #64748b;
}

.media-link span {
  min-width: 0;
  flex: 1;
}

.media-link strong,
.media-link small {
  display: block;
}

.media-link strong {
  overflow: hidden;
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.media-link small {
  margin-top: 2px;
  color: #64748b;
  font-size: 10px;
  text-transform: uppercase;
}

.resource-placeholder > svg {
  flex: 0 0 auto;
  color: #7c3aed;
}

.resource-placeholder div {
  min-width: 0;
}

.resource-placeholder strong,
.resource-placeholder span {
  display: block;
}

.resource-placeholder strong {
  margin-bottom: 2px;
  color: #334155;
  font-size: 12px;
}

.resource-placeholder span {
  font-size: 11px;
  line-height: 1.5;
}

.detail-navigation {
  margin-top: 20px;
  padding-top: 14px;
  border-top: 1px solid #e7edf5;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.detail-navigation button {
  min-width: 0;
  min-height: 56px;
  padding: 8px 9px;
  border: 1px solid #dbe4ef;
  border-radius: 7px;
  display: flex;
  align-items: center;
  gap: 7px;
  color: #475569;
  background: #f8fafc;
  cursor: pointer;
  text-align: left;
}

.detail-navigation button:hover:not(:disabled) {
  border-color: #93c5fd;
  color: #1d4ed8;
  background: #eff6ff;
}

.detail-navigation button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.detail-navigation button span {
  min-width: 0;
  flex: 1;
}

.detail-navigation small,
.detail-navigation strong {
  display: block;
}

.detail-navigation small {
  color: #64748b;
  font-size: 9px;
}

.detail-navigation strong {
  margin-top: 2px;
  overflow: hidden;
  color: #334155;
  font-size: 10px;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #64748b;
  font-size: 13px;
}

.spin {
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 640px) {
  .detail-panel {
    top: 8px;
    right: 8px;
    bottom: 8px;
    width: calc(100% - 16px);
  }

  .meta-grid {
    grid-template-columns: 1fr;
  }
}
</style>
