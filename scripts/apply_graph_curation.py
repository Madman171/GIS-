"""Apply approved entries from data/graph-curation.json to the local snapshot.

The default mode is a preview. Use --apply only after the review statuses in
the curation file have been changed to "approved".
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = ROOT / "data" / "graph-snapshot.json"
DEFAULT_CURATIONS = ROOT / "data" / "graph-curation.json"

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


def business_id(node: dict[str, Any]) -> str:
    label = str(node.get("primaryLabel", ""))
    properties = node.get("properties", {})
    key = PRIMARY_ID_KEYS.get(label)
    return str(node.get("businessId") or (properties.get(key) if key else "") or node.get("elementId", ""))


def relation_signature(relationship: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(relationship["sourceBusinessId"]),
        str(relationship["type"]),
        str(relationship["targetBusinessId"]),
    )


def make_relationship(
    snapshot_nodes: dict[tuple[str, str], dict[str, Any]],
    relationship_type: str,
    source_id: str,
    target_id: str,
) -> dict[str, Any]:
    if relationship_type not in RELATIONSHIP_ENDPOINTS:
        raise ValueError(f"不支持的关系类型: {relationship_type}")
    source_label, target_label = RELATIONSHIP_ENDPOINTS[relationship_type]
    source = snapshot_nodes.get((source_label, source_id))
    target = snapshot_nodes.get((target_label, target_id))
    if source is None or target is None:
        raise ValueError(
            f"关系端点不存在: {source_label}:{source_id} -> {target_label}:{target_id}"
        )
    return {
        "elementId": f"curation:{relationship_type}:{source_id}:{target_id}",
        "type": relationship_type,
        "sourceElementId": str(source["elementId"]),
        "targetElementId": str(target["elementId"]),
        "sourceLabel": source_label,
        "targetLabel": target_label,
        "sourceBusinessId": source_id,
        "targetBusinessId": target_id,
        "properties": {},
    }


def apply_draft(snapshot: dict[str, Any], draft: dict[str, Any]) -> dict[str, int]:
    nodes = {
        (str(node["primaryLabel"]), business_id(node)): node
        for node in snapshot["nodes"]
    }
    changed_subcategories = 0
    skipped_subcategories = 0
    for proposal in draft.get("subcategory_proposals", []):
        if proposal.get("review_status") != "approved":
            skipped_subcategories += 1
            continue
        key = ("KnowledgePoint", str(proposal["kp_id"]))
        node = nodes.get(key)
        if node is None:
            raise ValueError(f"分类草案中的知识点不存在: {proposal['kp_id']}")
        category = str(proposal.get("suggested_subcategory", "")).strip()
        if not category:
            raise ValueError(f"批准的分类不能为空: {proposal['kp_id']}")
        node.setdefault("properties", {})["subcategory"] = category
        changed_subcategories += 1

    relationships = snapshot["relationships"]
    existing = {relation_signature(item) for item in relationships}
    added_relationships = 0
    removed_relationships = 0
    skipped_relationships = 0

    for proposal in draft.get("relationship_proposals", []):
        if proposal.get("status") != "approved":
            skipped_relationships += 1
            continue
        operation = proposal.get("operation")
        removals = proposal.get("remove", [])
        additions = proposal.get("add", [])
        if operation == "add":
            additions = [
                {
                    "type": proposal["type"],
                    "source": proposal["source"],
                    "target": proposal["target"],
                }
            ]
        elif operation != "replace_cycle":
            raise ValueError(f"不支持的关系操作: {operation}")

        for item in removals:
            signature = (
                str(item["source"]),
                str(item["type"]),
                str(item["target"]),
            )
            before = len(relationships)
            relationships[:] = [
                relationship
                for relationship in relationships
                if relation_signature(relationship) != signature
            ]
            if len(relationships) != before:
                removed_relationships += 1
                existing.discard(signature)

        for item in additions:
            relationship = make_relationship(
                nodes,
                str(item["type"]),
                str(item["source"]),
                str(item["target"]),
            )
            signature = relation_signature(relationship)
            if signature in existing:
                continue
            relationships.append(relationship)
            existing.add(signature)
            added_relationships += 1

    return {
        "changedSubcategories": changed_subcategories,
        "skippedSubcategories": skipped_subcategories,
        "addedRelationships": added_relationships,
        "removedRelationships": removed_relationships,
        "skippedRelationshipProposals": skipped_relationships,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="应用已批准的图谱整理草案")
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--curations", type=Path, default=DEFAULT_CURATIONS)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="将已批准的变更写回快照；默认只预览",
    )
    args = parser.parse_args()

    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    draft = json.loads(args.curations.read_text(encoding="utf-8"))
    summary = apply_draft(snapshot, draft)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.apply:
        snapshot.setdefault("metadata", {})["curation_source"] = str(args.curations)
        args.snapshot.write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"已写入本地快照: {args.snapshot}")
    else:
        print("预览模式：未修改本地快照。批准后请重新执行并加 --apply。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
