# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

from learning_path_engine import LearningPathEngine


def node(node_id, name, difficulty, sort_order):
    return {
        "id": node_id,
        "labels": ["KnowledgePoint"],
        "properties": {
            "kp_id": node_id,
            "name": name,
            "difficulty": difficulty,
            "sort_order": sort_order,
        },
    }


def test_prerequisite_chain_and_learning_path():
    nodes = [
        node("A", "基础概念", "入门", 1),
        node("B", "路网建模", "中等", 2),
        node("C", "拓扑分析", "进阶", 3),
        node("D", "工程应用", "高级", 4),
    ]
    links = [
        {"type": "PREREQUISITE_OF", "source": "A", "target": "B"},
        {"type": "PREREQUISITE_OF", "source": "B", "target": "C"},
        {"type": "PREREQUISITE_OF", "source": "C", "target": "D"},
    ]
    engine = LearningPathEngine(nodes, links, max_depth=8)

    chain = engine.prerequisite_chain("D")
    assert [item["id"] for item in chain] == ["A", "B", "C"]

    path = engine.build_learning_path("C")
    assert [item["id"] for item in path[:3]] == ["A", "B", "C"]


def test_recommendation_and_difficulty_filter():
    nodes = [
        node("A", "基础概念", "入门", 1),
        node("B", "路网建模", "中等", 2),
        node("C", "拓扑分析", "进阶", 3),
    ]
    links = [
        {"type": "PREREQUISITE_OF", "source": "A", "target": "B"},
        {"type": "PREREQUISITE_OF", "source": "B", "target": "C"},
    ]
    engine = LearningPathEngine(nodes, links)

    recommendation = engine.recommend("B")
    assert recommendation["prerequisites"][0]["id"] == "A"
    assert recommendation["successors"][0]["id"] == "C"

    advanced = engine.filter_by_difficulty("进阶")
    assert [item["id"] for item in advanced] == ["C"]

