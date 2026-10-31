// Self-host a licensed Noto Serif SC subset. Builds do not call font services.
import { readFile, writeFile, glob } from 'node:fs/promises'
const root = new URL('../../', import.meta.url)
let vocabulary = await readFile(new URL('data/graph-snapshot.json', root), 'utf8')
for await (const file of glob(new URL('frontend/src/', root).pathname.replace(/^\/(?=[A-Z]:)/, '') + '**/*.{vue,js,css}')) vocabulary += await readFile(file, 'utf8')
const chars = [...new Set(vocabulary.match(/[\u3000-\u30ff\u3400-\u9fff\uff00-\uffef]/g))].sort().join('')
let styles = ''
for (let i = 0; i < chars.length; i += 180) {
  const response = await fetch('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@600&display=swap&text=' + encodeURIComponent(chars.slice(i, i + 180)), { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' } })
  if (!response.ok) throw new Error(`Font CSS: ${response.status}`)
  const css = await response.text()
  const url = css.match(/url\((https:[^)]+)\) format\('woff2'\)/)?.[1]
  if (!url || !url.includes('/l/font?')) throw new Error('Expected WOFF2 text subset')
  const font = await fetch(url)
  if (!font.ok) throw new Error(`Font file: ${font.status}`)
  const name = `noto-serif-sc-heading-${i / 180}.woff2`
  await writeFile(new URL('frontend/public/fonts/' + name, root), Buffer.from(await font.arrayBuffer()))
  styles += css.replaceAll(url, '/fonts/' + name) + '\n'
}
const license = await fetch('https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifsc/OFL.txt')
if (!license.ok) throw new Error('Font license unavailable')
await writeFile(new URL('frontend/public/fonts/Noto-Serif-SC-LICENSE.txt', root), await license.text())
await writeFile(new URL('frontend/public/fonts/heading-fonts.css', root), styles)
console.log(`Saved Noto Serif SC headings: ${chars.length} characters`)
