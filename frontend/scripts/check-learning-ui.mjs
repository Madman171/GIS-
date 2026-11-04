// Production-build QA against the real local grader. No mock grading or real student data.
import { chromium } from '@playwright/test'
import { readFile, mkdir, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { resolve } from 'node:path'
import assert from 'node:assert/strict'

const root = fileURLToPath(new URL('../../', import.meta.url))
const bank = JSON.parse(await readFile(resolve(root, 'backend/content/learning-bank.json'), 'utf8'))
const base = process.env.LEARNING_BASE_URL || 'http://127.0.0.1:5182'
const out = resolve(root, 'artifacts/learning-release/2026-11-04')
await mkdir(out, { recursive: true })
const browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || 'msedge', headless: true })
const results = []
try {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } })
  const page = await context.newPage()
  const errors = []
  page.on('pageerror', error => errors.push(error.message))
  await page.goto(`${base}/#learn`, { waitUntil: 'networkidle' })
  await page.getByRole('heading', { name: bank.chapters[0].title, exact: true }).waitFor()
  await page.screenshot({ path: resolve(out, 'learning-desktop.png') })
  async function fillQuestion(q, answer, container = page.locator(`#question-${q.id}`)) {
    if (q.type === 'single') await container.locator(`input[value="${answer}"]`).check()
    else if (q.type === 'multiple') for (const value of answer) await container.locator(`input[value="${value}"]`).check()
    else if (q.type === 'true_false') await container.locator('input[type=radio]').nth(answer ? 0 : 1).check()
    else await container.locator('input[inputmode=decimal]').fill(String(answer))
  }
  for (const [chapterIndex, chapter] of bank.chapters.entries()) {
    const chapterQs = bank.questions.filter(q => q.chapter_id === chapter.id)
    const practice = chapterQs.filter(q => q.category === 'practice')
    const exams = chapterQs.filter(q => q.category === 'exam')
    await page.getByRole('heading', { name: chapter.title, exact: true }).waitFor()
    await page.getByRole('button', { name: '学完了，开始练习', exact: true }).click()
    for (const [index, q] of practice.entries()) {
      await page.locator(`#question-${q.id}`).waitFor()
      const answer = q.type === 'numeric' ? q.answer.value : q.answer
      await fillQuestion(q, answer)
      await page.getByRole('button', { name: '核对答案', exact: true }).click()
      await page.locator(`#question-${q.id} .answer-feedback.is-correct`).waitFor()
      if (chapterIndex === 0 && index === 0) {
        await page.getByText('逐项解析', { exact: true }).click()
        await page.getByText('查阅依据', { exact: true }).click()
        assert((await page.locator('.source-list a').count()) > 0)
        await page.screenshot({ path: resolve(out, 'practice-feedback-desktop.png') })
        await page.getByRole('button', { name: /^回看知识点：/ }).click()
        await page.getByRole('dialog', { name: '知识点详情' }).waitFor()
        await page.getByRole('button', { name: '关闭详情', exact: true }).click()
        assert(await page.getByRole('heading', { name: '理解后，再向前一步' }).isVisible())
      }
      if (index < practice.length - 1) await page.getByRole('button', { name: '下一题 →', exact: true }).click()
    }
    // Reload really restores completed practice and the question, not just the count.
    if (chapterIndex === 0) {
      await page.reload({ waitUntil: 'networkidle' })
      await page.getByText('练习 4 / 4', { exact: true }).waitFor()
    }
    await page.getByRole('button', { name: '开始章节考试', exact: true }).click()
    assert(await page.getByRole('button', { name: '交卷并查看解析' }).isDisabled())
    assert.equal(await page.locator('.answer-feedback').count(), 0)
    if (chapterIndex === 0) {
      // A real failing attempt: first 2 correct = 40. Answers/feedback appear only after submission.
      for (const [index, q] of exams.entries()) {
        let answer = q.answer
        if (index >= 2) answer = q.type === 'true_false' ? !q.answer : q.options.find(o => o.id !== q.answer).id
        await fillQuestion(q, answer)
      }
      await page.getByRole('button', { name: '交卷并查看解析' }).click()
      await page.getByRole('heading', { name: '再巩固一下，你可以重试' }).waitFor()
      assert.equal(await page.locator('.exam-score strong').innerText(), '40')
      assert(await page.getByRole('button', { name: /2 路网数据与坐标/ }).isDisabled())
      await page.getByRole('button', { name: '重新考试', exact: true }).click()
    }
    for (const q of exams) await fillQuestion(q, q.type === 'numeric' ? q.answer.value : q.answer)
    await page.getByRole('button', { name: '交卷并查看解析' }).click()
    await page.getByRole('heading', { name: '本关通过，继续前行' }).waitFor()
    assert.equal(await page.locator('.exam-score strong').innerText(), '100')
    assert.equal(await page.locator('.exam-review-question').count(), 5)
    assert.equal(await page.locator('.answer-feedback').count(), 5)
    if (chapterIndex === 0) await page.screenshot({ path: resolve(out, 'exam-result-desktop.png') })
    results.push({ chapter: chapter.id, practice: practice.length, exam: exams.length, score: 100 })
    if (chapterIndex < bank.chapters.length - 1) await page.getByRole('button', { name: '进入下一关 →', exact: true }).click()
  }
  assert.equal(await page.locator('.learning-rail-heading > span').innerText(), '6 / 6 关已通过')
  await page.reload({ waitUntil: 'networkidle' })
  await page.getByText('6 / 6 关已通过', { exact: true }).waitFor()
  await page.getByRole('button', { name: '知识图谱', exact: true }).click()
  await page.getByRole('img', { name: '知识图谱可视化', exact: true }).waitFor()
  await page.getByRole('button', { name: '学习闯关', exact: true }).click()
  await page.getByText('6 / 6 关已通过', { exact: true }).waitFor()
  // Read stored results on phone and keyboard interaction on a fresh phone context.
  await page.setViewportSize({ width: 390, height: 844 })
  await page.screenshot({ path: resolve(out, 'exam-result-mobile.png') })
  assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth))
  const phone = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })
  const mobile = await phone.newPage()
  mobile.on('pageerror', e => errors.push(e.message))
  await mobile.goto(`${base}/#learn`, { waitUntil: 'networkidle' })
  await mobile.getByRole('button', { name: '学完了，开始练习' }).waitFor()
  await mobile.screenshot({ path: resolve(out, 'lesson-mobile.png') })
  await mobile.getByRole('button', { name: '学完了，开始练习' }).click()
  await mobile.locator('input[value="B"]').check()
  await mobile.getByRole('button', { name: '核对答案', exact: true }).click()
  await mobile.locator('.answer-feedback.is-correct').waitFor()
  await mobile.screenshot({ path: resolve(out, 'practice-feedback-mobile.png') })
  assert(await mobile.evaluate(() => document.documentElement.scrollWidth <= innerWidth))
  assert.equal(errors.length, 0, errors.join('\n'))
  await writeFile(resolve(out, 'browser-verification.json'), JSON.stringify({ base, chapters: results, practice_count: 24, exam_count: 30, tested_failed_attempt: true, reload_and_return_preserves_progress: true, knowledge_dialog_return: true, desktop_and_phone: true, script_errors: errors }, null, 2))
  console.log('PASS: 6 chapters, all 54 questions, failed exam + retry, unlocking, source links, knowledge dialog, reload persistence, 390px mobile, no script errors.')
} finally { await browser.close() }
