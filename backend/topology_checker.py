# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 后端服务
# 本文件为平台核心业务代码，受软件著作权保护

from collections import defaultdict
from math import hypot
from typing import Any, Dict, Iterable, List, Optional, Tuple


TOPOLOGY_RELATIONSHIPS = {
    "APPLIED_IN",
    "IMPLEMENTED_IN",
    "PART_OF",
    "PREREQUISITE_MODULE",
    "PREREQUISITE_OF",
    "RELATED_TO",
    "SUPPORTS",
}

LAYER_CONNECTOR_TYPES = {
    "INTERCHANGE",
    "RAMP",
    "LAYER_CONNECTOR",
}


def _node_id(node: Dict[str, Any]) -> str:
    if node.get("id") is not None:
        return str(node["id"])
    properties = node.get("properties", {})
    for key in ("module_id", "kp_id", "tool_id", "media_id", "road_id"):
        if properties.get(key) is not None:
            return str(properties[key])
    return ""


def _labels(node: Dict[str, Any]) -> List[str]:
    return [str(label) for label in node.get("labels", [])]


def _properties(node: Dict[str, Any]) -> Dict[str, Any]:
    properties = node.get("properties", node)
    return properties if isinstance(properties, dict) else {}


def _numeric(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coordinate_from(properties: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    x = _numeric(
        properties.get("x")
        if properties.get("x") is not None
        else properties.get("lon")
    )
    y = _numeric(
        properties.get("y")
        if properties.get("y") is not None
        else properties.get("lat")
    )
    if x is None or y is None:
        return None
    return x, y


def _layer_from(properties: Dict[str, Any]) -> Optional[str]:
    explicit_layer = str(properties.get("layer", "")).strip().lower()
    if explicit_layer:
        aliases = {
            "ground": "ground",
            "surface": "ground",
            "地面": "ground",
            "elevated": "elevated",
            "viaduct": "elevated",
            "高架": "elevated",
            "underground": "underground",
            "tunnel": "underground",
            "地下": "underground",
        }
        return aliases.get(explicit_layer, explicit_layer)

    elevation = _numeric(
        properties.get("elevation")
        if properties.get("elevation") is not None
        else properties.get("height")
    )
    if elevation is None:
        return None
    if elevation > 3:
        return "elevated"
    if elevation < -3:
        return "underground"
    return "ground"


def _is_intersection(properties: Dict[str, Any]) -> bool:
    value = properties.get("is_intersection", False)
    return value is True or str(value).strip().lower() in {"1", "true", "yes"}


def _issue(
    issue_type: str,
    severity: str,
    message: str,
    node_ids: Optional[Iterable[str]] = None,
    relationship_id: Optional[str] = None,
    suggestion: str = "",
) -> Dict[str, Any]:
    return {
        "type": issue_type,
        "severity": severity,
        "message": message,
        "nodeIds": list(node_ids or []),
        "relationshipId": relationship_id,
        "suggestion": suggestion,
    }


def identify_pseudo_nodes(
    nodes: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    degrees: Dict[str, int] = defaultdict(int)
    node_lookup = {_node_id(node): node for node in nodes}

    for relationship in relationships:
        if relationship.get("type") not in TOPOLOGY_RELATIONSHIPS:
            continue
        source = str(relationship.get("source", ""))
        target = str(relationship.get("target", ""))
        degrees[source] += 1
        degrees[target] += 1

    issues = []
    for node_id, node in node_lookup.items():
        properties = _properties(node)
        if degrees[node_id] != 2 or _is_intersection(properties):
            continue
        issues.append(
            _issue(
                "PSEUDO_NODE",
                "medium",
                "节点度为2且未标记为交叉口，可判定为伪节点。",
                [node_id],
                suggestion="合并相邻路段或将节点标记为真实交叉口。",
            )
        )
    return issues


def detect_dead_ends(
    relationships: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    degrees: Dict[str, int] = defaultdict(int)
    for relationship in relationships:
        if relationship.get("type") not in TOPOLOGY_RELATIONSHIPS:
            continue
        source = str(relationship.get("source", ""))
        target = str(relationship.get("target", ""))
        degrees[source] += 1
        degrees[target] += 1

    issues = []
    for relationship in relationships:
        if relationship.get("type") not in TOPOLOGY_RELATIONSHIPS:
            continue
        source = str(relationship.get("source", ""))
        target = str(relationship.get("target", ""))
        if degrees[source] > 1 and degrees[target] > 1:
            continue
        issues.append(
            _issue(
                "DEAD_END",
                "high",
                "关系边存在仅一端具有连通度的端点，疑似断头路。",
                [source, target],
                str(relationship.get("id", "")),
                suggestion="检查缺失线段并补齐道路连通关系。",
            )
        )
    return issues


def validate_multilayer_network(
    nodes: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    node_lookup = {_node_id(node): node for node in nodes}
    issues = []

    for relationship in relationships:
        source_id = str(relationship.get("source", ""))
        target_id = str(relationship.get("target", ""))
        source = node_lookup.get(source_id)
        target = node_lookup.get(target_id)
        if source is None or target is None:
            continue

        source_layer = _layer_from(_properties(source))
        target_layer = _layer_from(_properties(target))
        if (
            source_layer is None
            or target_layer is None
            or source_layer == target_layer
        ):
            continue

        relationship_type = str(relationship.get("type", "")).upper()
        if relationship_type in LAYER_CONNECTOR_TYPES:
            continue

        issues.append(
            _issue(
                "CROSS_LAYER_CONNECTION",
                "high",
                "检测到不同高程层之间的直接连接，缺少连接器语义。",
                [source_id, target_id],
                str(relationship.get("id", "")),
                suggestion="补充匝道、互通或跨层连接节点。",
            )
        )
    return issues


def validate_seamless_connections(
    nodes: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
    tolerance: float = 1.0,
) -> List[Dict[str, Any]]:
    node_lookup = {_node_id(node): node for node in nodes}
    issues = []

    for relationship in relationships:
        properties = relationship.get("properties", {})
        source_id = str(relationship.get("source", ""))
        target_id = str(relationship.get("target", ""))
        source_node = node_lookup.get(source_id)
        target_node = node_lookup.get(target_id)
        if source_node is None or target_node is None:
            continue

        source_node_coordinate = _coordinate_from(_properties(source_node))
        target_node_coordinate = _coordinate_from(_properties(target_node))
        edge_source_coordinate = _coordinate_from(
            {
                "x": properties.get("source_x"),
                "y": properties.get("source_y"),
                "lon": properties.get("source_lon"),
                "lat": properties.get("source_lat"),
            }
        )
        edge_target_coordinate = _coordinate_from(
            {
                "x": properties.get("target_x"),
                "y": properties.get("target_y"),
                "lon": properties.get("target_lon"),
                "lat": properties.get("target_lat"),
            }
        )

        endpoint_checks = [
            (source_node_coordinate, edge_source_coordinate),
            (target_node_coordinate, edge_target_coordinate),
        ]
        max_deviation = 0.0
        for node_coordinate, edge_coordinate in endpoint_checks:
            if node_coordinate is None or edge_coordinate is None:
                continue
            max_deviation = max(
                max_deviation,
                hypot(
                    node_coordinate[0] - edge_coordinate[0],
                    node_coordinate[1] - edge_coordinate[1],
                ),
            )

        if max_deviation <= tolerance:
            continue
        issues.append(
            _issue(
                "SEAM_GAP",
                "medium",
                "相邻路段端点坐标偏差超过阈值 {0}。".format(tolerance),
                [source_id, target_id],
                str(relationship.get("id", "")),
                suggestion="吸附端点坐标或拆分错误拓扑连接。",
            )
        )
        issues[-1]["deviation"] = round(max_deviation, 4)
    return issues


def calculate_topology_score(issues: List[Dict[str, Any]]) -> float:
    weights = {
        "PSEUDO_NODE": 0.5,
        "DEAD_END": 3.0,
        "CROSS_LAYER_CONNECTION": 8.0,
        "SEAM_GAP": 5.0,
    }
    deduction = sum(
        weights.get(str(issue.get("type")), 1.0)
        for issue in issues
    )
    return round(max(0.0, 100.0 - deduction), 2)


def check_topology(
    nodes: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
    coordinate_tolerance: float = 1.0,
) -> Dict[str, Any]:
    issues = []
    issues.extend(identify_pseudo_nodes(nodes, relationships))
    issues.extend(detect_dead_ends(relationships))
    issues.extend(validate_multilayer_network(nodes, relationships))
    issues.extend(
        validate_seamless_connections(
            nodes,
            relationships,
            coordinate_tolerance,
        )
    )

    issue_counts: Dict[str, int] = defaultdict(int)
    suggestions = []
    for issue in issues:
        issue_counts[issue["type"]] += 1
        if issue["suggestion"] and issue["suggestion"] not in suggestions:
            suggestions.append(issue["suggestion"])

    return {
        "score": calculate_topology_score(issues),
        "nodeCount": len(nodes),
        "relationshipCount": len(relationships),
        "summary": dict(issue_counts),
        "issues": issues,
        "suggestions": suggestions,
    }
