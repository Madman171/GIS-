<template>
  <div class="ai-pet-layer" :style="{ left: `${position.x}px`, top: `${position.y}px` }">
    <div v-if="suggestion && !muted && !chatOpen" class="pet-suggestion">
      <button type="button" class="suggestion-close" title="关闭建议" aria-label="关闭建议" @click="dismissSuggestion">×</button>
      <p>{{ suggestion.text }}</p>
      <button v-if="suggestion.actionLabel" type="button" class="suggestion-action" @click="$emit('suggestion-action', suggestion.action)">{{ suggestion.actionLabel }}</button>
    </div>

    <div v-if="chatOpen" class="pet-chat-popover">
      <div class="pet-chat-toolbar">
        <span><Sparkles :size="14" /> 图谱小助手</span>
        <button type="button" title="收起问答" aria-label="收起问答" @click="chatOpen = false"><X :size="15" /></button>
      </div>
      <ChatPanel class="compact-chat-panel" compact :messages="messages" :loading="loading" :configured="configured" @send="$emit('send', $event)" @select-reference="$emit('select-reference', $event)" />
    </div>

    <button ref="petButton" type="button" class="ai-pet-button" :class="{ active: chatOpen, dragging }" title="打开图谱小助手，可拖动" aria-label="打开图谱小助手，可拖动" @pointerdown="startDrag" @click="toggleChat">
      <span class="pet-halo" aria-hidden="true"></span>
      <canvas ref="petCanvas" class="pet-model-canvas" aria-hidden="true"></canvas>
      <span v-if="!modelReady" class="pet-fallback-icon" aria-hidden="true"><Bot :size="38" /></span>
      <span class="pet-sparkle" aria-hidden="true"><Sparkles :size="14" /></span>
    </button>

    <button type="button" class="pet-mute-button" :title="muted ? '开启建议' : '暂时关闭建议'" :aria-label="muted ? '开启建议' : '暂时关闭建议'" @click="toggleMute">{{ muted ? '·' : '✦' }}</button>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Bot, Sparkles, X } from '@lucide/vue'
import ChatPanel from './ChatPanel.vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  configured: { type: Boolean, default: false },
  suggestion: { type: Object, default: null },
})
const emit = defineEmits(['send', 'select-reference', 'dismiss-suggestion', 'toggle-mute', 'suggestion-action'])

const position = ref({ x: 0, y: 0 })
const chatOpen = ref(false)
const muted = ref(false)
const dragging = ref(false)
const dragMoved = ref(false)
const dragOffset = ref({ x: 0, y: 0 })
const petButton = ref(null)
const petCanvas = ref(null)
const modelReady = ref(false)
const STORAGE_KEY = 'gis-knowledge-ai-pet-position'

let renderer = null
let scene = null
let camera = null
let petModel = null
let modelClock = null
let animationFrame = 0
let dracoLoader = null
let mixer = null
let THREE = null
let actions = new Map()
let currentAction = null
let visualState = 'Idle'
let wingLeft = []
let wingRight = []
let headNode = null
let wavingArm = null

function disposeMaterial(material) {
  if (!material) return
  for (const value of Object.values(material)) {
    if (value && typeof value === 'object' && 'isTexture' in value) value.dispose()
  }
  material.dispose?.()
}

function disposePetModel() {
  if (animationFrame) cancelAnimationFrame(animationFrame)
  animationFrame = 0
  scene?.traverse((object) => {
    if (!object.isMesh) return
    object.geometry?.dispose()
    if (Array.isArray(object.material)) object.material.forEach(disposeMaterial)
    else disposeMaterial(object.material)
  })
  mixer = null
  actions.clear()
  currentAction = null
  visualState = 'Idle'
  wingLeft = []
  wingRight = []
  headNode = null
  wavingArm = null
  dracoLoader?.dispose()
  renderer?.dispose()
  renderer = null
  scene = null
  camera = null
  petModel = null
  modelClock = null
}

