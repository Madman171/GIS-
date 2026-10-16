# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import pytest

import import_snapshot


def snapshot():
    return {
        "nodes": [
            {
                "elementId": "n1",
                "primaryLabel": "KnowledgePoint",
                "businessId": "M1-001",
                "properties": {"kp_id": "M1-001", "name": "道路定义"},
            },
            {
                "elementId": "n2",
                "primaryLabel": "Module",
                "businessId": "M1",
                "properties": {"module_id": "M1", "name": "基础理论"},
            },
        ],
        "relationships": [
            {
                "type": "BELONGS_TO",
                "sourceElementId": "n1",
                "targetElementId": "n2",
                "sourceLabel": "KnowledgePoint",
                "targetLabel": "Module",
                "sourceBusinessId": "M1-001",
                "targetBusinessId": "M1",
                "properties": {},
            }
        ],
    }


def test_snapshot_dry_run():
    summary = import_snapshot.import_snapshot(
        snapshot(),
        apply_changes=False,
    )
    assert summary["nodeCount"] == 2
    assert summary["relationshipCount"] == 1


def test_snapshot_duplicate_business_id_is_rejected():
    data = snapshot()
    data["nodes"][1]["primaryLabel"] = "KnowledgePoint"
    data["nodes"][1]["businessId"] = "M1-001"
    data["nodes"][1]["properties"] = {
        "kp_id": "M1-001",
        "name": "重复知识点",
    }
    with pytest.raises(ValueError):
        import_snapshot.validate_snapshot(data)
