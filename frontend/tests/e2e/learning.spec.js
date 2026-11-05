import { expect, test } from '@playwright/test'
import { readFileSync } from 'node:fs'

const bank = JSON.parse(readFileSync(new URL('../../../backend/content/learning-bank.json', import.meta.url), 'utf8'))
const chapters = bank.chapters.map(c => {
  const qs = bank.questions.filter(q => q.chapter_id === c.id)
  return { id: c.id, title: c.title, objectives: c.objectives, prerequisites: c.prerequisite_chapters,
    practice_count: 4, exam_count: 5, knowledge_points: [...new Map(qs.map(q => [q.main_knowledge_point.id, q.main_knowledge_point])).values()] }
})
function publicQuestion(q) {
  const { id, type, category, stem, options, main_knowledge_point, auxiliary_knowledge_points, learning_objective } = q
  return { id, type, category, stem, options, main_knowledge_point, auxiliary_knowledge_points, learning_objective,
    ...(type === 'numeric' ? { numeric: { unit: q.answer.unit, tolerance: q.answer.tolerance } } : {}) }
}

test.beforeEach(async ({ page }) => {
  await page.route(url => url.pathname.startsWith('/api/'), async route => {
    const path = new URL(route.request().url()).pathname
    if (path === '/api/directory') return route.fulfill({ json: { data: { modules: [] } } })
    if (path === '/api/chat/status') return route.fulfill({ json: { data: { configured: false } } })
    if (path.startsWith('/api/graph/')) return route.fulfill({ json: { data: { nodes: [], links: [], summary: {} } } })
    if (path === '/api/learning/chapters') return route.fulfill({ json: { data: { version: '1.0.1', pass_score: 80, chapters } } })
    const match = path.match(/^\/api\/learning\/chapters\/(L\d\d)$/)
    if (match) {
      const ch = bank.chapters.find(c => c.id === match[1])
      return route.fulfill({ json: { data: { ...chapters.find(c => c.id === ch.id), lesson: ch.teaching_card,
        questions: bank.questions.filter(q => q.chapter_id === ch.id).map(publicQuestion) } } })
    }
    if (path === '/api/learning/chapters/L01/practice') {
      const payload = route.request().postDataJSON()
      expect(payload.question_id).toBe('L01-P01')
      const q = bank.questions.find(q => q.id === payload.question_id)
      return route.fulfill({ json: { data: { question_id: q.id, correct: payload.answer === 'B',
        submitted_answer: payload.answer, correct_answer: 'B', explanation: q.explanation,
        option_feedback: q.option_feedback, sources: [], main_knowledge_point: q.main_knowledge_point } } })
    }
    return route.fulfill({ status: 404, json: { detail: 'Not configured in this UI fixture' } })
  })
})

test('lesson, keyboard answer, immediate explanation and continued progress after reload', async ({ page }) => {
  await page.goto('/#learn')
  await expect(page.getByRole('heading', { name: 'GIS 与 QGIS 基础', exact: true })).toBeVisible()
  await expect(page.getByRole('button', { name: /2 路网数据与坐标/ })).toBeDisabled()
  await page.getByRole('button', { name: '学完了，开始练习' }).click()
  await expect(page.getByRole('button', { name: '核对答案', exact: true })).toBeDisabled()
  await page.locator('input[value="B"]').focus()
  await page.keyboard.press('Space')
  await page.getByRole('button', { name: '核对答案', exact: true }).click()
  await expect(page.getByText('回答正确', { exact: true })).toBeVisible()
  await expect(page.getByText('练习 1 / 4', { exact: true })).toBeVisible()
  await page.reload()
  await expect(page.getByText('练习 1 / 4', { exact: true })).toBeVisible()
  await expect(page.locator('#question-L01-P02')).toBeVisible()
})

test('mobile layout and denied storage keep the learning flow usable', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.addInitScript(() => { Storage.prototype.setItem = () => { throw new Error('storage unavailable') } })
  await page.goto('/#learn')
  await expect(page.getByText(/浏览器未能保存进度/)).toBeVisible()
  await expect(page.getByLabel('选择关卡', { exact: true })).toBeVisible()
  await page.getByRole('button', { name: '学完了，开始练习' }).click()
  await page.locator('input[value="B"]').check()
  await page.getByRole('button', { name: '核对答案', exact: true }).click()
  await expect(page.getByText('回答正确', { exact: true })).toBeVisible()
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
})

