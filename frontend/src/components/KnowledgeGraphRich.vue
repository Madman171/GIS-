<template>
  <div
    ref="graphContainer"
    class="graph-container"
    @mouseleave="clearTooltip"
  >
    <svg ref="svgRef" aria-label="知识图谱可视化"></svg>

    <div class="graph-canvas-badge">
      <span class="badge-dot"></span>
      {{ layoutLabel }}
    </div>

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
      <div class="legend-heading">
        <span>关系类型</span>
        <button
          type="button"
          title="恢复全部关系"
          @click="resetRelationVisibility"
        >
          全部显示
        </button>
      </div>
      <div v-if="difficultyLegend.length" class="node-legend">
        <span><i class="module-dot"></i>模块</span>
        <span v-for="item in difficultyLegend" :key="item.difficulty">
          <i :style="{ background: item.color }"></i>
          {{ item.difficulty }}
        </span>
        <span class="size-hint">圆点越大，重要性越高</span>
      </div>
      <div class="legend-items">
        <button
          v-for="relation in relationLegend"
          :key="relation.type"
          type="button"
          class="legend-item"
          :class="{ muted: hiddenRelationTypes.has(relation.type) }"
          @click="toggleRelation(relation.type)"
        >
          <i :style="{ background: relation.color }"></i>
          <span>{{ relation.label }}</span>
          <em>{{ relation.count }}</em>
        </button>
      </div>
    </div>

    <div
      v-if="hoveredNode"
      class="node-tooltip"
      :style="tooltipStyle"
    >
      <strong>{{ getNodeName(hoveredNode) }}</strong>
      <span>
        {{
          getNodeType(hoveredNode.labels) === 'Module'
            ? '教学模块'
            : '知识点'
        }}
      </span>
      <div v-if="hoveredNode.properties?.difficulty" class="tooltip-row">
        <i :style="{ background: getNodeColor(hoveredNode) }"></i>
        {{ hoveredNode.properties.difficulty }}
        <b v-if="hoveredNode.properties?.importance">
          {{ hoveredNode.properties.importance }}
        </b>
      </div>
      <small>{{ hoveredRelationCount }} 条直接关系</small>
    </div>

    <div class="graph-metrics">
      <span><b>{{ nodes.length }}</b>节点</span>
      <span><b>{{ links.length }}</b>关系</span>
      <span v-if="knowledgePointCount">
        <b>{{ knowledgePointCount }}</b>知识点
      </span>
    </div>

    <div
      v-if="nodes.length > 4 && !loading"
      ref="minimapContainer"
      class="graph-minimap"
      title="点击缩略图定位图谱"
      @click="handleMinimapClick"
    >
      <svg ref="minimapSvgRef" aria-label="图谱缩略图"></svg>
      <span>导航图</span>
    </div>
  </div>
</template>

<script setup>
import {
  computed,
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
  DIFFICULTY_COLORS,
  getImportanceScale,
  getNodeColor,
  getNodeName,
  getNodeType,
  RELATION_COLORS,
  RELATION_DASHES,
  RELATION_LABELS,
} from '../constants/graph'

const props = defineProps({
  nodes: { type: Array, default: () => [] },
  links: { type: Array, default: () => [] },
  selectedId: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  viewMode: { type: String, default: 'all' },
})

const emit = defineEmits(['node-click'])

const graphContainer = ref(null)
const svgRef = ref(null)
const minimapContainer = ref(null)
const minimapSvgRef = ref(null)
const hoveredNode = ref(null)
const tooltipPosition = ref({ x: 0, y: 0 })
const hiddenRelationTypes = ref(new Set())

let simulation = null
let resizeObserver = null
let renderTimer = null
let fitTimer = null
let zoomBehavior = null
let svgSelection = null
let graphSelection = null
let nodeSelection = null
let linkSelection = null
let labelSelection = null
let minimapSelection = null
let minimapViewportSelection = null
let renderedNodes = []
let renderedLinks = []
let renderSize = { width: 0, height: 0 }
let minimapModel = null
let minimapFrame = null

const relationLegend = computed(() => {
  const counts = new Map()
  for (const link of props.links) {
    counts.set(link.type, (counts.get(link.type) || 0) + 1)
  }
  return Array.from(counts.entries())
    .map(([type, count]) => ({
      type,
      count,
      label: RELATION_LABELS[type] || type,
      color: RELATION_COLORS[type] || '#64748b',
    }))
    .sort((left, right) => right.count - left.count)
})

const knowledgePointCount = computed(
  () =>
    props.nodes.filter(
      (node) => getNodeType(node.labels) === 'KnowledgePoint',
    ).length,
)

