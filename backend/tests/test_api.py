# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import deepseek_service
import main


def test_health(neo4j_client):
    response = neo4j_client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_directory_contains_frozen_graph(neo4j_client):
    response = neo4j_client.get("/api/directory")
    assert response.status_code == 200

    modules = response.json()["data"]["modules"]
    knowledge_point_count = sum(
        len(module["knowledgePoints"]) for module in modules
    )
    assert len(modules) == 9
    assert knowledge_point_count == 344


def test_module_graph(neo4j_client):
    response = neo4j_client.get("/api/modules/M1/graph")
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["summary"]["knowledgePointCount"] == 38
    assert len(data["nodes"]) == 39
    assert len(data["links"]) == 56


def test_course_graph_includes_every_module_and_knowledge_point(neo4j_client):
    response = neo4j_client.get("/api/graph/all")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["summary"]["moduleCount"] == 9
    assert data["summary"]["knowledgePointCount"] == 344
    ids = {node["id"] for node in data["nodes"]}
    assert len(ids) == 353
    assert all(link["source"] in ids and link["target"] in ids for link in data["links"])
    assert any(link["source"].split("-")[0] != link["target"].split("-")[0]
               for link in data["links"] if link["type"] == "RELATED_TO")


def test_course_graph_keeps_isolated_nodes_and_cross_module_links(client, monkeypatch):
    class Node(dict):
        def __init__(self, business_id, label, **properties):
            super().__init__(properties)
            self["module_id" if label == "Module" else "kp_id"] = business_id
            self.labels = {label}
            self.element_id = business_id

    class Relationship(dict):
        element_id = "cross-module"
        type = "RELATED_TO"

    a = Node("M1-001", "KnowledgePoint", name="基础知识")
    b = Node("M2-001", "KnowledgePoint", name="关联知识")
    isolated = Node("M9-001", "KnowledgePoint", name="独立知识")
    relationship = Relationship()
    relationship.start_node, relationship.end_node = a, b
    records = [
        {"source": a, "relationship": relationship, "target": b},
        {"source": b, "relationship": None, "target": None},
        {"source": isolated, "relationship": None, "target": None},
        {"source": Node("M1", "Module", name="基础理论"), "relationship": None, "target": None},
    ]
    monkeypatch.setattr(main, "_read_query", lambda *args: records)
    response = client.get("/api/graph/all")
    assert response.status_code == 200
    data = response.json()["data"]
    assert {node["id"] for node in data["nodes"]} == {"M1", "M1-001", "M2-001", "M9-001"}
    assert data["summary"] == {"moduleCount": 1, "knowledgePointCount": 3, "relationCount": 1}
    assert data["links"][0]["source"] == "M1-001"
    assert data["links"][0]["target"] == "M2-001"


def test_knowledge_point_detail(neo4j_client):
    response = neo4j_client.get("/api/knowledge-points/M1-001")
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["node"]["id"] == "M1-001"
    assert data["module"]["id"] == "M1"
    assert data["materials"] == {"videos": [], "slides": []}


def test_missing_knowledge_point(neo4j_client):
    response = neo4j_client.get("/api/knowledge-points/UNKNOWN-ID")
    assert response.status_code == 404


def test_search(neo4j_client):
    response = neo4j_client.get("/api/search", params={"keyword": "GIS"})
    assert response.status_code == 200
    assert len(response.json()["data"]["results"]) > 0


def test_learning_path_endpoint(neo4j_client):
    response = neo4j_client.get(
        "/api/knowledge-points/M1-001/learning-path"
    )
    assert response.status_code == 200
    assert response.json()["data"]["knowledgePointId"] == "M1-001"


