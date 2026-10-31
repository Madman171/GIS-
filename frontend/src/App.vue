<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">
        <div class="brand-copy">
          <h1><span class="brand-initial">GIS</span><span class="brand-name">交通路网教学知识图谱平台</span></h1>
          <span>V1.0 · 课程知识组织与图谱可视化</span>
        </div>
      </div>

      <div class="breadcrumb" aria-label="当前位置">
        <span>{{ stageTitle }}</span>
      </div>

      <div class="topbar-actions">
        <span class="connection-state" :class="{ error: Boolean(errorMessage) }">
          <i></i>
          {{ graphLoading ? '同步中' : errorMessage ? '连接异常' : isDesignPreview ? '本地快照预览' : 'Neo4j 在线' }}
        </span>
        <button
          type="button"
          class="mobile-button"
          title="打开知识目录"
          aria-label="打开知识目录"
          @click="openLeftPanel"
        >
          目录
        </button>
      </div>
    </header>

    <div v-if="errorMessage" class="error-banner">

      <span>{{ errorMessage }}</span>
      <button
        type="button"
        title="关闭提示"
        aria-label="关闭提示"
        @click="errorMessage = ''"
      >
        <span aria-hidden="true">×</span>
      </button>
    </div>

    <main class="workspace">
      <div
        class="column directory-column"
        :class="{ 'mobile-open': leftOpen }"
        :inert="isCompact && !leftOpen"
      >
        <DirectoryPanel
          :modules="directoryModules"
          :selected-module-id="selectedModuleId"
          :selected-knowledge-point-id="selectedKnowledgePointId"
          :loading="directoryLoading"
          :loading-module-id="loadingModuleId"
          :course-overview="graphScope === 'course'"
          @select-course="selectCourseOverview"
          @select-module="selectModule"
          @select-knowledge="selectKnowledgePoint"
        />
      </div>

      <section class="stage">
        <div class="stage-toolbar">
          <div class="stage-title">
            <div>
              <strong>{{ detail && selectedModule ? selectedModule.name : stageTitle }}</strong>
              <span v-if="!selectedModuleId">{{ stageSubtitle }}</span>
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
                <span>全景</span>
              </button>
              <button
                type="button"
                title="突出当前知识点的直接关系"
                :class="{ active: viewMode === 'focus' }"
                @click="viewMode = 'focus'"
              >
                <span>重点</span>
              </button>
              <button
                type="button"
                title="突出前置学习路径"
                :class="{ active: viewMode === 'path' }"
                @click="viewMode = 'path'"
              >
                <span>路径</span>
              </button>
            </div>
            <button
              type="button"
              class="refresh-button"
              :disabled="graphLoading"
              title="刷新当前数据"
              aria-label="刷新当前数据"
              @click="refreshCurrentData"
            >
              刷新数据
            </button>
            <button
              v-if="selectedModuleId || graphScope === 'course'"
              type="button"
              class="back-button"
              @click="backToOverview"
            >
              返回总览
            </button>
          </div>
        </div>

        <div class="canvas-shell">
          <div class="graph-view">
            <KnowledgeGraph
              :nodes="graphData.nodes"
              :links="graphData.links"
              :selected-id="selectedKnowledgePointId || selectedModuleId"
              :loading="graphLoading"
              :view-mode="viewMode"
              :course-overview="graphScope === 'course'"
              @node-click="handleGraphNode"
            />
          </div>

          <Teleport to="body">
          <KnowledgeDetail
            v-if="detailLoading || detail"
            :detail="detail"
            :loading="detailLoading"
            :learning-path="learningPath"
            :learning-path-cycle="learningPathCycle"
            :learning-path-loading="learningPathLoading"
            :learning-path-error="learningPathError"
            :can-go-back="knowledgeHistory.length > 0"
            :previous="previousKnowledge"
            :next="nextKnowledge"
            @close="closeDetail"
            @navigate="navigateFromDetail"
            @go-back="goBackKnowledge"
            @previous="navigateRelativeKnowledge('previous')"
            @next="navigateRelativeKnowledge('next')"
          />
          </Teleport>
        </div>
      </section>

      <AIPet
        :messages="chatMessages"
        :loading="chatLoading"
        :configured="chatConfigured"
        :suggestion="petSuggestion"
        @send="sendChat"
        @select-reference="selectChatReference"
        @dismiss-suggestion="dismissPetSuggestion"
        @suggestion-action="handlePetSuggestionAction"
      />
    </main>

    <button
      v-if="leftOpen"
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