const difficultyLegend = computed(() => {
  const values = new Set(
    props.nodes
      .filter(
        (node) => getNodeType(node.labels) === 'KnowledgePoint',
      )
      .map((node) => node.properties?.difficulty)
      .filter(Boolean),
  )
  return Array.from(values).map((difficulty) => ({
    difficulty,
    color: DIFFICULTY_COLORS[difficulty] || '#64748b',
  }))
})

const layoutLabel = computed(() =>
  knowledgePointCount.value > 0 ? '路网式知识轨道' : '课程模块网络',
)

const tooltipStyle = computed(() => ({
  left: `${tooltipPosition.value.x}px`,
  top: `${tooltipPosition.value.y}px`,
}))

const hoveredRelationCount = computed(() => {
  if (!hoveredNode.value) return 0
  return props.links.filter(
    (link) =>
      String(link.source) === String(hoveredNode.value.id) ||
      String(link.target) === String(hoveredNode.value.id),
  ).length
})

function nodeRadius(node) {
  if (getNodeType(node.labels) === 'Module') return 27
  const base = getNodeType(node.labels) === 'Tool' ? 13 : 11
  return base * getImportanceScale(node)
}

function truncateLabel(value, maxLength = 14) {
  const text = String(value || '')
  return text.length > maxLength
    ? `${text.slice(0, maxLength)}...`
    : text
}

function relationColor(type) {
  return RELATION_COLORS[type] || '#94a3b8'
}

function relationDash(type) {
  return RELATION_DASHES[type] || null
}

function relationOpacity(type) {
  if (hiddenRelationTypes.value.has(type)) return 0.04
  if (type === 'BELONGS_TO') return 0.16
  return 0.68
}

