<template>
  <article :id="`question-${question.id}`" class="learning-question">
    <div class="question-caption"><span>{{ index + 1 }} / {{ total }} · {{ labels[question.type] }}</span><span v-if="question.category === 'exam'">20 分</span></div>
    <fieldset :disabled="disabled"><legend>{{ question.stem }}</legend>
      <LearningDiagram v-if="question.diagram" :diagram="question.diagram" />
      <p v-if="question.type === 'multiple'" :id="`${question.id}-rule`" class="question-rule">选出全部正确项，多选、漏选或错选均不得分。</p>
      <div v-if="question.type === 'single' || question.type === 'multiple'" class="answer-options">
        <label v-for="option in question.options" :key="option.id" class="answer-option" :class="{ selected: selected(option.id) }">
          <input :type="question.type === 'multiple' ? 'checkbox' : 'radio'" :name="question.id" :value="option.id" :checked="selected(option.id)" :aria-describedby="question.type === 'multiple' ? `${question.id}-rule` : undefined" @change="choose(option.id, $event.target.checked)" />
          <span class="option-key">{{ option.id }}</span><span>{{ option.text }}</span>
        </label>
      </div>
      <div v-else-if="question.type === 'true_false'" class="answer-options boolean-options">
        <label v-for="value in [true, false]" :key="String(value)" class="answer-option" :class="{ selected: modelValue === value }"><input type="radio" :name="question.id" :checked="modelValue === value" @change="$emit('update:modelValue', value)" /><span>{{ value ? '正确' : '错误' }}</span></label>
      </div>
      <div v-else class="numeric-answer"><label :for="`${question.id}-input`">你的答案（{{ units[question.numeric.unit] || question.numeric.unit }}）</label><div><input :id="`${question.id}-input`" type="text" inputmode="decimal" autocomplete="off" maxlength="64" :value="modelValue ?? ''" :aria-describedby="`${question.id}-numeric-rule`" @input="$emit('update:modelValue', $event.target.value)" /><span>{{ question.numeric.unit }}</span></div><small :id="`${question.id}-numeric-rule`">填写数值，允许绝对误差 ±{{ question.numeric.tolerance }} {{ question.numeric.unit }}。</small></div>
    </fieldset>
    <slot />
  </article>
</template>
<script setup>
import LearningDiagram from './LearningDiagram.vue'
const props = defineProps({ question: { type: Object, required: true }, modelValue: { default: undefined }, index: { type: Number, default: 0 }, total: { type: Number, default: 4 }, disabled: { type: Boolean, default: false } })
const emit = defineEmits(['update:modelValue'])
const labels = { single: '单选题', multiple: '多选题', true_false: '判断题', numeric: '数值计算题' }
const units = { min: '分钟', m: '米', km: '千米' }
function selected(id) { return props.question.type === 'multiple' ? (Array.isArray(props.modelValue) && props.modelValue.includes(id)) : props.modelValue === id }
function choose(id, checked) {
  if (props.question.type === 'single') return emit('update:modelValue', id)
  const values = new Set(Array.isArray(props.modelValue) ? props.modelValue : [])
  if (checked) values.add(id); else values.delete(id)
  emit('update:modelValue', [...values].sort())
}
</script>
