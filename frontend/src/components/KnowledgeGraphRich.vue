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
        <span class="zoom-symbol" aria-hidden="true">+</span>
      </button>
      <button
        type="button"
        title="缩小"
        aria-label="缩小图谱"
        @click="zoomBy(0.8)"
      >
        <span class="zoom-symbol" aria-hidden="true">−</span>
      </button>
      <button
        type="button"
        title="适应画布"
        aria-label="适应画布"
        @click="fitGraph(true)"
      >
        适配
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
import { arrangeLearningGraph, arrangeCourseGraph, nodeBoundary, setLabelGeometry } from '../graph/layout'
import { LoaderCircle } from '@lucide/vue'
import {
  DIFFICULTY_COLORS,
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
  courseOverview: { type: Boolean, default: false },
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
  props.courseOverview ? '全课程知识网络 · 放大查看细节' : knowledgePointCount.value > 0 ? '模块知识网络' : '课程模块网络',
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

function relationColor(type) {
  return RELATION_COLORS[type] || '#94a3b8'
}

function relationDash(type) {
  return RELATION_DASHES[type] || null
}

function relationOpacity(type) {
  if (hiddenRelationTypes.value.has(type)) return 0.04
  if (props.courseOverview) return type === 'RELATED_TO' || type === 'BELONGS_TO' ? .09 : .3
  if (type === 'BELONGS_TO') return 0.16
  return 0.68
}

function relationStrokeWidth(type) {
  if (props.courseOverview) return type === 'BELONGS_TO' || type === 'RELATED_TO' ? .5 : .8
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
  updateCourseLabels()
}

function updateCourseLabels() {
  if (!props.courseOverview || !labelSelection || !svgSelection?.node()) return
  const transform = d3.zoomTransform(svgSelection.node())
  const occupied = []
  const visible = new Set()
  const texts = labelSelection.nodes()
  // Keep module names readable in the whole-course view. At closer zoom levels,
  // reveal only labels that fit on screen without covering another label.
  for (const node of renderedNodes.filter(n => getNodeType(n.labels) === 'Module')) {
    const font = Math.min(96, Math.max(18, 12 / transform.k))
    setLabelGeometry(node, 'middle', 0, node.radius + font * 1.25, font, font * 1.22)
    const text = d3.select(texts.find(el => el.__data__ === node))
    text.attr('font-size', font).selectAll('tspan').attr('y', (_, i) => node.labelY + i * node.labelStep)
    occupied.push(node.labelBounds)
    visible.add(node.id)
  }
  if (transform.k >= .65) {
    for (const node of renderedNodes.filter(n => getNodeType(n.labels) === 'KnowledgePoint')) {
      const box = node.labelBounds
      const x = box.left * transform.k + transform.x, y = box.top * transform.k + transform.y
      if (x > renderSize.width || y > renderSize.height || box.right * transform.k + transform.x < 0 || box.bottom * transform.k + transform.y < 0) continue
      if (occupied.some(other => box.left < other.right + 8 && box.right + 8 > other.left && box.top < other.bottom + 8 && box.bottom + 8 > other.top)) continue
      occupied.push(box)
      visible.add(node.id)
    }
  }
  labelSelection.style('display', n => visible.has(n.id) ? null : 'none')
}

function buildCurvedPath(link) {
  const source = link.source, target = link.target
  if (!Number.isFinite(source?.x) || !Number.isFinite(target?.x)) return ''
  const dx = target.x - source.x, dy = target.y - source.y
  const a = nodeBoundary(source, dx, dy, 2)
  const b = nodeBoundary(target, -dx, -dy, 3)
  return `M${a.x},${a.y} L${b.x},${b.y}`
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
    .attr('fill', '#2f70bb')
    .attr('fill-opacity', 0.08)
    .attr('stroke', '#2f70bb')
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

  const definitions = svgSelection.append('defs')
  const sphereColors = [...new Set(nodes.map(getNodeColor))]
  for (const color of sphereColors) {
    const gradient = definitions.append('radialGradient')
      .attr('id', `node-sphere-${color.slice(1)}`)
      .attr('cx', '32%').attr('cy', '27%').attr('r', '76%')
      .attr('fx', '28%').attr('fy', '23%')
    for (const [offset, tint] of [
      ['0%', d3.interpolateRgb(color, '#ffffff')(.9)],
      ['24%', d3.interpolateRgb(color, '#ffffff')(.48)],
      ['58%', color],
      ['100%', d3.color(color).darker(.45).formatHex()],
    ]) gradient.append('stop').attr('offset', offset).attr('stop-color', tint)
  }
  for (const [type, color] of Object.entries(RELATION_COLORS)) {
    definitions
      .append('marker')
      .attr('id', `graph-arrow-${type}`)
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 10)
      .attr('refY', 0)
      .attr('markerUnits', 'userSpaceOnUse')
      .attr('markerWidth', 4.5)
      .attr('markerHeight', 4.5)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', color)
  }

  zoomBehavior = d3
    .zoom()
    .scaleExtent([props.courseOverview ? .025 : .22, props.courseOverview ? 12 : 5])
    .on('zoom', (event) => {
      graphSelection.attr('transform', event.transform)
      updateCourseLabels()
      scheduleMinimapUpdate()
    })

  svgSelection.call(zoomBehavior)
  graphSelection = svgSelection.append('g')

  if (props.courseOverview) arrangeCourseGraph(nodes, links)
  else arrangeLearningGraph(nodes, width, height)
  const nodesById = new Map(nodes.map(node => [node.id, node]))
  links.forEach(link => { link.source = nodesById.get(link.source); link.target = nodesById.get(link.target) })

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
    .attr('vector-effect', props.courseOverview ? 'non-scaling-stroke' : null)
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
    .attr('tabindex', 0)
    .attr('role', 'button')
    .attr('aria-label', (node) => getNodeName(node))
    .on('keydown', (event, node) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault()
        emit('node-click', node)
      }
    })
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
    .attr('class', 'node-body')
    .attr('r', node => node.radius)
    .attr('fill', node => `url(#node-sphere-${getNodeColor(node).slice(1)})`)
    .attr('stroke', node => d3.color(getNodeColor(node)).darker(.4).formatHex())
    .attr('stroke-width', node => props.courseOverview && getNodeType(node.labels) === 'KnowledgePoint' ? .65 : 1.3)
    .attr('vector-effect', node => props.courseOverview && getNodeType(node.labels) === 'KnowledgePoint' ? 'non-scaling-stroke' : null)

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

  labelSelection = nodeGroups.append('text')
    .attr('class', node => getNodeType(node.labels) === 'Module' ? 'module-label' : 'knowledge-label')
    .attr('font-size', node => node.fontSize)
    .attr('font-weight', node => getNodeType(node.labels) === 'Module' || node.properties?.importance === '核心' ? 600 : 400)
    .attr('text-anchor', node => node.labelAnchor)
    .attr('fill', '#24373d')
    .attr('paint-order', 'stroke')
    .attr('stroke', '#f0f5f5')
    .attr('stroke-width', 4)
    .attr('stroke-linejoin', 'round')
    .style('pointer-events', 'auto')
    .style('user-select', 'none')
  labelSelection.each(function(node) {
    d3.select(this).selectAll('tspan').data(node.displayLines).enter().append('tspan')
      .attr('x', node.labelX).attr('y', (_, index) => node.labelY + index * node.labelStep).text(line => line)
  })

  applyVisualState(nodes, links)
  scheduleMinimapUpdate()
  fitTimer = setTimeout(() => {
    fitGraph(false)
  }, 500)

  function updatePositions(activeLinks) {
    activeLinks.forEach((link, index) => {
      link.path = buildCurvedPath(link, index)
    })
    linkSelection.attr('d', (link) => link.path || '')
    nodeSelection.attr(
      'transform',
      (node) => `translate(${node.x},${node.y})`,
    )
    if (props.courseOverview) {
      nodes.forEach(node => setLabelGeometry(node, node.labelAnchor, node.labelX, node.labelY))
      updateCourseLabels()
    }
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
    node.fx = node.x
    node.fy = node.y
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

  const usableWidth = Math.max(260, width - 64)
  const usableHeight = Math.max(props.courseOverview ? 180 : 220, height - (props.courseOverview ? 110 : 150))
  let scale = Math.max(props.courseOverview ? .025 : .22, Math.min(1.45, Math.min(usableWidth / bounds.width, usableHeight / bounds.height) * 0.96))
  const midX = bounds.x + bounds.width / 2
  const midY = bounds.y + bounds.height / 2
  const centerY = (height - 90) / 2
  if (props.courseOverview) {
    const canvas = graphContainer.value.getBoundingClientRect()
    const obstacles = [...graphContainer.value.querySelectorAll('.graph-legend,.graph-minimap,.graph-controls,.graph-canvas-badge')].map(el => {
      const rect = el.getBoundingClientRect()
      return { left: rect.left - canvas.left - 8, right: rect.right - canvas.left + 8, top: rect.top - canvas.top - 8, bottom: rect.bottom - canvas.top + 8 }
    })
    // Use the biggest circle that actually clears the controls, rather than
    // reserving an entire bottom strip for a legend tucked into one corner.
    for (let attempt = 0; attempt < 80; attempt++) {
      const covered = renderedNodes.some(node => {
        const x = width / 2 + (node.x - midX) * scale
        const y = centerY + (node.y - midY) * scale
        const r = node.radius * scale
        return obstacles.some(box => x - r < box.right && x + r > box.left && y - r < box.bottom && y + r > box.top)
      })
      if (!covered || scale <= .025) break
      scale = Math.max(.025, scale * .98)
    }
  }
  const transform = d3.zoomIdentity
    .translate(width / 2, centerY)
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
  () => [props.nodes, props.links, props.courseOverview],
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
