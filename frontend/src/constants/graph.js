export const NODE_TYPE_LABELS = {
  Module: '模块',
  KnowledgePoint: '知识点',
  Tool: '工具',
}

export const NODE_TYPE_COLORS = {
  Module: '#afd0da',
  KnowledgePoint: '#c1dbe5',
  Tool: '#d9cfb9',
}

export const DIFFICULTY_COLORS = {
  入门: '#c9ddd6',
  基础: '#bed9e5',
  中等: '#afd0da',
  进阶: '#c9c5d7',
  困难: '#dfcbbf',
  高级: '#dfcbbf',
  高阶: '#dfcbbf',
  未标注: '#cbd5d8',
}

export const IMPORTANCE_SCALE = {
  核心: 1.34,
  掌握: 1.18,
  熟悉: 1.04,
  了解: 0.92,
}

export const RELATION_COLORS = {
  BELONGS_TO: '#8eaaaF',
  PREREQUISITE_OF: '#668b9d',
  PREREQUISITE_MODULE: '#537e89',
  RELATED_TO: '#82969d',
  PART_OF: '#82969d',
  APPLIED_IN: '#9b897b',
  IMPLEMENTED_IN: '#9b897b',
  SUPPORTS: '#82969d',
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

export const MODULE_APPEARANCES = [
  { color: '#afd0da', tint: '#e2eef2', ink: '#395e6b' },
  { color: '#c2d7ca', tint: '#e8f0e9', ink: '#476653' },
  { color: '#c0d5df', tint: '#e7eff4', ink: '#436174' },
  { color: '#d8c9c2', tint: '#f1e9e5', ink: '#755b4e' },
  { color: '#c5d8d5', tint: '#e6efed', ink: '#44655f' },
  { color: '#d8d5bd', tint: '#efeee3', ink: '#696443' },
  { color: '#becedc', tint: '#e6edf4', ink: '#4c6277' },
  { color: '#cbd4c1', tint: '#ebefe5', ink: '#58664a' },
  { color: '#d9c5cd', tint: '#f1e7ec', ink: '#785867' },
]

export function getModuleAppearance(id = '') {
  const number = Number(String(id).match(/\d+/)?.[0] || 1)
  return MODULE_APPEARANCES[(Math.max(1, number) - 1) % MODULE_APPEARANCES.length]
}

export const MODULE_SUMMARIES = {
  M1: '认识路网结构，理解节点与拓扑关系',
  M2: '用里程定位道路，组织沿线事件',
  M3: '梳理路网数据，建立统一表达体系',
  M4: '掌握路径搜索与空间分析方法',
  M5: '理解静态路网与实时交通变化',
  M6: '连接多种交通方式，探索协同出行',
  M7: '结合主流 GIS 平台开展路网实操',
  M8: '组织知识与关系，构建课程图谱',
  M9: '从工程问题走向应用与研究前沿',
}

export function getNodeColor(node) {
  const type = getNodeType(node?.labels)
  if (type === 'Module') return getModuleAppearance(node.id).color
  if (type === 'Tool') return NODE_TYPE_COLORS.Tool
  return (
    DIFFICULTY_COLORS[node?.properties?.difficulty] ||
    NODE_TYPE_COLORS.KnowledgePoint
  )
}

export function getImportanceScale(node) {
  return IMPORTANCE_SCALE[node?.properties?.importance] || 1
}
