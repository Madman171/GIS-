# 数据库设计说明

## 软件信息

| 项目 | 内容 |
| --- | --- |
| 软件名称 | GIS交通路网教学知识图谱平台 |
| 版本 | V1.0 |
| 数据库 | Neo4j 5.26.30 |
| 快照生成时间 | 2026-09-23T01:29:37.265088+00:00 |

## 节点设计

| 标签 | 数量 | 主键 | 属性 |
| --- | ---: | --- | --- |
| `Module` | 9 | `module_id` | `knowledge_count`, `module_id`, `name`, `order`, `sort_order` |
| `KnowledgePoint` | 344 | `kp_id` | `description`, `difficulty`, `importance`, `kp_id`, `name`, `sort_order`, `subcategory` |
| `Tool` | 10 | `tool_id` | `category`, `name`, `tool_id`, `vendor` |
| `Media` | 0 | `media_id` | 无 |

## 关系设计

| 关系类型 | 起点 | 终点 | 数量 |
| --- | --- | --- | ---: |
| `APPLIED_IN` | `KnowledgePoint` | `KnowledgePoint` | 42 |
| `BELONGS_TO` | `KnowledgePoint` | `Module` | 344 |
| `IMPLEMENTED_IN` | `KnowledgePoint` | `Tool` | 11 |
| `PART_OF` | `KnowledgePoint` | `KnowledgePoint` | 28 |
| `PREREQUISITE_MODULE` | `Module` | `Module` | 5 |
| `PREREQUISITE_OF` | `KnowledgePoint` | `KnowledgePoint` | 86 |
| `RELATED_TO` | `KnowledgePoint` | `KnowledgePoint` | 497 |
| `SUPPORTS` | `Module` | `Module` | 3 |

## 数据完整性

1. 每类节点使用业务主键进行唯一性校验。
2. 所有关系的起点和终点必须能够匹配到已导入节点。
3. 导出脚本会检查重复节点主键和重复关系签名。
4. 导入文件使用 `MERGE`，可以重复执行。

## 数据恢复

在空白 Neo4j 数据库中按 `data/README.md` 的顺序执行导入文件。
完成后可重新执行本导出脚本，核对节点和关系数量是否一致。
