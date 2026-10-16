<template>
  <aside class="directory-panel">
    <div class="panel-heading">
      <div class="heading-icon">
        <Database :size="18" />
      </div>
      <div>
        <span class="eyebrow">知识目录</span>
        <h2>课程图谱</h2>
      </div>
    </div>

    <div class="directory-summary">
      <span>{{ modules.length }} 个模块</span>
      <span>{{ knowledgePointCount }} 个知识点</span>
    </div>

    <label class="search-box">
      <Search :size="16" />
      <input
        v-model.trim="keyword"
        type="search"
        placeholder="搜索模块或知识点"
        aria-label="搜索模块或知识点"
        @keydown.enter.prevent="locateFirstResult"
      />
    </label>

    <div v-if="loading" class="panel-state">
      <LoaderCircle class="spin" :size="20" />
      <span>正在加载目录</span>
    </div>

    <div v-else-if="filteredModules.length === 0" class="panel-state">
      <Search :size="20" />
      <span>没有匹配结果</span>
    </div>

    <nav v-else class="directory-tree" aria-label="知识图谱目录">
      <div
        v-for="module in filteredModules"
        :key="module.id"
        class="module-group"
      >
        <button
          type="button"
          class="module-row"
          :class="{ active: module.id === selectedModuleId }"
          :aria-expanded="isExpanded(module.id)"
          @click="toggleModule(module)"
        >
          <ChevronRight
            class="chevron"
            :class="{ expanded: isExpanded(module.id) }"
            :size="16"
          />
          <Layers3 :size="16" />
          <span class="module-name">{{ module.name }}</span>
          <span class="item-count">{{ module.knowledgePoints.length }}</span>
          <LoaderCircle
            v-if="loadingModuleId === module.id"
            class="spin"
            :size="14"
          />
        </button>

        <div
          v-if="isExpanded(module.id)"
          class="knowledge-list"
        >
          <button
            v-for="knowledge in module.knowledgePoints"
            :key="knowledge.id"
            type="button"
            class="knowledge-row"
            :class="{ active: knowledge.id === selectedKnowledgePointId }"
            @click="selectKnowledge(module.id, knowledge.id)"
          >
            <FileText :size="14" />
            <i
              class="knowledge-dot"
              :style="{
                background: getDifficultyColor(knowledge.properties),
              }"
            ></i>
            <span class="knowledge-name">{{ knowledge.name }}</span>
            <small
              v-if="knowledge.properties?.importance === '核心'"
              class="importance-badge"
            >
              核心
            </small>
          </button>
        </div>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import {
  ChevronRight,
  Database,
  FileText,
  Layers3,
  LoaderCircle,
  Search,
} from '@lucide/vue'
import { DIFFICULTY_COLORS } from '../constants/graph'

const props = defineProps({
  modules: { type: Array, default: () => [] },
  selectedModuleId: { type: String, default: '' },
  selectedKnowledgePointId: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  loadingModuleId: { type: String, default: '' },
})

const emit = defineEmits(['select-module', 'select-knowledge'])

const keyword = ref('')
const expandedModuleId = ref('')

const knowledgePointCount = computed(() =>
  props.modules.reduce(
    (total, module) => total + module.knowledgePoints.length,
    0,
  ),
)

const filteredModules = computed(() => {
  const query = keyword.value.toLowerCase()
  if (!query) return props.modules

  return props.modules
    .map((module) => {
      const moduleMatches = module.name.toLowerCase().includes(query)
      const matchingKnowledgePoints = module.knowledgePoints.filter(
        (knowledge) => knowledge.name.toLowerCase().includes(query),
      )

      if (moduleMatches) return module
      if (matchingKnowledgePoints.length) {
        return { ...module, knowledgePoints: matchingKnowledgePoints }
      }
      return null
    })
    .filter(Boolean)
})

watch(
  () => props.selectedModuleId,
  (moduleId) => {
    if (moduleId) expandedModuleId.value = moduleId
  },
)