import apiClient from './api/client'
import AIPet from './components/AIPet.vue'
import DirectoryPanel from './components/DirectoryPanel.vue'
import KnowledgeDetail from './components/KnowledgeDetail.vue'
import KnowledgeGraph from './components/KnowledgeGraphRich.vue'
import { getNodeType } from './constants/graph'
import { ASSISTANT_NAME } from './constants/assistant'

const emptyGraph = () => ({ nodes: [], links: [], summary: {} })
const isDesignPreview = Boolean(window.__GIS_DESIGN_PREVIEW__)

const directoryModules = ref([])
const directoryLoading = ref(true)
const overviewGraph = ref(emptyGraph())
const courseGraph = ref(null)
const graphScope = ref('modules')
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
      `你好，我是${ASSISTANT_NAME}，你的课程图谱小助手。你可以围绕当前知识图谱提出问题，我会依据相关知识点进行回答。`,
  },
])
const chatLoading = ref(false)
const chatConfigured = ref(false)
const leftOpen = ref(false)
const isCompact = ref(window.innerWidth <= 1100)
function syncCompactLayout() {
  isCompact.value = window.innerWidth <= 1100
}
const petSuggestion = ref(null)
const lastPetSuggestionAt = ref(0)
const PET_SUGGESTION_COOLDOWN = 45000

const moduleGraphCache = new Map()
const detailCache = new Map()
const learningPathCache = new Map()
let learningPathRequestToken = 0
let detailRequestToken = 0
let graphRequestToken = 0

const selectedModule = computed(() =>
  directoryModules.value.find((module) => module.id === selectedModuleId.value),
)

const stageTitle = computed(() => {
  if (graphScope.value === 'course') return '全部知识点'
  if (detail.value) return detail.value.node.properties.name || '知识点详情'
  if (selectedModule.value) return selectedModule.value.name
  return '知识图谱总览'
})

