import { chromium } from '@playwright/test'
import { mkdir, writeFile } from 'node:fs/promises'
const out = new URL('../../.taste-skill/screens/', import.meta.url)
await mkdir(out, { recursive: true })
const browser = await chromium.launch({ channel: 'msedge' })
const results = []
try {
  for (const width of [1440, 1363, 768, 390]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } })
    const errors = []
    page.on('pageerror', e => errors.push(e.message))
    await page.goto('http://127.0.0.1:5181')
    await page.evaluate(() => document.fonts.ready)
    await page.locator('.graph-node').first().waitFor()
    // Park the draggable companion clear of the graph's legend and minimap for review.
    await page.evaluate(() => localStorage.setItem('gis-knowledge-ai-pet-muted', 'true'))
    if (width <= 1100) await page.getByRole('button', { name: '打开知识目录', exact: true }).click()
    await page.locator('.module-row').first().click()
    await page.locator('.knowledge-row').first().waitFor()
    await page.waitForTimeout(1000)
    await page.screenshot({ path: new URL(`module-${width}.png`, out).pathname.replace(/^\/(?=[A-Z]:)/, '') })
    if (width <= 1100) await page.getByRole('button', { name: '打开知识目录', exact: true }).click()
    await page.locator('.knowledge-row').nth(6).click()
    await page.locator('.detail-panel h2').waitFor()
    await page.waitForTimeout(600)
    await page.screenshot({ path: new URL(`detail-${width}.png`, out).pathname.replace(/^\/(?=[A-Z]:)/, '') })
    const description = await page.locator('.content-section p').innerText()
    const title = await page.locator('.detail-panel h2').innerText()
    await page.locator('.detail-content').evaluate(el => el.scrollTop = el.scrollHeight)
    await page.screenshot({ path: new URL(`resources-${width}.png`, out).pathname.replace(/^\/(?=[A-Z]:)/, '') })
    await page.getByRole('button', { name: '关闭详情', exact: true }).click()
    await page.getByRole('button', { name: '打开小迪图谱小助手，可拖动', exact: true }).click()
    await page.locator('.chat-composer textarea').waitFor()
    await page.screenshot({ path: new URL(`chat-${width}.png`, out).pathname.replace(/^\/(?=[A-Z]:)/, '') })
    results.push({ width, title, description, errors, overflow: await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), resources: true, chat: true })
    await page.close()
  }
} finally { await browser.close() }
await writeFile(new URL('review.json', out), JSON.stringify(results, null, 2))
console.log(JSON.stringify(results, null, 2))
