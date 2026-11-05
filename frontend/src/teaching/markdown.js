// Small, text-only Markdown subset for our reviewed teaching documents.
// It never evaluates authored HTML or interpolates it with v-html.
export function safeLink(value) {
  try { const url = new URL(value); return url.protocol === 'https:' ? url.href : null } catch { return null }
}
export function inlineParts(text) {
  const parts = []; const pattern = /\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)]+)\)|\*([^*]+)\*/g
  let last = 0
  for (const match of text.matchAll(pattern)) {
    if (match.index > last) parts.push({ type: 'text', text: text.slice(last, match.index) })
    if (match[1]) parts.push({ type: 'strong', text: match[1] })
    else if (match[2]) parts.push({ type: 'link', text: match[2], href: safeLink(match[3]) })
    else parts.push({ type: 'em', text: match[4] })
    last = match.index + match[0].length
  }
  if (last < text.length) parts.push({ type: 'text', text: text.slice(last) })
  return parts
}
const cells = line => line.trim().replace(/^\||\|$/g, '').split('|').map(s => s.trim())
export function parseMarkdown(markdown) {
  const lines = markdown.split(/\r?\n/); const blocks = []
  const isStart = s => /^(?:#{1,6}\s|!\[|\||```|>|[-*]\s|\d+\.\s|---\s*$|\*\*引导解析)/.test(s)
  for (let i = 0; i < lines.length;) {
    const line = lines[i].trim()
    if (!line || /^---+$/.test(line)) { i++; continue }
    const heading = line.match(/^(#{1,6})\s+(.+)$/)
    if (heading) {
      if (heading[1].length === 1) { i++; continue }
      if (heading[1].length === 2 && heading[2].includes('自测答案与解析')) {
        let end = i + 1
        while (end < lines.length && !/^##\s/.test(lines[end])) end++
        blocks.push({ type: 'solution', blocks: parseMarkdown(lines.slice(i + 1, end).join('\n')) }); i = end; continue
      }
      blocks.push({ type: 'heading', level: heading[1].length, text: heading[2] }); i++; continue
    }
    if (line.startsWith('```')) {
      const code = []; i++
      while (i < lines.length && !lines[i].trim().startsWith('```')) code.push(lines[i++])
      blocks.push({ type: 'code', text: code.join('\n') }); i++; continue
    }
    const image = line.match(/^!\[([^\]]*)\]\(([^)]+)\)$/)
    if (image) {
      if (/^\/assets\/teaching\/[A-Za-z0-9/_-]+\.(?:svg|png|webp)$/.test(image[2])) blocks.push({ type: 'figure', alt: image[1], src: image[2] })
      i++; continue
    }
    if (line.startsWith('|') && /^\|[\s:|\-]+\|$/.test(lines[i + 1]?.trim() || '')) {
      const headers = cells(line); const rows = []; i += 2
      while (i < lines.length && lines[i].trim().startsWith('|')) rows.push(cells(lines[i++]))
      blocks.push({ type: 'table', headers, rows }); continue
    }
    if (/^[-*]\s/.test(line) || /^\d+\.\s/.test(line)) {
      const ordered = /^\d+\./.test(line); const items = []
      const rule = ordered ? /^\d+\.\s/ : /^[-*]\s/
      while (i < lines.length && rule.test(lines[i].trim())) items.push(lines[i++].trim().replace(rule, ''))
      blocks.push({ type: 'list', ordered, items }); continue
    }
    if (line.startsWith('>')) {
      const quote = []
      while (i < lines.length && lines[i].trim().startsWith('>')) quote.push(lines[i++].trim().replace(/^>\s?/, ''))
      blocks.push({ type: 'quote', text: quote.join(' ') }); continue
    }
    if (line.startsWith('**引导解析：**')) { blocks.push({ type: 'thoughtAnswer', text: line.replace('**引导解析：**', '').trim() }); i++; continue }
    const paragraph = [line]; i++
    while (i < lines.length && lines[i].trim() && !isStart(lines[i].trim())) paragraph.push(lines[i++].trim())
    blocks.push({ type: 'paragraph', text: paragraph.join(' ') })
  }
  return blocks
}