function relationStrokeWidth(type) {
  if (type === 'BELONGS_TO') return 0.8
  if (type === 'PREREQUISITE_OF') return 1.8
  if (type === 'RELATED_TO') return 1.35
  return 1.2
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
  if (minimapFrame) {
    cancelAnimationFrame(minimapFrame)
    minimapFrame = null
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
  if (svgSelection) svgSelection.selectAll('*').remove()
  nodeSelection = null
  linkSelection = null
  labelSelection = null
  graphSelection = null
}

function buildAdjacency(nodes) {
  const matrix = new Map(nodes.map((node) => [node.id, new Set([node.id])]))
  for (const link of props.links) {
    const source = linkEndpointId(link.source)
    const target = linkEndpointId(link.target)
    if (matrix.has(source)) matrix.get(source).add(target)
    if (matrix.has(target)) matrix.get(target).add(source)
  }
  return matrix
}

function linkEndpointId(value) {
  if (value && typeof value === 'object') return String(value.id)
  return String(value)
}

function buildPrerequisiteReachability(nodes, links) {
  const prerequisites = new Map()
  const successors = new Map()
  for (const node of nodes) {
    prerequisites.set(node.id, [])
    successors.set(node.id, [])
  }
  for (const link of links) {
    if (link.type !== 'PREREQUISITE_OF') continue
    const source = linkEndpointId(link.source)
    const target = linkEndpointId(link.target)
    prerequisites.get(target)?.push(source)
    successors.get(source)?.push(target)
  }

  const selected = String(props.selectedId || '')
  if (!prerequisites.has(selected)) return null

  const highlighted = new Set([selected])
  const collect = (start, graph) => {
    const queue = [...(graph.get(start) || [])]
    while (queue.length) {
      const current = queue.shift()
      if (highlighted.has(current)) continue
      highlighted.add(current)
      queue.push(...(graph.get(current) || []))
    }
  }
  collect(selected, prerequisites)
  collect(selected, successors)

  if (highlighted.size === 1) {
    for (const link of links) {
      if (link.type !== 'PREREQUISITE_OF') continue
      highlighted.add(linkEndpointId(link.source))
      highlighted.add(linkEndpointId(link.target))
    }
  }
  return highlighted
}

function applyVisualState(nodes, links) {
  if (!nodeSelection || !linkSelection) return

  const selected = String(props.selectedId || '')
  const adjacency = buildAdjacency(nodes)
  const neighbors = selected ? adjacency.get(selected) : null
  const pathNodes = buildPrerequisiteReachability(nodes, links)

  nodeSelection.attr('opacity', (node) => {
    if (props.viewMode === 'path' && pathNodes) {
      return pathNodes.has(node.id) ? 1 : 0.2
    }
    if (props.viewMode === 'focus' && selected && neighbors) {
      return neighbors.has(node.id) ? 1 : 0.2
    }
    return 1
  })

  nodeSelection
    .classed('node-selected', (node) => node.id === selected)
    .classed(
      'node-neighbor',
      (node) =>
        Boolean(selected) &&
        Boolean(neighbors) &&
        node.id !== selected &&
        neighbors.has(node.id),
    )

  linkSelection.attr('opacity', (link) => {
    if (hiddenRelationTypes.value.has(link.type)) return 0.04
    if (props.viewMode === 'path') {
      return link.type.includes('PREREQUISITE') ||
        link.type === 'SUPPORTS'
        ? 0.88
        : 0.06
    }
    if (props.viewMode === 'focus' && selected && neighbors) {
      return link.source.id === selected || link.target.id === selected
        ? 0.92
        : 0.05
    }
    return relationOpacity(link.type)
  })

  labelSelection.attr('opacity', (node) => {
    if (props.viewMode === 'path' && pathNodes) {
      return pathNodes.has(node.id) ? 1 : 0.16
    }
    if (props.viewMode === 'focus' && selected && neighbors) {
      return neighbors.has(node.id) ? 1 : 0.16
    }
    return 1
  })
}

function buildCurvedPath(link, index) {
  const source = link.source
  const target = link.target
  if (
    !Number.isFinite(source?.x) ||
    !Number.isFinite(source?.y) ||
    !Number.isFinite(target?.x) ||
    !Number.isFinite(target?.y)
  ) {
    return ''
  }
  const dx = target.x - source.x
  const dy = target.y - source.y
  const distance = Math.sqrt(dx * dx + dy * dy) || 1
  const curveBase =
    link.type === 'BELONGS_TO'
      ? 0
      : link.type === 'RELATED_TO'
        ? 0.17
        : 0.1
  const direction = index % 2 === 0 ? 1 : -1
  const offset = distance * curveBase * direction
  const midX = (source.x + target.x) / 2 - (dy / distance) * offset
  const midY = (source.y + target.y) / 2 + (dx / distance) * offset
  return `M${source.x},${source.y} Q${midX},${midY} ${target.x},${target.y}`
}

function radialPosition(index, count, radius, offset = -Math.PI / 2) {
  const angle = offset + (Math.PI * 2 * index) / Math.max(1, count)
  return {
    angle,
    x: Math.cos(angle) * radius,
    y: Math.sin(angle) * radius,
  }
}

function buildRadialLayout(nodes, width, height) {
  const moduleNode = nodes.find(
    (node) => getNodeType(node.labels) === 'Module',
  )
  const knowledgeNodes = nodes.filter(
    (node) => getNodeType(node.labels) === 'KnowledgePoint',
  )
  const toolNodes = nodes.filter(
    (node) => getNodeType(node.labels) === 'Tool',
  )
  if (!moduleNode || knowledgeNodes.length < 4) return null

  const centerX = width / 2
  const centerY = height / 2 + 8
  moduleNode.x = centerX
  moduleNode.y = centerY
  moduleNode.fx = null
  moduleNode.fy = null

  const rank = (node) => {
    const value = node.properties?.difficulty
    if (['入门', '基础', '简单'].includes(value)) return 0
    if (['中等', '进阶', 'intermediate'].includes(value)) return 1
    return 2
  }
  const grouped = [[], [], []]
  knowledgeNodes
    .slice()
    .sort(
      (left, right) =>
        (left.properties?.sort_order || 9999) -
        (right.properties?.sort_order || 9999),
    )
    .forEach((node) => grouped[rank(node)].push(node))

  const activeGroups = grouped.filter((group) => group.length)
  const baseRadius = Math.min(width, height) * 0.18
  const radiusStep = Math.min(width, height) * 0.135
  activeGroups.forEach((group, ringIndex) => {
    const radius =
      baseRadius + ringIndex * radiusStep * (activeGroups.length / 3 + 0.35)
    group.forEach((node, index) => {
      const position = radialPosition(
        index,
        group.length,
        radius,
        -Math.PI / 2 + ringIndex * 0.16,
      )
      node.x = centerX + position.x
      node.y = centerY + position.y
      node.angle = position.angle
      node.ringIndex = ringIndex
      node.fx = node.x
      node.fy = node.y
    })
  })

  toolNodes.forEach((node, index) => {
    const position = radialPosition(
      index,
      Math.max(1, toolNodes.length),
      baseRadius * 0.72,
      Math.PI / 4,
    )
    node.x = centerX + position.x
    node.y = centerY + position.y
    node.angle = position.angle
    node.ringIndex = -1
    node.fx = node.x
    node.fy = node.y
  })

  return {
    type: 'radial',
    centerX,
    centerY,
    radii: activeGroups.map(
      (_, index) =>
        baseRadius +
        index * radiusStep * (activeGroups.length / 3 + 0.35),
    ),
  }
}

function scheduleMinimapUpdate() {
  if (minimapFrame) cancelAnimationFrame(minimapFrame)
  minimapFrame = requestAnimationFrame(() => {
    minimapFrame = null
    drawMinimap()
  })
}

function drawMinimap() {
  if (!minimapSvgRef.value || !renderedNodes.length) return

  const positions = renderedNodes.filter(
    (node) => Number.isFinite(node.x) && Number.isFinite(node.y),
  )
  if (!positions.length) return

  const width = minimapContainer.value?.clientWidth || 150
  const height = minimapContainer.value?.clientHeight || 86
  const padding = 8
  const xExtent = d3.extent(positions, (node) => node.x)
  const yExtent = d3.extent(positions, (node) => node.y)
  const spanX = Math.max(1, xExtent[1] - xExtent[0])
  const spanY = Math.max(1, yExtent[1] - yExtent[0])
  const scale = Math.min(
    (width - padding * 2) / spanX,
    (height - padding * 2) / spanY,
  )
  const offsetX =
    (width - spanX * scale) / 2 - xExtent[0] * scale
  const offsetY =
    (height - spanY * scale) / 2 - yExtent[0] * scale

  minimapModel = {
    width,
    height,
    scale,
    offsetX,
    offsetY,
  }

  minimapSelection = d3.select(minimapSvgRef.value)
  minimapSelection
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)
    .selectAll('*')
    .remove()

  minimapSelection
    .append('g')
    .selectAll('circle')
    .data(positions)
    .enter()
    .append('circle')
    .attr(
      'cx',
      (node) => offsetX + node.x * scale,
    )
    .attr(
      'cy',
      (node) => offsetY + node.y * scale,
    )
    .attr('r', (node) =>
      String(node.id) === props.selectedId ? 3.2 : 1.8,
    )
    .attr('fill', (node) => getNodeColor(node))
    .attr('fill-opacity', (node) =>
      String(node.id) === props.selectedId ? 1 : 0.72,
    )

  minimapViewportSelection = minimapSelection
    .append('rect')
    .attr('class', 'minimap-viewport')
    .attr('rx', 3)
    .attr('fill', '#2563eb')
    .attr('fill-opacity', 0.08)
    .attr('stroke', '#2563eb')
    .attr('stroke-width', 1)

  updateMinimapViewport()
}