function playAction(name, reset = false) {
  visualState = name
  const next = actions.get(name) || actions.get('Idle')
  if (!next || !mixer) return
  if (currentAction === next && !reset) return
  next.reset().fadeIn(0.28).play()
  if (currentAction && currentAction !== next) currentAction.fadeOut(0.28)
  currentAction = next
}

function renderPet() {
  if (!renderer || !scene || !camera) return
  const delta = modelClock.getDelta()
  const elapsed = modelClock.elapsedTime
  mixer?.update(delta)
  if (petModel) {
    petModel.rotation.y = Math.sin(elapsed * 0.55) * 0.045
    petModel.position.y = Math.sin(elapsed * (visualState === 'Happy' ? 4.2 : 1.8)) * (visualState === 'Happy' ? 0.045 : 0.025)
    const flap = Math.sin(elapsed * 4.2) * (visualState === 'Hover' ? 0.16 : 0.08)
    wingLeft.forEach((node) => { node.rotation.z = flap })
    wingRight.forEach((node) => { node.rotation.z = -flap })
    if (headNode) {
      const tilt = visualState === 'Think' ? 0.10 + Math.sin(elapsed * 1.8) * 0.035 : Math.sin(elapsed * 0.8) * 0.018
      headNode.rotation.z = tilt
    }
    if (wavingArm) {
      wavingArm.rotation.z = visualState === 'Wave' ? -0.26 + Math.sin(elapsed * 7) * 0.22 : 0
    }
  }
  renderer.render(scene, camera)
  animationFrame = requestAnimationFrame(renderPet)
}

async function initPetModel() {
  const canvas = petCanvas.value
  if (!canvas) return
  try {
    const [threeModule, dracoModule, gltfModule] = await Promise.all([
      import('three'),
      import('three/examples/jsm/loaders/DRACOLoader.js'),
      import('three/examples/jsm/loaders/GLTFLoader.js'),
    ])
    THREE = threeModule
    const { DRACOLoader } = dracoModule
    const { GLTFLoader } = gltfModule
    const width = 140
    const height = 160
    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: 'low-power' })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75))
    renderer.setSize(width, height, false)
    renderer.outputColorSpace = THREE.SRGBColorSpace
    renderer.toneMapping = THREE.ACESFilmicToneMapping
    renderer.toneMappingExposure = 1.08

    scene = new THREE.Scene()
    camera = new THREE.OrthographicCamera(-1.28, 1.28, 1.48, -1.48, 0.01, 100)
    camera.position.set(0, 0, 6)
    camera.up.set(0, 1, 0)
    camera.lookAt(0, 0, 0)
    scene.add(new THREE.HemisphereLight(0xe0f2fe, 0x312e81, 2.4))
    const keyLight = new THREE.DirectionalLight(0xffffff, 2.6)
    keyLight.position.set(2, 3, 4)
    scene.add(keyLight)
    const rimLight = new THREE.DirectionalLight(0x67e8f9, 1.15)
    rimLight.position.set(-2, 1, -3)
    scene.add(rimLight)

    dracoLoader = new DRACOLoader()
    dracoLoader.setDecoderPath('/draco/')
    const loader = new GLTFLoader()
    loader.setDRACOLoader(dracoLoader)
    const gltf = await loader.loadAsync('/assets/ai-pet/spirit_pix.glb')
    petModel = gltf.scene
    petModel.traverse((node) => {
      if (node.name.startsWith('wing.L')) wingLeft.push(node)
      if (node.name.startsWith('wing.R')) wingRight.push(node)
      if (node.name === 'head' && node.isMesh) headNode = node
      if (node.name === 'sleeve.R' && node.isMesh) wavingArm = node
    })
    const bounds = new THREE.Box3().setFromObject(petModel)
    const size = bounds.getSize(new THREE.Vector3())
    const center = bounds.getCenter(new THREE.Vector3())
    const scale = 2.42 / Math.max(size.y, 0.01)
    petModel.scale.setScalar(scale)
    petModel.position.set(-center.x * scale, -center.y * scale, -center.z * scale)
    scene.add(petModel)

    mixer = new THREE.AnimationMixer(petModel)
    for (const clip of gltf.animations || []) actions.set(clip.name, mixer.clipAction(clip))
    modelClock = new THREE.Clock()
    modelReady.value = true
    // Keep the imported rest pose for the initial frame; actions are started
    // only after the model is visible, avoiding a flash while NLA clips settle.
    playAction('Idle', true)
    renderPet()
  } catch (error) {
    console.warn('AI pet 3D model failed to load; using fallback icon.', error)
    disposePetModel()
  }
}

