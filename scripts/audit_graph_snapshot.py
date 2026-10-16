"""Read-only audit for data/graph-snapshot.json."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "data" / "graph-snapshot.json"
ID_KEYS = {"Module": "module_id", "KnowledgePoint": "kp_id", "Tool": "tool_id", "Media": "media_id"}
ENDPOINTS = {
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


def node_id(node: dict[str, Any]) -> str:
    props = node.get("properties", {})
    return str(node.get("businessId") or props.get(ID_KEYS.get(node.get("primaryLabel"), "")) or node.get("elementId", ""))


def scc(graph: dict[str, set[str]]) -> list[list[str]]:
    index = 0
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    active: set[str] = set()
    result: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = low[node] = index
        index += 1
        stack.append(node)
        active.add(node)
        for target in graph.get(node, set()):
            if target not in indices:
                visit(target)
                low[node] = min(low[node], low[target])
            elif target in active:
                low[node] = min(low[node], indices[target])
        if low[node] != indices[node]:
            return
        component = []
        while True:
            target = stack.pop()
            active.remove(target)
            component.append(target)
            if target == node:
                break
        result.append(component)

    vertices = set(graph)
    vertices.update(target for targets in graph.values() for target in targets)
    for node in vertices:
        if node not in indices:
            visit(node)
    return result


def audit(path: Path) -> dict[str, Any]:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    nodes = snapshot["nodes"]
    relationships = snapshot["relationships"]
    by_element = {str(node["elementId"]): node for node in nodes}
    node_keys = Counter((str(node["primaryLabel"]), node_id(node)) for node in nodes)
    rel_keys = Counter((str(rel.get("sourceBusinessId")), str(rel.get("type")), str(rel.get("targetBusinessId"))) for rel in relationships)
    degree = Counter()
    memberships: dict[str, list[str]] = defaultdict(list)
    prerequisite_graph: dict[str, set[str]] = defaultdict(set)
    endpoint_errors = []
    invalid_directions = []
    self_loops = []

    for rel in relationships:
        source = by_element.get(str(rel.get("sourceElementId")))
        target = by_element.get(str(rel.get("targetElementId")))
        if source is None or target is None:
            endpoint_errors.append(rel)
            continue
        source_element = str(source["elementId"])
        target_element = str(target["elementId"])
        degree[source_element] += 1
        degree[target_element] += 1
        if source_element == target_element:
            self_loops.append(rel)
        rel_type = str(rel.get("type"))
        expected = ENDPOINTS.get(rel_type)
        actual = (str(source["primaryLabel"]), str(target["primaryLabel"]))
        if expected and expected != actual:
            invalid_directions.append({"type": rel_type, "source": node_id(source), "target": node_id(target), "actual": actual, "expected": expected})
        if rel_type == "BELONGS_TO":
            memberships[node_id(source)].append(node_id(target))
        if rel_type in {"PREREQUISITE_OF", "PREREQUISITE_MODULE"}:
            prerequisite_graph[node_id(source)].add(node_id(target))

    kps = [node for node in nodes if node.get("primaryLabel") == "KnowledgePoint"]
    modules = [node for node in nodes if node.get("primaryLabel") == "Module"]
    missing = {field: [node_id(node) for node in kps if not node.get("properties", {}).get(field)] for field in ("name", "description", "difficulty", "importance", "subcategory")}
    module_summary = {}
    for module in modules:
        module_id = node_id(module)
        members = [node for node in kps if module_id in memberships.get(node_id(node), [])]
        module_summary[module_id] = {
            "name": module.get("properties", {}).get("name", ""),
            "knowledge_points": len(members),
            "missing_subcategory": sum(not node.get("properties", {}).get("subcategory") for node in members),
        }
    cycles = [sorted(component) for component in scc(prerequisite_graph) if len(component) > 1 or component[0] in prerequisite_graph.get(component[0], set())]
    return {
        "metadata": snapshot.get("metadata", {}),
        "counts": {"nodes": len(nodes), "relationships": len(relationships), "labels": Counter(str(node.get("primaryLabel")) for node in nodes), "relationship_types": Counter(str(rel.get("type")) for rel in relationships)},
        "duplicate_business_ids": {str(key): value for key, value in node_keys.items() if value > 1},
        "duplicate_relationship_signatures": {str(key): value for key, value in rel_keys.items() if value > 1},
        "endpoint_errors": endpoint_errors,
        "invalid_directions": invalid_directions,
        "self_loops": self_loops,
        "orphan_nodes": [node_id(node) for node in nodes if degree[str(node["elementId"])] == 0],
        "unassigned_knowledge_points": [node_id(node) for node in kps if not memberships.get(node_id(node))],
        "multi_assigned_knowledge_points": [node_id(node) for node in kps if len(memberships.get(node_id(node), [])) > 1],
        "missing_fields": {field: values for field, values in missing.items() if values},
        "module_summary": module_summary,
        "prerequisite_cycles": cycles,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="审计 GIS 教学知识图谱快照")
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit(args.path)
    output = json.dumps(report, ensure_ascii=False, indent=2, default=dict) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