function updateMinimapViewport() {
  if (
    !minimapModel ||
    !minimapViewportSelection ||
    !svgSelection?.node() ||
    !renderSize.width ||
    !renderSize.height
  ) {
    return
  }

  const transform = d3.zoomTransform(svgSelection.node())
  const corners = [
    [0, 0],
    [renderSize.width, 0],
    [renderSize.width, renderSize.height],
    [0, renderSize.height],
  ].map((point) => transform.invert(point))
  const worldMinX = Math.min(...corners.map((point) => point[0]))
  const worldMaxX = Math.max(...corners.map((point) => point[0]))
  const worldMinY = Math.min(...corners.map((point) => point[1]))
  const worldMaxY = Math.max(...corners.map((point) => point[1]))

  const x =
    minimapModel.offsetX + worldMinX * minimapModel.scale
  const y =
    minimapModel.offsetY + worldMinY * minimapModel.scale
  const width =
    (worldMaxX - worldMinX) * minimapModel.scale
  const height =
    (worldMaxY - worldMinY) * minimapModel.scale

  minimapViewportSelection
    .attr('x', Math.max(0, x))
    .attr('y', Math.max(0, y))
    .attr(
      'width',
      Math.min(minimapModel.width, Math.max(4, width)),
    )
    .attr(
      'height',
      Math.min(minimapModel.height, Math.max(4, height)),
    )
}

function handleMinimapClick(event) {
  if (
    !minimapModel ||
    !svgSelection?.node() ||
    !zoomBehavior ||
    !renderSize.width ||
    !renderSize.height
  ) {
    return
  }

  const bounds = minimapContainer.value.getBoundingClientRect()
  const localX = event.clientX - bounds.left
  const localY = event.clientY - bounds.top
  const worldX =
    (localX - minimapModel.offsetX) / minimapModel.scale
  const worldY =
    (localY - minimapModel.offsetY) / minimapModel.scale
  const current = d3.zoomTransform(svgSelection.node())
  const target = d3.zoomIdentity
    .translate(renderSize.width / 2, renderSize.height / 2)
    .scale(current.k)
    .translate(-worldX, -worldY)

  svgSelection
    .transition()
    .duration(320)
    .call(zoomBehavior.transform, target)
}

