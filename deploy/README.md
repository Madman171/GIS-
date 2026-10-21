# 腾讯云生产部署

目标环境：

```text
腾讯云 Ubuntu Server 26.04 LTS
地区：广州
临时公开地址：http://服务器公网IP:8080
```

Neo4j 和 FastAPI 仅在 Docker 内部网络运行，不向公网开放端口。
为支持本机 SSH 隧道，Neo4j 仅在服务器 `127.0.0.1` 上监听
`7474` 和 `7687`，腾讯云安全组仍不得开放这两个端口。

## 一、腾讯云安全组

入站规则至少开放：

| 端口 | 来源 | 用途 |
| ---: | --- | --- |
| 22 | 你的公网 IP | SSH 管理 |
| 8080 | 0.0.0.0/0 | 临时网站访问 |
| 80 | 0.0.0.0/0 | 备案和域名完成后使用 |
| 443 | 0.0.0.0/0 | HTTPS |

不要开放：

```text
7474
7687
8000
5173
```

## 二、安装 Docker

登录服务器后执行：

```bash
cd /opt/gis-knowledge-platform
chmod +x deploy/*.sh
./deploy/install-docker-ubuntu.sh
```

如果脚本把当前用户加入了 Docker 组，需要退出 SSH 后重新登录。

## 三、配置环境变量

```bash
cd /opt/gis-knowledge-platform/deploy
cp .env.production.example .env
nano .env
```

填写：

```dotenv
PUBLIC_PORT=8080
NEO4J_PASSWORD=高强度数据库密码
DEEPSEEK_API_KEY=你的DeepSeekKey
CORS_ALLOW_ORIGINS=http://服务器公网IP:8080
CHAT_RATE_LIMIT_PER_MINUTE=5
CHAT_RATE_LIMIT_WHITELIST=
KG_MAX_LEARNING_PATH_LENGTH=8
ENABLE_TOPOLOGY_CHECK=true
TOPOLOGY_COORDINATE_TOLERANCE=1.0
ANSWER_MAX_REFERENCES=6
```

`.env` 文件权限建议：

```bash
chmod 600 .env
```

## 四、一键部署

```bash
cd /opt/gis-knowledge-platform
./deploy/deploy.sh
```

脚本会：

1. 构建前后端镜像。
2. 启动 Neo4j。
3. 导入数据库快照。
4. 启动 FastAPI。
5. 启动 Nginx 前端。
6. 执行健康检查。

## 五、公开访问

浏览器打开：

```text
http://服务器公网IP:8080
```

后端健康检查：

```text
http://服务器公网IP:8080/api/health
```

## GitHub 自动发布

代码发布由 GitHub Actions 完成。工作流会在 Pull Request 和 `main` 更新时
执行构建、测试和 Docker 构建；`main` 合并后按 Conventional Commits 创建
语义化版本和 GitHub Release。生产发布需要通过 GitHub `production`
Environment 审批，然后 SSH 调用 `remote-deploy.sh`。

GitHub Actions Secrets：

```text
DEPLOY_HOST
DEPLOY_PORT
DEPLOY_USER
DEPLOY_SSH_KEY
DEPLOY_KNOWN_HOSTS
DEPLOY_PATH=/opt/gis-knowledge-platform
```

服务器只需要提前完成一次 Git checkout、GitHub Deploy Key/只读 Deploy
Key 配置，以及 `deploy/.env` 配置。后续发布不会上传 `.env`，也不会重建
或覆盖 Neo4j 数据卷。

手工验证远程部署逻辑：

```bash
DEPLOY_PATH=/opt/gis-knowledge-platform \
  sh /opt/gis-knowledge-platform/deploy/remote-deploy.sh v1.0.0
```

## 六、常用命令

### 从本机 Neo4j 同步数据

应用层代码部署完成后，日常知识图谱维护不需要重新打包和上传。项目根目录
执行：

```powershell
.\scripts\sync_local_neo4j_to_server.ps1
```

该命令通过 SSH 隧道把本机 Neo4j 的最新快照直接导入服务器 Neo4j，只更新
图谱数据，不重建前端和后端容器。远程密码从 `deploy/.env` 的
`NEO4J_PASSWORD` 读取；也可设置 `NEO4J_REMOTE_PASSWORD` 覆盖它。

如果已经更新了本地 `data/graph-snapshot.json`，可跳过本机数据库导出：

```powershell
.\scripts\sync_local_neo4j_to_server.ps1 -SkipExport
```

同步后访问网页并刷新数据即可。该同步流程使用 `MERGE`，不会自动删除远程
数据库中本地快照没有的节点或关系。

查看状态：

```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml ps
```

查看日志：

```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f
```

重启：

```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml restart
```

停止：

```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml down
```

健康检查：

```bash
./deploy/health-check.sh
```

备份：

```bash
./deploy/backup.sh
```

## 七、ICP 备案与域名

广州地域服务器需要使用已备案域名才能正式通过 80/443 提供网站。

当前 Nginx 运行在容器中，因此不要在宿主机直接执行 `certbot --nginx`。
备案完成并配置 DNS A 记录后，再生成 HTTPS Compose 覆盖配置，向容器
挂载证书并开放 80/443 端口。

正式域名的 `CORS_ALLOW_ORIGINS` 应修改为：

```dotenv
CORS_ALLOW_ORIGINS=https://gis.example.com
```

修改后执行：

```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d backend
```
