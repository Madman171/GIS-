<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">
        <div class="brand-mark">
          <Network :size="21" />
        </div>
        <div class="brand-copy">
          <h1>GIS交通路网教学知识图谱平台</h1>
          <span>V1.0 · 课程知识组织与图谱可视化</span>
        </div>
      </div>

      <div class="breadcrumb">
        <Home :size="14" />
        <span>{{ stageTitle }}</span>
      </div>

      <div class="topbar-actions">
        <span class="connection-state" :class="{ error: Boolean(errorMessage) }">
          <i></i>
          {{ graphLoading ? '同步中' : errorMessage ? '连接异常' : 'Neo4j 在线' }}
        </span>
        <button
          type="button"
          class="mobile-button"
          title="打开知识目录"
          aria-label="打开知识目录"
          @click="openLeftPanel"
        >
          <PanelLeft :size="18" />
        </button>
        <button
          type="button"
          class="mobile-button"
          title="打开智能问答"
          aria-label="打开智能问答"
          @click="openChatPanel"
        >
          <MessageSquare :size="18" />
        </button>
      </div>
    </header>

    <div v-if="errorMessage" class="error-banner">
      <AlertCircle :size="16" />
      <span>{{ errorMessage }}</span>
      <button
        type="button"
        title="关闭提示"
        aria-label="关闭提示"
        @click="errorMessage = ''"
      >
        <X :size="15" />
      </button>
    </div>

    <main class="workspace">
      <div
        class="column directory-column"
        :class="{ 'mobile-open': leftOpen }"
      >
        <DirectoryPanel
          :modules="directoryModules"
          :selected-module-id="selectedModuleId"
          :selected-knowledge-point-id="selectedKnowledgePointId"
          :loading="directoryLoading"
          :loading-module-id="loadingModuleId"
          @select-module="selectModule"
          @select-knowledge="selectKnowledgePoint"
        />
      </div>

      <section class="stage">
        <div class="stage-toolbar">
          <div class="stage-title">
            <div class="stage-icon">
              <BookOpen :size="17" />
            </div>
            <div>
              <strong>{{ stageTitle }}</strong>
              <span>{{ stageSubtitle }}</span>
            </div>
          </div>

          <div class="stage-actions">
            <div
              class="view-switch"
              role="group"
              aria-label="图谱查看模式"
            >
              <button
                type="button"
                title="显示完整知识网络"
                :class="{ active: viewMode === 'all' }"
                @click="viewMode = 'all'"
              >
                <Network :size="13" />
                <span>全景</span>
              </button>
              <button
                type="button"
                title="突出当前知识点的直接关系"
                :class="{ active: viewMode === 'focus' }"
                @click="viewMode = 'focus'"
              >
                <Focus :size="13" />
                <span>重点</span>
              </button>
              <button
                type="button"
                title="突出前置学习路径"
                :class="{ active: viewMode === 'path' }"
                @click="viewMode = 'path'"
              >
                <Route :size="13" />
                <span>路径</span>
              </button>
            </div>
            <div class="graph-count">
              <span>{{ graphData.nodes.length }} 节点</span>
              <span>{{ graphData.links.length }} 关系</span>
              <span v-if="graphStats.coreCount">
                {{ graphStats.coreCount }} 核心
              </span>
              <span v-if="graphStats.advancedCount">
                {{ graphStats.advancedCount }} 进阶
              </span>
            </div>
            <button
              type="button"
              class="refresh-button"
              :disabled="graphLoading"
              title="刷新当前数据"
              aria-label="刷新当前数据"
              @click="refreshCurrentData"
            >
              <RefreshCw :size="14" />
              刷新数据
            </button>
            <button
              v-if="selectedModuleId"
              type="button"
              class="back-button"
              @click="backToOverview"
            >
              <RotateCcw :size="14" />
              返回总览
            </button>
          </div>
        </div>

        <div
          class="canvas-shell"
          :class="{ 'detail-open': detailLoading || detail }"
        >
          <div class="graph-view">
            <KnowledgeGraph
              :nodes="graphData.nodes"
              :links="graphData.links"
              :selected-id="selectedKnowledgePointId || selectedModuleId"
              :loading="graphLoading"
              :view-mode="viewMode"
              @node-click="handleGraphNode"
            />
          </div>

          <KnowledgeDetail
            v-if="detailLoading || detail"
            :detail="detail"
            :loading="detailLoading"
            :learning-path="learningPath"
            :learning-path-cycle="learningPathCycle"
            :learning-path-loading="learningPathLoading"
            :learning-path-error="learningPathError"
            :docked="true"
            :can-go-back="knowledgeHistory.length > 0"
            :previous="previousKnowledge"
            :next="nextKnowledge"
            @close="closeDetail"
            @navigate="navigateFromDetail"
            @go-back="goBackKnowledge"
            @previous="navigateRelativeKnowledge('previous')"
            @next="navigateRelativeKnowledge('next')"
          />
        </div>
      </section>

      <div
        class="column chat-column"
        :class="{ 'mobile-open': chatOpen }"
      >
        <ChatPanel
          :messages="chatMessages"
          :loading="chatLoading"
          :configured="chatConfigured"
          @send="sendChat"
          @select-reference="selectChatReference"
        />
      </div>
    </main>

    <button
      v-if="leftOpen || chatOpen"
      type="button"
      class="drawer-backdrop"
      title="关闭面板"
      aria-label="关闭面板"
      @click="closeDrawers"
    ></button>
  </div>