test('practice network failure preserves the selection and allows resubmission', async ({ page }) => {
  await page.goto('/#learn')
  await page.getByRole('button', { name: '学完了，开始练习' }).click()
  await page.locator('input[value="B"]').check()
  await page.route('**/api/learning/chapters/L01/practice', route => route.fulfill({ status: 503, json: { detail: '核对暂时不可用，请重试。' } }), { times: 1 })
  await page.getByRole('button', { name: '核对答案', exact: true }).click()
  await expect(page.getByRole('alert')).toContainText('核对暂时不可用')
  await expect(page.locator('input[value="B"]')).toBeChecked()
  await page.getByRole('button', { name: '核对答案', exact: true }).click()
  await expect(page.getByText('回答正确', { exact: true })).toBeVisible()
})

test('teaching can be read without video and self-check answers remain hidden until requested', async ({ page }) => {
  await page.goto('/#learn')
  const teaching = page.getByRole('region', { name: '教学讲解', exact: true })
  await expect(teaching).toContainText('从看地图到分析道路')
  const image = teaching.locator('figure img').first()
  await image.scrollIntoViewIfNeeded()
  await expect(image).toHaveJSProperty('complete', true)
  expect(await image.evaluate(img => img.naturalWidth)).toBeGreaterThan(0)
  const answers = teaching.locator('.teaching-self-check')
  await expect(answers).not.toHaveAttribute('open')
  await answers.locator('summary').click()
  await expect(answers).toHaveAttribute('open', '')
  await expect(answers).toContainText('研究站房占地可以使用面')
  await page.getByRole('button', { name: '学完了，开始练习' }).click()
  await expect(page.locator('#question-L01-P01')).toBeVisible()
})

test('chapter three presents shared units and readable mobile teaching tables', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.addInitScript(() => localStorage.setItem('gis-learning-progress-v1', JSON.stringify({
    version: '1.0.1', lastChapter: 'L03', chapters: { L01: { bestScore: 100 }, L02: { bestScore: 100 } },
  })))
  await page.goto('/#learn')
  const teaching = page.locator('.teaching-section')
  await expect(teaching.locator('.teaching-unit')).toHaveCount(4)
  const sample = teaching.locator('.teaching-unit').nth(1)
  await sample.locator(':scope > summary').click()
  await expect(sample).toContainText('地图上相交的道路，真的能转过去吗')
  await sample.locator('.teaching-self-check > summary').click()
  await expect(sample.locator('.teaching-self-check')).toHaveAttribute('open', '')
  for (const table of await teaching.locator('.teaching-table-wrap:visible').all()) {
    expect(await table.evaluate(el => el.getBoundingClientRect().right <= innerWidth)).toBe(true)
  }
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
})

test('a partial retake stays active after lesson review and reload', async ({ page }) => {
  const qs = bank.questions.filter(q => q.chapter_id === 'L01')
  const result = q => ({ question_id: q.id, correct: true,
    submitted_answer: q.type === 'numeric' ? String(q.answer.value) : q.answer,
    correct_answer: q.answer, explanation: q.explanation,
    option_feedback: q.option_feedback, sources: [], main_knowledge_point: q.main_knowledge_point })
  const practice = qs.filter(q => q.category === 'practice')
  const saved = { version: '1.0.1', lastChapter: 'L01', chapters: { L01: {
    learned: true, phase: 'result', bestScore: 100, examAnswers: {}, examInProgress: false,
    practiceAnswers: Object.fromEntries(practice.map(q => [q.id, q.answer])),
    practiceResults: Object.fromEntries(practice.map(q => [q.id, result(q)])),
    lastExam: { chapter_id: 'L01', score: 100, total: 100, correct_count: 5, question_count: 5,
      passed: true, results: qs.filter(q => q.category === 'exam').map(result) },
  } } }
  await page.addInitScript(value => {
    if (!sessionStorage.getItem('test-progress-seeded')) {
      localStorage.setItem('gis-learning-progress-v1', JSON.stringify(value))
      sessionStorage.setItem('test-progress-seeded', 'yes')
    }
  }, saved)
  await page.goto('/#learn')
  await page.getByRole('button', { name: '重新考试', exact: true }).click()
  await page.locator('#question-L01-E01 input[value="B"]').check()
  await page.getByRole('button', { name: '知识讲解', exact: true }).click()
  await page.reload()
  await page.getByRole('button', { name: '章节考试', exact: true }).click()
  await expect(page.locator('#question-L01-E01 input[value="B"]')).toBeChecked()
  await expect(page.getByRole('button', { name: '交卷并查看解析' })).toBeVisible()
})
