# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 图谱状态检查
# 本文件为平台数据运维代码，受软件著作权保护

import json
import sys
from pathlib import Path

from neo4j import GraphDatabase, READ_ACCESS


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from config import (  # noqa: E402
    NEO4J_DATABASE,
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USER,
)


def fetch_status(driver) -> dict:
    with driver.session(
        database=NEO4J_DATABASE,
        default_access_mode=READ_ACCESS,
    ) as session:
        version = session.run(
            """
            CALL dbms.components()
            YIELD versions
            RETURN versions[0] AS version
            """
        ).single()["version"]
        label_counts = {
            record["label"]: record["count"]
            for record in session.run(
                """
                MATCH (node)
                UNWIND labels(node) AS label
                RETURN label, count(*) AS count
                ORDER BY label
                """
            )
        }
        relationship_counts = {
            record["type"]: record["count"]
            for record in session.run(
                """
                MATCH ()-[relationship]->()
                RETURN type(relationship) AS type, count(*) AS count
                ORDER BY type
                """
            )
        }
        knowledge = session.run(
            """
            MATCH (knowledge:KnowledgePoint)
            RETURN
              count(*) AS total,
              count(
                CASE
                  WHEN knowledge.description IS NOT NULL
                   AND knowledge.difficulty IS NOT NULL
                   AND knowledge.importance IS NOT NULL
                  THEN 1
                END
              ) AS filled
            """
        ).single()
        return {
            "uri": NEO4J_URI,
            "database": NEO4J_DATABASE,
            "version": version,
            "nodeCount": sum(label_counts.values()),
            "relationshipCount": sum(relationship_counts.values()),
            "labelCounts": label_counts,
            "relationshipCounts": relationship_counts,
            "knowledgePointCount": knowledge["total"],
            "filledKnowledgePointCount": knowledge["filled"],
        }


def main() -> None:
    if not NEO4J_PASSWORD:
        raise RuntimeError("NEO4J_PASSWORD 未配置")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )
    try:
        driver.verify_connectivity()
        status = fetch_status(driver)
    finally:
        driver.close()

    print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