</template>

<script setup>
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
} from 'vue'
import {
  AlertCircle,
  BookOpen,
  Focus,
  Home,
  MessageSquare,
  Network,
  PanelLeft,
  RefreshCw,
  Route,
  RotateCcw,
  X,
} from '@lucide/vue'
import apiClient from './api/client'
import ChatPanel from './components/ChatPanel.vue'
import DirectoryPanel from './components/DirectoryPanel.vue'
import KnowledgeDetail from './components/KnowledgeDetail.vue'
import KnowledgeGraph from './components/KnowledgeGraphRich.vue'
import { getNodeType } from './constants/graph'

const emptyGraph = () => ({ nodes: [], links: [], summary: {} })

const directoryModules = ref([])
const directoryLoading = ref(true)
const overviewGraph = ref(emptyGraph())
const graphData = ref(emptyGraph())
const graphLoading = ref(true)
const errorMessage = ref('')
const viewMode = ref('all')

const selectedModuleId = ref('')
const selectedKnowledgePointId = ref('')
const loadingModuleId = ref('')
const detail = ref(null)
const detailLoading = ref(false)
const learningPath = ref([])
const learningPathCycle = ref(false)
const learningPathLoading = ref(false)
const learningPathError = ref('')
const knowledgeHistory = ref([])

const chatMessages = ref([
  {
    role: 'assistant',
    content:
      '你好，我是课程知识图谱助手。你可以围绕当前知识图谱提出问题，我会依据相关知识点进行回答。',
  },
])
const chatLoading = ref(false)
const chatConfigured = ref(false)
const leftOpen = ref(false)
const chatOpen = ref(false)

const moduleGraphCache = new Map()
const detailCache = new Map()
const learningPathCache = new Map()
let learningPathRequestToken = 0

const selectedModule = computed(() =>
  directoryModules.value.find((module) => module.id === selectedModuleId.value),
)

const stageTitle = computed(() => {
  if (detail.value) return detail.value.node.properties.name || '知识点详情'
  if (selectedModule.value) return selectedModule.value.name
  return '知识图谱总览'
})

const stageSubtitle = computed(() => {
  if (detail.value) return '知识点详情与关联知识'
  if (selectedModule.value) {
    return `${selectedModule.value.knowledgePoints.length} 个知识点`
  }
  return '点击模块查看对应知识点'
})

const graphStats = computed(() => {
  const nodes = graphData.value.nodes || []
  return {
    coreCount: nodes.filter(
      (node) => node.properties?.importance === '核心',
    ).length,
    advancedCount: nodes.filter((node) =>
      ['进阶', '高阶', '高级', '困难'].includes(
        node.properties?.difficulty,
      ),
    ).length,
  }
})

const currentModuleKnowledgePoints = computed(
  () => selectedModule.value?.knowledgePoints || [],
)

const currentKnowledgeIndex = computed(() =>
  currentModuleKnowledgePoints.value.findIndex(
    (item) => item.id === selectedKnowledgePointId.value,
  ),
)

const previousKnowledge = computed(() => {
  const index = currentKnowledgeIndex.value
  if (index <= 0) return null
  return currentModuleKnowledgePoints.value[index - 1]
})

