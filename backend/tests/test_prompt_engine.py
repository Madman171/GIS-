# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import prompt_engine


def context():
    return {
        "modules": [{"id": "M1", "name": "基础理论", "type": "Module"}],
        "selectedModule": {"id": "M1", "name": "基础理论", "type": "Module"},
        "selectedKnowledgePoint": {
            "id": "M1-002",
            "name": "路网拓扑",
            "type": "KnowledgePoint",
            "moduleId": "M1",
        },
        "prerequisiteChain": [
            {
                "id": "M1-001",
                "name": "道路定义",
                "type": "KnowledgePoint",
                "role": "prerequisite",
                "depth": 1,
            }
        ],
        "relatedKnowledgePoints": [],
        "searchMatches": [],
    }


def test_scene_classification():
    assert prompt_engine.classify_scene("什么是道路节点") == "concept_explanation"
    assert prompt_engine.classify_scene("推荐一条学习路径") == "learning_path"
    assert prompt_engine.classify_scene("如何检测断头路") == "topology_issue"


def test_context_priority_and_prompt():
    package = prompt_engine.build_prompt(
        "什么是道路节点",
        context(),
        max_references=6,
    )
    assert package.scene == "concept_explanation"
    assert package.context_nodes[0]["id"] == "M1-002"
    assert "知识来源：" in package.system_prompt


def test_answer_validation_adds_sources_and_hides_secrets():
    package = prompt_engine.build_prompt("什么是路网拓扑", context())
    answer = prompt_engine.validate_answer(
        "路网拓扑用于描述连接关系。API Key 不应出现。",
        package,
    )
    assert "敏感信息已隐藏" in answer
    assert "知识来源：" in answer
