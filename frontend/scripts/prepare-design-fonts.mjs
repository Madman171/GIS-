// Download a self-hosted Chinese subset covering the existing interface and knowledge content.
// Run only when the course vocabulary changes; normal builds require no external font service.
import { readFile, writeFile, mkdir } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { join } from 'node:path'
const root = fileURLToPath(new URL('../../', import.meta.url))
const { glob } = await import('node:fs/promises')
let text = await readFile(join(root, 'data/graph-snapshot.json'), 'utf8')
for await (const file of glob(join(root, 'frontend/src/**/*.{vue,js,css}').replaceAll('\\', '/'))) text += await readFile(file, 'utf8')
const chars = [...new Set(text.match(/[\u3000-\u30ff\u3400-\u9fff\uff00-\uffef]/g))].sort().join('')
const dir = join(root, 'frontend/public/fonts')
await mkdir(dir, { recursive: true })
let styles = ''
for (let i = 0; i < chars.length; i += 180) {
const response = await fetch('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&display=swap&text=' + encodeURIComponent(chars.slice(i, i + 180)), { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' } })
if (!response.ok) throw new Error('Font CSS request failed: ' + response.status)
const css = await response.text()
const url = css.match(/url\((https:[^)]+)\) format\('woff2'\)/)?.[1]
if (!url) throw new Error('No font URL in response')
if (!url.includes('/l/font?')) throw new Error('The font service did not return a text subset')
const font = await fetch(url)
if (!font.ok) throw new Error('Font download failed: ' + font.status)
const name = i === 0 ? 'noto-sans-sc-course.woff2' : `noto-sans-sc-course-${i / 180}.woff2`
await writeFile(join(dir, name), Buffer.from(await font.arrayBuffer()))
styles += css.replaceAll(url, '/fonts/' + name) + '\n'
}
await writeFile(join(dir, 'course-fonts.css'), styles)
console.log(`Saved Chinese font subset for ${chars.length} course characters`)