function centerSelectedNode(animate = true) {
  if (
    !svgSelection?.node() ||
    !zoomBehavior ||
    !renderSize.width ||
    !renderSize.height
  ) {
    return
  }

  const node = renderedNodes.find(
    (item) => item.id === String(props.selectedId || ''),
  )
  if (
    !node ||
    !Number.isFinite(node.x) ||
    !Number.isFinite(node.y)
  ) {
    return
  }

  const current = d3.zoomTransform(svgSelection.node())
  const scale = Math.max(current.k, 0.82)
  const target = d3.zoomIdentity
    .translate(renderSize.width / 2, renderSize.height / 2)
    .scale(scale)
    .translate(-node.x, -node.y)
  const selection = animate
    ? svgSelection.transition().duration(420)
    : svgSelection
  selection.call(zoomBehavior.transform, target)
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
  const nodeIds = new Set(nodes.map((node) => node.id))
  const links = props.links
    .filter(
      (link) =>
        nodeIds.has(String(link.source)) &&
        nodeIds.has(String(link.target)),
    )
    .map((link) => ({
      ...link,
      source: String(link.source),
      target: String(link.target),
    }))
  renderedNodes = nodes
  renderedLinks = links
  renderSize = { width, height }

  nodes.forEach((node, index) => {
    if (Number.isFinite(node.x) && Number.isFinite(node.y)) return
    const angle = (Math.PI * 2 * index) / Math.max(1, nodes.length)
    const radius = Math.min(width, height) * 0.34
    node.x = width / 2 + Math.cos(angle) * radius
    node.y = height / 2 + Math.sin(angle) * radius
  })

  const definitions = svgSelection.append('defs')
  for (const [type, color] of Object.entries(RELATION_COLORS)) {
    definitions
      .append('marker')
      .attr('id', `graph-arrow-${type}`)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 10)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', color)
  }

  zoomBehavior = d3
    .zoom()
    .scaleExtent([0.22, 5])
    .on('zoom', (event) => {
      graphSelection.attr('transform', event.transform)
      scheduleMinimapUpdate()
    })

  svgSelection.call(zoomBehavior)
  graphSelection = svgSelection.append('g')

  const radialLayout = buildRadialLayout(nodes, width, height)
  if (radialLayout) {
    graphSelection
      .append('g')
      .attr('class', 'module-fields')
      .selectAll('circle')
      .data(radialLayout.radii)
      .enter()
      .append('circle')
      .attr('cx', radialLayout.centerX)
      .attr('cy', radialLayout.centerY)
      .attr('r', (radius) => radius)
      .attr('fill', 'none')
      .attr('stroke', '#cbd5e1')
      .attr('stroke-opacity', 0.52)
      .attr('stroke-width', 1)
      .attr('stroke-dasharray', '2 7')

    graphSelection
      .append('circle')
      .attr('class', 'module-core-field')
      .attr('cx', radialLayout.centerX)
      .attr('cy', radialLayout.centerY)
      .attr('r', Math.min(width, height) * 0.105)
      .attr('fill', '#f5f3ff')
      .attr('fill-opacity', 0.72)
      .attr('stroke', '#c4b5fd')
      .attr('stroke-width', 1.2)
  }

  linkSelection = graphSelection
    .append('g')
    .attr('class', 'graph-links')
    .selectAll('path')
    .data(links)
    .enter()
    .append('path')
    .attr('class', (link) => `graph-link relation-${link.type}`)
    .attr('fill', 'none')
    .attr('stroke', (link) => relationColor(link.type))
    .attr('stroke-width', (link) => relationStrokeWidth(link.type))
    .attr('stroke-linecap', 'round')
    .attr('stroke-dasharray', (link) => relationDash(link.type))
    .attr('marker-end', (link) =>
      link.type === 'BELONGS_TO'
        ? null
        : `url(#graph-arrow-${link.type})`,
    )
    .attr('pointer-events', 'none')

  linkSelection
    .append('title')
    .text((link) => RELATION_LABELS[link.type] || link.type)

  const nodeGroups = graphSelection
    .append('g')
    .attr('class', 'graph-nodes')
    .selectAll('g')
    .data(nodes)
    .enter()
    .append('g')
    .attr(
      'class',
      (node) =>
        [
          'graph-node',
          `node-${getNodeType(node.labels)}`,
          node.properties?.importance === '核心' ? 'node-core' : '',
        ]
          .filter(Boolean)
          .join(' '),
    )
    .attr('cursor', 'pointer')
    .on('mouseenter', (event, node) => {
      hoveredNode.value = node
      updateTooltipPosition(event)
    })
    .on('mousemove', updateTooltipPosition)
    .on('mouseleave', clearTooltip)
    .on('click', (event, node) => {
      event.stopPropagation()
      emit('node-click', node)
    })
    .call(
      d3
        .drag()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded),
    )

  nodeGroups
    .append('circle')
    .attr('class', 'node-focus-ring')
    .attr('r', (node) => nodeRadius(node) + 8)
    .attr('fill', 'none')
    .attr('stroke', (node) => getNodeColor(node))
    .attr('stroke-width', 1.2)
    .attr('stroke-opacity', 0.2)

  nodeGroups
    .append('circle')
    .attr('class', 'node-pulse')
    .attr('r', (node) => nodeRadius(node) + 5)
    .attr('fill', 'none')
    .attr('stroke', (node) => getNodeColor(node))
    .attr('stroke-width', 2)

  nodeGroups
    .append('circle')
    .attr('class', 'node-body')
    .attr('r', nodeRadius)
    .attr('fill', (node) => getNodeColor(node))
    .attr('stroke', '#ffffff')
    .attr(
      'stroke-width',
      (node) => (getNodeType(node.labels) === 'Module' ? 3 : 2),
    )
    .style('filter', (node) =>
      node.properties?.importance === '核心'
        ? 'drop-shadow(0 0 7px rgba(124, 58, 237, 0.42))'
        : 'drop-shadow(0 3px 5px rgba(15, 23, 42, 0.14))',
    )

  nodeGroups
    .append('circle')
    .attr('class', 'node-importance-dot')
    .attr(
      'r',
      (node) => (getNodeType(node.labels) === 'Module' ? 4 : 2.7),
    )
    .attr('fill', '#ffffff')
    .attr('fill-opacity', 0.9)

  nodeGroups
    .append('title')
    .text((node) => {
      const type = getNodeType(node.labels)
      const details = [
        type === 'Module' ? '模块' : '知识点',
        node.properties?.difficulty,
        node.properties?.importance,
      ].filter(Boolean)
      return `${getNodeName(node)}（${details.join(' · ')}）`
    })

  nodeSelection = nodeGroups

  labelSelection = graphSelection
    .append('g')
    .attr('class', 'graph-labels')
    .selectAll('text')
    .data(nodes)
    .enter()
    .append('text')
    .attr('class', (node) =>
      getNodeType(node.labels) === 'Module'
        ? 'module-label'
        : 'knowledge-label',
    )
    .text((node) => truncateLabel(getNodeName(node)))
    .attr(
      'font-size',
      (node) => (getNodeType(node.labels) === 'Module' ? 13 : 9.5),
    )
    .attr(
      'font-weight',
      (node) => (getNodeType(node.labels) === 'Module' ? 750 : 520),
    )
    .attr('text-anchor', (node) => {
      if (getNodeType(node.labels) === 'Module') return 'middle'
      const cosine = Math.cos(node.angle || 0)
      if (cosine > 0.28) return 'start'
      if (cosine < -0.28) return 'end'
      return 'middle'
    })
    .attr('dx', (node) => {
      if (getNodeType(node.labels) === 'Module') return 0
      const cosine = Math.cos(node.angle || 0)
      if (cosine > 0.28) return 13
      if (cosine < -0.28) return -13
      return 0
    })
    .attr('dy', (node) => {
      if (getNodeType(node.labels) === 'Module') return -38
      const sine = Math.sin(node.angle || 0)
      return sine > 0.55 ? 17 : sine < -0.55 ? -14 : 3
    })
    .style('paint-order', 'stroke')
    .style('stroke', '#ffffff')
    .style('stroke-width', 3.2)
    .style('stroke-linejoin', 'round')
    .style('user-select', 'none')
    .style('pointer-events', 'none')

  if (radialLayout) {
    const forceLinks = links.filter(
      (link) => link.type !== 'BELONGS_TO',
    )
    simulation = d3
      .forceSimulation(nodes)
      .alpha(0.18)
      .alphaDecay(0.35)
      .force(
        'link',
        d3
          .forceLink(forceLinks)
          .id((node) => node.id)
          .distance((link) =>
            link.type === 'PREREQUISITE_OF' ? 112 : 132,
          )
          .strength((link) =>
            link.type === 'PREREQUISITE_OF' ? 0.04 : 0.02,
          ),
      )
      .force(
        'collision',
        d3.forceCollide().radius((node) => nodeRadius(node) + 16),
      )
      .on('tick', () => updatePositions(links))
  } else {
    simulation = d3
      .forceSimulation(nodes)
      .force(
        'link',
        d3
          .forceLink(links)
          .id((node) => node.id)
          .distance((link) =>
            link.type === 'PREREQUISITE_MODULE' ? 150 : 118,
          )
          .strength(0.42),
      )
      .force('charge', d3.forceManyBody().strength(-560))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('x', d3.forceX(width / 2).strength(0.04))
      .force('y', d3.forceY(height / 2).strength(0.05))
      .force(
        'collision',
        d3.forceCollide().radius((node) => nodeRadius(node) + 42),
      )
      .on('tick', () => updatePositions(links))
  }

  applyVisualState(nodes, links)
  scheduleMinimapUpdate()
  fitTimer = setTimeout(() => fitGraph(false), 500)

  function updatePositions(activeLinks) {
    activeLinks.forEach((link, index) => {
      link.path = buildCurvedPath(link, index)
    })
    linkSelection.attr('d', (link) => link.path || '')
    nodeSelection.attr(
      'transform',
      (node) => `translate(${node.x},${node.y})`,
    )
    labelSelection
      .attr('x', (node) => node.x)
      .attr('y', (node) => node.y)
    scheduleMinimapUpdate()
  }

  updatePositions(links)

  function dragStarted(event, node) {
    if (simulation && !event.active) {
      simulation.alphaTarget(0.18).restart()
    }
    node.fx = node.x
    node.fy = node.y
  }

  function dragged(event, node) {
    node.fx = event.x
    node.fy = event.y
    node.x = event.x
    node.y = event.y
    updatePositions(links)
  }

  function dragEnded(event, node) {
    if (simulation && !event.active) simulation.alphaTarget(0)
    if (!radialLayout) {
      node.fx = null
      node.fy = null
    }
  }
}