const nextKnowledge = computed(() => {
  const index = currentKnowledgeIndex.value
  if (
    index < 0 ||
    index >= currentModuleKnowledgePoints.value.length - 1
  ) {
    return null
  }
  return currentModuleKnowledgePoints.value[index + 1]
})

function getErrorMessage(error, fallback) {
  return (
    error?.response?.data?.detail ||
    error?.response?.data?.message ||
    error?.message ||
    fallback
  )
}

async function loadDirectory() {
  directoryLoading.value = true
  try {
    const response = await apiClient.get('/api/directory')
    directoryModules.value = response.data.data.modules
  } catch (error) {
    errorMessage.value = getErrorMessage(error, '知识目录加载失败')
  } finally {
    directoryLoading.value = false
  }
}

async function loadModuleOverview() {
  graphLoading.value = true
  try {
    const response = await apiClient.get('/api/graph/modules')
    overviewGraph.value = response.data.data
    graphData.value = response.data.data
  } catch (error) {
    errorMessage.value = getErrorMessage(error, '模块总览加载失败')
  } finally {
    graphLoading.value = false
  }
}

async function loadChatStatus() {
  try {
    const response = await apiClient.get('/api/chat/status')
    chatConfigured.value = Boolean(response.data.data.configured)
    if (!chatConfigured.value) {
      chatMessages.value[0].content =
        '你好，我是课程知识图谱助手。DeepSeek API Key 尚未配置，请在本地 backend/.env 中完成设置。'
    }
  } catch {
    chatConfigured.value = false
  }
}

async function selectModule(moduleId) {
  if (!moduleId) return

  selectedKnowledgePointId.value = ''
  detail.value = null
  learningPath.value = []
  learningPathCycle.value = false
  learningPathLoading.value = false
  learningPathError.value = ''
  learningPathRequestToken += 1
  selectedModuleId.value = moduleId
  loadingModuleId.value = moduleId
  graphLoading.value = true
  errorMessage.value = ''
  leftOpen.value = false

  try {
    if (!moduleGraphCache.has(moduleId)) {
      const response = await apiClient.get(`/api/modules/${moduleId}/graph`)
      moduleGraphCache.set(moduleId, response.data.data)
    }
    graphData.value = moduleGraphCache.get(moduleId)
  } catch (error) {
    errorMessage.value = getErrorMessage(error, '模块知识点加载失败')
  } finally {
    graphLoading.value = false
    loadingModuleId.value = ''
  }
}

async function loadKnowledgePoint(
  knowledgePointId,
  moduleId = '',
  options = {},
) {
  if (!knowledgePointId) return

  const previousId = selectedKnowledgePointId.value
  if (
    options.recordHistory !== false &&
    previousId &&
    previousId !== knowledgePointId
  ) {
    knowledgeHistory.value.push({
      id: previousId,
      moduleId: selectedModuleId.value,
    })
  }

  if (moduleId && moduleId !== selectedModuleId.value) {
    await selectModule(moduleId)
  }

  selectedKnowledgePointId.value = knowledgePointId
  detailLoading.value = true
  learningPath.value = []
  learningPathCycle.value = false
  learningPathError.value = ''
  errorMessage.value = ''
  leftOpen.value = false
  loadLearningPath(knowledgePointId)

  try {
    if (!detailCache.has(knowledgePointId)) {
      const response = await apiClient.get(
        `/api/knowledge-points/${knowledgePointId}`,
      )
      detailCache.set(knowledgePointId, response.data.data)
    }
    detail.value = detailCache.get(knowledgePointId)
  } catch (error) {
    detail.value = null
    errorMessage.value = getErrorMessage(error, '知识点详情加载失败')
  } finally {
    detailLoading.value = false
  }
}

