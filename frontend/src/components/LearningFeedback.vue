<template>
  <section class="answer-feedback" :class="result.correct ? 'is-correct' : 'is-incorrect'" :aria-label="`${result.correct ? '回答正确' : '需要再想想'}，答案与解析`">
    <div class="feedback-heading"><strong>{{ result.correct ? '回答正确' : '需要再想想' }}</strong><span>正确答案：{{ formatAnswer(result.correct_answer, question.type) }}</span></div>
    <p>{{ result.explanation }}</p>
    <details v-if="Object.keys(result.option_feedback || {}).length"><summary>逐项解析</summary><ul><li v-for="(text, option) in result.option_feedback" :key="option"><strong>{{ option }}</strong> {{ text }}</li></ul></details>
    <details v-if="result.sources?.length"><summary>查阅依据</summary><ul class="source-list"><li v-for="source in result.sources" :key="source.id"><a v-if="safeLink(source.url)" :href="source.url" target="_blank" rel="noopener noreferrer">{{ source.title }} ↗</a><span v-else>{{ source.title }}</span><small>{{ source.section }} · {{ source.support }}</small></li></ul></details>
    <button type="button" class="learning-text-button" @click="$emit('open-knowledge', question.main_knowledge_point.id)">回看知识点：{{ question.main_knowledge_point.name }}</button>
  </section>
</template>
<script setup>
import { formatAnswer } from '../learning/progress'
defineProps({ result: { type: Object, required: true }, question: { type: Object, required: true } })
defineEmits(['open-knowledge'])
function safeLink(value) { try { return new URL(value).protocol === 'https:' } catch { return false } }
</script>
