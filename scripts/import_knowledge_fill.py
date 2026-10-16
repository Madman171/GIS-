# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 知识点填充导入
# 本文件为平台数据处理代码，受软件著作权保护

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple
from xml.etree import ElementTree
from zipfile import ZipFile


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = ROOT_DIR / "docs"
SNAPSHOT_PATH = DATA_DIR / "graph-snapshot.json"

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(ROOT_DIR / "scripts"))

import export_graph  # noqa: E402
import import_snapshot  # noqa: E402


EXCEL_NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "office": (
        "http://schemas.openxmlformats.org/"
        "officeDocument/2006/relationships"
    ),
    "package": (
        "http://schemas.openxmlformats.org/"
        "package/2006/relationships"
    ),
}

SHEET_MODULE_MAP = {
    "模块五·动态路网": "M5",
    "模块六·多模态网络": "M6",
    "模块七·GIS实操": "M7",
    "模块八·知识图谱": "M8",
    "模块九·应用与前沿": "M9",
}

EXPECTED_HEADERS = [
    "编号",
    "知识点名称",
    "难度",
    "重要性",
    "知识点说明",
    "关联知识",
]

ALLOWED_DIFFICULTIES = {
    "入门",
    "基础",
    "中等",
    "进阶",
    "困难",
    "高级",
    "高阶",
}

ALLOWED_IMPORTANCE = {
    "了解",
    "熟悉",
    "掌握",
    "核心",
}

PRIMARY_ID_KEYS = {
    "Module": "module_id",
    "KnowledgePoint": "kp_id",
    "Tool": "tool_id",
    "Media": "media_id",
}


def column_name(reference: str) -> str:
    match = re.match(r"([A-Z]+)", reference or "")
    return match.group(1) if match else ""


def shared_strings(archive: ZipFile) -> List[str]:
    root = ElementTree.fromstring(
        archive.read("xl/sharedStrings.xml")
    )
    values = []
    for item in root.findall("main:si", EXCEL_NS):
        values.append(
            "".join(
                node.text or ""
                for node in item.findall(".//main:t", EXCEL_NS)
            )
        )
    return values


def cell_value(cell, strings: List[str]) -> str:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "inlineStr":
        return "".join(
            node.text or ""
            for node in cell.findall(".//main:t", EXCEL_NS)
        ).strip()

    value = cell.find("main:v", EXCEL_NS)
    if value is None or value.text is None:
        return ""

    if cell_type == "s":
        index = int(value.text)
        return strings[index].strip() if index < len(strings) else ""
    return value.text.strip()


def workbook_sheets(
    workbook_path: Path,
) -> Dict[str, List[Dict[str, str]]]:
    with ZipFile(workbook_path) as archive:
        strings = shared_strings(archive)
        workbook = ElementTree.fromstring(
            archive.read("xl/workbook.xml")
        )
        relationships = ElementTree.fromstring(
            archive.read("xl/_rels/workbook.xml.rels")
        )
        relationship_targets = {
            item.attrib["Id"]: item.attrib["Target"]
            for item in relationships.findall(
                "package:Relationship",
                EXCEL_NS,
            )
        }

        result: Dict[str, List[Dict[str, str]]] = {}
        for sheet in workbook.findall(
            "main:sheets/main:sheet",
            EXCEL_NS,
        ):
            sheet_name = sheet.attrib["name"]
            relationship_id = sheet.attrib[
                "{http://schemas.openxmlformats.org/"
                "officeDocument/2006/relationships}id"
            ]
            target = relationship_targets[relationship_id]
            if not target.startswith("xl/"):
                target = "xl/" + target.lstrip("/")

            sheet_root = ElementTree.fromstring(archive.read(target))
            rows = []
            for row in sheet_root.findall(
                "main:sheetData/main:row",
                EXCEL_NS,
            ):
                values = {}
                for cell in row.findall("main:c", EXCEL_NS):
                    name = column_name(cell.attrib.get("r", ""))
                    if name:
                        values[name] = cell_value(cell, strings)
                rows.append(values)

            if rows:
                headers = [
                    rows[0].get(column, "")
                    for column in ("A", "B", "C", "D", "E", "F")
                ]
                if headers != EXPECTED_HEADERS:
                    raise ValueError(
                        "{0} 表头不匹配: {1}".format(
                            sheet_name,
                            headers,
                        )
                    )
            result[sheet_name] = rows
        return result