function updateTooltipPosition(event) {
  if (!graphContainer.value) return
  const bounds = graphContainer.value.getBoundingClientRect()
  const x = event.clientX - bounds.left
  const y = event.clientY - bounds.top
  const maxX = Math.max(12, bounds.width - 270)
  const maxY = Math.max(12, bounds.height - 150)
  tooltipPosition.value = {
    x: Math.min(Math.max(12, x + 14), maxX),
    y: Math.min(Math.max(12, y + 14), maxY),
  }
}

function clearTooltip() {
  hoveredNode.value = null
}

function toggleRelation(type) {
  const next = new Set(hiddenRelationTypes.value)
  if (next.has(type)) next.delete(type)
  else next.add(type)
  hiddenRelationTypes.value = next
  applyVisualState(
    nodeSelection?.data?.() || [],
    linkSelection?.data?.() || [],
  )
}

function resetRelationVisibility() {
  hiddenRelationTypes.value = new Set()
  applyVisualState(
    nodeSelection?.data?.() || [],
    linkSelection?.data?.() || [],
  )
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
      Math.min(width / bounds.width, height / bounds.height) * 0.86,
    ),
  )
  const midX = bounds.x + bounds.width / 2
  const midY = bounds.y + bounds.height / 2
  const transform = d3.zoomIdentity
    .translate(width / 2, height / 2)
    .scale(scale)
    .translate(-midX, -midY)
  const target = animate
    ? svgSelection.transition().duration(450)
    : svgSelection
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
  () => {
    applyVisualState(
      nodeSelection?.data?.() || [],
      linkSelection?.data?.() || [],
    )
    nextTick(() => centerSelectedNode(true))
    scheduleMinimapUpdate()
  },
)

