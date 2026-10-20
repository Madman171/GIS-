"""Build a reviewable curation draft from the current graph snapshot.

The draft is intentionally non-destructive: it suggests missing subcategories
and records relationship proposals, but it never edits graph-snapshot.json.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = ROOT / "data" / "graph-snapshot.json"
DEFAULT_OUTPUT = ROOT / "data" / "graph-curation.json"


TAXONOMY: dict[str, dict[str, Any]] = {
    "M1": {
        "default": "基础概念",
        "rules": [
            ("拓扑规则", ("拓扑", "连通", "节点重合", "悬挂节点", "断头路", "伪节点", "交叉口", "匝道", "桥梁", "隧道", "单向", "双向")),
            ("图论与网络模型", ("图论", "邻接矩阵", "关联矩阵", "度值", "有向", "无向", "加权", "Node-Edge")),
            ("数据模型", ("矢量", "栅格", "数据模型", "空间数据")),
        ],
    },
    "M2": {
        "default": "线性参考",
        "rules": [
            ("事件数据模型", ("事件", "事故", "拥堵", "施工", "管制")),
            ("动态分段", ("动态分段", "分段", "里程", "定位")),
            ("线性参考", ("线性参考", "路线", "路段", "桩号")),
        ],
    },
    "M3": {
        "default": "路网数据体系",
        "rules": [
            ("数据质量与清洗", ("质量", "清洗", "纠错", "冗余", "异常", "缺失", "一致性")),
            ("数据格式与转换", ("格式", "转换", "Shapefile", "GeoJSON", "FileGDB", "GPX", "坐标系")),
            ("数据源与采集", ("数据源", "OSM", "高德", "百度", "采集", "众源")),
            ("属性与编码规范", ("属性", "字段", "编码", "道路等级", "路面", "限速")),
        ],
    },
    "M4": {
        "default": "空间分析算法",
        "rules": [
            ("路径与可达性", ("最短路径", "最优路径", "可达", "路径规划", "服务区")),
            ("网络指标", ("中心性", "介数", "度中心性", "连通性指标", "网络密度")),
            ("流量与分配", ("交通分配", "流量", "OD", "阻抗", "拥堵")),
            ("算法基础", ("算法", "Dijkstra", "A*", "弗洛伊德", "模型")),
        ],
    },
    "M5": {
        "default": "时空数据模型",
        "rules": [
            ("动态路网", ("动态路网", "实时", "状态更新", "动态")),
            ("时间建模", ("时间", "时序", "时间片", "时间窗", "持续")),
            ("时空分析", ("时空", "轨迹", "演化", "预测")),
        ],
    },
    "M6": {
        "default": "多模态网络",
        "rules": [
            ("换乘与枢纽", ("换乘", "枢纽", "接驳", "步行")),
            ("交通方式建模", ("公交", "地铁", "轨道", "步行", "骑行", "汽车", "多模式")),
            ("综合交通分析", ("综合交通", "联运", "多模态", "出行链")),
        ],
    },
    "M7": {
        "default": "GIS平台实操",
        "rules": [
            ("数据库与存储", ("PostGIS", "数据库", "存储", "索引", "SQL")),
            ("桌面GIS操作", ("ArcGIS", "QGIS", "SuperMap", "MapGIS", "图层", "插件")),
            ("网络分析工具", ("最短路径", "服务区", "可达性", "OD", "pgRouting", "NetworkX")),
            ("WebGIS与发布", ("WebGIS", "渲染", "切片", "发布", "前端", "移动端")),
            ("自动化与脚本", ("脚本", "自动化", "GeoPandas", "PyQGIS", "批量")),
        ],
    },
    "M8": {
        "default": "知识图谱方法",
        "rules": [
            ("本体与模式设计", ("本体", "Ontology", "实体类型", "关系类型", "模式层", "Schema")),
            ("知识抽取与融合", ("抽取", "实体对齐", "消歧", "多源", "融合", "冲突")),
            ("图数据库与查询", ("Neo4j", "图数据库", "Cypher", "存储", "查询")),
            ("推理与可视化", ("推理", "嵌入", "TransE", "RotatE", "可视化")),
            ("动态与大模型融合", ("动态知识图谱", "实时更新", "大模型", "融合应用")),
        ],
    },
}


def node_business_id(node: dict[str, Any]) -> str:
    properties = node.get("properties", {})
    label = str(node.get("primaryLabel", ""))
    key = {
        "Module": "module_id",
        "KnowledgePoint": "kp_id",
        "Tool": "tool_id",
        "Media": "media_id",
    }.get(label)
    return str(node.get("businessId") or (properties.get(key) if key else "") or node.get("elementId", ""))


def suggest(module_id: str, text: str) -> tuple[str, str, list[str]]:
    taxonomy = TAXONOMY.get(module_id, {"default": "待定义", "rules": []})
    matches: list[tuple[int, int, str, list[str]]] = []
    for order, (category, keywords) in enumerate(taxonomy["rules"]):
        hit = [keyword for keyword in keywords if keyword.lower() in text.lower()]
        if hit:
            matches.append((len(hit), -order, category, hit))
    if not matches:
        return taxonomy["default"], "low", []
    matches.sort(reverse=True)
    score, _, category, hit = matches[0]
    confidence = "high" if score >= 2 else "medium"
    return category, confidence, hit


def build_draft(snapshot: dict[str, Any]) -> dict[str, Any]:
    modules = {
        node_business_id(node): node.get("properties", {}).get("name", "")
        for node in snapshot.get("nodes", [])
        if node.get("primaryLabel") == "Module"
    }
    proposals = []
    for node in snapshot.get("nodes", []):
        if node.get("primaryLabel") != "KnowledgePoint":
            continue
        properties = node.get("properties", {})
        if properties.get("subcategory"):
            continue
        kp_id = node_business_id(node)
        module_id = kp_id.split("-", 1)[0]
        text = f"{properties.get('name', '')} {properties.get('description', '')}"
        category, confidence, keywords = suggest(module_id, text)
        proposals.append(
            {
                "kp_id": kp_id,
                "name": properties.get("name", ""),
                "module_id": module_id,
                "module_name": modules.get(module_id, ""),
                "current_subcategory": "",
                "suggested_subcategory": category,
                "confidence": confidence,
                "matched_keywords": keywords,
                "review_status": "pending",
            }
        )

    return {
        "metadata": {
            "source": "data/graph-snapshot.json",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "purpose": "审阅后再应用，不直接修改图谱快照",
            "proposal_count": len(proposals),
            "confidence_counts": dict(Counter(item["confidence"] for item in proposals)),
        },
        "subcategory_proposals": proposals,
        "relationship_proposals": [
            {
                "id": "rel-001",
                "status": "pending",
                "operation": "add",
                "type": "IMPLEMENTED_IN",
                "source": "M7-020",
                "target": "T003",
                "reason": "PostGIS空间数据库路网数据表创建应明确关联PostGIS工具。",
            },
            {
                "id": "rel-002",
                "status": "pending",
                "operation": "replace_cycle",
                "remove": [
                    {"type": "PREREQUISITE_OF", "source": "M7-020", "target": "M8-021"},
                    {"type": "PREREQUISITE_OF", "source": "M8-021", "target": "M7-020"},
                ],
                "add": [
                    {"type": "RELATED_TO", "source": "M7-020", "target": "M8-021"}
                ],
                "reason": "两个数据库实践主题当前互为前置，形成学习路径循环；先改为普通关联，待教学顺序确认后再决定是否保留单向前置。",
            },
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="生成图谱分类和关系调整草案")
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    draft = build_draft(snapshot)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(draft, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "Generated {0} subcategory proposals and {1} relationship proposals: {2}".format(
            draft["metadata"]["proposal_count"],
            len(draft["relationship_proposals"]),
            args.output,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
