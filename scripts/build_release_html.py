# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import html
import json
import re
from pathlib import Path
from typing import List


ROOT_DIR = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT_DIR / "release"
DOCS_DIR = RELEASE_DIR / "documentation"
OUTPUT_PATH = RELEASE_DIR / "soft-copyright-documentation.html"

DOCUMENT_ORDER = [
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

EXTRA_DOCUMENTS = [
    "software-overview.md",
    "application-information.md",
    "submission-checklist.md",
    "source-code-print-guide.md",
]


def inline_markup(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(
        r"`([^`]+)`",
        r"<code>\1</code>",
        escaped,
    )
    escaped = re.sub(
        r"\*\*([^*]+)\*\*",
        r"<strong>\1</strong>",
        escaped,
    )
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        escaped,
    )
    return escaped


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(
        re.match(r"^:?-{3,}:?$", cell) for cell in cells
    )


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: List[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]

        if line.startswith("```"):
            language = line[3:].strip()
            code_lines = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            class_name = (
                ' class="language-{0}"'.format(html.escape(language))
                if language
                else ""
            )
            output.append(
                "<pre><code{0}>{1}</code></pre>".format(
                    class_name,
                    html.escape("\n".join(code_lines)),
                )
            )
            index += 1
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            output.append(
                "<h{0}>{1}</h{0}>".format(
                    level,
                    inline_markup(heading_match.group(2)),
                )
            )
            index += 1
            continue

        if (
            line.strip().startswith("|")
            and index + 1 < len(lines)
            and is_table_separator(lines[index + 1])
        ):
            headers = [
                cell.strip()
                for cell in line.strip().strip("|").split("|")
            ]
            index += 2
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(
                    [
                        cell.strip()
                        for cell in lines[index].strip().strip("|").split("|")
                    ]
                )
                index += 1
            output.append("<table><thead><tr>")
            output.extend(
                "<th>{0}</th>".format(inline_markup(cell))
                for cell in headers
            )
            output.append("</tr></thead><tbody>")
            for row in rows:
                output.append("<tr>")
                output.extend(
                    "<td>{0}</td>".format(inline_markup(cell))
                    for cell in row
                )
                output.append("</tr>")
            output.append("</tbody></table>")
            continue

        list_match = re.match(r"^[-*]\s+(.*)$", line)
        if list_match:
            items = []
            while index < len(lines):
                match = re.match(r"^[-*]\s+(.*)$", lines[index])
                if not match:
                    break
                items.append(match.group(1))
                index += 1
            output.append("<ul>")
            output.extend(
                "<li>{0}</li>".format(inline_markup(item))
                for item in items
            )
            output.append("</ul>")
            continue

        number_match = re.match(r"^\d+\.\s+(.*)$", line)
        if number_match:
            items = []
            while index < len(lines):
                match = re.match(r"^\d+\.\s+(.*)$", lines[index])
                if not match:
                    break
                items.append(match.group(1))
                index += 1
            output.append("<ol>")
            output.extend(
                "<li>{0}</li>".format(inline_markup(item))
                for item in items
            )
            output.append("</ol>")
            continue

        if not line.strip():
            index += 1
            continue

        paragraph_lines = [line.strip()]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip():
                break
            if (
                candidate.startswith("#")
                or candidate.startswith("```")
                or candidate.strip().startswith("|")
                or re.match(r"^[-*]\s+", candidate)
                or re.match(r"^\d+\.\s+", candidate)
            ):
                break
            paragraph_lines.append(candidate.strip())
            index += 1
        output.append(
            "<p>{0}</p>".format(
                inline_markup(" ".join(paragraph_lines))
            )
        )

    return "\n".join(output)


def document_section(path: Path, title: str) -> str:
    content = path.read_text(encoding="utf-8")
    return (
        '<section class="document">\n'
        "<h1>{0}</h1>\n{1}\n"
        "</section>\n"
    ).format(html.escape(title), markdown_to_html(content))


def screenshot_section() -> str:
    screenshots = [
        ("01-overview.png", "系统首页和模块总览"),
        ("02-directory-module.png", "左侧目录和模块展开"),
        ("03-knowledge-detail.png", "知识点详情"),
        ("04-deepseek-chat.png", "DeepSeek 智能问答"),
        ("05-mobile.png", "移动端界面"),
    ]
    blocks = ['<section class="document"><h1>界面截图</h1>']
    for filename, caption in screenshots:
        blocks.append(
            '<figure><img src="screenshots/{0}" alt="{1}" />'
            "<figcaption>{1}</figcaption></figure>".format(
                filename,
                html.escape(caption),
            )
        )
    blocks.append("</section>")
    return "\n".join(blocks)


def build_document() -> str:
    sections = []
    for filename in DOCUMENT_ORDER:
        path = DOCS_DIR / filename
        if path.exists():
            sections.append(document_section(path, filename))
    for filename in EXTRA_DOCUMENTS:
        path = RELEASE_DIR / filename
        if path.exists():
            sections.append(document_section(path, filename))
    sections.append(screenshot_section())

    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GIS交通路网教学知识图谱平台 V1.0 软著材料</title>
  <style>
    :root {
      color: #1f2937;
      background: #ffffff;
      font: 14px/1.7 "Microsoft YaHei", "PingFang SC", sans-serif;
    }
    body {
      max-width: 960px;
      margin: 0 auto;
      padding: 32px;
    }
    .document {
      page-break-before: always;
    }
    .document:first-child {
      page-break-before: auto;
    }
    h1, h2, h3, h4 {
      color: #111827;
      break-after: avoid;
    }
    h1 {
      padding-bottom: 10px;
      border-bottom: 2px solid #7c3aed;
      font-size: 24px;
    }
    h2 {
      margin-top: 26px;
      font-size: 19px;
    }
    h3 {
      margin-top: 20px;
      font-size: 16px;
    }
    p {
      margin: 9px 0;
    }
    code {
      padding: 2px 5px;
      border-radius: 3px;
      color: #7c2d12;
      background: #fff7ed;
    }
    pre {
      padding: 14px;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      overflow-x: auto;
      white-space: pre-wrap;
      background: #f8fafc;
    }
    pre code {
      padding: 0;
      color: #0f172a;
      background: transparent;
    }
    table {
      width: 100%;
      margin: 14px 0;
      border-collapse: collapse;
    }
    th, td {
      padding: 7px 9px;
      border: 1px solid #cbd5e1;
      text-align: left;
      vertical-align: top;
    }
    th {
      background: #f1f5f9;
    }
    figure {
      margin: 22px 0;
      text-align: center;
    }
    figure img {
      max-width: 100%;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
    }
    figcaption {
      margin-top: 7px;
      color: #64748b;
      font-size: 12px;
    }
    @media print {
      body {
        max-width: none;
        padding: 0;
      }
    }
  </style>
</head>
<body>
<header>
  <h1>GIS交通路网教学知识图谱平台 V1.0</h1>
  <p>软件著作权说明材料</p>
</header>
__CONTENT__
</body>
</html>
""".replace("__CONTENT__", "\n".join(sections))


def main() -> None:
    OUTPUT_PATH.write_text(build_document(), encoding="utf-8")
    manifest = json.loads(
        (RELEASE_DIR / "source-code-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    print(
        "Generated HTML release document: {0}".format(OUTPUT_PATH)
    )
    print(
        "Source pages: {0}".format(
            manifest["metadata"]["total_pages"]
        )
    )


if __name__ == "__main__":
    main()