watch(
  () => props.viewMode,
  () => {
    applyVisualState(
      nodeSelection?.data?.() || [],
      linkSelection?.data?.() || [],
    )
  },
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
    linear-gradient(rgba(148, 163, 184, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.1) 1px, transparent 1px),
    linear-gradient(rgba(37, 99, 235, 0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37, 99, 235, 0.035) 1px, transparent 1px),
    #fbfdff;
  background-size:
    24px 24px,
    24px 24px,
    120px 120px,
    120px 120px;
}

.graph-container svg {
  display: block;
  width: 100%;
  height: 100%;
}

.graph-canvas-badge {
  position: absolute;
  top: 14px;
  right: 14px;
  padding: 6px 9px;
  border: 1px solid #dbeafe;
  border-radius: 999px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #1e40af;
  background: rgba(239, 246, 255, 0.94);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
  font-size: 10px;
  font-weight: 700;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
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
  background: rgba(255, 255, 255, 0.86);
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
  border-radius: 7px;
  display: grid;
  place-items: center;
  color: #475569;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 5px 14px rgba(15, 23, 42, 0.08);
  cursor: pointer;
}

.graph-controls button:hover {
  color: #1d4ed8;
  border-color: #93c5fd;
  background: #eff6ff;
}

.graph-legend {
  position: absolute;
  left: 14px;
  bottom: 14px;
  width: min(520px, calc(100% - 28px));
  padding: 9px 10px;
  border: 1px solid #dbe4ef;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.1);
  backdrop-filter: blur(8px);
}

