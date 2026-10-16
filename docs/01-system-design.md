# 系统设计说明书

## 一、软件信息

| 项目 | 内容 |
| --- | --- |
| 软件名称 | GIS交通路网教学知识图谱平台 |
| 软件版本 | V1.0 |
| 软件类型 | 教学知识图谱可视化 Web 平台 |
| 后端技术 | Python 3.12、FastAPI |
| 前端技术 | Vue 3、Vite、D3.js、Axios |
| 数据库 | Neo4j 5.x |
| 智能问答 | DeepSeek API |

## 二、建设目标

本软件面向 GIS 交通路网课程教学，将模块、知识点、前置关系、相关关系、
工具关系等内容组织为知识图谱，并通过网页提供目录浏览、图谱可视化、
知识点详情、媒体资源和智能问答能力。

## 三、总体架构

系统采用前后端分离架构：

```text
浏览器
├── Vue 3 页面
├── D3.js 知识图谱
└── Axios API 客户端
        │
        ▼
FastAPI 后端
├── 目录与图谱接口
├── 知识点详情接口
├── 媒体访问
├── 搜索服务
└── DeepSeek 图谱问答服务
        │
        ▼
Neo4j 知识图谱数据库
```

前端负责页面布局和交互，后端负责数据查询、业务聚合和外部 AI 服务调用，
Neo4j 负责保存教学知识图谱。

## 四、前端设计

### 页面框架

网页采用三栏式布局：

| 区域 | 功能 |
| --- | --- |
| 左侧 | 完整知识目录、模块折叠和知识点选择 |
| 中间 | 模块总览、知识点子图和详情面板 |
| 右侧 | DeepSeek 智能问答和关联知识点引用 |

### 前端组件

| 组件 | 主要职责 |
| --- | --- |
| `App.vue` | 页面状态、接口调用、模块和知识点联动 |
| `DirectoryPanel.vue` | 知识目录、目录搜索和知识点选择 |
| `KnowledgeGraph.vue` | D3 力导向图、缩放、拖拽和节点点击 |
| `KnowledgeDetail.vue` | 知识点属性、关联知识和教学媒体 |
| `ChatPanel.vue` | 问答消息、配置状态和引用节点 |
| `api/client.js` | Axios 实例、基础地址和请求超时 |
| `constants/graph.js` | 节点颜色、类型和关系统一名称 |

### 页面状态

页面使用三个主要状态：

1. 模块总览：只显示模块节点和模块关系。
2. 模块知识点：显示当前模块和所属知识点。
3. 知识点详情：在中间区域显示详情抽屉。

## 五、后端设计

### 应用入口

`backend/main.py` 负责：

1. 创建 FastAPI 应用。
2. 管理 Neo4j Driver 生命周期。
3. 配置 CORS。
4. 提供知识图谱、目录、搜索和问答接口。
5. 挂载本地教学媒体目录。

### 配置模块

`backend/config.py` 从 `backend/.env` 读取：

- Neo4j 地址、用户、密码和数据库名。
- DeepSeek API Key、地址、模型和参数。
- CORS 允许来源。

密钥和密码不写入前端代码，也不提交到源码仓库。

### DeepSeek 服务

`backend/deepseek_service.py` 负责：

1. 检查 API Key 是否配置。
2. 使用 OpenAI 兼容 SDK 调用 DeepSeek。
3. 设置系统提示词和回答约束。
4. 处理超时、连接失败、状态异常和空回答。

模型不能直接生成并执行 Cypher。

### 自主业务引擎

| 文件 | 自主设计职责 |
| --- | --- |
| `topology_checker.py` | 伪节点、断头路、跨层连接和线段衔接校验 |
| `learning_path_engine.py` | 前置依赖链、难度递进路径和知识点推荐 |
| `prompt_engine.py` | 四类教学问答模板、上下文权重排序和答案规则校验 |
| `import_snapshot.py` | 图谱快照解析、完整性校验和参数化导入 |

## 六、数据设计

系统使用属性图模型：

```text
(KnowledgePoint)-[:BELONGS_TO]->(Module)
(KnowledgePoint)-[:PREREQUISITE_OF]->(KnowledgePoint)
(KnowledgePoint)-[:RELATED_TO]->(KnowledgePoint)
(Module)-[:PREREQUISITE_MODULE]->(Module)
(KnowledgePoint)-[:HAS_MEDIA]->(Media)
```

节点业务主键：

| 标签 | 主键 |
| --- | --- |
| Module | `module_id` |
| KnowledgePoint | `kp_id` |
| Tool | `tool_id` |
| Media | `media_id` |

详细字段和关系统计见 `02-database-design.md`。

## 七、核心业务流程

### 模块总览

1. 页面启动时读取目录和模块总览。
2. 后端只读查询 Neo4j。
3. 返回节点、关系和统计信息。
4. D3 渲染模块力导向图。

### 知识点展开

1. 用户点击模块。
2. 前端请求模块子图接口。
3. 后端查询模块、知识点和内部关系。
4. 前端更新左侧目录和中间图谱。

### 知识点详情

1. 用户点击知识点。
2. 后端读取属性和关联节点。
3. 后端查询 `HAS_MEDIA`。
4. 前端显示详情抽屉和教学资源。

### 智能问答

1. 用户输入问题。
2. 后端取得当前模块和知识点。
3. 根据问题关键词搜索相关知识点。
4. 构建有限图谱上下文。
5. DeepSeek 根据上下文生成回答。
6. 返回答案和相关节点引用。
7. 前端显示回答，点击引用可跳转。

## 八、安全设计

1. 数据查询全部使用参数化 Cypher。
2. 普通业务接口采用只读事务。
3. 浏览器不能提交任意 Cypher。
4. API Key 和数据库密码使用环境变量。
5. 媒体导入检查路径穿越和文件扩展名。
6. DeepSeek 输入限制为 500 个字符。
7. 上游 AI 异常不会直接暴露 Key 或内部堆栈。
8. 教学问答白名单可绕过限流，知识浏览接口不执行限流。

## 九、异常设计

| 场景 | 处理方式 |
| --- | --- |
| Neo4j 不可用 | 健康检查返回 HTTP 503 |
| 知识点不存在 | 返回 HTTP 404 |
| DeepSeek 未配置 | 返回 HTTP 503 |
| DeepSeek 超时或服务异常 | 返回 HTTP 502 |
| 图谱为空 | 前端显示空状态 |
| 媒体为空 | 显示资源待添加状态 |

## 十、部署结构

开发阶段：

```text
Vite 5173 -> FastAPI 8000 -> Neo4j 7687
```

生产阶段建议：

```text
Nginx
├── 静态前端文件
└── /api 反向代理
        │
        ▼
Uvicorn/FastAPI
        │
        ▼
Neo4j
```