def test_module_difficulty_filter(neo4j_client):
    response = neo4j_client.get(
        "/api/modules/M1/knowledge-points",
        params={"difficulty": "入门"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["difficulty"] == "入门"


def test_topology_check_endpoint(neo4j_client):
    response = neo4j_client.post(
        "/api/topology/check",
        json={"coordinate_tolerance": 1.0},
    )
    assert response.status_code == 200
    payload = response.json()["data"]
    assert 0 <= payload["score"] <= 100
    assert payload["nodeCount"] > 0


def test_chat_status_without_key(client, monkeypatch):
    monkeypatch.setattr(deepseek_service, "DEEPSEEK_API_KEY", "")
    response = client.get("/api/chat/status")
    assert response.status_code == 200
    assert response.json()["data"]["configured"] is False


def test_chat_without_key_returns_503(client, monkeypatch):
    monkeypatch.setattr(deepseek_service, "DEEPSEEK_API_KEY", "")
    response = client.post(
        "/api/chat",
        json={
            "question": "什么是GIS？",
            "module_id": "M1",
            "knowledge_point_id": "M1-001",
        },
    )
    assert response.status_code == 503


def test_chat_uses_graph_context(client, monkeypatch):
    captured = {}

    def fake_answer(question, graph_context):
        captured["question"] = question
        captured["context"] = graph_context
        return {
            "answer": "这是模拟回答。",
            "scene": "concept_explanation",
            "references": [
                {
                    "id": "M1-001",
                    "name": "GIS交通路网的专业定义",
                    "type": "KnowledgePoint",
                    "moduleId": "M1",
                }
            ],
        }

    monkeypatch.setattr(deepseek_service, "DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(
        deepseek_service,
        "teaching_qa",
        fake_answer,
    )
    monkeypatch.setattr(
        main,
        "_build_chat_context",
        lambda driver, query: {
            "modules": [],
            "selectedModule": None,
            "selectedKnowledgePoint": {"id": "M1-001"},
            "relatedKnowledgePoints": [],
            "prerequisiteChain": [],
            "learningPath": [],
            "searchMatches": [
                {
                    "id": "M1-001",
                    "name": "GIS交通路网的专业定义",
                    "type": "KnowledgePoint",
                    "moduleId": "M1",
                }
            ],
        },
    )

    response = client.post(
        "/api/chat",
        json={
            "question": "什么是交通路网数据模型？",
            "module_id": "M1",
            "knowledge_point_id": "M1-001",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "这是模拟回答。"
    assert payload["references"]
    assert captured["question"] == "什么是交通路网数据模型？"
    assert captured["context"]["selectedKnowledgePoint"]["id"] == "M1-001"


def test_chat_upstream_error_returns_502(client, monkeypatch):
    def fail_answer(question, graph_context):
        raise deepseek_service.QaEngineRequestError("模拟上游失败")

    monkeypatch.setattr(deepseek_service, "DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(
        deepseek_service,
        "teaching_qa",
        fail_answer,
    )
    monkeypatch.setattr(
        main,
        "_build_chat_context",
        lambda driver, query: {
            "modules": [],
            "selectedModule": None,
            "selectedKnowledgePoint": None,
            "relatedKnowledgePoints": [],
            "prerequisiteChain": [],
            "learningPath": [],
            "searchMatches": [],
        },
    )

    response = client.post(
        "/api/chat",
        json={"question": "测试问题"},
    )
    assert response.status_code == 502


def test_chat_rate_limit_returns_429(client, monkeypatch):
    monkeypatch.setattr(deepseek_service, "DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(
        deepseek_service,
        "teaching_qa",
        lambda question, graph_context: {
            "answer": "模拟回答",
            "scene": "concept_explanation",
            "references": [],
        },
    )
    monkeypatch.setattr(
        main,
        "_build_chat_context",
        lambda driver, query: {
            "modules": [],
            "selectedModule": None,
            "selectedKnowledgePoint": None,
            "relatedKnowledgePoints": [],
            "prerequisiteChain": [],
            "learningPath": [],
            "searchMatches": [],
        },
    )
    headers = {"X-Real-IP": "203.0.113.10"}

    for _ in range(5):
        response = client.post(
            "/api/chat",
            json={"question": "测试限流"},
            headers=headers,
        )
        assert response.status_code == 200

    response = client.post(
        "/api/chat",
        json={"question": "测试限流"},
        headers=headers,
    )
    assert response.status_code == 429
