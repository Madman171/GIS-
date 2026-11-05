<template>
  <section class="learning-center" aria-label="学习闯关">
    <aside class="learning-rail">
      <div class="learning-rail-heading"><h2>学习闯关</h2><span>{{ passedCount }} / {{ chapters.length || 6 }} 关已通过</span></div>
      <progress :value="passedCount" :max="chapters.length || 6" aria-label="已通过关卡" />
      <label class="chapter-mobile-label" for="learning-chapter">选择关卡</label>
      <select id="learning-chapter" class="chapter-mobile-select" :value="activeId" :disabled="busy" @change="selectChapter($event.target.value)">
        <option v-for="(item, index) in chapters" :key="item.id" :value="item.id" :disabled="!unlocked(item)">第{{ index + 1 }}关 · {{ item.title }}{{ unlocked(item) ? '' : ' · 待解锁' }}</option>
      </select>
      <nav class="learning-chapter-list" aria-label="六关学习路线">
        <button v-for="(item, index) in chapters" :key="item.id" type="button" :disabled="!unlocked(item) || busy" :class="{ current: activeId === item.id }" :aria-current="activeId === item.id ? 'step' : undefined" @click="selectChapter(item.id)">
          <span class="chapter-order" :class="{ passed: stateFor(item.id).bestScore >= passScore }">{{ index + 1 }}</span>
          <span><strong>{{ item.title }}</strong><small>{{ chapterStatus(item) }}</small></span>
        </button>
      </nav>
      <p class="local-progress-note">进度保存在当前浏览器。<br />章节考试达到{{ passScore }}分，解锁下一关。</p>
    </aside>

    <div ref="scrollPane" class="learning-pane" :aria-busy="loading || chapterLoading">
      <div class="learning-page-content">
        <div v-if="loading" class="learning-state"><h1>学习闯关</h1><p>正在准备六关内容…</p></div>
        <div v-else-if="!chapters.length" class="learning-state"><h1>学习内容暂时未能加载</h1><p>{{ error }}</p><button type="button" class="learning-primary" @click="initialize">重新加载</button></div>
        <template v-else>
          <header class="learning-title-row">
            <div><h1>{{ currentMeta?.title }}</h1><p>第{{ chapterNumber }}关 · {{ currentMeta?.practice_count }}道练习 · {{ currentMeta?.exam_count }}道章节考试</p></div>
            <img src="/assets/ai-pet/xiaodi-2d-v1.png" alt="学习伙伴小迪" width="64" height="80" class="learning-xiaodi" />
          </header>
          <div v-if="storageWarning" class="learning-notice" role="status">{{ storageWarning }}</div>
          <div v-if="error" class="learning-error" role="alert"><span>{{ error }}</span><button v-if="!current" type="button" class="learning-text-button" @click="selectChapter(activeId)">重试</button></div>
          <nav class="learning-phase-nav" aria-label="本关学习步骤">
            <button type="button" :class="{ active: phase === 'lesson' }" :disabled="busy" @click="setPhase('lesson')">知识讲解</button>
            <button type="button" :class="{ active: phase === 'practice' }" :disabled="!record.learned || busy" @click="openPractice">练习 {{ practiceDone }} / {{ currentMeta?.practice_count }}</button>
            <button type="button" :class="{ active: phase === 'exam' || phase === 'result' }" :disabled="!practiceComplete || busy" @click="openExamTab">章节考试</button>
          </nav>
          <div v-if="chapterLoading" class="learning-state"><p>正在加载本关讲解和题目…</p></div>
          <template v-else-if="current">
            <template v-if="phase === 'lesson'">
            <div class="lesson-grid">
              <section class="lesson-main learning-surface"><h2>从概念开始</h2><p v-for="(paragraph, index) in lessonParagraphs" :key="index">{{ paragraph }}</p></section>
              <aside class="lesson-context"><section><h2>本关目标</h2><ul class="lesson-objectives"><li v-for="goal in current.objectives" :key="goal">{{ goal }}</li></ul></section><section class="knowledge-return"><h2>对应知识点</h2><button v-for="point in visibleKnowledge" :key="point.id" type="button" class="knowledge-study-link" @click="$emit('open-knowledge', point.id)"><span>{{ point.name }}</span><span aria-hidden="true">↗</span></button><button v-if="current.knowledge_points.length > 4" type="button" class="learning-text-button" @click="allKnowledge = !allKnowledge">{{ allKnowledge ? '收起' : `查看全部${current.knowledge_points.length}个知识点` }}</button></section></aside>
              <p class="learning-origin">本课程习题为原创教学题。道路、时间、速度和阈值等自拟数据均为教学假设。</p>
            </div>
            <TeachingSection :chapter-id="activeId" context="chapter" />
            <div class="lesson-start"><button type="button" class="learning-primary" @click="startPractice">{{ record.learned ? '继续练习' : '学完了，开始练习' }}</button><span>每题提交后，立即查看解析。</span></div>
            </template>

            <section v-else-if="phase === 'practice'" class="practice-area">
              <div class="practice-navigation"><h2>理解后，再向前一步</h2><div role="group" aria-label="选择练习题"><button v-for="(question, index) in practiceQuestions" :key="question.id" type="button" :class="{ active: practiceIndex === index, checked: validPracticeResult(question) }" :aria-label="`第${index + 1}题${validPracticeResult(question) ? '，已核对' : ''}`" :aria-pressed="practiceIndex === index" :disabled="busy" @click="practiceIndex = index">{{ index + 1 }}<span v-if="validPracticeResult(question)" aria-hidden="true"></span></button></div></div>
              <LearningQuestion v-if="practiceQuestion" :key="practiceQuestion.id" :question="practiceQuestion" :index="practiceIndex" :total="practiceQuestions.length" :model-value="record.practiceAnswers[practiceQuestion.id]" :disabled="busy" @update:model-value="updatePracticeAnswer(practiceQuestion, $event)">
                <div class="practice-actions"><button type="button" class="learning-primary" :disabled="busy || !isAnswered(record.practiceAnswers[practiceQuestion.id], practiceQuestion.type)" @click="checkPractice">{{ busy ? '正在核对…' : '核对答案' }}</button><span v-if="!isAnswered(record.practiceAnswers[practiceQuestion.id], practiceQuestion.type)">填写答案后可核对。</span><button v-if="validPracticeResult(practiceQuestion) && practiceIndex < practiceQuestions.length - 1" type="button" class="learning-secondary" @click="nextPractice">下一题 →</button></div>
                <LearningFeedback v-if="validPracticeResult(practiceQuestion)" :result="record.practiceResults[practiceQuestion.id]" :question="practiceQuestion" @open-knowledge="$emit('open-knowledge', $event)" />
              </LearningQuestion>
              <div class="practice-completion" aria-live="polite"><span>已核对 {{ practiceDone }} / {{ practiceQuestions.length }} 题{{ practiceComplete ? '，现在可以检验本关所学。' : '，完成全部练习后可参加章节考试。' }}</span><button v-if="practiceComplete" type="button" class="learning-secondary" @click="beginExam">开始章节考试</button></div>
            </section>

            <form v-else-if="phase === 'exam'" class="exam-area" @submit.prevent="submitExam">
              <div class="exam-intro"><div><h2>章节考试</h2><p>共5题，每题20分。全部作答后交卷，{{ passScore }}分通过。</p></div><span aria-live="polite">已作答 {{ examDone }} / {{ examQuestions.length }}</span></div>
              <LearningQuestion v-for="(question, index) in examQuestions" :key="question.id" :question="question" :index="index" :total="examQuestions.length" :model-value="record.examAnswers[question.id]" :disabled="busy" @update:model-value="updateExamAnswer(question.id, $event)" />
              <div class="exam-submit"><span>{{ examDone < examQuestions.length ? `还需完成${examQuestions.length - examDone}题` : '已完成全部题目，可以交卷。' }}</span><button type="submit" class="learning-primary" :disabled="busy || examDone !== examQuestions.length">{{ busy ? '正在判卷…' : '交卷并查看解析' }}</button></div>
            </form>

            <section v-else-if="phase === 'result' && record.lastExam" class="exam-review">
              <header class="exam-result-summary" :class="{ passed: record.lastExam.passed }"><div><h2>{{ record.lastExam.passed ? '本关通过，继续前行' : '再巩固一下，你可以重试' }}</h2><p>答对{{ record.lastExam.correct_count }} / {{ record.lastExam.question_count }}题 · {{ passScore }}分通过</p></div><p class="exam-score"><strong>{{ record.lastExam.score }}</strong><span> / {{ record.lastExam.total }}分</span></p></header>
              <div class="result-actions"><button v-if="record.lastExam.passed && nextChapter" type="button" class="learning-primary" @click="selectChapter(nextChapter.id)">进入下一关 →</button><span v-else-if="record.lastExam.passed" class="learning-finish">六关已完成。你可以回到图谱，继续探索交通路网。</span><button type="button" class="learning-secondary" @click="beginExam">重新考试</button><button type="button" class="learning-text-button" @click="setPhase('lesson')">回顾本关讲解</button></div>
              <h2 class="review-heading">逐题回顾</h2>
              <article v-for="(question, index) in examQuestions" :key="question.id" class="exam-review-question"><h3 class="question-caption">{{ index + 1 }} / {{ examQuestions.length }} · {{ typeLabels[question.type] }}</h3><p class="review-question-stem">{{ question.stem }}</p><LearningDiagram v-if="question.diagram" :diagram="question.diagram" /><ul v-if="question.options.length" class="review-options"><li v-for="option in question.options" :key="option.id"><strong>{{ option.id }}</strong> {{ option.text }}</li></ul><p>你的答案：{{ formatAnswer(examResult(question.id)?.submitted_answer, question.type) }}{{ question.type === 'numeric' ? ` ${question.numeric.unit}` : '' }}</p><LearningFeedback v-if="examResult(question.id)" :result="examResult(question.id)" :question="question" @open-knowledge="$emit('open-knowledge', $event)" /></article>
            </section>
          </template>
        </template>
      </div>
      <p class="learning-live-status" role="status" aria-live="polite">{{ liveMessage }}</p>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import api from '../api/client'
