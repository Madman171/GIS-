# GIS交通路网教学知识图谱平台

版本：V1.0.0

面向大学生创新创业训练计划项目与软件著作权申报的教学知识图谱平台。目标形态是三栏式网页：

- 左侧：知识图谱目录，按模块组织知识点。
- 中间：知识图谱可视化，首页先展示模块，点击模块后展示知识点，点击知识点后展示详情，并为后续视频和 PPT 留出位置。
- 右侧：基于知识图谱上下文的 DeepSeek 智能问答窗口。

## 当前状态

当前仓库已经完成三栏式可交互原型：

1. 左侧显示 9 个模块和 344 个知识点的完整目录。
2. 中间先展示模块总览，点击模块后加载对应知识点子图。
3. 点击知识点后显示属性、关联知识和视频/PPT 预留区域。
4. 右侧完成 DeepSeek 图谱问答、状态检查和关联知识点跳转。
5. 后端使用只读事务和参数化查询，浏览器不再执行任意 Cypher。

在继续开发页面前，必须先以实际 Neo4j 数据为准冻结知识图谱 Schema。当前实际数据库与既有交接文档存在差异，不能直接照搬文档中的节点数量、关系类型或初始化查询。

## 技术栈

| 层级 | 技术 |
| --- | --- |
| 前端 | Vue 3、Vite、Axios、D3.js |
| 后端 | Python、FastAPI、Neo4j Python Driver |
| 数据库 | Neo4j |
| 智能问答 | DeepSeek API，通过本地环境变量启用 |

## 目录结构

```text
gis-knowledge-platform/
├── backend/
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## 基础环境

项目固定使用以下版本，不要继续使用已经停止维护的 Python 3.7：

- Python 3.12.10。
- Node.js 24.21.0。
- Neo4j 5.x。

### 启动后端

```powershell
cd E:\gis-knowledge-platform\backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock.txt
Copy-Item .env.example .env
python main.py
```

后端默认地址为 `http://localhost:8000`。

当前开发机使用了项目内的 Python 3.12.10 运行环境，虚拟环境位于
`backend/.venv`。可执行以下命令检查环境：

```powershell
.\scripts\check_environment.ps1
```

运行后端测试：

```powershell
cd backend
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock.txt
.\.venv\Scripts\python.exe -m pytest
```

### 启动前端

```powershell
cd E:\gis-knowledge-platform\frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

开发环境通过 Vite 将 `/api` 代理到后端，前端代码不直接写死 `localhost:8000`。

运行前端 E2E 测试：

```powershell
npm run test:e2e
```

## 配置原则

- 数据库密码、DeepSeek API Key 只写入本地 `.env`，不得提交到 Git。
- `.env.example` 只保留占位值。
- 前端通过 `VITE_API_BASE_URL` 区分本地开发和部署环境。
- 后端查询应逐步改为只读业务接口和参数化查询，不建议长期保留任意 Cypher 执行接口。

## 后端接口

| 接口 | 用途 |
| --- | --- |
| `GET /api/health` | 检查后端和 Neo4j 连接 |
| `GET /api/graph/modules` | 读取模块总览图谱 |
| `GET /api/directory` | 读取左侧目录和各模块知识点 |
| `GET /api/modules/{module_id}/graph` | 读取指定模块的知识点子图 |
| `GET /api/knowledge-points/{kp_id}` | 读取知识点详情和关联关系 |
| `GET /api/search` | 搜索模块与知识点 |
| `GET /api/chat/status` | 检查 DeepSeek 配置状态 |
| `POST /api/chat` | 基于知识图谱上下文进行智能问答 |

## 开发顺序

1. 冻结真实 Neo4j Schema 和数据统计。
2. 重构后端为模块总览、模块详情、知识点详情、搜索和问答接口。
3. 重构前端三栏布局和目录导航。
4. 实现模块总览到知识点展开的图谱交互。
5. 实现知识点详情面板及视频/PPT 扩展位。
6. 接入受控的 DeepSeek 智能问答。
7. 完成部署、测试、截图、说明书和软著材料。

## GitHub 自动测试、版本与发布

项目使用 GitHub Actions 自动执行前端构建、Playwright E2E、后端测试和
Docker 镜像构建。`main` 合并后，Release 工作流按 Conventional Commits
计算语义化版本并创建 `v1.0.0` 形式的 Git tag 和 GitHub Release。

生产部署由 `production` Environment 控制，需要审批后才会通过 SSH 更新
腾讯云服务器。服务器上的 `deploy/.env` 不进入 Git，Neo4j 数据卷也不会
因为代码发布而被覆盖。

首次接入 GitHub 时需要完成：

1. 创建私有仓库并设置 `origin`。
2. 将当前 `main` 推送到 GitHub，并推送初始 tag `v1.0.0`。
3. 设置 `main` 分支保护：必须 Pull Request、CI 通过、至少一名审核者，禁止强推。
4. 创建 `production` Environment，并配置部署审批者。
5. 配置 `DEPLOY_HOST`、`DEPLOY_PORT`、`DEPLOY_USER`、`DEPLOY_SSH_KEY`、
   `DEPLOY_KNOWN_HOSTS` 和 `DEPLOY_PATH` Secrets。

部署目标默认使用 `/opt/gis-knowledge-platform`。部署失败时会自动恢复到
上一个 commit 并重新执行健康检查。

## 腾讯云部署

腾讯云 Ubuntu 服务器生产部署文件位于：

```text
deploy/
```

部署步骤见 `deploy/README.md`。临时公开访问使用：

```text
http://服务器公网IP:8080
```

## Neo4j同步

推荐通过 SSH 隧道直接编辑腾讯云 Neo4j，使平台和数据库使用同一份数据：

```powershell
.\scripts\open_neo4j_tunnel.ps1
```

隧道建立后：

```text
Neo4j Bolt: bolt://localhost:17687
Neo4j Browser: http://localhost:17474
```

本机 Neo4j 作为主编写库时，可执行一键同步。脚本会临时建立 SSH 隧道，
将本机图谱快照直接通过 Bolt 写入服务器 Neo4j，不再生成部署包、上传压缩包
或重建前后端容器：

```powershell
.\scripts\sync_local_neo4j_to_server.ps1
```

脚本默认先从本机 Neo4j 导出最新快照；如果已经直接修改了
`data/graph-snapshot.json`，可跳过本机导出：

```powershell
.\scripts\sync_local_neo4j_to_server.ps1 -SkipExport
```

远程 Neo4j 密码优先读取环境变量 `NEO4J_REMOTE_PASSWORD`，否则读取本机
`deploy/.env` 中的 `NEO4J_PASSWORD`。默认只更新快照中已有的节点和关系，
不会删除服务器上额外存在的数据。远程数据库名默认是 `neo4j`，可以通过
`-RemoteDatabase` 修改。

如果已经确认本地快照是唯一数据源，并且需要清理快照节点范围内的远程旧关系，
显式加上：

```powershell
.\scripts\sync_local_neo4j_to_server.ps1 -SkipExport -PruneRelationships
```

该开关默认关闭，避免误删远程仍在使用的关系。

网页工具栏提供“刷新数据”按钮，浏览器窗口重新获得焦点时也会自动刷新当前模块和知识点详情。