function clampPosition(x, y) {
  const width = 140
  const height = 160
  return { x: Math.max(8, Math.min(x, window.innerWidth - width - 8)), y: Math.max(70, Math.min(y, window.innerHeight - height - 10)) }
}

function savePosition() { localStorage.setItem(STORAGE_KEY, JSON.stringify(position.value)) }

function startDrag(event) {
  if (event.button !== 0) return
  const rect = petButton.value?.getBoundingClientRect()
  if (!rect) return
  event.preventDefault()
  dragging.value = true
  dragMoved.value = false
  dragOffset.value = { x: event.clientX - rect.left, y: event.clientY - rect.top }
  playAction('Hover', true)
  petButton.value.setPointerCapture?.(event.pointerId)
  window.addEventListener('pointermove', moveDrag)
  window.addEventListener('pointerup', stopDrag, { once: true })
}

function moveDrag(event) {
  if (!dragging.value) return
  const next = clampPosition(event.clientX - dragOffset.value.x, event.clientY - dragOffset.value.y)
  if (Math.abs(next.x - position.value.x) > 2 || Math.abs(next.y - position.value.y) > 2) dragMoved.value = true
  position.value = next
}

function stopDrag() {
  if (!dragging.value) return
  dragging.value = false
  window.removeEventListener('pointermove', moveDrag)
  savePosition()
  playAction(props.loading ? 'Think' : (chatOpen.value ? 'Talk' : 'Idle'), true)
  window.setTimeout(() => { dragMoved.value = false }, 0)
}

function toggleChat(event) {
  if (dragMoved.value) { event.preventDefault(); return }
  chatOpen.value = !chatOpen.value
  playAction(chatOpen.value ? 'Happy' : 'Idle', true)
}

function dismissSuggestion() { emit('dismiss-suggestion') }

function toggleMute() {
  muted.value = !muted.value
  localStorage.setItem('gis-knowledge-ai-pet-muted', String(muted.value))
  emit('toggle-mute', muted.value)
}

function handleResize() { position.value = clampPosition(position.value.x, position.value.y) }

watch(() => props.loading, (loading) => { if (!dragging.value) playAction(loading ? 'Think' : (chatOpen.value ? 'Talk' : 'Idle'), true) })
watch(chatOpen, (open) => { if (!dragging.value) playAction(open ? 'Talk' : 'Idle', true) })
watch(() => props.suggestion, (next, previous) => { if (next && next !== previous && !muted.value) playAction('Wave', true) })

onMounted(() => {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null')
    const savedMuted = localStorage.getItem('gis-knowledge-ai-pet-muted')
    position.value = saved && Number.isFinite(saved.x) && Number.isFinite(saved.y) ? clampPosition(saved.x, saved.y) : clampPosition(window.innerWidth - 168, window.innerHeight - 190)
    muted.value = savedMuted === 'true'
  } catch {
    position.value = clampPosition(window.innerWidth - 168, window.innerHeight - 190)
  }
  window.addEventListener('resize', handleResize)
  initPetModel()
})

onBeforeUnmount(() => {
  window.removeEventListener('pointermove', moveDrag)
  window.removeEventListener('pointerup', stopDrag)
  window.removeEventListener('resize', handleResize)
  disposePetModel()
})
</script>

