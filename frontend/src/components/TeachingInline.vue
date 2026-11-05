<template><span><template v-for="(part, index) in parts" :key="index"><strong v-if="part.type === 'strong'">{{ part.text }}</strong><em v-else-if="part.type === 'em'">{{ part.text }}</em><a v-else-if="part.type === 'link' && part.href" :href="part.href" target="_blank" rel="noopener noreferrer">{{ part.text }}</a><template v-else>{{ part.text }}</template></template></span></template>
<script setup>
import { computed } from 'vue'
import { inlineParts } from '../teaching/markdown'
const props = defineProps({ text: { type: String, required: true } })
const parts = computed(() => inlineParts(props.text))
</script>
