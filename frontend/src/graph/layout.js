// Circular course map. Positions arrange real nodes only; links always
// come from the source graph, never from proximity or the visual ordering.
export function labelLines(text, capacity = 12) {
  const lines = []
  let line = '', size = 0
  for (const char of String(text || '')) {
    const weight = /[\x00-\x7f]/.test(char) ? .55 : 1
    if (size + weight > capacity && line) { lines.push(line); line = ''; size = 0 }
    line += char; size += weight
  }
  if (line) lines.push(line)
  return lines
}

export function prepareNode(node) {
  const module = node.labels.includes('Module')
  node.lines = labelLines(node.properties?.name, 11)
  node.displayLines = node.lines.length > 2 ? [node.lines[0], node.lines[1].slice(0, -1) + '…'] : node.lines
  node.radius = module ? 42 : node.properties?.importance === '核心' ? 29 : 23
  node.fontSize = module ? 16 : 14
  node.labelStep = 19
  node.boxWidth = node.boxHeight = node.radius * 2
  return node
}

export function setLabelGeometry(node, anchor, x, y, fontSize = node.fontSize, step = node.labelStep) {
  node.labelAnchor = anchor
  node.labelX = x
  node.labelY = y
  node.fontSize = fontSize
  node.labelStep = step
  const textWidth = Math.max(...node.displayLines.map(line => [...line].reduce((sum, c) => sum + (/[\x00-\x7f]/.test(c) ? .55 : 1), 0))) * fontSize
  const left = anchor === 'middle' ? -textWidth / 2 : anchor === 'start' ? x : x - textWidth
  node.labelBounds = { left: node.x + left, right: node.x + left + textWidth, top: node.y + y - fontSize, bottom: node.y + y + (node.displayLines.length - 1) * step + 4 }
}

function place(node, x, y, angle = -Math.PI / 2) {
  node.x = node.fx = x
  node.y = node.fy = y
  const side = Math.cos(angle)
  const anchor = Math.abs(side) < .32 ? 'middle' : side > 0 ? 'start' : 'end'
  const labelX = anchor === 'middle' ? 0 : Math.sign(side) * (node.radius + 11)
  const labelY = anchor === 'middle'
    ? (Math.sin(angle) < 0 ? -node.radius - 13 - (node.displayLines.length - 1) * 19 : node.radius + 25)
    : 5 - (node.displayLines.length - 1) * 19 / 2
  setLabelGeometry(node, anchor, labelX, labelY)
}

export function arrangeCourseGraph(nodes, links = []) {
  nodes.forEach(prepareNode)
  const modules = nodes.filter(n => n.labels.includes('Module')).sort((a,b) => a.id.localeCompare(b.id, undefined, { numeric: true }))
  const membership = new Map(links.filter(link => link.type === 'BELONGS_TO').map(link => [String(link.source?.id ?? link.source), String(link.target?.id ?? link.target)]))
  const order = new Map(modules.map((n, i) => [n.id, i]))
  const knowledge = nodes.filter(n => n.labels.includes('KnowledgePoint')).sort((a,b) => (order.get(membership.get(a.id) || a.properties?.module_id) ?? 999) - (order.get(membership.get(b.id) || b.properties?.module_id) ?? 999) || (a.properties?.sort_order ?? 999) - (b.properties?.sort_order ?? 999) || a.id.localeCompare(b.id))
  // A compact cluster of real module nodes occupies the middle. No synthetic topic
  // or links are added. Knowledge points remain on one continuous outer circle.
  const slots = [[0,0],[-720,-600],[0,-600],[720,-600],[720,0],[720,600],[0,600],[-720,600],[-720,0]]
  modules.forEach((node, i) => {
    node.radius = i === 0 ? 130 : 100
    node.boxWidth = node.boxHeight = node.radius * 2
    node.lines = labelLines(node.properties?.name, 7)
    node.displayLines = node.lines.length > 2 ? [node.lines[0], node.lines[1].slice(0, -1) + '…'] : node.lines
    const [x,y] = slots[i] || [Math.cos(i) * 1000, Math.sin(i) * 1000]
    place(node, x, y)
    setLabelGeometry(node, 'middle', 0, node.radius + 90, 72, 88)
  })
  const radius = Math.max(1700, knowledge.length * 35 / (2 * Math.PI))
  knowledge.forEach((node, i) => {
    node.radius = node.properties?.importance === '核心' ? 15 : 11
    node.boxWidth = node.boxHeight = node.radius * 2
    const angle = -Math.PI / 2 + i * Math.PI * 2 / knowledge.length
    node.orbit = radius
    place(node, Math.cos(angle) * radius, Math.sin(angle) * radius, angle)
  })
}