import { emptyChapter, formatAnswer, isAnswered, loadProgress, PROGRESS_KEY } from '../learning/progress'
import LearningQuestion from './LearningQuestion.vue'
import LearningFeedback from './LearningFeedback.vue'
import LearningDiagram from './LearningDiagram.vue'
import TeachingSection from './TeachingSection.vue'
import '../learning/learning.css'

defineEmits(['open-knowledge'])
const chapters = ref([]), current = ref(null), activeId = ref(''), loading = ref(true), chapterLoading = ref(false)
const progress = ref({ version: '', lastChapter: '', chapters: {} }), storageWarning = ref(''), error = ref(''), liveMessage = ref('')
const phase = ref('lesson'), practiceIndex = ref(0), busy = ref(false), allKnowledge = ref(false), passScore = ref(80), scrollPane = ref(null)
let requestId = 0
let mounted = true
const typeLabels = { single: '单选题', multiple: '多选题', true_false: '判断题', numeric: '数值计算题' }
const currentMeta = computed(() => chapters.value.find(c => c.id === activeId.value))
const chapterNumber = computed(() => chapters.value.findIndex(c => c.id === activeId.value) + 1)
const record = computed(() => activeId.value ? stateFor(activeId.value) : emptyChapter())
const passedCount = computed(() => chapters.value.filter(c => stateFor(c.id).bestScore !== null && stateFor(c.id).bestScore >= passScore.value).length)
const practiceQuestions = computed(() => current.value?.questions.filter(q => q.category === 'practice') || [])
const examQuestions = computed(() => current.value?.questions.filter(q => q.category === 'exam') || [])
const practiceQuestion = computed(() => practiceQuestions.value[practiceIndex.value])
const practiceDone = computed(() => practiceQuestions.value.filter(q => validPracticeResult(q)).length)
const practiceComplete = computed(() => practiceQuestions.value.length > 0 && practiceDone.value === practiceQuestions.value.length)
const examDone = computed(() => examQuestions.value.filter(q => isAnswered(record.value.examAnswers[q.id], q.type)).length)
const nextChapter = computed(() => chapters.value[chapterNumber.value])
const visibleKnowledge = computed(() => allKnowledge.value ? current.value.knowledge_points : current.value.knowledge_points.slice(0, 4))
const lessonParagraphs = computed(() => {
  const sentences = (current.value?.lesson || '').match(/[^。]+。?/g) || []
  const paragraphs = []; let text = ''
  for (const sentence of sentences) { text += sentence; if (text.length > 88) { paragraphs.push(text); text = '' } }
  if (text) paragraphs.push(text)
  return paragraphs
})
function stateFor(id) { if (!progress.value.chapters[id]) progress.value.chapters[id] = emptyChapter(); return progress.value.chapters[id] }
function unlocked(c) { return c.prerequisites.every(id => stateFor(id).bestScore !== null && stateFor(id).bestScore >= passScore.value) }
function chapterStatus(c) {
  if (stateFor(c.id).bestScore !== null && stateFor(c.id).bestScore >= passScore.value) return `已通过 · 最高${stateFor(c.id).bestScore}分`
  if (!unlocked(c)) return '完成前置关卡后解锁'
  return stateFor(c.id).learned ? '继续学习' : '可以开始'
}
function validPracticeResult(q) { const r = record.value.practiceResults[q.id]; return r && r.question_id === q.id && typeof r.correct === 'boolean' && typeof r.explanation === 'string' ? r : null }
function save() {
  try { window.localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress.value)) }
  catch { storageWarning.value = '浏览器未能保存进度，本次学习可以继续；关闭页面后可能需要重新开始。' }
}
function resetScroll() { nextTick(() => scrollPane.value?.scrollTo({ top: 0, behavior: 'instant' })) }
function setPhase(value) { phase.value = value; record.value.phase = value; save(); error.value = ''; resetScroll() }
function errorText(err) { return typeof err?.response?.data?.detail === 'string' ? err.response.data.detail : '暂时无法完成请求，请检查网络后重试。' }
async function initialize() {
  loading.value = true; error.value = ''
  try {
    const { data: response } = await api.get('/api/learning/chapters')
    if (!mounted) return
    chapters.value = response.data.chapters; passScore.value = response.data.pass_score
    const restored = loadProgress(response.data.version, chapters.value)
    progress.value = restored.progress; storageWarning.value = restored.warning
    const hashId = window.location.hash.split('/')[1]
    const target = chapters.value.find(c => c.id === (hashId || progress.value.lastChapter) && unlocked(c)) || chapters.value[0]
    await selectChapter(target.id)
  } catch (err) { error.value = errorText(err) }
  finally { loading.value = false }
}
async function selectChapter(id) {
  const meta = chapters.value.find(c => c.id === id)
  if (!meta || !unlocked(meta) || busy.value) return
  const token = ++requestId
  activeId.value = id; current.value = null; chapterLoading.value = true; error.value = ''; allKnowledge.value = false
  progress.value.lastChapter = id
  history.replaceState(null, '', `#learn/${id}`)
  save()
  try {
    const { data: response } = await api.get(`/api/learning/chapters/${id}`)
    if (token !== requestId) return
    current.value = response.data
    phase.value = record.value.phase
    if (!record.value.learned || (['exam', 'result'].includes(phase.value) && !practiceComplete.value)) phase.value = 'lesson'
    if (phase.value === 'result' && !record.value.lastExam) phase.value = 'lesson'
    const first = practiceQuestions.value.findIndex(q => !validPracticeResult(q))
    practiceIndex.value = Math.max(0, first)
    resetScroll()
  } catch (err) { if (token === requestId) error.value = errorText(err) }
  finally { if (token === requestId) chapterLoading.value = false }
}
function startPractice() { record.value.learned = true; openPractice() }
function openPractice() { if (!record.value.learned) return; setPhase('practice') }
function updatePracticeAnswer(q, answer) { record.value.practiceAnswers[q.id] = answer; delete record.value.practiceResults[q.id]; liveMessage.value = ''; save() }
async function checkPractice() {
  const q = practiceQuestion.value
  if (!q || busy.value || !isAnswered(record.value.practiceAnswers[q.id], q.type)) return
  busy.value = true; error.value = ''; liveMessage.value = ''
  try {
    const { data: response } = await api.post(`/api/learning/chapters/${activeId.value}/practice`, { question_id: q.id, answer: record.value.practiceAnswers[q.id] })
    if (!mounted) return
    record.value.practiceResults[q.id] = response.data
    liveMessage.value = response.data.correct ? '回答正确，解析已显示。' : '这题需要再想想，正确答案和解析已显示。'
    save()
  } catch (err) { error.value = errorText(err); liveMessage.value = error.value }
  finally { busy.value = false }
}
function nextPractice() { practiceIndex.value = Math.min(practiceIndex.value + 1, practiceQuestions.value.length - 1); liveMessage.value = ''; resetScroll() }
function beginExam() { if (!practiceComplete.value) return; record.value.examAnswers = {}; record.value.examInProgress = true; setPhase('exam') }
function openExamTab() { if (!practiceComplete.value) return; setPhase(record.value.examInProgress ? 'exam' : record.value.lastExam ? 'result' : 'exam') }
function updateExamAnswer(id, answer) { record.value.examAnswers[id] = answer; save() }
async function submitExam() {
  if (busy.value || examDone.value !== examQuestions.value.length) return
  busy.value = true; error.value = ''
  try {
    const { data: response } = await api.post(`/api/learning/chapters/${activeId.value}/exam`, { answers: record.value.examAnswers })
    if (!mounted) return
    record.value.lastExam = response.data
    record.value.examInProgress = false
    record.value.bestScore = Math.max(record.value.bestScore ?? 0, response.data.score)
    setPhase('result'); liveMessage.value = `本次考试${response.data.score}分，${response.data.passed ? '本关已通过' : '可查看解析后重新考试'}。`
  } catch (err) { error.value = errorText(err); liveMessage.value = error.value }
  finally { busy.value = false }
}
function examResult(id) { return record.value.lastExam?.results.find(r => r.question_id === id) }
function hashChanged() { const id = window.location.hash.split('/')[1]; if (id && id !== activeId.value) selectChapter(id) }
onMounted(() => { initialize(); window.addEventListener('hashchange', hashChanged) })
onBeforeUnmount(() => { mounted = false; requestId++; window.removeEventListener('hashchange', hashChanged) })
</script>