<style scoped>
.ai-pet-layer { position: fixed; z-index: 60; width: 140px; height: 160px; user-select: none; pointer-events: none; }
.ai-pet-button { width: 140px; height: 160px; padding: 0; border: 0; position: relative; display: grid; place-items: center; color: #fff; background: transparent; cursor: grab; pointer-events: auto; appearance: none; touch-action: none; transition: transform 0.2s ease, filter 0.2s ease; }
.ai-pet-button:hover, .ai-pet-button.active { transform: translateY(-3px) scale(1.035); filter: drop-shadow(0 12px 18px rgba(65, 135, 220, 0.22)); }
.ai-pet-button.dragging { cursor: grabbing; transform: scale(1.04); }
.pet-halo { position: absolute; left: 12px; right: 12px; top: 22px; bottom: 12px; border-radius: 48% 48% 44% 44%; background: radial-gradient(ellipse at 50% 46%, rgba(191, 232, 255, 0.24), rgba(147, 197, 253, 0.13) 52%, rgba(96, 165, 250, 0)); filter: blur(5px); pointer-events: none; }
.pet-model-canvas { width: 140px; height: 160px; display: block; pointer-events: none; }
.pet-fallback-icon { position: absolute; inset: 0; display: grid; place-items: center; color: #368cd4; }
.pet-sparkle { position: absolute; top: 15px; right: 17px; width: 25px; height: 25px; border-radius: 50%; display: grid; place-items: center; color: #1775cb; background: rgba(255, 250, 206, 0.96); box-shadow: 0 5px 14px rgba(50, 120, 210, 0.2); }
.pet-mute-button { position: absolute; right: 1px; bottom: 3px; width: 25px; height: 25px; padding: 0; border: 1px solid #dbeafe; border-radius: 50%; color: #64748b; background: rgba(255, 255, 255, 0.94); cursor: pointer; pointer-events: auto; font-size: 12px; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12); }
.pet-chat-popover { position: absolute; right: 0; bottom: 150px; width: 340px; height: min(540px, calc(100vh - 100px)); overflow: hidden; border: 1px solid #dbe4ef; border-radius: 14px; background: #fff; box-shadow: 0 20px 60px rgba(15, 23, 42, 0.2); pointer-events: auto; }
.pet-chat-toolbar { height: 38px; padding: 0 10px 0 13px; display: flex; align-items: center; justify-content: space-between; color: #334155; background: #f8fafc; border-bottom: 1px solid #e7edf5; font-size: 12px; font-weight: 700; }
.pet-chat-toolbar span { display: flex; align-items: center; gap: 5px; color: #2563eb; }
.pet-chat-toolbar button { width: 25px; height: 25px; padding: 0; border: 0; border-radius: 5px; display: grid; place-items: center; color: #64748b; background: transparent; cursor: pointer; }
.pet-chat-toolbar button:hover { background: #e2e8f0; }
:deep(.compact-chat-panel) { height: calc(100% - 38px); border: 0; }
:deep(.compact-chat-panel .chat-header) { display: none; }
:deep(.compact-chat-panel .message-list) { padding: 12px; }
:deep(.compact-chat-panel .quick-prompts) { padding-top: 7px; }
.pet-suggestion { position: absolute; right: 4px; bottom: 150px; width: 250px; padding: 11px 12px; border: 1px solid #bfdbfe; border-radius: 12px; color: #1e40af; background: #eff6ff; box-shadow: 0 12px 30px rgba(30, 64, 175, 0.16); transform: translateX(-4px); pointer-events: auto; }
.pet-suggestion p { margin: 0 18px 8px 0; font-size: 12px; line-height: 1.55; }
.suggestion-close { position: absolute; top: 5px; right: 7px; border: 0; color: #3b82f6; background: transparent; cursor: pointer; font-size: 16px; }
.suggestion-action { padding: 5px 8px; border: 1px solid #93c5fd; border-radius: 6px; color: #1d4ed8; background: #fff; cursor: pointer; font-size: 11px; }
@media (max-width: 520px) { .ai-pet-layer { transform: scale(0.82); transform-origin: bottom right; } .pet-chat-popover { position: fixed; right: 10px; bottom: 76px; width: min(92vw, 360px); height: min(560px, calc(100vh - 92px)); } .pet-suggestion { position: fixed; right: 12px; bottom: 76px; width: min(78vw, 280px); } }
</style>
