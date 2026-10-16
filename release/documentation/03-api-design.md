# 接口设计说明书

## 一、接口规范

所有业务接口使用 `/api` 前缀，默认返回 JSON。

通用成功格式：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

问答接口成功时直接返回答案：

```json
{
  "code": 200,
  "message": "问答成功",
  "answer": "回答内容",
  "references": [],
  "model": "deepseek-chat"
}
```

错误使用标准 HTTP 状态码：

| 状态码 | 含义 |
| --- | --- |
| 200 | 成功 |
| 404 | 资源不存在 |
| 429 | 提问过于频繁 |
| 422 | 请求参数错误 |
| 502 | DeepSeek 上游异常 |
| 503 | 数据库或 AI 服务未就绪 |

## 二、健康检查

### `GET /api/health`

检查 FastAPI 服务和 Neo4j 连接。

响应：

```json
{
  "status": "ok",
  "message": "后端服务正常",
  "database": "connected"
}
```

## 三、模块总览

### `GET /api/graph/modules`

返回模块节点和模块间关系。

响应数据：

```json
{
  "nodes": [],
  "links": [],
  "summary": {
    "moduleCount": 9,
    "knowledgePointCount": null,
    "relationCount": 8
  }
}
```

节点格式：

```json
{
  "id": "M1",
  "elementId": "...",
  "labels": ["Module"],
  "properties": {
    "module_id": "M1",
    "name": "基础理论与拓扑建模"
  }
}
```

关系格式：

```json
{
  "id": "...",
  "type": "PREREQUISITE_MODULE",
  "source": "M1",
  "target": "M2",
  "properties": {}
}
```

## 四、目录接口

### `GET /api/directory`

一次返回九个模块和各模块的知识点目录，数据量较小，不返回完整描述。

响应数据：

```json
{
  "modules": [
    {
      "id": "M1",
      "name": "基础理论与拓扑建模",
      "properties": {},
      "knowledgePoints": [
        {
          "id": "M1-001",
          "name": "GIS交通路网的专业定义与核心研究范畴",
          "properties": {}
        }
      ]
    }
  ]
}
```

## 五、模块子图

### `GET /api/modules/{module_id}/graph`

查询参数：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `module_id` | 路径参数 | 是 | 模块业务主键 |
| `internal_relation_limit` | 查询参数 | 否 | 模块内关系上限，默认 800 |

返回模块、模块下全部知识点、`BELONGS_TO` 关系和知识点内部关系。

不存在的模块返回 HTTP 404。

## 六、知识点详情

### `GET /api/knowledge-points/{knowledge_point_id}`

返回：

- 知识点节点。
- 所属模块。
- 关联知识点、模块或工具。
- 视频和课件资源。

示例：

```json
{
  "node": {
    "id": "M1-001",
    "labels": ["KnowledgePoint"],
    "properties": {
      "name": "GIS交通路网的专业定义与核心研究范畴",
      "description": "...",
      "difficulty": "入门",
      "importance": "核心"
    }
  },
  "module": {
    "id": "M1",
    "labels": ["Module"],
    "properties": {
      "name": "基础理论与拓扑建模"
    }
  },
  "relations": [],
  "materials": {
    "videos": [],
    "slides": []
  }
}
```

## 七、搜索接口

### `GET /api/search`

查询参数：

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | ---: | --- |
| `keyword` | 字符串 | 无 | 搜索关键词，长度 1 至 100 |
| `limit` | 整数 | 20 | 返回数量，范围 1 至 50 |

搜索模块和知识点的名称及描述。

## 八、DeepSeek 状态

### `GET /api/chat/status`

响应：

```json
{
  "configured": true,
  "model": "deepseek-chat",
  "message": "DeepSeek API 已配置"
}
```

该接口不返回 API Key。

## 九、智能问答

### `POST /api/chat`

请求：

```json
{
  "question": "什么是交通路网数据模型？",
  "module_id": "M1",
  "knowledge_point_id": "M1-001"
}
```

参数约束：

| 参数 | 必填 | 最大长度 |
| --- | --- | ---: |
| `question` | 是 | 500 |
| `module_id` | 否 | 50 |
| `knowledge_point_id` | 否 | 50 |

处理流程：

1. 查询当前模块和知识点。
2. 提取问题搜索词。
3. 搜索相关知识点。
4. 构建有限图谱上下文。
5. 调用 DeepSeek。
6. 返回答案和最多 12 个关联知识点。

## 十、媒体静态资源

### `GET /media/{path}`

由 FastAPI 静态文件服务提供。

支持：

- `/media/videos/*`
- `/media/slides/*`
- `/media/covers/*`

真实文件默认不进入源码仓库。