.legend-heading {
  margin-bottom: 7px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #334155;
  font-size: 10px;
  font-weight: 700;
}

.legend-heading button {
  padding: 0;
  border: 0;
  color: #2563eb;
  background: transparent;
  cursor: pointer;
  font-size: 9px;
}

.node-legend {
  margin-bottom: 7px;
  padding-bottom: 7px;
  border-bottom: 1px solid #edf2f7;
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  color: #64748b;
  font-size: 9px;
}

.node-legend span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.node-legend i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.node-legend .module-dot {
  background: #7c3aed;
  box-shadow: 0 0 0 2px #ede9fe;
}

.node-legend .size-hint {
  margin-left: auto;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.legend-item {
  min-height: 24px;
  padding: 0 7px;
  border: 1px solid #e2e8f0;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 5px;
  color: #475569;
  background: #ffffff;
  cursor: pointer;
  font-size: 9px;
}

.legend-item:hover {
  border-color: #93c5fd;
  color: #1d4ed8;
}

.legend-item.muted {
  opacity: 0.35;
}

.legend-item i {
  width: 14px;
  height: 3px;
  border-radius: 999px;
}

.legend-item em {
  color: #94a3b8;
  font-size: 8px;
  font-style: normal;
}

.node-tooltip {
  position: absolute;
  z-index: 12;
  width: min(250px, calc(100% - 24px));
  padding: 10px 11px;
  border: 1px solid #dbe4ef;
  border-radius: 8px;
  color: #334155;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.17);
  pointer-events: none;
}

.node-tooltip strong,
.node-tooltip span,
.node-tooltip small {
  display: block;
}

.node-tooltip strong {
  color: #0f172a;
  font-size: 12px;
  line-height: 1.45;
}

.node-tooltip span {
  margin-top: 2px;
  color: #64748b;
  font-size: 9px;
}

.node-tooltip .tooltip-row {
  margin-top: 8px;
  padding-top: 7px;
  border-top: 1px solid #edf2f7;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
}

.tooltip-row i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.tooltip-row b {
  margin-left: auto;
  color: #7c3aed;
}

.node-tooltip small {
  margin-top: 6px;
  color: #64748b;
  font-size: 9px;
}

.graph-metrics {
  position: absolute;
  right: 14px;
  bottom: 14px;
  padding: 7px 9px;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  display: flex;
  gap: 12px;
  color: #64748b;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
  font-size: 9px;
}

.graph-metrics span {
  display: flex;
  align-items: baseline;
  gap: 3px;
}

.graph-metrics b {
  color: #1e293b;
  font-size: 11px;
}

.graph-minimap {
  position: absolute;
  right: 14px;
  bottom: 58px;
  width: 168px;
  height: 104px;
  padding: 14px 6px 6px;
  border: 1px solid #dbe4ef;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.1);
  cursor: crosshair;
  backdrop-filter: blur(8px);
}

.graph-minimap svg {
  width: 100%;
  height: 100%;
}

.graph-minimap > span {
  position: absolute;
  top: 5px;
  left: 8px;
  color: #64748b;
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0;
}

:deep(.node-selected .node-body) {
  stroke: #0f172a;
  stroke-width: 3.4;
}

:deep(.node-selected .node-pulse) {
  opacity: 0.8;
  transform-box: fill-box;
  transform-origin: center;
  animation: node-pulse 1.8s ease-out infinite;
}

:deep(.node-core .node-focus-ring) {
  stroke-opacity: 0.5;
}

:deep(.node-neighbor .node-focus-ring) {
  stroke-opacity: 0.34;
}

:deep(.graph-link) {
  transition: opacity 0.18s ease;
}

:deep(.module-label) {
  fill: #4c1d95;
}

:deep(.knowledge-label) {
  fill: #334155;
}

.spin {
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes node-pulse {
  0% {
    opacity: 0.85;
    transform: scale(0.82);
  }
  100% {
    opacity: 0;
    transform: scale(1.5);
  }
}

@media (max-width: 760px) {
  .graph-canvas-badge {
    top: 10px;
    right: 10px;
  }

  .graph-controls {
    top: 10px;
    left: 10px;
  }

  .graph-controls button {
    width: 32px;
    height: 32px;
  }

  .graph-legend {
    right: 10px;
    bottom: 10px;
    left: 10px;
    width: auto;
    max-height: 112px;
    overflow-y: auto;
  }

  .graph-metrics {
    display: none;
  }

  .graph-minimap {
    display: none;
  }
}
</style>
