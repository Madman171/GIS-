# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import json
from pathlib import Path


SNAPSHOT_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "graph-snapshot.json"
)


def test_snapshot_counts():
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    metadata = snapshot["metadata"]
    assert metadata["module_count"] == 9
    assert metadata["knowledge_point_count"] == 344
    assert metadata["tool_count"] == 10
    assert metadata["media_count"] == 0
    assert metadata["relationship_count"] == len(
        snapshot["relationships"]
    )
    assert metadata["knowledge_fill_record_count"] == 192


def test_knowledge_fill_fields_and_relationships():
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    nodes = {
        node["businessId"]: node
        for node in snapshot["nodes"]
    }
    filled = nodes["M5-001"]["properties"]
    assert filled["difficulty"] == "入门"
    assert filled["importance"] == "核心"
    assert filled["description"]

    signatures = {
        (
            relationship["sourceBusinessId"],
            relationship["type"],
            relationship["targetBusinessId"],
        )
        for relationship in snapshot["relationships"]
    }
    assert ("M5-001", "RELATED_TO", "M5-002") in signatures


def test_snapshot_graph_integrity():
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    node_ids = {node["elementId"] for node in snapshot["nodes"]}
    business_ids = {
        (node["primaryLabel"], node["businessId"])
        for node in snapshot["nodes"]
    }

    assert len(node_ids) == len(snapshot["nodes"])
    assert len(business_ids) == len(snapshot["nodes"])

    for relationship in snapshot["relationships"]:
        assert relationship["sourceElementId"] in node_ids
        assert relationship["targetElementId"] in node_ids


def test_snapshot_relationship_types():
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    relationship_types = {
        relationship["type"]
        for relationship in snapshot["relationships"]
    }
    assert relationship_types == {
        "APPLIED_IN",
        "BELONGS_TO",
        "IMPLEMENTED_IN",
        "PART_OF",
        "PREREQUISITE_MODULE",
        "PREREQUISITE_OF",
        "RELATED_TO",
        "SUPPORTS",
    }

