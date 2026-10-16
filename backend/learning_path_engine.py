# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 后端服务
# 本文件为平台核心业务代码，受软件著作权保护

from collections import defaultdict, deque
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from neo4j import READ_ACCESS


DIFFICULTY_ORDER = {
    "入门": 1,
    "基础": 1,
    "简单": 2,
    "中等": 3,
    "进阶": 4,
    "困难": 5,
    "高级": 5,
    "高阶": 5,
    "专家": 6,
}

DIFFICULTY_ALIASES = {
    "beginner": "入门",
    "easy": "基础",
    "medium": "中等",
    "intermediate": "进阶",
    "hard": "困难",
    "advanced": "高级",
}


def difficulty_rank(value: Any) -> int:
    normalized = DIFFICULTY_ALIASES.get(
        str(value or "").strip().lower(),
        str(value or "").strip(),
    )
    return DIFFICULTY_ORDER.get(normalized, 3)


class LearningPathEngine:
    def __init__(
        self,
        nodes: Iterable[Dict[str, Any]],
        relationships: Iterable[Dict[str, Any]],
        max_depth: int = 8,
    ) -> None:
        self.max_depth = max(1, int(max_depth))
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.prerequisites: Dict[str, List[str]] = defaultdict(list)
        self.successors: Dict[str, List[str]] = defaultdict(list)

        for node in nodes:
            node_id = self._node_id(node)
            if node_id:
                self.nodes[node_id] = node

        for relationship in relationships:
            if relationship.get("type") != "PREREQUISITE_OF":
                continue
            source = str(relationship.get("source", ""))
            target = str(relationship.get("target", ""))
            if not source or not target:
                continue
            self.prerequisites[target].append(source)
            self.successors[source].append(target)

    @staticmethod
    def _node_id(node: Dict[str, Any]) -> str:
        if node.get("id") is not None:
            return str(node["id"])
        properties = node.get("properties", {})
        return str(properties.get("kp_id", ""))

    @staticmethod
    def _properties(node: Dict[str, Any]) -> Dict[str, Any]:
        properties = node.get("properties", node)
        return properties if isinstance(properties, dict) else {}

    def node(self, knowledge_point_id: str) -> Optional[Dict[str, Any]]:
        return self.nodes.get(str(knowledge_point_id))

    def prerequisite_chain(
        self,
        knowledge_point_id: str,
        max_depth: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        root = str(knowledge_point_id)
        depth_limit = min(
            self.max_depth,
            int(max_depth) if max_depth is not None else self.max_depth,
        )
        visited: Set[str] = set()
        queue = deque((predecessor, 1) for predecessor in self.prerequisites[root])
        collected: List[Tuple[int, str]] = []

        while queue:
            node_id, depth = queue.popleft()
            if node_id in visited or depth > depth_limit:
                continue
            visited.add(node_id)
            collected.append((depth, node_id))
            for predecessor in self.prerequisites[node_id]:
                queue.append((predecessor, depth + 1))

        collected.sort(
            key=lambda item: (
                -item[0],
                difficulty_rank(self._properties(self.nodes[item[1]]).get("difficulty"))
                if item[1] in self.nodes
                else 3,
            )
        )
        return [
            self._path_item(node_id, "prerequisite", depth)
            for depth, node_id in collected
        ]

    def build_learning_path(
        self,
        target_knowledge_point_id: str,
        include_successors: int = 2,
    ) -> List[Dict[str, Any]]:
        target_id = str(target_knowledge_point_id)
        path = self.prerequisite_chain(target_id, self.max_depth)
        if target_id in self.nodes:
            path.append(self._path_item(target_id, "target", 0))

        successors = sorted(
            self.successors[target_id],
            key=lambda node_id: (
                difficulty_rank(
                    self._properties(self.nodes[node_id]).get("difficulty")
                )
                if node_id in self.nodes
                else 3,
                self._properties(self.nodes[node_id]).get("sort_order", 9999)
                if node_id in self.nodes
                else 9999,
            ),
        )
        for node_id in successors[: max(0, int(include_successors))]:
            path.append(self._path_item(node_id, "successor", 1))
        return path

    def recommend(
        self,
        knowledge_point_id: str,
    ) -> Dict[str, Any]:
        target_id = str(knowledge_point_id)
        prerequisite_items = self.prerequisite_chain(target_id)
        successor_items = [
            self._path_item(node_id, "successor", 1)
            for node_id in self.successors[target_id]
        ]
        successor_items.sort(
            key=lambda item: (
                item["difficultyRank"],
                item["sortOrder"],
            )
        )
        return {
            "knowledgePoint": self._path_item(target_id, "current", 0),
            "prerequisites": prerequisite_items,
            "successors": successor_items,
            "recommendedPath": self.build_learning_path(target_id),
        }

    def filter_by_difficulty(
        self,
        difficulty: str,
        module_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        expected_rank = difficulty_rank(difficulty)
        result = []
        for node_id, node in self.nodes.items():
            properties = self._properties(node)
            if module_id and str(properties.get("module_id", "")) != str(module_id):
                continue
            if difficulty_rank(properties.get("difficulty")) != expected_rank:
                continue
            result.append(self._path_item(node_id, "knowledge", 0))
        result.sort(key=lambda item: (item["sortOrder"], item["name"]))
        return result

    def _path_item(
        self,
        node_id: str,
        role: str,
        depth: int,
    ) -> Dict[str, Any]:
        node = self.nodes.get(str(node_id), {})
        properties = self._properties(node)
        return {
            "id": str(node_id),
            "name": properties.get("name", "未命名知识点"),
            "description": properties.get("description"),
            "difficulty": properties.get("difficulty", "未标注"),
            "difficultyRank": difficulty_rank(properties.get("difficulty")),
            "importance": properties.get("importance"),
            "moduleId": properties.get("module_id"),
            "sortOrder": properties.get("sort_order", 9999),
            "role": role,
            "depth": int(depth),
        }


def load_learning_graph(
    driver,
    database: str,
    max_depth: int = 8,
) -> LearningPathEngine:
    with driver.session(
        database=database,
        default_access_mode=READ_ACCESS,
    ) as session:
        node_records = list(
            session.run(
                """
                MATCH (knowledge:KnowledgePoint)
                OPTIONAL MATCH (knowledge)-[:BELONGS_TO]->(module:Module)
                RETURN knowledge, module.module_id AS module_id
                """,
                timeout=10.0,
            )
        )
        relationship_records = list(
            session.run(
                """
                MATCH (source:KnowledgePoint)-[relationship:PREREQUISITE_OF]->
                      (target:KnowledgePoint)
                RETURN source.kp_id AS source, target.kp_id AS target
                """,
                timeout=10.0,
            )
        )

    nodes = []
    for record in node_records:
        knowledge = record["knowledge"]
        properties = dict(knowledge)
        if record["module_id"]:
            properties["module_id"] = record["module_id"]
        nodes.append(
            {
                "id": str(properties.get("kp_id", knowledge.element_id)),
                "labels": list(knowledge.labels),
                "properties": properties,
            }
        )

    relationships = [
        {
            "type": "PREREQUISITE_OF",
            "source": record["source"],
            "target": record["target"],
        }
        for record in relationship_records
    ]
    return LearningPathEngine(nodes, relationships, max_depth=max_depth)

