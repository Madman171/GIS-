// Read-only production-build QA. Seeded progress exists only in this isolated browser.
import { chromium } from '@playwright/test'
import { readFile, mkdir, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { resolve } from 'node:path'
import assert from 'node:assert/strict'

const root = fileURLToPath(new URL('../../', import.meta.url))
const registry = JSON.parse(await readFile(resolve(root, 'frontend/src/teaching/content.json'), 'utf8'))
const base = process.env.LEARNING_BASE_URL || 'http://127.0.0.1:5182'
const out = resolve(root, process.env.TEACHING_QA_OUT || 'artifacts/teaching-release/2026-11-05/local')
await mkdir(out, { recursive: true })
const browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || 'msedge', headless: true })
const errors = [], checked = [], chapters = [], images = new Set()
try {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } })
  await context.addInitScript(() => localStorage.setItem('gis-learning-progress-v1', JSON.stringify({
    version: '1.0.1', lastChapter: 'L01', chapters: Object.fromEntries(['L01','L02','L03','L04','L05','L06'].map(id => [id, { bestScore: 100 }])),
  })))
  const page = await context.newPage()
  page.on('pageerror', e => errors.push(e.message))
  await page.goto(`${base}/#learn`, { waitUntil: 'networkidle' })
  for (const [id, unitIds] of Object.entries(registry.chapterLessons)) {
    await page.locator('.learning-chapter-list button').nth(Number(id.slice(1))-1).click()
    await page.locator('.teaching-section').waitFor()
    await page.waitForFunction(n => document.querySelectorAll('.teaching-unit').length === n, unitIds.length)
    for (const [index, unitId] of unitIds.entries()) {
      const unit = page.locator('.teaching-unit').nth(index)
      const lesson = registry.lessons.find(l => l.id === unitId)
      assert((await unit.locator(':scope > summary').innerText()).includes(lesson.title))
      if (!(await unit.evaluate(el => el.open))) await unit.locator(':scope > summary').click()
      assert.equal(await unit.locator('.teaching-self-check').count(), 1)
      assert.equal(await unit.locator('.teaching-self-check').evaluate(el => el.open), false)
      await unit.locator('.teaching-self-check > summary').click()
      assert(await unit.locator('.teaching-self-check').evaluate(el => el.open))
      for (const image of await unit.locator('figure img').all()) {
        await image.scrollIntoViewIfNeeded()
        await image.evaluate(img => img.decode())
        assert((await image.evaluate(img => img.naturalWidth)) > 0)
        images.add(await image.getAttribute('src'))
      }
    }
    chapters.push({ id, lessons: unitIds })
  }
  await page.getByRole('button', { name: '知识图谱', exact: true }).click()
  await page.locator('.module-row').first().waitFor()
  const response = await context.request.get(`${base}/api/directory`)
  const modules = (await response.json()).data.modules
  let currentModule = ''
  for (const [kid, lessonIds] of Object.entries(registry.knowledgePointLessons)) {
    const module = modules.find(m => m.knowledgePoints.some(n => n.id === kid))
    assert(module, kid)
    if (currentModule !== module.id) {
      await page.locator('.module-row').filter({ hasText: module.name }).click()
      currentModule = module.id
    }
    await page.locator('.knowledge-row').filter({ hasText: registry.knowledgePointNames[kid] }).first().click()
    const dialog = page.getByRole('dialog', { name: '知识点详情' })
    await dialog.locator('.teaching-unit').first().waitFor()
    assert.equal(await dialog.locator('.teaching-unit').count(), lessonIds.length, kid)
    assert((await dialog.locator('.teaching-unit > summary').first().innerText()).includes(registry.lessons.find(l => l.id === lessonIds[0]).title), kid)
    checked.push(kid)
    await page.getByRole('button', { name: '关闭详情', exact: true }).click()
  }
  const other = modules.flatMap(m => m.knowledgePoints.map(n => ({ ...n, module: m }))).find(n => !registry.knowledgePointLessons[n.id])
  if (currentModule !== other.module.id) await page.locator('.module-row').filter({ hasText: other.module.name }).click()
  await page.locator('.knowledge-row').filter({ hasText: other.name || other.properties.name }).first().click()
  await page.locator('.detail-content').waitFor()
  assert.equal(await page.locator('.detail-panel .teaching-section').count(), 0)
  await page.getByRole('button', { name: '关闭详情', exact: true }).click()

  await page.getByRole('button', { name: '学习闯关', exact: true }).click()
  await page.locator('.learning-chapter-list button').nth(2).click()
  const sample = page.locator('.teaching-unit').nth(1)
  await sample.locator(':scope > summary').click()
  for (const width of [1440,768,390]) {
    await page.setViewportSize({ width, height: width === 768 ? 1024 : 900 })
    await sample.locator(':scope > summary').scrollIntoViewIfNeeded()
    await page.screenshot({ path: resolve(out, `reading-${width}.png`) })
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `overflow ${width}`)
    for (const table of await page.locator('.teaching-table-wrap:visible').all()) assert(await table.evaluate(el => el.getBoundingClientRect().right <= innerWidth))
  }
  await page.setViewportSize({ width: 1440, height: 900 })
  for (const path of images) {
    await page.goto(`${base}${path}`)
    await page.screenshot({ path: resolve(out, path.split('/').at(-1)+'.png') })
    const outside = await page.locator('svg text').evaluateAll(nodes => nodes.filter(n => { const b=n.getBBox(); return b.x < 0 || b.y < 0 || b.x+b.width > n.ownerSVGElement.viewBox.baseVal.width || b.y+b.height > n.ownerSVGElement.viewBox.baseVal.height }).map(n=>n.textContent))
    assert.deepEqual(outside, [], path)
  }
  assert.equal(images.size, 8)
  assert.deepEqual(errors, [])
  await writeFile(resolve(out, 'verification.json'), JSON.stringify({ base, covered_nodes: checked, chapters, image_count: images.size, unchanged_summary_node: other.id, viewport_widths:[1440,768,390], script_errors: errors }, null, 2))
  console.log('PASS: all 24 node popups, six chapters / ten units, eight SVGs, hidden self-checks, unchanged other nodes and three viewport sizes.')
} catch (error) { throw error } finally { await browser.close() }
