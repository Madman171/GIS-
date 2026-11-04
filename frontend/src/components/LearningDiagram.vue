<template>
  <figure class="learning-diagram">
    <svg viewBox="0 0 440 200" role="img" :aria-labelledby="`${uid}-title ${uid}-desc`">
      <title :id="`${uid}-title`">题设有向路网示意图</title>
      <desc :id="`${uid}-desc`">{{ description }}；布局仅表示连接，不代表地理坐标。</desc>
      <defs><marker :id="uid" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" /></marker></defs>
      <g v-for="(edge, i) in diagram.edges" :key="i" :class="{ 'edge-closed': isClosed(edge) }">
        <line :x1="line(edge).x1" :y1="line(edge).y1" :x2="line(edge).x2" :y2="line(edge).y2" :marker-end="`url(#${uid})`" />
        <text v-if="diagram.unit === 'min' || isClosed(edge)" :x="label(edge).x" :y="label(edge).y" text-anchor="middle">{{ diagram.unit === 'min' ? `${edge[2]} 分钟` : '' }}{{ isClosed(edge) ? ' · 封闭' : '' }}</text>
      </g>
      <g v-for="id in ids" :key="id"><circle :cx="position(id).x" :cy="position(id).y" r="18" /><text :x="position(id).x" :y="position(id).y + 5" text-anchor="middle" class="diagram-node-name">{{ id }}</text></g>
    </svg>
    <figcaption>原创教学示意 · 箭头为允许方向{{ diagram.blocked.length ? '；标注“封闭”的边不可用' : '' }}</figcaption>
  </figure>
</template>
<script setup>
import { computed, useId } from 'vue'
const props = defineProps({ diagram: { type: Object, required: true } })
const uid = `route-${useId().replace(/[^a-z0-9]/gi, '')}`
const ids = computed(() => [...new Set(props.diagram.edges.flatMap(e => e.slice(0, 2)))])
const description = computed(() => props.diagram.edges.map(e => `${e[0]}到${e[1]}${props.diagram.unit === 'min' ? `，${e[2]}分钟` : ''}${isClosed(e) ? '，封闭' : ''}`).join('；'))
const positions = { S: [40, 100], T: [400, 100], A: [180, 38], B: [180, 162], C: [300, 162] }
function position(id) { const [x, y] = positions[id] || [220, 100]; return { x, y } }
function isClosed(edge) { return props.diagram.blocked.some(e => e[0] === edge[0] && e[1] === edge[1]) }
function line(edge) {
  const a = position(edge[0]), b = position(edge[1]), dx = b.x - a.x, dy = b.y - a.y, length = Math.hypot(dx, dy)
  return { x1: a.x + dx / length * 21, y1: a.y + dy / length * 21, x2: b.x - dx / length * 24, y2: b.y - dy / length * 24 }
}
function label(edge) {
  const a = position(edge[0]), b = position(edge[1])
  return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 - (a.y === b.y ? 9 : 8) }
}
</script>