async function loadLearningPath(knowledgePointId) {
  if (!knowledgePointId) {
    learningPath.value = []
    learningPathCycle.value = false
    learningPathLoading.value = false
    return
  }

  const requestToken = ++learningPathRequestToken
  learningPathLoading.value = true
  learningPathError.value = ''

  if (learningPathCache.has(knowledgePointId)) {
    const cached = learningPathCache.get(knowledgePointId)
    learningPath.value = cached.path
    learningPathCycle.value = cached.hasCycle
    learningPathLoading.value = false
    return
  }

  try {
    const response = await apiClient.get(
      `/api/knowledge-points/${knowledgePointId}/learning-path`,
    )
    if (requestToken !== learningPathRequestToken) return
    const path = response.data.data.path || []
    const hasCycle = Boolean(response.data.data.hasCycle)
    learningPathCache.set(knowledgePointId, { path, hasCycle })
    learningPath.value = path
    learningPathCycle.value = hasCycle
  } catch (error) {
    if (requestToken !== learningPathRequestToken) return
    learningPath.value = []
    learningPathCycle.value = false
    learningPathError.value = getErrorMessage(
      error,
      '学习路径暂时无法加载',
    )
  } finally {
    if (requestToken === learningPathRequestToken) {
      learningPathLoading.value = false
    }
  }
}

async function selectKnowledgePoint({ moduleId, knowledgePointId }) {
  await loadKnowledgePoint(knowledgePointId, moduleId)
}

function handleGraphNode(node) {
  const type = getNodeType(node.labels)
  if (type === 'Module') {
    selectModule(node.id)
  } else if (type === 'KnowledgePoint') {
    loadKnowledgePoint(node.id)
  }
}

function closeDetail() {
  detail.value = null
  selectedKnowledgePointId.value = ''
  learningPath.value = []
  learningPathCycle.value = false
  learningPathLoading.value = false
  learningPathError.value = ''
  learningPathRequestToken += 1
}

function goBackKnowledge() {
  const previous = knowledgeHistory.value.pop()
  if (!previous) return
  loadKnowledgePoint(previous.id, previous.moduleId, {
    recordHistory: false,
  })
}

function navigateRelativeKnowledge(direction) {
  const target =
    direction === 'previous' ? previousKnowledge.value : nextKnowledge.value
  if (!target) return
  loadKnowledgePoint(target.id, selectedModuleId.value)
}

function backToOverview() {
  selectedModuleId.value = ''
  selectedKnowledgePointId.value = ''
  detail.value = null
  learningPath.value = []
  learningPathCycle.value = false
  learningPathLoading.value = false
  learningPathError.value = ''
  learningPathRequestToken += 1
  graphData.value = overviewGraph.value
  graphLoading.value = false
  leftOpen.value = false
  knowledgeHistory.value = []
}

async function refreshCurrentData(options = {}) {
  const silent = Boolean(options.silent)
  if (!silent) graphLoading.value = true
  errorMessage.value = ''

  try {
    const directoryResponse = await apiClient.get('/api/directory')
    directoryModules.value = directoryResponse.data.data.modules

    if (selectedModuleId.value) {
      const moduleResponse = await apiClient.get(
        `/api/modules/${selectedModuleId.value}/graph`,
      )
      moduleGraphCache.set(selectedModuleId.value, moduleResponse.data.data)
      graphData.value = moduleResponse.data.data
    } else {
      const overviewResponse = await apiClient.get('/api/graph/modules')
      overviewGraph.value = overviewResponse.data.data
      graphData.value = overviewResponse.data.data
    }

    if (selectedKnowledgePointId.value) {
      const detailResponse = await apiClient.get(
        `/api/knowledge-points/${selectedKnowledgePointId.value}`,
      )
      detailCache.set(
        selectedKnowledgePointId.value,
        detailResponse.data.data,
      )
      detail.value = detailResponse.data.data
      learningPathCache.delete(selectedKnowledgePointId.value)
      loadLearningPath(selectedKnowledgePointId.value)
    }
  } catch (error) {
    if (!silent) {
      errorMessage.value = getErrorMessage(error, '刷新平台数据失败')
    }
  } finally {
    if (!silent) graphLoading.value = false
  }
}

function handleWindowFocus() {
  if (document.visibilityState === 'visible') {
    refreshCurrentData({ silent: true })
  }
}

function navigateFromDetail({ type, id, moduleId }) {
  if (type === 'Module') {
    selectModule(id)
  } else if (type === 'KnowledgePoint') {
    loadKnowledgePoint(id, moduleId || selectedModuleId.value)
  }
}

