# 第三方组件与许可证说明

## 一、说明

本清单用于软件开发过程和软件著作权材料整理。软件作者应保留各依赖自带的
许可证文件，并遵守对应条款。本清单不构成法律意见。

## 二、前端组件

| 组件 | 版本 | 许可证 | 用途 |
| --- | --- | --- | --- |
| Vue | 3.5.43 | MIT | 页面框架 |
| Vite | 8.3.0 | MIT | 前端构建 |
| Axios | 1.20.0 | MIT | HTTP 请求 |
| D3.js | 7.9.0 | ISC | 知识图谱可视化 |
| Lucide Vue | 1.47.0 | ISC | 图标 |
| Playwright Test | 1.63.0 | Apache-2.0 | 自动化测试 |

## 三、后端组件

| 组件 | 版本 | 许可证 | 用途 |
| --- | --- | --- | --- |
| FastAPI | 0.141.1 | MIT | Web API 框架 |
| Uvicorn | 0.53.0 | BSD-3-Clause | ASGI 服务 |
| Pydantic | 2.13.5 | MIT | 请求数据模型 |
| Neo4j Python Driver | 5.28.6 | Apache-2.0 | Neo4j 连接 |
| python-dotenv | 1.2.3 | BSD-3-Clause | 环境变量加载 |
| OpenAI Python SDK | 1.109.1 | Apache-2.0 | DeepSeek OpenAI 兼容调用 |
| Pytest | 9.1.1 | MIT | 后端测试 |

## 四、数据库及外部服务

### Neo4j Community

- 产品：Neo4j Community
- 当前数据库版本：5.26.30
- 许可证：GPLv3
- 说明：Neo4j Community 不是 MIT/Apache 许可。软件分发或部署方式必须符合
  GPLv3 要求；如需闭源商业分发，应单独评估 Neo4j 商业许可。

### DeepSeek API

- 服务：DeepSeek API
- 用途：自然语言问答
- 说明：DeepSeek API 是外部网络服务，不属于本项目自带开源组件。
  使用时应遵守 DeepSeek 开放平台协议、计费规则、数据处理规则及内容政策。

## 五、项目自有内容

以下内容由项目作者负责确认权利：

1. GIS 交通路网知识点文本。
2. 教学视频、PPT、PDF 和封面。
3. 软件名称、界面设计、图标和说明文档。
4. 项目截图和演示数据。

如果引用教材、论文、网络图片或其他第三方素材，应保留授权依据或替换为
自有内容。

## 六、许可证保留

正式发布时建议保留：

```text
frontend/package-lock.json
backend/requirements.lock.txt
THIRD_PARTY_LICENSES.md
```

并在安装目录或说明文档中提供开源许可证文本。

## 七、合规检查

1. 不在源码中提交第三方 API Key。
2. 不删除第三方包的版权和许可证文件。
3. 不将 GPLv3 组件描述为 MIT/Apache。
4. 视频、PPT 和图片来源必须可追溯。
5. DeepSeek 输出用于教学展示时，应遵守服务协议和内容规范。

