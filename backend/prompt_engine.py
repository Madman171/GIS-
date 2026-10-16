# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 后端服务
# 本文件为平台核心业务代码，受软件著作权保护

import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple


SCENE_KEYWORDS = {
    "learning_path": {
        "学习",
        "路径",
        "先学",
        "顺序",
        "前置",
        "入门到",
    },
    "topology_issue": {
        "拓扑",
        "断头",
        "伪节点",
        "高程",
        "高架",
        "地下",
        "衔接",
        "连通",
    },
    "application_scenario": {
        "应用",
        "场景",
        "案例",
        "工程",
        "实际",
        "实践",
    },
}

SCENE_RULES = {
    "concept_explanation": (
        "你正在解释GIS交通路网教学知识图谱中的概念。"
        "先给出明确定义，再说明关键构成、适用条件和与相关知识点的关系。"
    ),
    "learning_path": (
        "你正在生成学习路径。必须按照前置知识、基础知识、进阶知识的顺序组织，"
        "不得跳过图谱中不存在的前置知识点。"
    ),
    "topology_issue": (
        "你正在分析交通路网拓扑问题。区分伪节点、断头路、跨层错误连接和"
        "线段衔接偏差，并给出可执行的检查或清理建议。"
    ),
    "application_scenario": (
        "你正在讲解工程应用场景。说明该知识点在道路建模、导航、交通分析或"
        "GIS平台中的实际用途，不得虚构不存在的项目案例。"
    ),
}


@dataclass
class PromptPackage:
    scene: str
    system_prompt: str
    user_prompt: str
    context_nodes: List[Dict[str, Any]]


def classify_scene(question: str) -> str:
    normalized = str(question or "").strip()
    scores = {
        scene: sum(1 for keyword in keywords if keyword in normalized)
        for scene, keywords in SCENE_KEYWORDS.items()
    }
    best_scene = max(scores, key=scores.get)
    return best_scene if scores[best_scene] > 0 else "concept_explanation"


def _context_weight(item: Dict[str, Any], selected_id: str) -> Tuple[int, int, int]:
    item_id = str(item.get("id", ""))
    role = str(item.get("role", ""))
    return (
        0 if item_id == selected_id and selected_id else 1,
        0 if role in {"current", "target", "prerequisite"} else 1,
        int(item.get("depth", 99) or 99),
    )


def assemble_context(
    graph_context: Dict[str, Any],
    max_references: int = 6,
) -> List[Dict[str, Any]]:
    selected = graph_context.get("selectedKnowledgePoint") or {}
    selected_id = str(selected.get("id", ""))
    candidates: List[Dict[str, Any]] = []

    if selected:
        candidates.append({**selected, "role": "current", "depth": 0})

    for item in graph_context.get("prerequisiteChain", []):
        candidates.append({**item, "role": "prerequisite"})

    for item in graph_context.get("relatedKnowledgePoints", []):
        candidates.append({**item, "role": "related"})

    for item in graph_context.get("searchMatches", []):
        candidates.append({**item, "role": "search"})

    selected_module = graph_context.get("selectedModule")
    if selected_module:
        candidates.append({**selected_module, "role": "module"})

    deduplicated = {}
    for item in candidates:
        item_id = str(item.get("id", ""))
        if not item_id:
            continue
        current = deduplicated.get(item_id)
        if current is None or _context_weight(item, selected_id) < _context_weight(
            current,
            selected_id,
        ):
            deduplicated[item_id] = item

    ordered = sorted(
        deduplicated.values(),
        key=lambda item: _context_weight(item, selected_id),
    )
    return ordered[: max(1, int(max_references))]


def build_prompt(
    question: str,
    graph_context: Dict[str, Any],
    max_references: int = 6,
) -> PromptPackage:
    scene = classify_scene(question)
    context_nodes = assemble_context(graph_context, max_references)
    context_json = json.dumps(
        {
            "scene": scene,
            "knowledgeContext": context_nodes,
            "moduleContext": graph_context.get("selectedModule"),
            "availableModules": graph_context.get("modules", []),
            "prerequisiteChain": graph_context.get("prerequisiteChain", []),
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )

    system_prompt = (
        "你是GIS交通路网教学知识图谱平台的自主教学问答引擎。"
        "只能依据给定的教学知识图谱上下文回答，不得编造不存在的知识点、关系、"
        "项目案例或数据。回答必须限定在GIS、交通路网、空间分析和相关教学范围。"
        "回答中优先引用知识点名称，并在末尾用“知识来源：”列出实际使用的知识点。"
        "如果上下文不足，明确说明知识图谱中没有足够资料。"
        "不得输出Cypher，不得声称执行过数据库写操作。"
        + SCENE_RULES[scene]
    )
    user_prompt = (
        "教学知识图谱上下文：\n{0}\n\n"
        "用户问题：{1}"
    ).format(context_json, question)
    return PromptPackage(
        scene=scene,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        context_nodes=context_nodes,
    )


def validate_answer(
    answer: str,
    prompt_package: PromptPackage,
) -> str:
    normalized = str(answer or "").strip()
    if not normalized:
        raise ValueError("教学问答引擎返回了空回答")

    forbidden_fragments = (
        "sk-",
        "API Key",
        "数据库密码",
        "密码是",
    )
    for fragment in forbidden_fragments:
        normalized = normalized.replace(fragment, "敏感信息已隐藏")

    unsupported_claims = (
        "我执行了数据库查询",
        "我执行了Cypher",
        "数据库中显示",
        "系统已修改数据",
    )
    for claim in unsupported_claims:
        normalized = normalized.replace(
            claim,
            "根据给定的教学知识图谱上下文",
        )

    context_names = [
        str(node.get("name", "")).strip()
        for node in prompt_package.context_nodes
        if node.get("name")
    ]
    domain_terms = (
        "GIS",
        "交通",
        "路网",
        "空间",
        "道路",
        "轨迹",
        "拓扑",
        "地图",
        "地理",
    )
    in_domain = any(
        term.lower() in normalized.lower()
        for term in domain_terms
    ) or any(
        name and name[: min(6, len(name))] in normalized
        for name in context_names
    )
    if not in_domain:
        raise ValueError("回答超出GIS交通路网教学知识图谱的领域范围")

    if not any(
        marker in normalized
        for marker in ("知识来源：", "知识来源:")
    ):
        references = context_names
        if references:
            normalized += "\n\n知识来源：" + "、".join(references[:4])
    return normalized


def matched_references(
    answer: str,
    context_nodes: Iterable[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    answer_text = str(answer or "")
    references = []
    for node in context_nodes:
        name = str(node.get("name", "")).strip()
        if not name:
            continue
        short_name = name[: min(8, len(name))]
        if name in answer_text or short_name in answer_text:
            references.append(
                {
                    "id": node.get("id"),
                    "name": name,
                    "type": node.get("type", "KnowledgePoint"),
                    "moduleId": node.get("moduleId"),
                }
            )
    if references:
        return references
    return [
        {
            "id": node.get("id"),
            "name": node.get("name", "未命名知识点"),
            "type": node.get("type", "KnowledgePoint"),
            "moduleId": node.get("moduleId"),
        }
        for node in list(context_nodes)[:3]
    ]

