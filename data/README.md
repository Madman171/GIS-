# Neo4j 数据导入说明

本目录由 `scripts/export_graph.py` 从实际 Neo4j 数据库只读导出。

## 快照统计

- 模块节点：9
- 知识点节点：344
- 工具节点：10
- 媒体节点：0
- 关系总数：1016
- Neo4j 版本：5.26.30

## 导入顺序

1. `schema.cypher`
2. `modules.cypher`
3. `knowledge-points.cypher`
4. `tools.cypher`
5. `media.cypher`
6. `relationships.cypher`

节点文件使用 `MERGE` 和主键匹配，关系文件在节点导入完成后执行。
`graph-snapshot.json` 用于数据核对和备份，不用于 Neo4j 导入。

## 本地整理草案

`graph-curation.json` 是由 `scripts/build_graph_curation_draft.py` 生成的非破坏性
审阅文件，包含缺失 `subcategory` 的候选分类和待确认的关系调整建议。它不会自动
修改 `graph-snapshot.json`。确认后可先预览，再应用已标记为 `approved` 的条目：

```powershell
backend\.venv\Scripts\python.exe scripts\apply_graph_curation.py
backend\.venv\Scripts\python.exe scripts\apply_graph_curation.py --apply
```
