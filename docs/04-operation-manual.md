# 操作手册

## 一、系统启动

### 启动 Neo4j

确认 Neo4j 服务已启动：

```text
bolt://localhost:7687
http://localhost:7474
```

### 启动后端

```powershell
cd E:\gis-knowledge-platform\backend
.\.venv\Scripts\python.exe main.py
```

后端地址：

```text
http://localhost:8000
```

### 启动前端

```powershell
cd E:\gis-knowledge-platform\frontend
npm run dev
```

浏览器打开终端显示的地址，通常为：

```text
http://localhost:5173
```

## 二、页面说明

页面分为三个区域：

1. 左侧知识目录。
2. 中间知识图谱。
3. 右侧智能问答。

### 左侧知识目录

目录按模块组织知识点，并显示模块和知识点数量。

操作方法：

1. 点击模块名称可以展开或折叠知识点。
2. 点击模块名称会同步加载模块知识图谱。
3. 点击知识点会打开知识点详情。
4. 在搜索框中输入名称可以过滤模块和知识点。

### 中间知识图谱

初始状态显示模块总览。点击模块后显示该模块的知识点及内部关系。

图谱操作：

1. 鼠标滚轮缩放。
2. 拖动节点调整位置。
3. 点击模块进入模块子图。
4. 点击知识点打开详情。
5. 使用左上角按钮放大、缩小和适应画布。
6. 点击“返回总览”返回九个模块。

节点颜色：

| 颜色 | 类型 |
| --- | --- |
| 紫色 | 模块 |
| 蓝色 | 知识点 |
| 青绿色 | 工具，预留 |

### 知识点详情

详情面板显示：

1. 知识点名称。
2. 难度。
3. 重要性。
4. 分类。
5. 所属模块。
6. 知识点说明。
7. 关联知识。
8. 视频和课件。

点击关联知识可以继续跳转。

## 三、智能问答

右上状态显示：

- `已连接`：DeepSeek 已配置。
- `待配置`：尚未填写 API Key。

提问方法：

1. 可先选择模块或知识点。
2. 在右侧输入问题。
3. 点击发送按钮或按 Enter。
4. 等待回答。
5. 点击回答下方的知识点引用可以跳转。

建议问题：

- 什么是交通路网数据模型？
- 轨迹数据有哪些关键技术？
- 推荐一条学习路径。

## 四、维护知识图谱

新增知识点示例：

```cypher
MATCH (module:Module {module_id: 'M1'})
MERGE (knowledge:KnowledgePoint {kp_id: 'M1-999'})
SET knowledge.name = '新的知识点',
    knowledge.description = '知识点说明',
    knowledge.difficulty = '中等',
    knowledge.importance = '重点',
    knowledge.sort_order = 999
MERGE (knowledge)-[:BELONGS_TO]->(module)
```

修改完成后，先在本机 Neo4j 中检查数据，再执行下面的命令同步到腾讯云：

```powershell
cd E:\gis-knowledge-platform
.\scripts\sync_local_neo4j_to_server.ps1
```

脚本会自动完成以下步骤：

1. 从本机 Neo4j 导出最新图谱快照。
2. 临时建立 SSH 隧道。
3. 使用参数化事务把快照直接写入远程 Neo4j。
4. 关闭隧道并检查线上健康接口。

整个过程不需要重新生成部署包，也不需要重新构建前端或后端容器。若本地
快照文件已经由其他导入脚本更新，可使用：

```powershell
.\scripts\sync_local_neo4j_to_server.ps1 -SkipExport
```

脚本从 `deploy/.env` 的 `NEO4J_PASSWORD` 读取远程数据库密码；也可以在当前
PowerShell 会话中设置 `NEO4J_REMOTE_PASSWORD`。同步采用 `MERGE`，会更新和
新增快照中的数据，不会删除远程数据库中额外存在的节点或关系。

同步完成后刷新网页，或点击页面顶部的“刷新数据”按钮即可看到变更。只需改
Neo4j 数据时不需要重启后端。

## 五、导入视频和 PPT

1. 将视频放入 `backend/media/videos`。
2. 将 PDF 或 PPT 放入 `backend/media/slides`。
3. 将封面放入 `backend/media/covers`。
4. 编辑 `data/media-manifest.json`。
5. 执行检查：

```powershell
cd E:\gis-knowledge-platform
backend\.venv\Scripts\python.exe scripts\import_media.py
```

6. 检查通过后写入数据库：

```powershell
backend\.venv\Scripts\python.exe scripts\import_media.py --apply
```

详细格式见 `08-media-import.md`。

## 六、常见问题

### 页面提示“连接异常”

检查后端和 Neo4j 是否启动，并访问：

```text
http://localhost:8000/api/health
```

### 新修改的 Neo4j 数据没有显示

刷新浏览器页面。页面存在内存缓存，完整刷新后会重新获取。

### DeepSeek 显示“待配置”

检查 `backend/.env` 中的 `DEEPSEEK_API_KEY`，并重启后端。

### DeepSeek 返回服务异常

检查：

1. API Key 是否正确。
2. 账户是否有余额。
3. 本机是否可以访问 DeepSeek。
4. 网络是否稳定。

### 提示“提问过于频繁”

系统按 IP 限制提问频率，默认每分钟最多 5 次。稍等一分钟后再提问。

### 视频无法播放

建议使用 MP4 或 WebM。浏览器对编码格式支持不同，优先使用 H.264 编码 MP4。

### PPT 无法在网页中预览

浏览器通常不能直接预览 PPTX。建议同时上传 PDF 预览版。

## 七、环境检查

```powershell
cd E:\gis-knowledge-platform
.\scripts\check_environment.ps1
```

该命令检查 Python、pip 依赖、Node.js 和 npm 版本。