function isExpanded(moduleId) {
  return Boolean(keyword.value) || expandedModuleId.value === moduleId
}

function toggleModule(module) {
  expandedModuleId.value =
    expandedModuleId.value === module.id ? '' : module.id
  emit('select-module', module.id)
}

function selectKnowledge(moduleId, knowledgePointId) {
  emit('select-knowledge', { moduleId, knowledgePointId })
}

function locateFirstResult() {
  const module = filteredModules.value[0]
  if (!module) return
  const knowledge = module.knowledgePoints[0]
  if (knowledge) {
    emit('select-knowledge', {
      moduleId: module.id,
      knowledgePointId: knowledge.id,
    })
    return
  }
  emit('select-module', module.id)
}

function getDifficultyColor(properties = {}) {
  return (
    DIFFICULTY_COLORS[properties.difficulty] ||
    DIFFICULTY_COLORS.未标注
  )
}
</script>

<style scoped>
.directory-panel {
  height: 100%;
  min-height: 0;
  padding: 18px 14px;
  border-right: 1px solid #e2e8f0;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-heading {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 4px;
}

.heading-icon {
  width: 34px;
  height: 34px;
  border-radius: 7px;
  display: grid;
  place-items: center;
  color: #ffffff;
  background: #7c3aed;
}

.eyebrow {
  display: block;
  margin-bottom: 2px;
  color: #64748b;
  font-size: 11px;
}

h2 {
  margin: 0;
  color: #0f172a;
  font-size: 16px;
  line-height: 1.2;
}

.directory-summary {
  display: flex;
  justify-content: space-between;
  margin: 14px 4px 12px;
  color: #64748b;
  font-size: 12px;
}

.search-box {
  height: 38px;
  padding: 0 10px;
  border: 1px solid #d7dee8;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  background: #f8fafc;
}

.search-box:focus-within {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
  background: #ffffff;
}

.search-box input {
  width: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  color: #0f172a;
  background: transparent;
  font-size: 13px;
}

.directory-tree {
  min-height: 0;
  margin-top: 10px;
  padding-right: 2px;
  overflow-y: auto;
}

.module-group + .module-group {
  margin-top: 3px;
}

.module-row,
.knowledge-row {
  width: 100%;
  border: 0;
  display: flex;
  align-items: center;
  color: #334155;
  background: transparent;
  cursor: pointer;
  text-align: left;
}

.module-row {
  min-height: 38px;
  padding: 7px 8px;
  border-radius: 6px;
  gap: 7px;
}

.module-row:hover,
.module-row.active {
  color: #5b21b6;
  background: #f3e8ff;
}

.chevron {
  flex: 0 0 auto;
  transition: transform 0.18s ease;
}

.chevron.expanded {
  transform: rotate(90deg);
}

.module-name {
  min-width: 0;
  flex: 1;
  overflow: hidden;
  font-size: 13px;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-count {
  flex: 0 0 auto;
  color: #64748b;
  font-size: 11px;
}

.knowledge-list {
  margin: 2px 0 6px 24px;
  border-left: 1px solid #e2e8f0;
}

.knowledge-row {
  min-height: 34px;
  padding: 6px 8px;
  border-radius: 0 6px 6px 0;
  gap: 7px;
  font-size: 12px;
  line-height: 1.35;
}

.knowledge-row:hover,
.knowledge-row.active {
  color: #1d4ed8;
  background: #eff6ff;
}

.knowledge-row span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.knowledge-name {
  flex: 1;
}

.knowledge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex: 0 0 auto;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.9);
}

.importance-badge {
  flex: 0 0 auto;
  padding: 1px 4px;
  border-radius: 4px;
  color: #6d28d9;
  background: #f3e8ff;
  font-size: 8px;
  font-weight: 700;
}

.panel-state {
  flex: 1;
  min-height: 160px;
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
</style>
