# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import topology_checker


def node(node_id, **properties):
    return {
        "id": node_id,
        "labels": ["RoadNode"],
        "properties": properties,
    }


def relationship(relationship_id, source, target, **properties):
    return {
        "id": relationship_id,
        "type": properties.pop("type", "RELATED_TO"),
        "source": source,
        "target": target,
        "properties": properties,
    }


def test_pseudo_node_detection():
    nodes = [node("A"), node("B"), node("C")]
    links = [
        relationship("r1", "A", "B"),
        relationship("r2", "B", "C"),
    ]

    issues = topology_checker.identify_pseudo_nodes(nodes, links)

    assert len(issues) == 1
    assert issues[0]["type"] == "PSEUDO_NODE"
    assert issues[0]["nodeIds"] == ["B"]


def test_dead_end_detection():
    nodes = [node("A"), node("B"), node("C")]
    links = [
        relationship("r1", "A", "B"),
        relationship("r2", "B", "C"),
        relationship("r3", "C", "A"),
    ]

    assert topology_checker.detect_dead_ends(links) == []

    links.append(relationship("r4", "C", "D"))
    issues = topology_checker.detect_dead_ends(links)
    assert any(issue["type"] == "DEAD_END" for issue in issues)


def test_multilayer_validation():
    nodes = [
        node("A", layer="ground"),
        node("B", layer="elevated"),
    ]
    links = [relationship("r1", "A", "B")]

    issues = topology_checker.validate_multilayer_network(nodes, links)
    assert issues[0]["type"] == "CROSS_LAYER_CONNECTION"

    connector = relationship("r2", "A", "B", type="RAMP")
    assert topology_checker.validate_multilayer_network(
        nodes,
        [connector],
    ) == []


def test_seamless_connection_detection():
    nodes = [
        node("A", x=0, y=0),
        node("B", x=10, y=0),
    ]
    links = [
        relationship(
            "r1",
            "A",
            "B",
            source_x=0,
            source_y=0,
            target_x=15,
            target_y=0,
        )
    ]

    issues = topology_checker.validate_seamless_connections(
        nodes,
        links,
        tolerance=1,
    )
    assert issues[0]["type"] == "SEAM_GAP"
    assert issues[0]["deviation"] == 5.0


def test_topology_score():
    issues = [
        {"type": "PSEUDO_NODE"},
        {"type": "DEAD_END"},
        {"type": "CROSS_LAYER_CONNECTION"},
    ]
    assert topology_checker.calculate_topology_score(issues) == 88.5

