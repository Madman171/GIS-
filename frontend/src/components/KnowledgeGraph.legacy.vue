<template>
  <!-- Legacy implementation retained temporarily during graph refactor. -->
  <div ref="graphContainer" class="graph-container">
    <svg ref="svgRef" aria-label="知识图谱可视化"></svg>

    <div v-if="loading" class="graph-state">
      <LoaderCircle class="spin" :size="24" />
      <span>正在加载图谱</span>
    </div>

    <div v-else-if="nodes.length === 0" class="graph-state">
      <Network :size="28" />
      <strong>暂无可展示内容</strong>
      <span>请从左侧目录选择模块</span>
    </div>

    <div class="graph-controls">
      <button
        type="button"
        title="放大"
        aria-label="放大图谱"
        @click="zoomBy(1.25)"
      >
        <ZoomIn :size="16" />
      </button>
      <button
        type="button"
        title="缩小"
        aria-label="缩小图谱"
        @click="zoomBy(0.8)"
      >
        <ZoomOut :size="16" />
      </button>
      <button
        type="button"
        title="适应画布"
        aria-label="适应画布"
        @click="fitGraph(true)"
      >
        <Maximize2 :size="16" />
      </button>
    </div>

    <div class="graph-legend">
      <span><i class="legend-module"></i>模块</span>
      <span><i class="legend-knowledge"></i>知识点</span>
    </div>
  </div>
</template>

