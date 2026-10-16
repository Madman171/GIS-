# 视频与 PPT 导入说明

## 数据设计

媒体文件本体存放在 `backend/media`，Neo4j 只保存媒体元数据和文件地址：

```cypher
(:KnowledgePoint)-[:HAS_MEDIA]->(:Media)
```

`Media` 节点属性：

| 属性 | 说明 |
| --- | --- |
| `media_id` | 媒体唯一标识 |
| `type` | `video` 或 `slides` |
| `title` | 资源标题 |
| `format` | `mp4`、`webm`、`pdf`、`ppt` 或 `pptx` |
| `url` | 浏览器访问地址 |
| `cover_url` | 视频封面地址，可选 |
| `order` | 同一知识点下的显示顺序 |

## 文件目录

```text
backend/media/
├── videos/
├── slides/
└── covers/
```

推荐文件命名：

```text
videos/M1-001.mp4
slides/M1-001.pdf
covers/M1-001.jpg
```

## 导入清单

将媒体文件放入对应目录后，编辑 `data/media-manifest.json`：

```json
{
  "items": [
    {
      "media_id": "M1-001-video-01",
      "knowledge_point_id": "M1-001",
      "type": "video",
      "title": "GIS交通路网基础介绍",
      "file": "videos/M1-001.mp4",
      "cover": "covers/M1-001.jpg",
      "order": 1
    },
    {
      "media_id": "M1-001-slides-01",
      "knowledge_point_id": "M1-001",
      "type": "slides",
      "title": "知识点配套课件",
      "file": "slides/M1-001.pdf",
      "order": 1
    }
  ]
}
```

## 检查清单

默认只检查，不写入数据库：

```powershell
backend\.venv\Scripts\python.exe scripts\import_media.py
```

确认检查通过后写入 Neo4j：

```powershell
backend\.venv\Scripts\python.exe scripts\import_media.py --apply
```

## 浏览器支持

1. MP4 和 WebM 用于视频播放。
2. PDF 用于网页预览。
3. PPTX 通常只能下载，建议同时提供 PDF 预览版。
4. 媒体文件默认不进入源码提交，需单独备份。