const stageSubtitle = computed(() => {
  if (graphScope.value === 'course') return '放大探索知识关系，点击节点查看详情'
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
  () => (graphScope.value === 'course'
    ? directoryModules.value.find(module => module.knowledgePoints.some(point => point.id === selectedKnowledgePointId.value))
    : selectedModule.value)?.knowledgePoints || [],
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
  const requestToken = ++graphRequestToken
  graphLoading.value = true
  try {
    const response = await apiClient.get('/api/graph/modules')
    overviewGraph.value = response.data.data
    if (requestToken === graphRequestToken) graphData.value = response.data.data
  } catch (error) {
    if (requestToken === graphRequestToken) errorMessage.value = getErrorMessage(error, '模块总览加载失败')
  } finally {
    if (requestToken === graphRequestToken) graphLoading.value = false
  }
}

async function selectCourseOverview() {
  const requestToken = ++graphRequestToken
  closeDetail()
  knowledgeHistory.value = []
  selectedModuleId.value = ''
  graphScope.value = 'course'
  viewMode.value = 'all'
  leftOpen.value = false
  loadingModuleId.value = ''
  graphLoading.value = true
  errorMessage.value = ''
  try {
    if (!courseGraph.value) {
      const response = await apiClient.get('/api/graph/all')
      if (requestToken !== graphRequestToken) return
      courseGraph.value = response.data.data
    }
    if (requestToken === graphRequestToken) graphData.value = courseGraph.value
  } catch (error) {
    if (requestToken === graphRequestToken) errorMessage.value = getErrorMessage(error, '全部知识点加载失败')
  } finally {
    if (requestToken === graphRequestToken) graphLoading.value = false
  }
}

async function loadChatStatus() {
  try {
    const response = await apiClient.get('/api/chat/status')
    chatConfigured.value = Boolean(response.data.data.configured)
    if (!chatConfigured.value) {
      chatMessages.value[0].content =
        `你好，我是${ASSISTANT_NAME}，你的课程图谱小助手。问答服务暂未连接，你可以先浏览图谱和知识点。`
    }
  } catch {
    chatConfigured.value = false
  }
}

async function selectModule(moduleId) {
  if (!moduleId) return

  const requestToken = ++graphRequestToken
  graphScope.value = 'module'
  detailRequestToken += 1
  detailLoading.value = false
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
    if (requestToken === graphRequestToken) graphData.value = moduleGraphCache.get(moduleId)
  } catch (error) {
    if (requestToken === graphRequestToken) errorMessage.value = getErrorMessage(error, '模块知识点加载失败')
  } finally {
    if (requestToken !== graphRequestToken) return
    graphLoading.value = false
    loadingModuleId.value = ''
    offerPetSuggestion({
      id: `module-${moduleId}`,
      text: '先点一个知识点吧，我可以帮你整理它的前置学习顺序。',
    })
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

  if (graphScope.value !== 'course' && moduleId && moduleId !== selectedModuleId.value) {
    await selectModule(moduleId)
  }

  selectedKnowledgePointId.value = knowledgePointId
  const requestToken = ++detailRequestToken
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
    if (requestToken === detailRequestToken) detail.value = detailCache.get(knowledgePointId)
  } catch (error) {
    if (requestToken === detailRequestToken) {
      detail.value = null
      errorMessage.value = getErrorMessage(error, '知识点详情加载失败')
    }
  } finally {
    if (requestToken === detailRequestToken) detailLoading.value = false
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
    offerKnowledgePathSuggestion(cached.path.length)
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
    offerKnowledgePathSuggestion(path.length)
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
  detailRequestToken += 1
  detailLoading.value = false
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
  graphRequestToken += 1
  graphScope.value = 'modules'
  detailRequestToken += 1
  detailLoading.value = false
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
  const requestToken = ++graphRequestToken
  const scope = graphScope.value
  const moduleId = selectedModuleId.value
  const silent = Boolean(options.silent)
  if (!silent) graphLoading.value = true
  errorMessage.value = ''

  try {
    const directoryResponse = await apiClient.get('/api/directory')
    if (requestToken !== graphRequestToken) return
    directoryModules.value = directoryResponse.data.data.modules
    if (scope === 'course') {
      const response = await apiClient.get('/api/graph/all')
      if (requestToken !== graphRequestToken) return
      courseGraph.value = response.data.data
      graphData.value = response.data.data
    } else if (moduleId) {
      const moduleResponse = await apiClient.get(
        `/api/modules/${moduleId}/graph`,
      )
      if (requestToken !== graphRequestToken) return
      moduleGraphCache.set(moduleId, moduleResponse.data.data)
      graphData.value = moduleResponse.data.data
    } else {
      const overviewResponse = await apiClient.get('/api/graph/modules')
      if (requestToken !== graphRequestToken) return
      overviewGraph.value = overviewResponse.data.data
      graphData.value = overviewResponse.data.data
    }

    if (selectedKnowledgePointId.value) {
      const knowledgeId = selectedKnowledgePointId.value
      const detailToken = detailRequestToken
      const detailResponse = await apiClient.get(
        `/api/knowledge-points/${knowledgeId}`,
      )
      if (requestToken !== graphRequestToken || detailToken !== detailRequestToken || selectedKnowledgePointId.value !== knowledgeId) return
      detailCache.set(
        knowledgeId,
        detailResponse.data.data,
      )
      detail.value = detailResponse.data.data
      learningPathCache.delete(knowledgeId)
      loadLearningPath(knowledgeId)
    }
  } catch (error) {
    if (!silent && requestToken === graphRequestToken) {
      errorMessage.value = getErrorMessage(error, '刷新平台数据失败')
    }
  } finally {
    if (requestToken === graphRequestToken) graphLoading.value = false
  }
}

function handleWindowFocus() {
  if (document.visibilityState === 'visible') {
    refreshCurrentData({ silent: true })
  }
}

function navigateFromDetail({ type, id, moduleId, viewMode: requestedViewMode }) {
  if (requestedViewMode) viewMode.value = requestedViewMode
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
      source: 'ai_pet',
      event_type: 'pet_chat',
      view_mode: viewMode.value,
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

function offerKnowledgePathSuggestion(pathLength) {
  if (pathLength > 0) {
    offerPetSuggestion({
      id: `path-${selectedKnowledgePointId.value}`,
      text: `我发现这个知识点有 ${pathLength} 个前置内容，要打开学习路径吗？`,
      action: 'path',
      actionLabel: '查看学习路径',
    })
  } else {
    offerPetSuggestion({
      id: `direct-${selectedKnowledgePointId.value}`,
      text: '这个知识点暂时没有前置关系，可以直接开始学习。',
    })
  }
}

function offerPetSuggestion(suggestion) {
  const now = Date.now()
  if (now - lastPetSuggestionAt.value < PET_SUGGESTION_COOLDOWN) return
  lastPetSuggestionAt.value = now
  petSuggestion.value = suggestion
}

function dismissPetSuggestion() {
  petSuggestion.value = null
}

function handlePetSuggestionAction(action) {
  if (action === 'path') viewMode.value = 'path'
  petSuggestion.value = null
}

function openLeftPanel() {
  leftOpen.value = true
}

function closeDrawers() {
  leftOpen.value = false
}

onMounted(() => {
  window.addEventListener('resize', syncCompactLayout)
  Promise.all([
    loadDirectory(),
    loadModuleOverview(),
    loadChatStatus(),
  ])
  window.addEventListener('focus', handleWindowFocus)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', syncCompactLayout)
  window.removeEventListener('focus', handleWindowFocus)
})
</script>
