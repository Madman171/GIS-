import { expect, test } from '@playwright/test'


const modules = [
  {
    id: 'M1',
    name: '基础理论与拓扑建模',
    properties: { module_id: 'M1', name: '基础理论与拓扑建模' },
    knowledgePoints: [
      {
        id: 'M1-001',
        name: 'GIS交通路网的专业定义',
        properties: { kp_id: 'M1-001', name: 'GIS交通路网的专业定义' },
      },
    ],
  },
  {
    id: 'M2',
    name: '线性参考与事件数据模型',
    properties: { module_id: 'M2', name: '线性参考与事件数据模型' },
    knowledgePoints: [],
  },
]

const overviewGraph = {
  nodes: modules.map((module) => ({
    id: module.id,
    labels: ['Module'],
    properties: module.properties,
  })),
  links: [
    {
      id: 'module-link',
      type: 'PREREQUISITE_MODULE',
      source: 'M1',
      target: 'M2',
      properties: {},
    },
  ],
  summary: {
    moduleCount: 2,
    relationCount: 1,
  },
}

const moduleGraph = {
  nodes: [
    ...overviewGraph.nodes,
    {
      id: 'M1-001',
      labels: ['KnowledgePoint'],
      properties: {
        kp_id: 'M1-001',
        name: 'GIS交通路网的专业定义',
      },
    },
  ],
  links: [
    {
      id: 'belongs-link',
      type: 'BELONGS_TO',
      source: 'M1-001',
      target: 'M1',
      properties: {},
    },
  ],
  summary: {
    nodeCount: 3,
    knowledgePointCount: 1,
    relationCount: 1,
  },
}

const detail = {
  node: {
    id: 'M1-001',
    labels: ['KnowledgePoint'],
    properties: {
      kp_id: 'M1-001',
      name: 'GIS交通路网的专业定义',
      description: '测试知识点说明。',
      difficulty: '入门',
      importance: '核心',
    },
  },
  module: overviewGraph.nodes[0],
  relations: [],
  materials: {
    videos: [],
    slides: [],
  },
}


test.beforeEach(async ({ page }) => {
  await page.route('**/api/directory', async (route) => {
    await route.fulfill({
      json: { code: 200, message: 'ok', data: { modules } },
    })
  })
  await page.route('**/api/graph/modules', async (route) => {
    await route.fulfill({
      json: { code: 200, message: 'ok', data: overviewGraph },
    })
  })
  await page.route('**/api/chat/status', async (route) => {
    await route.fulfill({
      json: {
        code: 200,
        message: 'ok',
        data: {
          configured: true,
          model: 'deepseek-chat',
          message: 'DeepSeek API 已配置',
        },
      },
    })
  })
})


test('directory, graph, detail and chat flow', async ({ page }) => {
  await page.route('**/api/modules/M1/graph', async (route) => {
    await route.fulfill({
      json: { code: 200, message: 'ok', data: moduleGraph },
    })
  })
  await page.route('**/api/knowledge-points/M1-001', async (route) => {
    await route.fulfill({
      json: { code: 200, message: 'ok', data: detail },
    })
  })
  await page.route(
    '**/api/knowledge-points/M1-001/learning-path',
    async (route) => {
      await route.fulfill({
        json: {
          code: 200,
          message: 'ok',
          data: {
            knowledgePointId: 'M1-001',
            path: [],
            pathCount: 0,
            hasCycle: false,
          },
        },
      })
    },
  )
  await page.route('**/api/chat', async (route) => {
    await route.fulfill({
      json: {
        code: 200,
        message: 'ok',
        answer: '这是基于知识图谱生成的测试回答。',
        model: 'deepseek-chat',
        references: [
          {
            id: 'M1-001',
            name: 'GIS交通路网的专业定义',
            type: 'KnowledgePoint',
            moduleId: 'M1',
          },
        ],
      },
    })
  })

  const modelResponse = page.waitForResponse((response) =>
    response.url().endsWith('/assets/ai-pet/spirit_pix.glb'),
  )
  await page.goto('/')
  await expect((await modelResponse).status()).toBe(200)

  await expect(page.locator('.ai-pet-button')).toBeVisible()
  await expect(page.locator('.pet-model-canvas')).toBeVisible()
  await expect(page.locator('.ai-pet-button')).toHaveCSS('background-color', 'rgba(0, 0, 0, 0)')
  await page.locator('.ai-pet-button').click()
  await expect(page.locator('.status-dot')).toHaveText('已连接')
  await page.locator('.pet-chat-toolbar button').click()
  await expect(page.locator('.module-row')).toHaveCount(2)
  await expect(page.locator('.view-switch button')).toHaveCount(3)

  await page.locator('.module-row').first().click()
  await expect(page.locator('.stage-title strong')).toContainText(
    '基础理论与拓扑建模',
  )
  await expect(page.locator('.knowledge-row')).toHaveCount(1)
  await expect(page.locator('.graph-canvas-badge')).toContainText(
    '路网式知识轨道',
  )

  await page.locator('.view-switch button').nth(1).click()
  await expect(page.locator('.view-switch button.active')).toContainText(
    '重点',
  )

  await page.locator('.knowledge-row').first().click()
  await expect(page.locator('.detail-panel h2')).toHaveText(
    'GIS交通路网的专业定义',
  )
  await expect(page.locator('.learning-path-section')).toContainText(
    '暂无已配置的前置知识',
  )

  await page.locator('.refresh-button').click()
  await expect(page.locator('.detail-panel h2')).toHaveText(
    'GIS交通路网的专业定义',
  )

  await page.locator('.ai-pet-button').click()
  await expect(page.locator('.pet-chat-popover')).toBeVisible()
  await page.locator('.pet-chat-popover .chat-composer textarea').fill(
    '什么是GIS交通路网的专业定义？',
  )
  await page.locator('.pet-chat-popover .send-button').click()

  await expect(page.locator('.message-row.assistant')).toHaveCount(2)
  await expect(page.locator('.message-bubble').last()).toContainText(
    '这是基于知识图谱生成的测试回答。',
  )
  await expect(page.locator('.message-references button')).toHaveCount(1)
})