def load_snapshot(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def business_id(node: Dict[str, Any]) -> str:
    label = str(node.get("primaryLabel", ""))
    key = PRIMARY_ID_KEYS[label]
    value = node.get("properties", {}).get(key)
    if value is None:
        raise ValueError("节点缺少业务主键: {0}".format(label))
    return str(value)


def build_sequence_index(
    snapshot: Dict[str, Any],
) -> Tuple[Dict[int, Dict[str, Any]], Dict[str, int]]:
    modules = sorted(
        (
            node
            for node in snapshot["nodes"]
            if node["primaryLabel"] == "Module"
        ),
        key=lambda node: (
            node["properties"].get("sort_order", 9999),
            node["properties"].get("module_id", ""),
        ),
    )
    module_ids = [business_id(module) for module in modules]
    module_order = {
        module_id: index
        for index, module_id in enumerate(module_ids)
    }

    module_by_knowledge_point = {}
    for relationship in snapshot["relationships"]:
        if relationship["type"] != "BELONGS_TO":
            continue
        if relationship["targetLabel"] != "Module":
            continue
        module_by_knowledge_point[
            relationship["sourceBusinessId"]
        ] = relationship["targetBusinessId"]

    knowledge_points = [
        node
        for node in snapshot["nodes"]
        if node["primaryLabel"] == "KnowledgePoint"
    ]
    knowledge_points.sort(
        key=lambda node: (
            module_order.get(
                module_by_knowledge_point.get(business_id(node), ""),
                9999,
            ),
            node["properties"].get("sort_order", 9999),
            business_id(node),
        )
    )

    sequence_index = {}
    module_sequence = Counter()
    for sequence, node in enumerate(knowledge_points, start=1):
        module_id = module_by_knowledge_point.get(business_id(node))
        if not module_id:
            raise ValueError(
                "知识点缺少所属模块: {0}".format(business_id(node))
            )
        sequence_index[sequence] = node
        module_sequence[module_id] += 1
    return sequence_index, dict(module_sequence)


def parse_reference_numbers(value: str) -> List[int]:
    text = str(value or "")
    numbers: List[int] = []

    range_pattern = re.compile(
        r"(?<!\d)(\d{1,3})\s*[‐‑‒–—－-]\s*(\d{1,3})(?!\d)"
    )
    for match in range_pattern.finditer(text):
        start = int(match.group(1))
        end = int(match.group(2))
        if start <= end:
            numbers.extend(range(start, end + 1))
        else:
            numbers.extend(range(end, start + 1))
    text = range_pattern.sub(" ", text)

    for token in re.findall(r"(?<!\d)(\d{1,3})(?!\d)", text):
        number = int(token)
        if number > 0:
            numbers.append(number)

    return list(dict.fromkeys(numbers))


def validate_workbook_rows(
    rows_by_sheet: Dict[str, List[Dict[str, str]]],
    sequence_index: Dict[int, Dict[str, Any]],
    module_sequence: Dict[str, int],
) -> List[Dict[str, Any]]:
    records = []
    seen_numbers: Set[int] = set()

    for sheet_name, module_id in SHEET_MODULE_MAP.items():
        rows = rows_by_sheet.get(sheet_name)
        if not rows:
            raise ValueError("缺少工作表: {0}".format(sheet_name))

        sheet_records = []
        for row in rows[1:]:
            raw_number = row.get("A", "").strip()
            if not raw_number.isdigit():
                continue

            number = int(raw_number)
            if number in seen_numbers:
                raise ValueError("知识点编号重复: {0}".format(number))
            seen_numbers.add(number)

            node = sequence_index.get(number)
            if node is None:
                raise ValueError("编号无对应知识点: {0}".format(number))
            node_id = business_id(node)
            if not node_id.startswith(module_id + "-"):
                raise ValueError(
                    "编号 {0} 与工作表 {1} 不匹配".format(
                        number,
                        sheet_name,
                    )
                )

            name = row.get("B", "").strip()
            expected_name = str(node["properties"].get("name", "")).strip()
            if not name:
                raise ValueError(
                    "编号 {0} 缺少知识点名称".format(
                        number,
                    )
                )

            difficulty = row.get("C", "").strip()
            importance = row.get("D", "").strip()
            description = row.get("E", "").strip()
            related_text = row.get("F", "").strip()
            missing = [
                field
                for field, value in (
                    ("难度", difficulty),
                    ("重要性", importance),
                    ("知识点说明", description),
                )
                if not value
            ]
            if missing:
                raise ValueError(
                    "编号 {0} 缺少字段: {1}".format(
                        number,
                        "、".join(missing),
                    )
                )
            if difficulty not in ALLOWED_DIFFICULTIES:
                raise ValueError(
                    "编号 {0} 难度非法: {1}".format(
                        number,
                        difficulty,
                    )
                )
            if importance not in ALLOWED_IMPORTANCE:
                raise ValueError(
                    "编号 {0} 重要性非法: {1}".format(
                        number,
                        importance,
                    )
                )

            references = parse_reference_numbers(related_text)
            invalid_references = [
                reference
                for reference in references
                if reference not in sequence_index
            ]
            if invalid_references:
                raise ValueError(
                    "编号 {0} 关联知识越界: {1}".format(
                        number,
                        invalid_references,
                    )
                )

            sheet_records.append(
                {
                    "number": number,
                    "module_id": module_id,
                    "node_id": node_id,
                    "name": name,
                    "original_name": expected_name,
                    "name_changed": name != expected_name,
                    "difficulty": difficulty,
                    "importance": importance,
                    "description": description,
                    "related_text": related_text,
                    "references": references,
                }
            )

        expected_count = module_sequence[module_id]
        if len(sheet_records) != expected_count:
            raise ValueError(
                "{0} 行数不一致: Excel={1}, 快照={2}".format(
                    sheet_name,
                    len(sheet_records),
                    expected_count,
                )
            )
        records.extend(sheet_records)

    if len(records) != 192:
        raise ValueError(
            "填充记录应为 192 条，实际为 {0} 条".format(len(records))
        )
    return records


def iter_existing_relationships(
    snapshot: Dict[str, Any],
) -> Iterable[Tuple[str, str, str]]:
    for relationship in snapshot["relationships"]:
        yield (
            str(relationship["sourceBusinessId"]),
            str(relationship["type"]),
            str(relationship["targetBusinessId"]),
        )


def update_snapshot(
    snapshot: Dict[str, Any],
    records: List[Dict[str, Any]],
    sequence_index: Dict[int, Dict[str, Any]],
    workbook_name: str,
) -> Dict[str, Any]:
    node_lookup = {
        business_id(node): node
        for node in snapshot["nodes"]
    }

    for record in records:
        properties = node_lookup[record["node_id"]]["properties"]
        properties["name"] = record["name"]
        properties["difficulty"] = record["difficulty"]
        properties["importance"] = record["importance"]
        properties["description"] = record["description"]

    existing_signatures = set(iter_existing_relationships(snapshot))
    semantic_pairs = {
        frozenset((source, target))
        for source, relationship_type, target in existing_signatures
        if relationship_type != "BELONGS_TO"
    }
    added_links = []
    added_pairs: Set[Tuple[str, str]] = set()
    for record in records:
        source_id = record["node_id"]
        for reference in record["references"]:
            target_id = business_id(sequence_index[reference])
            if source_id == target_id:
                continue
            pair = frozenset((source_id, target_id))
            if pair in semantic_pairs:
                continue

            signature = (source_id, "RELATED_TO", target_id)
            if signature in existing_signatures:
                continue
            if (source_id, target_id) in added_pairs:
                continue

            added_pairs.add((source_id, target_id))
            added_links.append(
                {
                    "elementId": "import:RELATED_TO:{0}:{1}".format(
                        source_id,
                        target_id,
                    ),
                    "type": "RELATED_TO",
                    "sourceElementId": node_lookup[source_id][
                        "elementId"
                    ],
                    "targetElementId": node_lookup[target_id][
                        "elementId"
                    ],
                    "sourceLabel": "KnowledgePoint",
                    "targetLabel": "KnowledgePoint",
                    "sourceBusinessId": source_id,
                    "targetBusinessId": target_id,
                    "properties": {},
                }
            )
            semantic_pairs.add(pair)
            existing_signatures.add(signature)

    snapshot["relationships"].extend(added_links)
    snapshot["metadata"]["relationship_count"] = len(
        snapshot["relationships"]
    )
    snapshot["metadata"]["knowledge_fill_source"] = workbook_name
    snapshot["metadata"]["knowledge_fill_imported_at"] = (
        datetime.now(timezone.utc).isoformat()
    )
    snapshot["metadata"]["knowledge_fill_record_count"] = len(records)
    snapshot["metadata"]["knowledge_fill_added_related_count"] = len(
        added_links
    )
    return {
        "updated_nodes": len(records),
        "added_related_links": len(added_links),
    }


def write_snapshot(snapshot: Dict[str, Any], path: Path) -> None:
    path.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_generated_files(snapshot: Dict[str, Any]) -> None:
    nodes = snapshot["nodes"]
    relationships = snapshot["relationships"]
    metadata = snapshot["metadata"]

    export_graph.write_text(
        DATA_DIR / "modules.cypher",
        export_graph.build_node_cypher(nodes, "Module"),
    )
    export_graph.write_text(
        DATA_DIR / "knowledge-points.cypher",
        export_graph.build_node_cypher(nodes, "KnowledgePoint"),
    )
    export_graph.write_text(
        DATA_DIR / "tools.cypher",
        export_graph.build_node_cypher(nodes, "Tool"),
    )
    export_graph.write_text(
        DATA_DIR / "media.cypher",
        export_graph.build_node_cypher(nodes, "Media"),
    )
    export_graph.write_text(
        DATA_DIR / "relationships.cypher",
        export_graph.build_relationship_cypher(relationships),
    )
    export_graph.write_text(
        DATA_DIR / "README.md",
        export_graph.build_data_readme(metadata),
    )
    export_graph.write_text(
        DOCS_DIR / "02-database-design.md",
        export_graph.build_database_document(
            nodes,
            relationships,
            metadata,
        ),
    )


def apply_to_neo4j(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return import_snapshot.import_snapshot(
        snapshot,
        apply_changes=True,
    )


def print_summary(
    workbook_path: Path,
    records: List[Dict[str, Any]],
    result: Dict[str, Any],
    neo4j_result: Dict[str, Any] | None = None,
) -> None:
    difficulty_counts = Counter(
        record["difficulty"]
        for record in records
    )
    renamed_count = sum(
        1
        for record in records
        if record["name_changed"]
    )
    print("工作簿: {0}".format(workbook_path))
    print("填充知识点: {0}".format(len(records)))
    print(
        "难度分布: {0}".format(
            ", ".join(
                "{0}={1}".format(key, difficulty_counts[key])
                for key in sorted(difficulty_counts)
            )
        )
    )
    print("更新节点: {0}".format(result["updated_nodes"]))
    print("同步名称修订: {0}".format(renamed_count))
    print("新增 RELATED_TO 关系: {0}".format(
        result["added_related_links"]
    ))
    if neo4j_result is not None:
        print(
            "Neo4j 导入: 节点 {0}，关系 {1}".format(
                neo4j_result["nodeCount"],
                neo4j_result["relationshipCount"],
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="导入知识点填充工作簿并更新图谱快照"
    )
    parser.add_argument(
        "workbook",
        type=Path,
        help="知识点填充 .xlsx 文件路径",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="写入 graph-snapshot.json 和生成的 Cypher 文件",
    )
    parser.add_argument(
        "--apply-neo4j",
        action="store_true",
        help="同时将更新后的快照写入 Neo4j，需要 --apply",
    )
    args = parser.parse_args()

    if args.apply_neo4j and not args.apply:
        raise ValueError("--apply-neo4j 必须与 --apply 一起使用")
    if not args.workbook.is_file():
        raise FileNotFoundError(
            "工作簿不存在: {0}".format(args.workbook)
        )

    snapshot = load_snapshot(SNAPSHOT_PATH)
    sequence_index, module_sequence = build_sequence_index(snapshot)
    rows_by_sheet = workbook_sheets(args.workbook)
    records = validate_workbook_rows(
        rows_by_sheet,
        sequence_index,
        module_sequence,
    )
    result = update_snapshot(
        snapshot,
        records,
        sequence_index,
        args.workbook.name,
    )

    neo4j_result = None
    if args.apply:
        write_snapshot(snapshot, SNAPSHOT_PATH)
        write_generated_files(snapshot)
        if args.apply_neo4j:
            neo4j_result = apply_to_neo4j(snapshot)

    print_summary(
        args.workbook,
        records,
        result,
        neo4j_result,
    )
    if not args.apply:
        print("当前为校验模式；添加 --apply 后写入项目数据文件。")


if __name__ == "__main__":
    main()
