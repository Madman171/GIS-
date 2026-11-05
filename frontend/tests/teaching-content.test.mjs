import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync, existsSync } from 'node:fs'
import { inlineParts, parseMarkdown, safeLink } from '../src/teaching/markdown.js'

const content = JSON.parse(readFileSync(new URL('../src/teaching/content.json', import.meta.url), 'utf8'))
const bank = JSON.parse(readFileSync(new URL('../../backend/content/learning-bank.json', import.meta.url), 'utf8'))

test('all graded targets have teaching in their chapter; no nonexistent mapping or image', () => {
  const target = [...new Set(bank.questions.map(q => q.main_knowledge_point.id))].sort()
  assert.deepEqual(Object.keys(content.knowledgePointLessons).sort(), target)
  const units = new Map(content.lessons.map(l => [l.id, l]))
  for (const q of bank.questions) {
    const taught = content.chapterLessons[q.chapter_id].flatMap(id => units.get(id).knowledgePointIds)
    assert.ok(taught.includes(q.main_knowledge_point.id), q.id)
  }
  const sources = new Set(content.sources.map(s => s.id))
  for (const lesson of content.lessons) {
    assert.ok(lesson.sourceIds.every(id => sources.has(id)), lesson.id)
    const blocks = parseMarkdown(lesson.markdown)
    assert.equal(blocks.filter(b => b.type === 'solution').length, 1, lesson.id)
    assert.ok(blocks.find(b => b.type === 'solution').blocks.length > 0, lesson.id)
    for (const figure of blocks.filter(b => b.type === 'figure')) {
      assert.ok(figure.alt.length > 8)
      assert.ok(existsSync(new URL(`../public${figure.src}`, import.meta.url)), figure.src)
    }
    assert.ok(blocks.filter(b => b.type === 'table').every(b => b.rows.every(r => r.length === b.headers.length)), lesson.id)
  }
})

test('authored text cannot become HTML, unsafe links or escaped image paths', () => {
  assert.equal(safeLink('javascript:alert(1)'), null)
  assert.equal(safeLink('data:text/html,<script>'), null)
  assert.equal(safeLink('https://docs.qgis.org/3.44/'), 'https://docs.qgis.org/3.44/')
  const parts = inlineParts('<img src=x onerror=alert(1)> **重点** [假链接](javascript:alert)')
  assert.equal(parts[0].type, 'text')
  assert.match(parts[0].text, /onerror/)
  assert.equal(parts.at(-1).href, null)
  for (const src of ['https://evil.test/x.svg', '/assets/teaching/../x.svg', '/assets/teaching/%2e%2e/x.svg', '/assets/teaching/x.svg?bad']) {
    assert.equal(parseMarkdown(`![示意](${src})`).length, 0)
  }
})

test('self-check solutions stay grouped; tables, code and next section remain separate', () => {
  const blocks = parseMarkdown('# 重复标题\n\n| 段 | 分钟 |\n|---|---|\n| A | 2 |\n\n## 自测答案与解析\n\n1. 先统一单位\n\n### 说明\n\n```text\n<x>\n```\n\n## 参考\n\n新的段落')
  assert.deepEqual(blocks.map(b => b.type), ['table', 'solution', 'heading', 'paragraph'])
  assert.equal(blocks[1].blocks.find(b => b.type === 'code').text, '<x>')
  assert.equal(blocks[0].rows[0][1], '2')
})
