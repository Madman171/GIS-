<template>
  <section v-if="lessons.length" class="teaching-section" :class="`teaching-${context}`" aria-label="教学讲解">
    <header class="teaching-section-header"><component :is="context === 'chapter' ? 'h2' : 'h3'">{{ context === 'chapter' ? '本关教学' : '教学讲解' }}</component><p>{{ context === 'chapter' ? '按顺序阅读，遇到思考题先判断，再展开解析。' : '结合例子理解本知识点，再查看解析检验思路。' }}</p></header>
    <details v-for="(lesson, index) in lessons" :key="`${chapterId || knowledgePointId}-${lesson.id}`" class="teaching-unit" :open="index === 0">
      <summary><span class="teaching-unit-title">{{ lesson.title }}</span><span class="teaching-unit-meta">{{ lesson.level }} · 约{{ lesson.readingTime }}</span></summary>
      <article class="teaching-article" :aria-label="lesson.title">
        <TeachingBlocks :blocks="lesson.blocks" :heading-base="context === 'chapter' ? 3 : 4" />
        <details v-if="!lesson.embeddedSources" class="teaching-sources"><summary>查阅依据</summary><ul><li v-for="source in lesson.sources" :key="source.id"><a :href="source.url" target="_blank" rel="noopener noreferrer">{{ source.title }}</a><span>{{ source.section }} · {{ source.version_or_date }}</span></li></ul></details>
      </article>
    </details>
    <p class="teaching-estimate">阅读时间为估计，包含看图与思考；自测用于理解，不计入章节成绩。</p>
  </section>
</template>
<script setup>
import { computed } from 'vue'
import registry from '../teaching/content.json'
import { parseMarkdown } from '../teaching/markdown'
import TeachingBlocks from './TeachingBlocks.vue'
import '../teaching/teaching.css'
const props = defineProps({ knowledgePointId: { type: String, default: '' }, chapterId: { type: String, default: '' }, context: { type: String, default: 'knowledge' } })
const sourceMap = new Map(registry.sources.map(s => [s.id, s]))
const parsed = new Map(registry.lessons.map(l => [l.id, { ...l, blocks: parseMarkdown(l.markdown), sources: l.sourceIds.map(id => sourceMap.get(id)) }]))
const lessons = computed(() => (props.chapterId ? registry.chapterLessons[props.chapterId] || [] : registry.knowledgePointLessons[props.knowledgePointId] || []).map(id => parsed.get(id)).filter(Boolean))
</script>
