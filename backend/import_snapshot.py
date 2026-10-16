# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 后端服务
# 本文件为平台核心业务代码，受软件著作权保护

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from neo4j import GraphDatabase

from config import (
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


def load_snapshot(path: Path) -> Dict[str, Any]:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(snapshot.get("nodes"), list):
        raise ValueError("快照缺少 nodes 数组")
    if not isinstance(snapshot.get("relationships"), list):
        raise ValueError("快照缺少 relationships 数组")
    return snapshot


def node_business_id(node: Dict[str, Any]) -> str:
    label = str(node.get("primaryLabel", ""))
    key = PRIMARY_ID_KEYS.get(label)
    properties = node.get("properties", {})
    if key and properties.get(key) is not None:
        return str(properties[key])
    if node.get("businessId") is not None:
        return str(node["businessId"])
    return str(node.get("elementId", ""))


def validate_snapshot(snapshot: Dict[str, Any]) -> None:
    nodes = snapshot["nodes"]
    relationships = snapshot["relationships"]
    node_ids: Set[str] = set()
    business_ids: Set[Tuple[str, str]] = set()

    for node in nodes:
        element_id = str(node.get("elementId", ""))
        if not element_id or element_id in node_ids:
            raise ValueError("节点 elementId 缺失或重复")
        node_ids.add(element_id)

        label = str(node.get("primaryLabel", ""))
        if label not in PRIMARY_ID_KEYS:
            raise ValueError("不支持的节点标签: {0}".format(label))
        business_id = node_business_id(node)
        business_key = (label, business_id)
        if not business_id or business_key in business_ids:
            raise ValueError("节点业务主键缺失或重复")
        business_ids.add(business_key)

    relationship_signatures: Set[Tuple[str, str, str]] = set()
    for relationship in relationships:
        relationship_type = str(relationship.get("type", ""))
        if not re.match(r"^[A-Z][A-Z0-9_]*$", relationship_type):
            raise ValueError("非法关系类型: {0}".format(relationship_type))
        source = str(relationship.get("sourceElementId", ""))
        target = str(relationship.get("targetElementId", ""))
        if source not in node_ids or target not in node_ids:
            raise ValueError("关系端点无法匹配节点")
        signature = (
            str(relationship.get("sourceBusinessId", "")),
            relationship_type,
            str(relationship.get("targetBusinessId", "")),
        )
        if signature in relationship_signatures:
            raise ValueError("关系签名重复: {0}".format(signature))
        relationship_signatures.add(signature)


def upsert_node(tx, node: Dict[str, Any]) -> None:
    label = str(node["primaryLabel"])
    properties = node.get("properties", {})
    id_key = PRIMARY_ID_KEYS[label]
    business_id = node_business_id(node)
    tx.run(
        (
            "MERGE (node:{0} {{{1}: $business_id}}) "
            "SET node = $properties"
        ).format(label, id_key),
        business_id=business_id,
        properties=properties,
        timeout=10.0,
    )


def upsert_relationship(tx, relationship: Dict[str, Any]) -> None:
    source_label = str(relationship["sourceLabel"])
    target_label = str(relationship["targetLabel"])
    source_key = PRIMARY_ID_KEYS[source_label]
    target_key = PRIMARY_ID_KEYS[target_label]
    relationship_type = str(relationship["type"])
    tx.run(
        (
            "MATCH (source:{0} {{{1}: $source_id}}), "
            "(target:{2} {{{3}: $target_id}}) "
            "MERGE (source)-[relationship:{4}]->(target) "
            "SET relationship = $properties"
        ).format(
            source_label,
            source_key,
            target_label,
            target_key,
            relationship_type,
        ),
        source_id=str(relationship["sourceBusinessId"]),
        target_id=str(relationship["targetBusinessId"]),
        properties=relationship.get("properties", {}),
        timeout=10.0,
    )


def import_snapshot(snapshot: Dict[str, Any], apply_changes: bool) -> Dict[str, Any]:
    validate_snapshot(snapshot)
    summary = {
        "nodeCount": len(snapshot["nodes"]),
        "relationshipCount": len(snapshot["relationships"]),
        "labels": dict(
            Counter(
                str(node["primaryLabel"])
                for node in snapshot["nodes"]
            )
        ),
        "relationshipTypes": dict(
            Counter(
                str(relationship["type"])
                for relationship in snapshot["relationships"]
            )
        ),
    }
    if not apply_changes:
        return summary

    if not NEO4J_PASSWORD:
        raise RuntimeError("NEO4J_PASSWORD 未配置")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            for node in snapshot["nodes"]:
                session.execute_write(upsert_node, node)
            for relationship in snapshot["relationships"]:
                session.execute_write(upsert_relationship, relationship)
    finally:
        driver.close()
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="校验并导入GIS交通路网教学知识图谱快照"
    )
    parser.add_argument(
        "--path",
        default=str(
            Path(__file__).resolve().parents[1]
            / "data"
            / "graph-snapshot.json"
        ),
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="确认后将快照写入Neo4j",
    )
    args = parser.parse_args()

    snapshot = load_snapshot(Path(args.path))
    summary = import_snapshot(snapshot, apply_changes=args.apply)
    mode = "已导入" if args.apply else "校验通过"
    print("{0}: {1}".format(mode, json.dumps(summary, ensure_ascii=False)))


if __name__ == "__main__":
    main()

