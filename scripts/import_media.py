# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import quote

from neo4j import GraphDatabase, READ_ACCESS


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
MEDIA_DIR = BACKEND_DIR / "media"
MANIFEST_PATH = ROOT_DIR / "data" / "media-manifest.json"

sys.path.insert(0, str(BACKEND_DIR))

from config import (  # noqa: E402
    NEO4J_DATABASE,
    NEO4J_PASSWORD,
    NEO4J_URI,
    NEO4J_USER,
)


ALLOWED_MEDIA_TYPES = {
    "video": {".mp4", ".webm"},
    "slides": {".pdf", ".ppt", ".pptx"},
}
ALLOWED_COVER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_manifest() -> List[Dict[str, Any]]:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            "Media manifest not found: {0}".format(MANIFEST_PATH)
        )

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("media-manifest.json must contain an items array")
    return items


def safe_media_path(relative_path: str) -> Path:
    if not relative_path:
        raise ValueError("Media file path cannot be empty")

    candidate = (MEDIA_DIR / relative_path).resolve()
    media_root = MEDIA_DIR.resolve()
    try:
        candidate.relative_to(media_root)
    except ValueError as exc:
        raise ValueError(
            "Media path escapes backend/media: {0}".format(relative_path)
        ) from exc
    return candidate


def validate_item(
    item: Dict[str, Any],
    apply_changes: bool,
) -> Dict[str, Any]:
    required_fields = (
        "media_id",
        "knowledge_point_id",
        "type",
        "title",
        "file",
    )
    missing = [
        field for field in required_fields if not str(item.get(field, "")).strip()
    ]
    if missing:
        raise ValueError(
            "Media item is missing fields: {0}".format(", ".join(missing))
        )

    media_type = str(item["type"]).strip()
    if media_type not in ALLOWED_MEDIA_TYPES:
        raise ValueError(
            "Unsupported media type: {0}".format(media_type)
        )

    file_path = safe_media_path(str(item["file"]).strip())
    extension = file_path.suffix.lower()
    if extension not in ALLOWED_MEDIA_TYPES[media_type]:
        raise ValueError(
            "Extension {0} is not valid for {1}".format(
                extension,
                media_type,
            )
        )
    if apply_changes and not file_path.is_file():
        raise FileNotFoundError(
            "Media file does not exist: {0}".format(file_path)
        )

    cover_value = str(item.get("cover", "")).strip()
    cover_path = None
    if cover_value:
        cover_path = safe_media_path(cover_value)
        if cover_path.suffix.lower() not in ALLOWED_COVER_EXTENSIONS:
            raise ValueError(
                "Unsupported cover extension: {0}".format(
                    cover_path.suffix
                )
            )
        if apply_changes and not cover_path.is_file():
            raise FileNotFoundError(
                "Cover file does not exist: {0}".format(cover_path)
            )

    file_relative = file_path.relative_to(MEDIA_DIR.resolve()).as_posix()
    cover_relative = None
    if cover_path:
        cover_relative = cover_path.relative_to(MEDIA_DIR.resolve()).as_posix()

    return {
        "media_id": str(item["media_id"]).strip(),
        "knowledge_point_id": str(item["knowledge_point_id"]).strip(),
        "type": media_type,
        "title": str(item["title"]).strip(),
        "format": extension.lstrip("."),
        "url": "/media/{0}".format(quote(file_relative, safe="/")),
        "cover_url": (
            "/media/{0}".format(quote(cover_relative, safe="/"))
            if cover_relative
            else None
        ),
        "order": int(item.get("order", 9999)),
    }


def ensure_knowledge_points(driver, knowledge_point_ids) -> None:
    with driver.session(
        database=NEO4J_DATABASE,
        default_access_mode=READ_ACCESS,
    ) as session:
        records = session.run(
            """
            MATCH (knowledge:KnowledgePoint)
            WHERE knowledge.kp_id IN $knowledge_point_ids
            RETURN collect(DISTINCT knowledge.kp_id) AS ids
            """,
            {"knowledge_point_ids": knowledge_point_ids},
            timeout=10.0,
        ).single()

    found_ids = set(records["ids"] if records else [])
    missing_ids = sorted(set(knowledge_point_ids) - found_ids)
    if missing_ids:
        raise ValueError(
            "Knowledge points not found: {0}".format(", ".join(missing_ids))
        )


def upsert_media_item(tx, item: Dict[str, Any]) -> None:
    tx.run(
        """
        MATCH (knowledge:KnowledgePoint {kp_id: $knowledge_point_id})
        MERGE (media:Media {media_id: $media_id})
        SET media.type = $type,
            media.title = $title,
            media.format = $format,
            media.url = $url,
            media.cover_url = $cover_url,
            media.order = $order
        MERGE (knowledge)-[:HAS_MEDIA]->(media)
        """,
        item,
        timeout=10.0,
    )


def apply_media_items(driver, items: List[Dict[str, Any]]) -> None:
    with driver.session(database=NEO4J_DATABASE) as session:
        for item in items:
            session.execute_write(upsert_media_item, item)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and import teaching media metadata."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write validated media nodes and relationships to Neo4j.",
    )
    args = parser.parse_args()

    if not NEO4J_PASSWORD:
        raise RuntimeError(
            "NEO4J_PASSWORD is not configured. Set backend/.env first."
        )

    raw_items = load_manifest()
    if not raw_items:
        print("Media manifest is empty. Nothing to import.")
        return

    media_ids = [
        str(item.get("media_id", "")).strip()
        for item in raw_items
    ]
    duplicate_ids = sorted(
        media_id
        for media_id, count in Counter(media_ids).items()
        if media_id and count > 1
    )
    if duplicate_ids:
        raise ValueError(
            "Duplicate media IDs: {0}".format(", ".join(duplicate_ids))
        )

    validated_items = [
        validate_item(item, apply_changes=args.apply)
        for item in raw_items
    ]

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )
    try:
        driver.verify_connectivity()
        ensure_knowledge_points(
            driver,
            {
                item["knowledge_point_id"]
                for item in validated_items
            },
        )
        if args.apply:
            apply_media_items(driver, validated_items)
    finally:
        driver.close()

    mode = "Imported" if args.apply else "Validated"
    print(
        "{0} {1} media items.".format(
            mode,
            len(validated_items),
        )
    )
    for item in validated_items:
        print(
            "{0}: {1} -> {2}".format(
                item["knowledge_point_id"],
                item["type"],
                item["url"],
            )
        )


if __name__ == "__main__":
    main()