<script setup>
import {
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from 'vue'
import * as d3 from 'd3'
import {
  LoaderCircle,
  Maximize2,
  Network,
  ZoomIn,
  ZoomOut,
} from '@lucide/vue'
import {
  getNodeName,
  getNodeType,
  NODE_TYPE_COLORS,
  RELATION_LABELS,
} from '../constants/graph'

const props = defineProps({
  nodes: { type: Array, default: () => [] },
  links: { type: Array, default: () => [] },
  selectedId: { type: String, default: '' },
  loading: { type: Boolean, default: false },
})

const emit = defineEmits(['node-click'])

const graphContainer = ref(null)
const svgRef = ref(null)

let simulation = null
let resizeObserver = null
let renderTimer = null
let fitTimer = null
let zoomBehavior = null
let svgSelection = null
let graphSelection = null
let nodeSelection = null

function nodeRadius(node) {
  return getNodeType(node.labels) === 'Module' ? 21 : 10
}

function clearTimers() {
  if (renderTimer) {
    clearTimeout(renderTimer)
    renderTimer = null
  }
  if (fitTimer) {
    clearTimeout(fitTimer)
    fitTimer = null
  }
}

function stopSimulation() {
  if (simulation) {
    simulation.stop()
    simulation = null
  }
}

function clearGraph() {
  stopSimulation()
  if (svgSelection) {
    svgSelection.selectAll('*').remove()
  }
  nodeSelection = null
  graphSelection = null
}

function truncateLabel(value, maxLength = 12) {
  const text = String(value || '')
  return text.length > maxLength
    ? `${text.slice(0, maxLength)}...`
    : text
}

function updateSelection() {
  if (!nodeSelection) return

  nodeSelection
    .attr('stroke', (node) =>
      node.id === props.selectedId ? '#0f172a' : '#ffffff',
    )
    .attr('stroke-width', (node) =>
      node.id === props.selectedId ? 3 : 2,
    )
}

function renderGraph() {
  clearTimers()
  stopSimulation()

  if (!svgRef.value || !graphContainer.value) return

  const width = graphContainer.value.clientWidth
  const height = graphContainer.value.clientHeight

  svgSelection = d3.select(svgRef.value)
  clearGraph()
  svgSelection = d3.select(svgRef.value)

  if (!width || !height) return

  svgSelection
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)

  if (!props.nodes.length) return

  const nodes = props.nodes.map((node) => ({
    ...node,
    id: String(node.id),
  }))
  const links = props.links
    .filter((link) => {
      const nodeIds = new Set(nodes.map((node) => node.id))
      return nodeIds.has(String(link.source)) && nodeIds.has(String(link.target))
    })
    .map((link) => ({
      ...link,
      source: String(link.source),
      target: String(link.target),
    }))

  const definitions = svgSelection.append('defs')
  definitions
    .append('marker')
    .attr('id', 'graph-arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 10)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#94a3b8')

  zoomBehavior = d3
    .zoom()
    .scaleExtent([0.25, 4])
    .on('zoom', (event) => {
      graphSelection.attr('transform', event.transform)
    })

  svgSelection.call(zoomBehavior)

  graphSelection = svgSelection.append('g')

  const link = graphSelection
    .append('g')
    .attr('class', 'graph-links')
    .selectAll('line')
    .data(links)
    .enter()
    .append('line')
    .attr('stroke', '#94a3b8')
    .attr('stroke-opacity', 0.5)
    .attr('stroke-width', (item) =>
      item.type === 'BELONGS_TO' ? 1.2 : 1.5,
    )
    .attr('marker-end', 'url(#graph-arrow)')

  link
    .append('title')
    .text((item) => RELATION_LABELS[item.type] || item.type)

  nodeSelection = graphSelection
    .append('g')
    .attr('class', 'graph-nodes')
    .selectAll('circle')
    .data(nodes)
    .enter()
    .append('circle')
    .attr('class', 'graph-node')
    .attr('r', nodeRadius)
    .attr('fill', (node) => NODE_TYPE_COLORS[getNodeType(node.labels)])
    .attr('stroke', '#ffffff')
    .attr('stroke-width', 2)
    .attr('cursor', 'pointer')
    .call(
      d3
        .drag()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded),
    )
    .on('click', (event, node) => {
      event.stopPropagation()
      emit('node-click', node)
    })

  nodeSelection
    .append('title')
    .text((node) => {
      const type = getNodeType(node.labels)
      return `${type === 'Module' ? '模块' : '知识点'}：${getNodeName(node)}`
    })

  const label = graphSelection
    .append('g')
    .attr('class', 'graph-labels')
    .selectAll('text')
    .data(nodes)
    .enter()
    .append('text')
    .text((node) => truncateLabel(getNodeName(node)))
    .attr('font-size', (node) =>
      getNodeType(node.labels) === 'Module' ? 12 : 10,
    )
    .attr('font-weight', (node) =>
      getNodeType(node.labels) === 'Module' ? 700 : 500,
    )
    .attr('text-anchor', 'middle')
    .attr('dy', (node) => (getNodeType(node.labels) === 'Module' ? -29 : -17))
    .attr('fill', '#334155')
    .style('paint-order', 'stroke')
    .style('stroke', '#ffffff')
    .style('stroke-width', 3)
    .style('stroke-linejoin', 'round')
    .style('user-select', 'none')
    .style('pointer-events', 'none')

  updateSelection()

  simulation = d3
    .forceSimulation(nodes)
    .force(
      'link',
      d3
        .forceLink(links)
        .id((node) => node.id)
        .distance((item) =>
          item.type === 'BELONGS_TO' ? 74 : 108,
        )
        .strength((item) =>
          item.type === 'BELONGS_TO' ? 0.9 : 0.55,
        ),
    )
    .force(
      'charge',
      d3.forceManyBody().strength((node) =>
        getNodeType(node.labels) === 'Module' ? -520 : -190,
      ),
    )
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('x', d3.forceX(width / 2).strength(0.025))
    .force('y', d3.forceY(height / 2).strength(0.035))
    .force(
      'collision',
      d3
        .forceCollide()
        .radius((node) => nodeRadius(node) + 30)
        .iterations(2),
    )
    .on('tick', () => {
      nodes.forEach((node) => {
        const padding = nodeRadius(node) + 18
        node.x = Math.max(padding, Math.min(width - padding, node.x))
        node.y = Math.max(padding, Math.min(height - padding, node.y))
      })

      link
        .attr('x1', (item) => item.source.x)
        .attr('y1', (item) => item.source.y)
        .attr('x2', (item) => item.target.x)
        .attr('y2', (item) => item.target.y)

      nodeSelection
        .attr('cx', (node) => node.x)
        .attr('cy', (node) => node.y)

      label
        .attr('x', (node) => node.x)
        .attr('y', (node) => node.y)
    })

  fitTimer = setTimeout(() => fitGraph(false), 650)

  function dragStarted(event, node) {
    if (!event.active) simulation.alphaTarget(0.25).restart()
    node.fx = node.x
    node.fy = node.y
  }

  function dragged(event, node) {
    node.fx = event.x
    node.fy = event.y
  }

  function dragEnded(event, node) {
    if (!event.active) simulation.alphaTarget(0)
    node.fx = null
    node.fy = null
  }
}

