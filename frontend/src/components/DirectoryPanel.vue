<template>
  <aside class="directory-panel">
    <div class="panel-heading">
      <div>
        <span class="eyebrow">知识目录</span>
        <h2>课程图谱</h2>
      </div>
    </div>


    <label class="search-box">
      <input
        v-model.trim="keyword"
        type="search"
        placeholder="搜索模块或知识点"
        aria-label="搜索模块或知识点"
        @keydown.enter.prevent="locateFirstResult"
      />
    </label>

    <button
      v-if="!loading"
      type="button"
      class="course-overview-row"
      :class="{ active: courseOverview }"
      :aria-current="courseOverview ? 'page' : undefined"
      @click="$emit('select-course')"
    >全部知识点</button>

    <div v-if="loading" class="panel-state">
      <LoaderCircle class="spin" :size="20" />
      <span>正在加载目录</span>
    </div>

    <div v-else-if="filteredModules.length === 0" class="panel-state">

      <span>没有匹配结果</span>
    </div>

    <nav v-else class="directory-tree" aria-label="知识图谱目录">
      <div
        v-for="module in filteredModules"
        :key="module.id"
        class="module-group"
        :style="{ '--module-tint': getModuleAppearance(module.id).tint, '--module-ink': getModuleAppearance(module.id).ink, '--module-color': getModuleAppearance(module.id).color }"
      >
        <button
          type="button"
          class="module-row"
          :class="{ active: module.id === selectedModuleId }"
          :aria-expanded="isExpanded(module.id)"
          @click="toggleModule(module)"
        >
          <span class="module-tag" aria-hidden="true">模块</span>
          <span class="module-copy">
            <span class="module-name">{{ module.name }}</span>
            <span v-if="MODULE_SUMMARIES[module.id]" class="module-summary">{{ MODULE_SUMMARIES[module.id] }}</span>
          </span>
          <span class="chevron" :class="{ expanded: isExpanded(module.id) }" aria-hidden="true">›</span>
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
import { LoaderCircle } from '@lucide/vue'
import { DIFFICULTY_COLORS, getModuleAppearance, MODULE_SUMMARIES } from '../constants/graph'

const props = defineProps({
  modules: { type: Array, default: () => [] },
  selectedModuleId: { type: String, default: '' },
  selectedKnowledgePointId: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  loadingModuleId: { type: String, default: '' },
  courseOverview: { type: Boolean, default: false },
})

const emit = defineEmits(['select-module', 'select-knowledge', 'select-course'])

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
