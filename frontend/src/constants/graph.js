export const NODE_TYPE_LABELS = {
  Module: '模块',
  KnowledgePoint: '知识点',
  Tool: '工具',
}

export const NODE_TYPE_COLORS = {
  Module: '#7c3aed',
  KnowledgePoint: '#2563eb',
  Tool: '#0f766e',
}

export const DIFFICULTY_COLORS = {
  入门: '#0ea5e9',
  基础: '#2563eb',
  中等: '#6366f1',
  进阶: '#8b5cf6',
  困难: '#e11d48',
  高级: '#dc2626',
  高阶: '#dc2626',
  未标注: '#64748b',
}

export const IMPORTANCE_SCALE = {
  核心: 1.34,
  掌握: 1.18,
  熟悉: 1.04,
  了解: 0.92,
}

export const RELATION_COLORS = {
  BELONGS_TO: '#94a3b8',
  PREREQUISITE_OF: '#2563eb',
  PREREQUISITE_MODULE: '#0ea5e9',
  RELATED_TO: '#0f766e',
  PART_OF: '#16a34a',
  APPLIED_IN: '#d97706',
  IMPLEMENTED_IN: '#7c3aed',
  SUPPORTS: '#db2777',
}

export const RELATION_DASHES = {
  BELONGS_TO: '3 5',
  RELATED_TO: '7 5',
  PART_OF: '2 4',
  SUPPORTS: '10 4',
}

export const RELATION_LABELS = {
  BELONGS_TO: '属于',
  PREREQUISITE_OF: '前置知识',
  PREREQUISITE_MODULE: '模块前置',
  RELATED_TO: '相关知识',
  PART_OF: '组成部分',
  APPLIED_IN: '应用于',
  IMPLEMENTED_IN: '实现于',
  SUPPORTS: '支撑',
}

export function getNodeType(labels = []) {
  if (labels.includes('Module')) return 'Module'
  if (labels.includes('KnowledgePoint')) return 'KnowledgePoint'
  if (labels.includes('Tool')) return 'Tool'
  return labels[0] || 'Unknown'
}

export function getNodeName(node) {
  return node?.properties?.name || '未命名'
}

export function getNodeColor(node) {
  const type = getNodeType(node?.labels)
  if (type === 'Module') return NODE_TYPE_COLORS.Module
  if (type === 'Tool') return NODE_TYPE_COLORS.Tool
  return (
    DIFFICULTY_COLORS[node?.properties?.difficulty] ||
    NODE_TYPE_COLORS.KnowledgePoint
  )
}

export function getImportanceScale(node) {
  return IMPORTANCE_SCALE[node?.properties?.importance] || 1
}