function fitGraph(animate = true) {
  if (!graphSelection || !svgSelection || !zoomBehavior) return
  if (!graphSelection.node()) return

  const width = graphContainer.value?.clientWidth || 0
  const height = graphContainer.value?.clientHeight || 0
  if (!width || !height) return

  const bounds = graphSelection.node().getBBox()
  if (!bounds.width || !bounds.height) return

  const scale = Math.max(
    0.3,
    Math.min(
      2,
      Math.min(width / bounds.width, height / bounds.height) * 0.82,
    ),
  )
  const midX = bounds.x + bounds.width / 2
  const midY = bounds.y + bounds.height / 2
  const transform = d3.zoomIdentity
    .translate(width / 2, height / 2)
    .scale(scale)
    .translate(-midX, -midY)
  const target = animate ? svgSelection.transition().duration(450) : svgSelection

  target.call(zoomBehavior.transform, transform)
}

function zoomBy(factor) {
  if (!svgSelection || !zoomBehavior) return
  svgSelection
    .transition()
    .duration(180)
    .call(zoomBehavior.scaleBy, factor)
}

function scheduleRender(delay = 80) {
  nextTick(() => {
    if (renderTimer) clearTimeout(renderTimer)
    renderTimer = setTimeout(renderGraph, delay)
  })
}

watch(
  () => [props.nodes, props.links],
  () => scheduleRender(),
  { flush: 'post' },
)

watch(
  () => props.selectedId,
  () => updateSelection(),
)

onMounted(() => {
  scheduleRender(120)
  resizeObserver = new ResizeObserver(() => scheduleRender(120))
  if (graphContainer.value) {
    resizeObserver.observe(graphContainer.value)
  }
})

onBeforeUnmount(() => {
  clearTimers()
  stopSimulation()
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }
})
</script>

<style scoped>
.graph-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 0;
  overflow: hidden;
  background:
    linear-gradient(rgba(148, 163, 184, 0.09) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.09) 1px, transparent 1px),
    #ffffff;
  background-size: 24px 24px;
}

.graph-container svg {
  display: block;
  width: 100%;
  height: 100%;
}

.graph-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #64748b;
  background: rgba(255, 255, 255, 0.82);
  font-size: 13px;
  text-align: center;
}

.graph-state strong {
  color: #334155;
  font-size: 14px;
}

.graph-controls {
  position: absolute;
  top: 14px;
  left: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.graph-controls button {
  width: 34px;
  height: 34px;
  padding: 0;
  border: 1px solid #dbe4ef;
  border-radius: 6px;
  display: grid;
  place-items: center;
  color: #475569;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
  cursor: pointer;
}

.graph-controls button:hover {
  color: #1d4ed8;
  border-color: #93c5fd;
}

.graph-legend {
  position: absolute;
  left: 14px;
  bottom: 14px;
  padding: 7px 9px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  display: flex;
  gap: 12px;
  color: #475569;
  background: rgba(255, 255, 255, 0.92);
  font-size: 11px;
}

.graph-legend span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.graph-legend i {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.legend-module {
  background: #7c3aed;
}

.legend-knowledge {
  background: #2563eb;
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
