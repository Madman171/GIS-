# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import json
import re
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT_DIR / "release"
DOCS_DIR = RELEASE_DIR / "documentation"

REQUIRED_FILES = [
    RELEASE_DIR / "INDEX.md",
    RELEASE_DIR / "application-information.md",
    RELEASE_DIR / "application-information.json",
    RELEASE_DIR / "software-overview.md",
    RELEASE_DIR / "submission-checklist.md",
    RELEASE_DIR / "source-code-print-guide.md",
    RELEASE_DIR / "source-code-full.txt",
    RELEASE_DIR / "source-code-submission.txt",
    RELEASE_DIR / "source-code-first-30-pages.txt",
    RELEASE_DIR / "source-code-last-30-pages.txt",
    RELEASE_DIR / "source-code-manifest.json",
    RELEASE_DIR / "soft-copyright-documentation.html",
    RELEASE_DIR
    / "GIS交通路网教学知识图谱平台-V1.0-软著说明材料.pdf",
    RELEASE_DIR
    / "GIS交通路网教学知识图谱平台-核心源代码-V1.0.docx",
    RELEASE_DIR
    / "GIS交通路网教学知识图谱平台-V1.0-软件使用说明书.docx",
]

DOCUMENT_FILES = [
    "00-version-baseline.md",
    "01-system-design.md",
    "02-database-design.md",
    "03-api-design.md",
    "04-operation-manual.md",
    "05-deployment-guide.md",
    "06-test-report.md",
    "07-third-party-licenses.md",
    "08-media-import.md",
    "09-deepseek-setup.md",
]

SCREENSHOT_FILES = [
    "01-overview.png",
    "02-directory-module.png",
    "03-knowledge-detail.png",
    "04-deepseek-chat.png",
    "05-mobile.png",
]


def fail(message: str) -> None:
    raise RuntimeError(message)


def validate_required_files() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail("Missing release files: {0}".format(", ".join(missing)))

    missing_docs = [
        name for name in DOCUMENT_FILES if not (DOCS_DIR / name).exists()
    ]
    if missing_docs:
        fail("Missing documents: {0}".format(", ".join(missing_docs)))

    missing_screenshots = [
        name
        for name in SCREENSHOT_FILES
        if not (RELEASE_DIR / "screenshots" / name).exists()
    ]
    if missing_screenshots:
        fail(
            "Missing screenshots: {0}".format(
                ", ".join(missing_screenshots)
            )
        )


def validate_manifest() -> None:
    manifest = json.loads(
        (RELEASE_DIR / "source-code-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    metadata = manifest["metadata"]
    if metadata["source_file_count"] < 20:
        fail("Unexpected source file count")
    if metadata["total_pages"] <= 60:
        fail("Expected more than 60 source pages")

    for item in manifest["files"]:
        path = item["path"]
        if re.search(r"(^|/)(\.env|node_modules|\.venv|\.python|dist)(/|$)", path):
            fail("Forbidden path in source manifest: {0}".format(path))
    return metadata


def validate_no_secrets() -> None:
    secret_patterns = [
        re.compile(r"88888888"),
        re.compile(r"sk-[A-Za-z0-9]{16,}"),
    ]
    for path in RELEASE_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt", ".json", ".html"}:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in secret_patterns:
            if pattern.search(content):
                fail(
                    "Possible secret found in {0}: {1}".format(
                        path,
                        pattern.pattern,
                    )
                )


def main() -> None:
    validate_required_files()
    metadata = validate_manifest()
    validate_no_secrets()

    submission = (
        RELEASE_DIR / "source-code-submission.txt"
    ).read_text(encoding="utf-8")
    last_page = "第 {0} 页".format(metadata["total_pages"])
    if "第 1 页" not in submission or last_page not in submission:
        fail("Submission source does not contain first and last pages")

    print("Release validation passed.")
    print("Documents: {0}".format(len(DOCUMENT_FILES)))
    print("Screenshots: {0}".format(len(SCREENSHOT_FILES)))
    print("Source submission: first 30 pages + last 30 pages")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Validation failed: {0}".format(exc), file=sys.stderr)
        raise
