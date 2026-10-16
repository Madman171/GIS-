# 部署说明

腾讯云 Ubuntu 一键部署包位于 `deploy/`，详细步骤见
`deploy/README.md`。该部署使用 Docker Compose、Nginx、FastAPI 和 Neo4j。

## 一、目标环境

本项目开发环境固定版本：

| 组件 | 版本 |
| --- | --- |
| Python | 3.12.10 |
| Node.js | 24.21.0 |
| npm | 11.x |
| Neo4j | 5.x |
| 浏览器 | Microsoft Edge 或其他现代浏览器 |

## 二、目录要求

```text
E:\gis-knowledge-platform
├── backend
├── frontend
├── data
├── docs
├── scripts
└── release
```

## 三、Neo4j 初始化

在 Neo4j Browser 中按顺序执行：

1. `data/schema.cypher`
2. `data/modules.cypher`
3. `data/knowledge-points.cypher`
4. `data/tools.cypher`
5. `data/media.cypher`
6. `data/relationships.cypher`

导入完成后检查：

```cypher
MATCH (module:Module) RETURN count(module);
MATCH (knowledge:KnowledgePoint) RETURN count(knowledge);
MATCH ()-[relationship]->() RETURN count(relationship);
```

预期：

```text
Module: 9
KnowledgePoint: 344
Relationship: 1016
```

## 四、后端部署

创建虚拟环境：

```powershell
cd E:\gis-knowledge-platform\backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock.txt
Copy-Item .env.example .env
```

配置 `backend/.env`：

```dotenv
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=<实际密码>
NEO4J_DATABASE=neo4j

DEEPSEEK_API_KEY=<实际Key>
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

开发启动：

```powershell
python main.py
```

生产启动建议关闭 reload：

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app `
  --host 127.0.0.1 `
  --port 8000 `
  --workers 2
```

## 五、前端构建

```powershell
cd E:\gis-knowledge-platform\frontend
npm ci
npm run build
```

构建产物：

```text
frontend/dist
```

## 六、Nginx 推荐配置

```nginx
server {
    listen 80;
    server_name example.com;

    root /var/www/gis-knowledge-platform;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /media/ {
        proxy_pass http://127.0.0.1:8000/media/;
    }
}
```

## 七、生产环境注意事项

1. 不要将 `backend/.env` 提交到源码仓库。
2. 使用独立只读 Neo4j 账号运行查询服务。
3. 限制 CORS 来源，不使用通配符。
4. 为 DeepSeek 接口配置限流和日志。
5. 媒体文件建议迁移到对象存储。
6. 定期备份 Neo4j 数据和媒体目录。
7. 为容器 Nginx 挂载证书并配置 HTTPS，不要在宿主机重复安装一套 Nginx。
8. Uvicorn 建议由 systemd、NSSM 或容器平台托管。

## 八、测试命令

后端：

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest
```

前端：

```powershell
cd frontend
npm run build
npm run test:e2e
```

## 九、发布检查

1. 前端构建成功。
2. 后端健康检查返回正常。
3. Neo4j 节点和关系数量正确。
4. DeepSeek 状态接口正常。
5. 问答可以返回结果。
6. 媒体目录可以访问。
7. `.env`、虚拟环境和依赖目录未进入发布包。
