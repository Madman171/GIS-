<template>
  <template v-for="(block, index) in blocks" :key="index">
    <component :is="`h${Math.min(6, headingBase + block.level - 2)}`" v-if="block.type === 'heading'"><TeachingInline :text="block.text" /></component>
    <p v-else-if="block.type === 'paragraph'"><TeachingInline :text="block.text" /></p>
    <figure v-else-if="block.type === 'figure'"><img :src="block.src" :alt="block.alt" loading="lazy" /></figure>
    <pre v-else-if="block.type === 'code'"><code>{{ block.text }}</code></pre>
    <blockquote v-else-if="block.type === 'quote'"><TeachingInline :text="block.text" /></blockquote>
    <component :is="block.ordered ? 'ol' : 'ul'" v-else-if="block.type === 'list'"><li v-for="(item, j) in block.items" :key="j"><TeachingInline :text="item" /></li></component>
    <div v-else-if="block.type === 'table'" class="teaching-table-wrap" role="region" aria-label="教学对照表，可横向滚动" tabindex="0"><table><thead><tr><th v-for="(cell, j) in block.headers" :key="j" scope="col"><TeachingInline :text="cell" /></th></tr></thead><tbody><tr v-for="(row, j) in block.rows" :key="j"><td v-for="(cell, k) in row" :key="k"><TeachingInline :text="cell" /></td></tr></tbody></table></div>
    <details v-else-if="block.type === 'thoughtAnswer'" class="teaching-answer"><summary>查看思考解析</summary><p><TeachingInline :text="block.text" /></p></details>
    <details v-else-if="block.type === 'solution'" class="teaching-answer teaching-self-check"><summary>查看自测答案与解析</summary><TeachingBlocks :blocks="block.blocks" :heading-base="headingBase" /></details>
  </template>
</template>
<script setup>
import TeachingInline from './TeachingInline.vue'
defineProps({ blocks: { type: Array, required: true }, headingBase: { type: Number, default: 3 } })
</script>