async function sendChat(question) {
  chatMessages.value.push({ role: 'user', content: question })
  chatLoading.value = true

  try {
    const response = await apiClient.post('/api/chat', {
      question,
      module_id: selectedModuleId.value || null,
      knowledge_point_id: selectedKnowledgePointId.value || null,
    })
    chatMessages.value.push({
      role: 'assistant',
      content: response.data.answer,
      references: response.data.references || [],
    })
  } catch (error) {
    chatMessages.value.push({
      role: 'assistant',
      content: getErrorMessage(
        error,
        '智能问答暂时不可用，请稍后再试。',
      ),
    })
  } finally {
    chatLoading.value = false
  }
}

function selectChatReference(reference) {
  if (reference.type === 'Module') {
    selectModule(reference.id)
    return
  }
  if (reference.type === 'KnowledgePoint') {
    loadKnowledgePoint(reference.id, reference.moduleId || '')
  }
}

function openLeftPanel() {
  chatOpen.value = false
  leftOpen.value = true
}

function openChatPanel() {
  leftOpen.value = false
  chatOpen.value = true
}

function closeDrawers() {
  leftOpen.value = false
  chatOpen.value = false
}

onMounted(() => {
  Promise.all([
    loadDirectory(),
    loadModuleOverview(),
    loadChatStatus(),
  ])
  window.addEventListener('focus', handleWindowFocus)
})

onBeforeUnmount(() => {
  window.removeEventListener('focus', handleWindowFocus)
})
</script>

<style scoped>
.app-shell {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  color: #1f2937;
  background: #f5f7fa;
  overflow: hidden;
}

.topbar {
  min-height: 64px;
  padding: 0 18px;
  border-bottom: 1px solid #dfe7f1;
  display: grid;
  grid-template-columns: minmax(320px, 1fr) auto minmax(260px, 1fr);
  align-items: center;
  gap: 18px;
  background: #ffffff;
}

