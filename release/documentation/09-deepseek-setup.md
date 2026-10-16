# DeepSeek 智能问答配置说明

## 一、获取 API Key

1. 访问 DeepSeek 开放平台：

   ```text
   https://platform.deepseek.com/
   ```

2. 注册或登录账号。
3. 进入 API Keys 页面。
4. 创建一个新的 API Key。
5. 立即复制并妥善保存，页面通常不会再次完整显示该 Key。
6. 确认账号中已有可用额度。

不要将 API Key 粘贴到聊天记录、源代码、截图或 Git 仓库中。

## 二、配置后端

进入后端目录：

```powershell
cd E:\gis-knowledge-platform\backend
Copy-Item .env.example .env
```

编辑 `backend/.env`：

```dotenv
DEEPSEEK_API_KEY=sk-你的实际Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TIMEOUT_SECONDS=30
DEEPSEEK_MAX_TOKENS=800
DEEPSEEK_TEMPERATURE=0.2
CHAT_RATE_LIMIT_PER_MINUTE=5
```

`backend/.env` 已被 Git 忽略，不会进入源码提交文件。

## 三、重启后端

```powershell
cd E:\gis-knowledge-platform\backend
.\.venv\Scripts\Activate.ps1
python main.py
```

## 四、检查配置

浏览器访问：

```text
http://localhost:8000/api/chat/status
```

未配置时返回：

```json
{
  "configured": false,
  "model": "deepseek-chat",
  "message": "DeepSeek API Key 尚未配置"
}
```

配置成功后返回：

```json
{
  "configured": true,
  "model": "deepseek-chat",
  "message": "DeepSeek API 已配置"
}
```

## 五、网页使用

1. 打开知识图谱平台。
2. 选择模块或知识点。
3. 在右侧智能问答窗口输入问题。
4. 后端会根据当前模块、知识点和问题搜索相关内容。
5. DeepSeek 仅依据检索到的图谱上下文回答。
6. 回答下方会显示相关知识点，点击后可以直接跳转。

## 六、常用参数

| 参数 | 说明 |
| --- | --- |
| `DEEPSEEK_API_KEY` | API 密钥 |
| `DEEPSEEK_BASE_URL` | DeepSeek API 地址 |
| `DEEPSEEK_MODEL` | 默认 `deepseek-chat` |
| `DEEPSEEK_TIMEOUT_SECONDS` | 请求超时时间 |
| `DEEPSEEK_MAX_TOKENS` | 单次回答最大长度 |
| `DEEPSEEK_TEMPERATURE` | 回答随机性，知识问答建议使用较低值 |
| `CHAT_RATE_LIMIT_PER_MINUTE` | 每个IP每分钟最大提问次数 |

## 七、注意事项

1. 网页不会把图谱全文发送给模型，只会发送当前问题相关的有限上下文。
2. 模型不会直接生成或执行 Cypher。
3. API Key 无效、账户欠费或网络异常时，接口会返回可读错误。
4. DeepSeek 是外部服务，正式部署前应阅读其服务条款和数据处理规则。
