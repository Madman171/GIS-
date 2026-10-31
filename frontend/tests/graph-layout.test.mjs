import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { arrangeLearningGraph, arrangeCourseGraph, nodeBoundary, labelLines } from '../src/graph/layout.js'

const snapshot = JSON.parse(await readFile(new URL('../../data/graph-snapshot.json', import.meta.url), 'utf8'))
const sourceNodes = snapshot.nodes.map(n => ({ id: n.businessId, labels: n.labels, properties: n.properties }))
const modules = sourceNodes.filter(n => n.labels.includes('Module'))
const clone = value => structuredClone(value)

test('every real module keeps its names and readable, non-overlapping circular nodes and labels', () => {
  for (const module of modules) {
    const ids = new Set(snapshot.relationships.filter(r => r.type === 'BELONGS_TO' && r.targetBusinessId === module.id).map(r => r.sourceBusinessId))
    const original = sourceNodes.filter(n => n.id === module.id || ids.has(n.id))
    for (const width of [1100, 600, 390]) {
      const nodes = clone(original)
      arrangeLearningGraph(nodes, width, 720)
      assert.equal(nodes.length, original.length)
      nodes.forEach((node, i) => {
        assert.equal(node.lines.join(''), original[i].properties.name)
        assert.ok(Number.isFinite(node.x) && Number.isFinite(node.y))
        assert.ok(node.boxWidth > 0 && node.boxHeight > 0)
        for (const other of nodes.slice(i + 1)) {
          assert.ok(Math.hypot(node.x - other.x, node.y - other.y) > node.radius + other.radius, `${module.id}: circles overlap`)
          const a = node.labelBounds, b = other.labelBounds
          assert.ok(!(a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top), `${module.id}: ${node.id} label overlaps ${other.id}`)
        }
      })
      const center = nodes.find(n => n.id === module.id)
      assert.equal(new Set(nodes.filter(n => !n.labels.includes('Module')).map(n => n.orbit)).size, 1, 'every small knowledge point uses the same outer circle')
      assert.equal(center.x, 0)
      assert.equal(center.y, 0)
      for (const n of nodes.filter(n => n !== center)) {
        assert.ok(center.radius > n.radius)
        assert.ok(Math.abs(Math.hypot(n.x, n.y) - n.orbit) < .001, 'knowledge points lie on circular orbits')
      }
    }
  }
})

test('overview layout is stable and wraps mixed Chinese/English names without loss', () => {
  const a = clone(modules), b = clone(modules)
  arrangeLearningGraph(a); arrangeLearningGraph(b)
  assert.deepEqual(a.map(n => [n.id,n.x,n.y]), b.map(n => [n.id,n.x,n.y]))
  const title = '交通路网Node-Edge节点边基础模型定义'
  assert.equal(labelLines(title).join(''), title)
  assert.ok(labelLines(title).length > 1)
})

test('links meet circular boundaries in every direction, including diagonal arrows', () => {
  const node = { x: 100, y: 80, radius: 30 }
  assert.deepEqual(nodeBoundary(node, 400, 0), { x: 130, y: 80 })
  assert.deepEqual(nodeBoundary(node, 0, -200), { x: 100, y: 50 })
  assert.deepEqual(nodeBoundary(node, -400, 0, 4), { x: 66, y: 80 })
  const point = nodeBoundary(node, 100, 100, 3)
  assert.ok(Math.abs(Math.hypot(point.x - node.x, point.y - node.y) - 33) < .001)
})

test('whole-course view retains every knowledge point on one outer circle and modules in the middle', () => {
  const nodes = clone(sourceNodes.filter(n => n.labels.includes('Module') || n.labels.includes('KnowledgePoint')))
  const links = snapshot.relationships.map(r => ({ type: r.type, source: r.sourceBusinessId, target: r.targetBusinessId }))
  const originalLinks = clone(links)
  arrangeCourseGraph(nodes, links)
  const knowledge = nodes.filter(n => n.labels.includes('KnowledgePoint'))
  const centers = nodes.filter(n => n.labels.includes('Module'))
  assert.equal(knowledge.length, 344)
  assert.equal(centers.length, 9)
  assert.equal(new Set(knowledge.map(n => n.orbit)).size, 1)
  for (const node of knowledge) {
    assert.equal(node.lines.join(''), node.properties.name)
    assert.ok(Math.abs(Math.hypot(node.x, node.y) - node.orbit) < .001)
    assert.ok(node.radius < Math.min(...centers.map(n => n.radius)))
    for (const center of centers) assert.ok(Math.hypot(center.x, center.y) + center.radius < node.orbit)
  }
  assert.deepEqual(links, originalLinks, 'layout does not add, remove or rewrite relationships')
})