.brand {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-mark {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  color: #ffffff;
  background: #7c3aed;
}

.brand-copy {
  min-width: 0;
}

.brand-copy h1 {
  margin: 0 0 2px;
  overflow: hidden;
  color: #0f172a;
  font-size: 16px;
  line-height: 1.3;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.brand-copy span {
  display: block;
  color: #64748b;
  font-size: 11px;
}

.breadcrumb {
  max-width: 360px;
  padding: 6px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #475569;
  background: #f8fafc;
  font-size: 12px;
}

.breadcrumb span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.topbar-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.connection-state {
  padding: 5px 8px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #166534;
  background: #f0fdf4;
  font-size: 11px;
  white-space: nowrap;
}

.connection-state i {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
}

.connection-state.error {
  color: #991b1b;
  background: #fef2f2;
}

.connection-state.error i {
  background: #ef4444;
}

.mobile-button {
  width: 34px;
  height: 34px;
  padding: 0;
  border: 1px solid #dbe4ef;
  border-radius: 6px;
  display: none;
  place-items: center;
  color: #475569;
  background: #ffffff;
  cursor: pointer;
}

.error-banner {
  min-height: 38px;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #991b1b;
  background: #fef2f2;
  border-bottom: 1px solid #fecaca;
  font-size: 12px;
}

.error-banner span {
  flex: 1;
}

.error-banner button {
  width: 26px;
  height: 26px;
  padding: 0;
  border: 0;
  border-radius: 5px;
  display: grid;
  place-items: center;
  color: #991b1b;
  background: transparent;
  cursor: pointer;
}

.workspace {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 292px minmax(0, 1fr) 366px;
  overflow: hidden;
}

.column {
  min-width: 0;
  min-height: 0;
}

.stage {
  min-width: 0;
  min-height: 0;
  padding: 14px;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
  overflow: hidden;
}

.stage-toolbar {
  min-height: 46px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.stage-title {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 9px;
}

.stage-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  color: #1d4ed8;
  background: #eff6ff;
}

.stage-title strong,
.stage-title span {
  display: block;
}

.stage-title strong {
  max-width: 520px;
  overflow: hidden;
  color: #0f172a;
  font-size: 14px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stage-title span {
  margin-top: 2px;
  color: #64748b;
  font-size: 11px;
}

.stage-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.graph-count {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #64748b;
  font-size: 11px;
  white-space: nowrap;
}

.graph-count span {
  padding: 4px 6px;
  border: 1px solid #e2e8f0;
  border-radius: 5px;
  background: #ffffff;
}

.view-switch {
  height: 32px;
  padding: 3px;
  border: 1px solid #dbe4ef;
  border-radius: 7px;
  display: flex;
  align-items: center;
  gap: 2px;
  background: #f8fafc;
}

.view-switch button {
  height: 24px;
  padding: 0 7px;
  border: 0;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 4px;
  color: #64748b;
  background: transparent;
  cursor: pointer;
  font-size: 10px;
}

.view-switch button:hover {
  color: #1d4ed8;
}

.view-switch button.active {
  color: #1d4ed8;
  background: #ffffff;
  box-shadow: 0 2px 7px rgba(15, 23, 42, 0.1);
}

.back-button,
.refresh-button {
  height: 34px;
  padding: 0 10px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #334155;
  background: #ffffff;
  cursor: pointer;
  font-size: 11px;
}

.back-button:hover,
.refresh-button:hover {
  border-color: #93c5fd;
  color: #1d4ed8;
}

.refresh-button:disabled {
  cursor: wait;
  opacity: 0.55;
}

.canvas-shell {
  position: relative;
  flex: 1;
  min-height: 0;
  border: 1px solid #dfe7f1;
  border-radius: 8px;
  background: #ffffff;
  overflow: hidden;
}

.canvas-shell.detail-open {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(340px, 390px);
}

.graph-view {
  width: 100%;
  height: 100%;
  min-width: 0;
  min-height: 0;
}

.drawer-backdrop {
  position: fixed;
  z-index: 30;
  inset: 64px 0 0;
  border: 0;
  background: rgba(15, 23, 42, 0.34);
}

@media (max-width: 1320px) {
  .workspace {
    grid-template-columns: 260px minmax(0, 1fr) 332px;
  }

  .brand-copy span {
    display: none;
  }
}

@media (max-width: 1380px) {
  .canvas-shell.detail-open {
    display: block;
  }

  :deep(.detail-panel.docked) {
    position: absolute;
    z-index: 8;
    top: 14px;
    right: 14px;
    bottom: 14px;
    width: min(410px, calc(100% - 28px));
    height: auto;
    border: 1px solid #dfe7f1;
    border-radius: 8px;
    box-shadow: 0 18px 50px rgba(15, 23, 42, 0.16);
  }
}

@media (max-width: 1100px) {
  .topbar {
    grid-template-columns: minmax(260px, 1fr) auto;
  }

  .breadcrumb {
    display: none;
  }

  .mobile-button {
    display: grid;
  }

  .workspace {
    grid-template-columns: 250px minmax(0, 1fr);
  }

  .chat-column {
    position: fixed;
    z-index: 40;
    top: 64px;
    right: 0;
    bottom: 0;
    width: min(92vw, 360px);
    box-shadow: -18px 0 40px rgba(15, 23, 42, 0.16);
    transform: translateX(105%);
    transition: transform 0.22s ease;
  }

  .chat-column.mobile-open {
    transform: translateX(0);
  }
}

@media (max-width: 760px) {
  .topbar {
    position: relative;
    grid-template-columns: minmax(0, 1fr) auto;
    min-height: 58px;
    padding: 0 88px 0 10px;
    gap: 8px;
  }

  .brand-mark {
    width: 34px;
    height: 34px;
  }

  .brand-copy h1 {
    max-width: 210px;
    font-size: 14px;
  }

  .topbar-actions {
    position: absolute;
    top: 11px;
    right: 10px;
  }

  .connection-state {
    display: none;
  }

  .workspace {
    display: block;
  }

  .directory-column {
    position: fixed;
    z-index: 40;
    top: 58px;
    left: 0;
    bottom: 0;
    width: min(88vw, 300px);
    box-shadow: 18px 0 40px rgba(15, 23, 42, 0.16);
    transform: translateX(-105%);
    transition: transform 0.22s ease;
  }

  .directory-column.mobile-open {
    transform: translateX(0);
  }

  .stage {
    width: 100%;
    height: 100%;
    padding: 8px;
  }

  .stage-toolbar {
    min-height: 42px;
    margin-bottom: 7px;
  }

  .graph-count {
    display: none;
  }

  .view-switch button {
    padding: 0 6px;
  }

  .view-switch button span {
    display: none;
  }

  .stage-title strong {
    max-width: 220px;
  }

  .drawer-backdrop {
    inset: 58px 0 0;
  }

  .chat-column {
    top: 58px;
  }
}
</style>