function overlaps(a, b) {
  const boxes = n => [
    { left: n.x - n.radius - 5, right: n.x + n.radius + 5, top: n.y - n.radius - 5, bottom: n.y + n.radius + 5 },
    n.labelBounds,
  ]
  return boxes(a).some(x => boxes(b).some(y => x.left < y.right + 8 && x.right + 8 > y.left && x.top < y.bottom + 8 && x.bottom + 8 > y.top))
}

function placeRing(group, radius, inside = [], capped = false) {
  for (let attempt = 0; attempt < 100; attempt++, radius += 12) {
    group.forEach((n, i) => {
      if (capped && group.length > 4 && i < 2) {
        const angle = i === 0 ? -Math.PI / 2 : Math.PI / 2
        n.orbit = radius
        place(n, 0, Math.sin(angle) * radius, angle)
        return
      }
      // Even vertical spacing on each semicircle leaves room for outside labels,
      // rather than crowding many long titles at the top of a uniform-angle ring.
      const offset = capped && group.length > 4 ? 2 : 0
      const length = group.length - offset
      const index = i - offset
      const rightCount = Math.ceil(length / 2)
      const right = index < rightCount
      const count = right ? rightCount : length - rightCount
      const slot = right ? index : length - index - 1
      const vertical = -1 + (slot + .5) * 2 / count
      const angle = right ? Math.asin(vertical) : Math.PI - Math.asin(vertical)
      n.orbit = radius
      place(n, Math.cos(angle) * radius, Math.sin(angle) * radius, angle)
    })
    if (!group.some((n, i) => [...group.slice(i + 1), ...inside].some(other => overlaps(n, other)))) return radius
  }
  return radius
}

export function arrangeLearningGraph(nodes) {
  nodes.forEach(prepareNode)
  const knowledge = nodes.filter(n => !n.labels.includes('Module'))
  const modules = nodes.filter(n => n.labels.includes('Module'))
  if (!knowledge.length) {
    const ordered = [...modules].sort((a,b) => a.id.localeCompare(b.id, undefined, { numeric: true }))
    if (!ordered.length) return
    place(ordered[0], 0, 0)
    ordered.slice(1).forEach(n => { n.radius = 34; n.boxWidth = n.boxHeight = 68 })
    placeRing(ordered.slice(1), 220, [ordered[0]])
    return
  }
  modules.forEach((n, i) => place(n, i * 160, 0))
  const ordered = [...knowledge].sort((a,b) => (a.properties?.importance === '核心' ? 0 : 1) - (b.properties?.importance === '核心' ? 0 : 1) || (a.properties?.sort_order ?? 999) - (b.properties?.sort_order ?? 999) || a.id.localeCompare(b.id))
  ordered.forEach(node => {
    node.radius = node.properties?.importance === '核心' ? 22 : 18
    node.boxWidth = node.boxHeight = node.radius * 2
  })
  placeRing(ordered, Math.max(240, ordered.length * 12), modules, true)
}

export function nodeBoundary(node, dx, dy, extra = 0) {
  const t = (node.radius + extra) / Math.max(Math.hypot(dx, dy), .00001)
  return { x: node.x + dx * t, y: node.y + dy * t }
}
