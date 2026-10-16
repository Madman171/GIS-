# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT_DIR = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT_DIR / "release"
LINES_PER_PAGE = 50
PAGE_WIDTH = 100

SOURCE_PATTERNS = [
    "backend/*.py",
    "frontend/*.html",
    "frontend/*.js",
    "frontend/*.json",
    "frontend/src/**/*.js",
    "frontend/src/**/*.vue",
    "frontend/src/**/*.css",
    "scripts/build_copyright_source.py",
    "scripts/export_graph.py",
    "scripts/import_media.py",
]

EXCLUDED_PARTS = {
    ".git",
    ".python",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
    "release",
    "test-results",
    "playwright-report",
}

EXCLUDED_FILES = {
    "package-lock.json",
}


def collect_source_files() -> List[Path]:
    files = set()
    for pattern in SOURCE_PATTERNS:
        for path in ROOT_DIR.glob(pattern):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT_DIR)
            if any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if path.name in EXCLUDED_FILES:
                continue
            files.add(path)

    return sorted(
        files,
        key=lambda path: path.relative_to(ROOT_DIR).as_posix().lower(),
    )


def normalize_source_line(line: str) -> str:
    return line.replace("\t", "    ").rstrip()


def collect_code_lines(files: List[Path]) -> List[str]:
    lines = []
    for path in files:
        relative = path.relative_to(ROOT_DIR).as_posix()
        lines.append("")
        lines.append("=" * PAGE_WIDTH)
        lines.append("FILE: {0}".format(relative))
        lines.append("=" * PAGE_WIDTH)
        content = path.read_text(encoding="utf-8").splitlines()
        lines.extend(normalize_source_line(line) for line in content)
        if not content or content[-1].strip():
            lines.append("")
    return lines


def paginate(code_lines: List[str]) -> List[List[str]]:
    return [
        code_lines[index:index + LINES_PER_PAGE]
        for index in range(0, len(code_lines), LINES_PER_PAGE)
    ]


def render_pages(pages: List[List[str]], start_page: int = 1) -> str:
    total_pages = len(pages)
    rendered = []

    for offset, page_lines in enumerate(pages):
        page_number = start_page + offset
        rendered.extend(
            [
                "GIS交通路网教学知识图谱平台 V1.0",
                "源代码整理件  第 {0} 页 / 共 {1} 页".format(
                    page_number,
                    total_pages,
                ),
                "-" * PAGE_WIDTH,
            ]
        )
        padded = page_lines + [""] * (LINES_PER_PAGE - len(page_lines))
        rendered.extend(padded[:LINES_PER_PAGE])
        rendered.append("")
        if offset < len(pages) - 1:
            rendered.append("\f")

    return "\n".join(rendered).rstrip() + "\n"


def file_manifest(files: List[Path]) -> List[Dict[str, object]]:
    manifest = []
    for path in files:
        content = path.read_bytes()
        manifest.append(
            {
                "path": path.relative_to(ROOT_DIR).as_posix(),
                "bytes": len(content),
                "lines": len(path.read_text(encoding="utf-8").splitlines()),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    return manifest


def main() -> None:
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    source_files = collect_source_files()
    if not source_files:
        raise RuntimeError("No source files found")

    code_lines = collect_code_lines(source_files)
    pages = paginate(code_lines)
    total_pages = len(pages)

    (RELEASE_DIR / "source-code-full.txt").write_text(
        render_pages(pages),
        encoding="utf-8",
    )

    if total_pages <= 60:
        submission_text = render_pages(pages)
        submission_note = (
            "总页数不超过60页，送审版本采用全部源码。"
        )
    else:
        first_pages = pages[:30]
        last_pages = pages[-30:]
        first_text = render_pages(first_pages, start_page=1)
        last_text = render_pages(
            last_pages,
            start_page=total_pages - 29,
        )
        (RELEASE_DIR / "source-code-first-30-pages.txt").write_text(
            first_text,
            encoding="utf-8",
        )
        (RELEASE_DIR / "source-code-last-30-pages.txt").write_text(
            last_text,
            encoding="utf-8",
        )
        submission_text = (
            first_text.rstrip()
            + "\n\f\n"
            + last_text
        )
        submission_note = (
            "总页数超过60页，送审版本采用前30页和后30页。"
        )

    (RELEASE_DIR / "source-code-submission.txt").write_text(
        submission_text,
        encoding="utf-8",
    )

    manifest = {
        "metadata": {
            "software_name": "GIS交通路网教学知识图谱平台",
            "version": "V1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_file_count": len(source_files),
            "source_line_count": len(code_lines),
            "lines_per_page": LINES_PER_PAGE,
            "total_pages": total_pages,
            "submission_note": submission_note,
        },
        "files": file_manifest(source_files),
    }
    (RELEASE_DIR / "source-code-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    readme = """# 软著源码整理件

软件名称：GIS交通路网教学知识图谱平台

版本：V1.0

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `source-code-full.txt` | 全部源码分页整理 |
| `source-code-submission.txt` | 总页数不超过60页时生成 |
| `source-code-first-30-pages.txt` | 总页数超过60页时生成 |
| `source-code-last-30-pages.txt` | 总页数超过60页时生成 |
| `source-code-manifest.json` | 源码文件、行数、页数和SHA-256清单 |

## 分页规则

1. 每页正文最多50行。
2. 页眉包含软件名称、版本号和页码。
3. 不包含第三方依赖、虚拟环境、构建产物和真实密钥。
4. 生成内容为UTF-8纯文本，可转换为Word或PDF后送审。

{0}
""".format(submission_note)
    (RELEASE_DIR / "README.md").write_text(readme, encoding="utf-8")

    print(
        "Generated {0} pages from {1} source files ({2} code lines).".format(
            total_pages,
            len(source_files),
            len(code_lines),
        )
    )
    print(submission_note)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Build failed: {0}".format(exc), file=sys.stderr)
        raise
