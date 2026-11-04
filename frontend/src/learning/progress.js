export const PROGRESS_KEY = 'gis-learning-progress-v1'

export function emptyChapter() {
  return { learned: false, practiceAnswers: {}, practiceResults: {}, examAnswers: {}, examInProgress: false, bestScore: null, lastExam: null, phase: 'lesson' }
}

export function loadProgress(version, chapters, storage) {
  const result = { version, lastChapter: chapters[0]?.id, chapters: {} }
  let warning = ''
  try {
    const raw = (storage ?? window.localStorage).getItem(PROGRESS_KEY)
    const saved = raw ? JSON.parse(raw) : null
    if (saved?.version === version && saved.chapters && typeof saved.chapters === 'object') {
      if (chapters.some(c => c.id === saved.lastChapter)) result.lastChapter = saved.lastChapter
      for (const chapter of chapters) {
        const value = saved.chapters[chapter.id]
        if (!value || typeof value !== 'object') continue
        const state = emptyChapter()
        state.learned = value.learned === true
        if (Number.isInteger(value.bestScore) && value.bestScore >= 0 && value.bestScore <= 100 && value.bestScore % 20 === 0) state.bestScore = value.bestScore
        for (const field of ['practiceAnswers', 'practiceResults', 'examAnswers']) {
          if (value[field] && !Array.isArray(value[field]) && typeof value[field] === 'object') state[field] = value[field]
        }
        if (value.lastExam && Array.isArray(value.lastExam.results) && value.lastExam.results.length === chapter.exam_count && value.lastExam.chapter_id === chapter.id) state.lastExam = value.lastExam
        state.examInProgress = value.examInProgress === true || (value.phase === 'exam' && !state.lastExam)
        if (['lesson', 'practice', 'exam', 'result'].includes(value.phase)) state.phase = value.phase
        if (state.phase === 'result' && !state.lastExam) state.phase = 'lesson'
        result.chapters[chapter.id] = state
      }
    }
  } catch {
    warning = '暂时无法读取已保存的进度，本次学习可以继续。'
  }
  return { progress: result, warning }
}

export function isAnswered(answer, type) {
  if (type === 'true_false') return typeof answer === 'boolean'
  if (type === 'multiple') return Array.isArray(answer) && answer.length > 0
  return answer !== undefined && answer !== null && String(answer).trim().length > 0
}

export function formatAnswer(answer, type) {
  if (answer === undefined || answer === null || answer === '') return '未作答'
  if (type === 'true_false') return answer === true ? '正确' : '错误'
  if (type === 'multiple') return Array.isArray(answer) ? answer.join('、') : String(answer)
  if (typeof answer === 'object' && answer.value !== undefined) return `${answer.value} ${answer.unit}`
  return String(answer)
}
