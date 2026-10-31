// Local design review only: serve the production build with the repository's real graph snapshot.
// This server neither connects to Neo4j nor calls a language model.
import http from 'node:http'
import { readFile, stat } from 'node:fs/promises'
import { resolve, extname, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = fileURLToPath(new URL('../../', import.meta.url))
const dist = resolve(root, 'frontend/dist')
const snapshot = JSON.parse(await readFile(resolve(root, 'data/graph-snapshot.json'), 'utf8'))
const nodes = snapshot.nodes.map(n => ({ id: n.businessId, labels: n.labels, properties: n.properties }))
const byElement = new Map(snapshot.nodes.map(n => [n.elementId, n.businessId]))
const byId = new Map(nodes.map(n => [n.id, n]))
const links = snapshot.relationships.map((r, i) => ({ id: r.elementId || String(i), type: r.type,
  source: r.sourceBusinessId || byElement.get(r.sourceElementId), target: r.targetBusinessId || byElement.get(r.targetElementId), properties: r.properties || {} }))
const modules = nodes.filter(n => n.labels.includes('Module')).sort((a,b) => a.id.localeCompare(b.id, undefined, { numeric: true }))
const directory = modules.map(m => ({ ...m, name: m.properties.name, knowledgePoints: nodes.filter(n => n.labels.includes('KnowledgePoint') && links.some(l => l.type === 'BELONGS_TO' && l.source === n.id && l.target === m.id)).map(n => ({ ...n, name: n.properties.name })).sort((a,b) => (a.properties.sort_order || 0) - (b.properties.sort_order || 0)) }))
function graph(group) {
  const ids = new Set(group.map(n => n.id))
  return { nodes: group, links: links.filter(l => ids.has(l.source) && ids.has(l.target)), summary: {} }
}
function pathTo(id) {
  const seen = new Set([id]), visiting = new Set([id]), path = []
  let hasCycle = false
  function visit(current, depth) {
    if (depth > 8) return
    for (const link of links.filter(l => l.type === 'PREREQUISITE_OF' && l.target === current)) {
      if (visiting.has(link.source)) { hasCycle = true; continue }
      if (seen.has(link.source)) continue
      seen.add(link.source); visiting.add(link.source)
      visit(link.source, depth + 1)
      visiting.delete(link.source)
      const n = byId.get(link.source)
      if (n) path.push({ id: n.id, name: n.properties.name, difficulty: n.properties.difficulty, depth })
    }
  }
  visit(id, 1)
  return { knowledgePointId: id, path, hasCycle, pathCount: path.length }
}
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2', '.glb': 'model/gltf-binary', '.wasm': 'application/wasm', '.json': 'application/json' }
http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost')
    const p = decodeURIComponent(url.pathname)
    let data
    if (p === '/api/directory') data = { modules: directory }
    else if (p === '/api/graph/modules') data = graph(modules)
    else if (p === '/api/graph/all') data = graph(nodes.filter(n => n.labels.includes('Module') || n.labels.includes('KnowledgePoint')))
    else if (/^\/api\/modules\/[^/]+\/graph$/.test(p)) {
      const m = directory.find(m => m.id === p.split('/')[3])
      data = graph(m ? [byId.get(m.id), ...m.knowledgePoints] : [])
    } else if (/^\/api\/knowledge-points\/[^/]+\/learning-path$/.test(p)) data = pathTo(p.split('/')[3])
    else if (/^\/api\/knowledge-points\/[^/]+$/.test(p)) {
      const id = p.split('/')[3]
      const node = byId.get(id)
      const membership = links.find(l => l.type === 'BELONGS_TO' && l.source === id)
      const relations = links.filter(l => (l.source === id || l.target === id) && !['BELONGS_TO','HAS_MEDIA'].includes(l.type)).map(l => ({ type: l.type, direction: l.source === id ? 'outgoing' : 'incoming', node: byId.get(l.source === id ? l.target : l.source) })).filter(r => r.node)
      const media = links.filter(l => l.type === 'HAS_MEDIA' && l.source === id).map(l => byId.get(l.target)).filter(Boolean).map(n => ({ id: n.id, ...n.properties }))
      data = { node, module: byId.get(membership?.target), relations, materials: { videos: media.filter(m => m.type === 'video'), slides: media.filter(m => m.type === 'slides') } }
    } else if (p === '/api/chat/status') data = { configured: false, model: '', message: '本地设计预览不连接模型服务' }
    else if (p.startsWith('/api/')) { res.writeHead(404); res.end(); return }
    if (data !== undefined) {
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' })
      res.end(JSON.stringify({ code: 200, message: 'local snapshot preview', data })); return
    }
    let file = resolve(dist, '.' + p)
    if (file !== dist && !file.startsWith(dist + sep)) { res.writeHead(403); res.end(); return }
    try { if (!(await stat(file)).isFile()) file = resolve(dist, 'index.html') } catch { file = resolve(dist, 'index.html') }
    res.writeHead(200, { 'Content-Type': mime[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache' })
    let content = await readFile(file)
    if (extname(file) === '.html') {
      const requested = url.searchParams.get('knowledge')
      const n = byId.get(requested)
      const m = directory.find(m => m.knowledgePoints.some(k => k.id === requested))
      if (url.searchParams.get('view') === 'course') {
        const startup = `<script>document.addEventListener('DOMContentLoaded',()=>{let tries=0;const timer=setInterval(()=>{if(++tries>120){clearInterval(timer);return}const row=document.querySelector('.course-overview-row');if(row){const menu=document.querySelector('.mobile-button');if(menu&&getComputedStyle(menu).display!=='none')menu.click();row.click();clearInterval(timer)}},100)});</script>`
        content = Buffer.from(content.toString().replace('</head>', startup + '</head>'))
      }
      const boot = `<script>window.__GIS_DESIGN_PREVIEW__=true;${n && m ? `document.addEventListener('DOMContentLoaded',()=>{let stage=0;let count=0;const tick=setInterval(()=>{if(++count>120){clearInterval(tick);return}if(stage===0){const menu=document.querySelector('.mobile-button');if(menu&&getComputedStyle(menu).display!=='none')menu.click();const row=[...document.querySelectorAll('.module-row')].find(el=>el.textContent.includes(${JSON.stringify(m.name)}));if(row){row.click();stage=1}}else{const row=[...document.querySelectorAll('.knowledge-row')].find(el=>el.textContent.includes(${JSON.stringify(n.properties.name)}));if(row){row.click();clearInterval(tick)}}},100)});` : ''}</script>`
      content = Buffer.from(content.toString().replace('<head>', '<head>' + boot))
    }
    res.end(content)
  } catch (error) { console.error(error.message); res.writeHead(500); res.end('Local preview error') }
}).listen(5181, '127.0.0.1', () => console.log('Local design preview: http://127.0.0.1:5181 (repository snapshot; no live AI)'))
