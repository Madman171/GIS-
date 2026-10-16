# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from neo4j import GraphDatabase, READ_ACCESS


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = ROOT_DIR / "docs"

sys.path.insert(0, str(BACKEND_DIR))

from config import (  # noqa: E402
    NEO4J_DATABASE,
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USER,
)


PRIMARY_ID_KEYS = {
    "Module": "module_id",
    "KnowledgePoint": "kp_id",
    "Tool": "tool_id",
    "Media": "media_id",
}


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    return str(value)


def primary_label(labels: List[str]) -> str:
    for label in ("Module", "KnowledgePoint", "Tool", "Media"):
        if label in labels:
            return label
    return sorted(labels)[0] if labels else "Node"


def primary_id_key(label: str) -> str:
    return PRIMARY_ID_KEYS.get(label, "id")


def business_id(label: str, properties: Dict[str, Any]) -> Optional[str]:
    value = properties.get(primary_id_key(label))
    return str(value) if value is not None else None


def cypher_literal(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(cypher_literal(item) for item in value) + "]"
    if isinstance(value, dict):
        entries = ", ".join(
            "{0}: {1}".format(
                "`{0}`".format(str(key).replace("`", "``")),
                cypher_literal(item),
            )
            for key, item in value.items()
        )
        return "{" + entries + "}"
    return json.dumps(str(value), ensure_ascii=False)


def cypher_map(properties: Dict[str, Any]) -> str:
    entries = ", ".join(
        "{0}: {1}".format(
            "`{0}`".format(str(key).replace("`", "``")),
            cypher_literal(value),
        )
        for key, value in properties.items()
    )
    return "{" + entries + "}"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def fetch_graph(driver) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    with driver.session(
        database=NEO4J_DATABASE,
        default_access_mode=READ_ACCESS,
    ) as session:
        node_records = list(
            session.run(
                """
                MATCH (node)
                RETURN node
                ORDER BY
                  labels(node)[0],
                  coalesce(
                    node.module_id,
                    node.kp_id,
                    node.tool_id,
                    node.media_id,
                    ''
                  )
                """,
                timeout=15.0,
            )
        )
        relationship_records = list(
            session.run(
                """
                MATCH (source)-[relationship]->(target)
                RETURN source, relationship, target
                ORDER BY type(relationship), elementId(relationship)
                """,
                timeout=20.0,
            )
        )

    nodes = []
    for record in node_records:
        node = record["node"]
        labels = sorted(node.labels)
        properties = {
            key: json_safe(value)
            for key, value in dict(node).items()
        }
        nodes.append(
            {
                "elementId": node.element_id,
                "labels": labels,
                "primaryLabel": primary_label(labels),
                "businessId": business_id(primary_label(labels), properties),
                "properties": properties,
            }
        )

    relationships = []
    for record in relationship_records:
        source = record["source"]
        relationship = record["relationship"]
        target = record["target"]
        source_labels = sorted(source.labels)
        target_labels = sorted(target.labels)
        source_label = primary_label(source_labels)
        target_label = primary_label(target_labels)
        source_properties = {
            key: json_safe(value)
            for key, value in dict(source).items()
        }
        target_properties = {
            key: json_safe(value)
            for key, value in dict(target).items()
        }
        relationships.append(
            {
                "elementId": relationship.element_id,
                "type": relationship.type,
                "sourceElementId": source.element_id,
                "targetElementId": target.element_id,
                "sourceLabel": source_label,
                "targetLabel": target_label,
                "sourceBusinessId": business_id(
                    source_label,
                    source_properties,
                ),
                "targetBusinessId": business_id(
                    target_label,
                    target_properties,
                ),
                "properties": {
                    key: json_safe(value)
                    for key, value in dict(relationship).items()
                },
            }
        )

    return nodes, relationships


def validate_graph(
    nodes: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
) -> None:
    node_element_ids = set()
    business_ids = set()

    for node in nodes:
        if node["elementId"] in node_element_ids:
            raise ValueError(
                "Duplicate node element ID: {0}".format(node["elementId"])
            )
        node_element_ids.add(node["elementId"])

        if not node["businessId"]:
            raise ValueError(
                "Missing business ID for node {0}".format(node["elementId"])
            )
        business_key = (node["primaryLabel"], node["businessId"])
        if business_key in business_ids:
            raise ValueError(
                "Duplicate business ID: {0}".format(business_key)
            )
        business_ids.add(business_key)

    relationship_signatures = set()
    for relationship in relationships:
        if relationship["sourceElementId"] not in node_element_ids:
            raise ValueError("Relationship source is missing from nodes")
        if relationship["targetElementId"] not in node_element_ids:
            raise ValueError("Relationship target is missing from nodes")
        if not relationship["sourceBusinessId"]:
            raise ValueError("Relationship source business ID is missing")
        if not relationship["targetBusinessId"]:
            raise ValueError("Relationship target business ID is missing")

        signature = (
            relationship["sourceBusinessId"],
            relationship["type"],
            relationship["targetBusinessId"],
        )
        if signature in relationship_signatures:
            raise ValueError(
                "Duplicate relationship signature: {0}".format(signature)
            )
        relationship_signatures.add(signature)


def build_schema_cypher() -> str:
    return """// GIS交通路网教学知识图谱平台 V1.0
// Neo4j schema constraints and indexes.

CREATE CONSTRAINT module_id_unique IF NOT EXISTS
FOR (node:Module) REQUIRE node.module_id IS UNIQUE;

CREATE CONSTRAINT knowledge_point_id_unique IF NOT EXISTS
FOR (node:KnowledgePoint) REQUIRE node.kp_id IS UNIQUE;

CREATE CONSTRAINT tool_id_unique IF NOT EXISTS
FOR (node:Tool) REQUIRE node.tool_id IS UNIQUE;

CREATE CONSTRAINT media_id_unique IF NOT EXISTS
FOR (node:Media) REQUIRE node.media_id IS UNIQUE;

CREATE INDEX module_name_index IF NOT EXISTS
FOR (node:Module) ON (node.name);

CREATE INDEX knowledge_point_name_index IF NOT EXISTS
FOR (node:KnowledgePoint) ON (node.name);

CREATE INDEX knowledge_point_module_index IF NOT EXISTS
FOR (node:KnowledgePoint) ON (node.kp_id);
"""


def build_node_cypher(
    nodes: List[Dict[str, Any]],
    label: str,
) -> str:
    lines = [
        "// GIS交通路网教学知识图谱平台 V1.0",
        "// Generated node import file for {0}.".format(label),
        "",
    ]
    id_key = primary_id_key(label)

    for node in nodes:
        if node["primaryLabel"] != label:
            continue
        node_id = node["businessId"]
        properties = node["properties"]
        lines.append(
            "MERGE (node:{0} {{{1}: {2}}})".format(
                label,
                id_key,
                cypher_literal(node_id),
            )
        )
        lines.append("SET node = {0};".format(cypher_map(properties)))
        lines.append("")

    return "\n".join(lines)


def build_relationship_cypher(
    relationships: List[Dict[str, Any]],
) -> str:
    lines = [
        "// GIS交通路网教学知识图谱平台 V1.0",
        "// Generated relationship import file.",
        "",
    ]

    for relationship in relationships:
        relationship_type = relationship["type"]
        if not re.match(r"^[A-Z][A-Z0-9_]*$", relationship_type):
            raise ValueError(
                "Unsupported relationship type: {0}".format(
                    relationship_type
                )
            )

        source_id_key = primary_id_key(relationship["sourceLabel"])
        target_id_key = primary_id_key(relationship["targetLabel"])
        lines.append(
            (
                "MATCH (source:{0} {{{1}: {2}}}), "
                "(target:{3} {{{4}: {5}}})"
            ).format(
                relationship["sourceLabel"],
                source_id_key,
                cypher_literal(relationship["sourceBusinessId"]),
                relationship["targetLabel"],
                target_id_key,
                cypher_literal(relationship["targetBusinessId"]),
            )
        )
        lines.append(
            "MERGE (source)-[relationship:{0}]->(target)".format(
                relationship_type
            )
        )
        if relationship["properties"]:
            lines.append(
                "SET relationship = {0};".format(
                    cypher_map(relationship["properties"])
                )
            )
        else:
            lines[-1] += ";"
        lines.append("")

    return "\n".join(lines)


def build_data_readme(metadata: Dict[str, Any]) -> str:
    return """# Neo4j 数据导入说明

本目录由 `scripts/export_graph.py` 从实际 Neo4j 数据库只读导出。

## 快照统计

- 模块节点：{module_count}
- 知识点节点：{knowledge_point_count}
- 工具节点：{tool_count}
- 媒体节点：{media_count}
- 关系总数：{relationship_count}
- Neo4j 版本：{neo4j_version}

## 导入顺序

1. `schema.cypher`
2. `modules.cypher`
3. `knowledge-points.cypher`
4. `tools.cypher`
5. `media.cypher`
6. `relationships.cypher`

节点文件使用 `MERGE` 和主键匹配，关系文件在节点导入完成后执行。
`graph-snapshot.json` 用于数据核对和备份，不用于 Neo4j 导入。
""".format(**metadata)


def build_database_document(
    nodes: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
    metadata: Dict[str, Any],
) -> str:
    label_counts = Counter(node["primaryLabel"] for node in nodes)
    relationship_counts = Counter(
        relationship["type"] for relationship in relationships
    )
    relation_shapes = Counter(
        (
            relationship["type"],
            relationship["sourceLabel"],
            relationship["targetLabel"],
        )
        for relationship in relationships
    )
    properties_by_label = defaultdict(set)

    for node in nodes:
        properties_by_label[node["primaryLabel"]].update(
            node["properties"].keys()
        )

    lines = [
        "# 数据库设计说明",
        "",
        "## 软件信息",
        "",
        "| 项目 | 内容 |",
        "| --- | --- |",
        "| 软件名称 | GIS交通路网教学知识图谱平台 |",
        "| 版本 | V1.0 |",
        "| 数据库 | Neo4j {0} |".format(metadata["neo4j_version"]),
        "| 快照生成时间 | {0} |".format(metadata["generated_at"]),
        "",
        "## 节点设计",
        "",
        "| 标签 | 数量 | 主键 | 属性 |",
        "| --- | ---: | --- | --- |",
    ]

    for label in ("Module", "KnowledgePoint", "Tool", "Media"):
        properties = ", ".join(
            "`{0}`".format(key)
            for key in sorted(properties_by_label.get(label, set()))
        )
        lines.append(
            "| `{0}` | {1} | `{2}` | {3} |".format(
                label,
                label_counts.get(label, 0),
                primary_id_key(label),
                properties or "无",
            )
        )

    lines.extend(
        [
            "",
            "## 关系设计",
            "",
            "| 关系类型 | 起点 | 终点 | 数量 |",
            "| --- | --- | --- | ---: |",
        ]
    )

    for relationship_type in sorted(relationship_counts):
        shapes = [
            shape
            for shape in relation_shapes
            if shape[0] == relationship_type
        ]
        for _, source_label, target_label in sorted(shapes):
            count = relation_shapes[
                (relationship_type, source_label, target_label)
            ]
            lines.append(
                "| `{0}` | `{1}` | `{2}` | {3} |".format(
                    relationship_type,
                    source_label,
                    target_label,
                    count,
                )
            )

    lines.extend(
        [
            "",
            "## 数据完整性",
            "",
            "1. 每类节点使用业务主键进行唯一性校验。",
            "2. 所有关系的起点和终点必须能够匹配到已导入节点。",
            "3. 导出脚本会检查重复节点主键和重复关系签名。",
            "4. 导入文件使用 `MERGE`，可以重复执行。",
            "",
            "## 数据恢复",
            "",
            "在空白 Neo4j 数据库中按 `data/README.md` 的顺序执行导入文件。",
            "完成后可重新执行本导出脚本，核对节点和关系数量是否一致。",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    if not NEO4J_PASSWORD:
        raise RuntimeError(
            "NEO4J_PASSWORD is not configured. Set backend/.env first."
        )

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )

    try:
        driver.verify_connectivity()
        with driver.session(
            database=NEO4J_DATABASE,
            default_access_mode=READ_ACCESS,
        ) as session:
            neo4j_version = session.run(
                """
                CALL dbms.components()
                YIELD name, versions
                RETURN versions[0] AS version
                """
            ).single()["version"]

        nodes, relationships = fetch_graph(driver)
        validate_graph(nodes, relationships)
    finally:
        driver.close()

    label_counts = Counter(node["primaryLabel"] for node in nodes)
    metadata = {
        "module_count": label_counts.get("Module", 0),
        "knowledge_point_count": label_counts.get("KnowledgePoint", 0),
        "tool_count": label_counts.get("Tool", 0),
        "media_count": label_counts.get("Media", 0),
        "relationship_count": len(relationships),
        "neo4j_version": neo4j_version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    snapshot = {
        "metadata": metadata,
        "nodes": nodes,
        "relationships": relationships,
    }

    write_text(
        DATA_DIR / "graph-snapshot.json",
        json.dumps(snapshot, ensure_ascii=False, indent=2),
    )
    write_text(DATA_DIR / "schema.cypher", build_schema_cypher())
    write_text(
        DATA_DIR / "modules.cypher",
        build_node_cypher(nodes, "Module"),
    )
    write_text(
        DATA_DIR / "knowledge-points.cypher",
        build_node_cypher(nodes, "KnowledgePoint"),
    )
    write_text(DATA_DIR / "tools.cypher", build_node_cypher(nodes, "Tool"))
    write_text(DATA_DIR / "media.cypher", build_node_cypher(nodes, "Media"))
    write_text(
        DATA_DIR / "relationships.cypher",
        build_relationship_cypher(relationships),
    )
    write_text(DATA_DIR / "README.md", build_data_readme(metadata))
    write_text(
        DOCS_DIR / "02-database-design.md",
        build_database_document(nodes, relationships, metadata),
    )

    print(
        "Exported {0} nodes and {1} relationships.".format(
            len(nodes),
            len(relationships),
        )
    )
    print(
        "Modules: {0}, KnowledgePoints: {1}, Tools: {2}, Media: {3}".format(
            metadata["module_count"],
            metadata["knowledge_point_count"],
            metadata["tool_count"],
            metadata["media_count"],
        )
    )
    print("Output: {0}".format(DATA_DIR))


if __name__ == "__main__":
    main()
