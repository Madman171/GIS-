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
from collections import Counter, defaultdict
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

RELATIONSHIP_ENDPOINTS = {
    "BELONGS_TO": ("KnowledgePoint", "Module"),
    "PREREQUISITE_OF": ("KnowledgePoint", "KnowledgePoint"),
    "RELATED_TO": ("KnowledgePoint", "KnowledgePoint"),
    "PART_OF": ("KnowledgePoint", "KnowledgePoint"),
    "APPLIED_IN": ("KnowledgePoint", "KnowledgePoint"),
    "IMPLEMENTED_IN": ("KnowledgePoint", "Tool"),
    "SUPPORTS": ("Module", "Module"),
    "PREREQUISITE_MODULE": ("Module", "Module"),
    "HAS_MEDIA": ("KnowledgePoint", "Media"),
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


def build_relationship_prune_plan(
    snapshot: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Group snapshot relationships for an explicit, scoped prune operation."""
    groups: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for relationship in snapshot["relationships"]:
        relationship_type = str(relationship["type"])
        endpoint = RELATIONSHIP_ENDPOINTS.get(relationship_type)
        if endpoint is None:
            continue
        source_label, target_label = endpoint
        key = (relationship_type, source_label, target_label)
        group = groups.setdefault(
            key,
            {
                "type": relationship_type,
                "sourceLabel": source_label,
                "targetLabel": target_label,
                "sourceKey": PRIMARY_ID_KEYS[source_label],
                "targetKey": PRIMARY_ID_KEYS[target_label],
                "keep": set(),
            },
        )
        group["keep"].add(
            "{0}\x1f{1}".format(
                str(relationship["sourceBusinessId"]),
                str(relationship["targetBusinessId"]),
            )
        )
    return list(groups.values())


def delete_extra_relationships(
    tx,
    relationship_type: str,
    source_label: str,
    target_label: str,
    source_key: str,
    target_key: str,
    source_ids: List[str],
    target_ids: List[str],
    keep_signatures: List[str],
) -> int:
    if not source_ids or not target_ids:
        return 0
    result = tx.run(
        (
            "MATCH (source:{0})-[relationship:{1}]->(target:{2}) "
            "WHERE source.{3} IN $source_ids "
            "AND target.{4} IN $target_ids "
            "AND NOT (source.{3} + $separator + target.{4} IN $keep_signatures) "
            "DELETE relationship "
            "RETURN count(relationship) AS deleted"
        ).format(
            source_label,
            relationship_type,
            target_label,
            source_key,
            target_key,
        ),
        source_ids=source_ids,
        target_ids=target_ids,
        separator="\x1f",
        keep_signatures=keep_signatures,
        timeout=30.0,
    ).single()
    return int(result["deleted"]) if result else 0


def prune_snapshot_relationships(tx, snapshot: Dict[str, Any]) -> int:
    nodes_by_label: Dict[str, Set[str]] = defaultdict(set)
    for node in snapshot["nodes"]:
        label = str(node["primaryLabel"])
        nodes_by_label[label].add(node_business_id(node))

    deleted = 0
    for group in build_relationship_prune_plan(snapshot):
        deleted += delete_extra_relationships(
            tx,
            relationship_type=group["type"],
            source_label=group["sourceLabel"],
            target_label=group["targetLabel"],
            source_key=group["sourceKey"],
            target_key=group["targetKey"],
            source_ids=sorted(nodes_by_label[group["sourceLabel"]]),
            target_ids=sorted(nodes_by_label[group["targetLabel"]]),
            keep_signatures=sorted(group["keep"]),
        )
    return deleted


def import_snapshot(
    snapshot: Dict[str, Any],
    apply_changes: bool,
    prune_relationships: bool = False,
) -> Dict[str, Any]:
    validate_snapshot(snapshot)
    summary = {
        "nodeCount": len(snapshot["nodes"]),
        "relationshipCount": len(snapshot["relationships"]),
        "pruneRelationships": prune_relationships,
        "deletedRelationshipCount": 0,
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
            if prune_relationships:
                summary["deletedRelationshipCount"] = session.execute_write(
                    prune_snapshot_relationships,
                    snapshot,
                )
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
    parser.add_argument(
        "--prune-relationships",
        action="store_true",
        help=(
            "删除快照节点范围内、快照中不存在的同类型关系；"
            "默认关闭，必须与 --apply 一起使用"
        ),
    )
    args = parser.parse_args()

    snapshot = load_snapshot(Path(args.path))
    if args.prune_relationships and not args.apply:
        raise SystemExit("--prune-relationships 必须与 --apply 一起使用")
    summary = import_snapshot(
        snapshot,
        apply_changes=args.apply,
        prune_relationships=args.prune_relationships,
    )
    mode = "已导入" if args.apply else "校验通过"
    print("{0}: {1}".format(mode, json.dumps(summary, ensure_ascii=False)))


if __name__ == "__main__":
    main()

