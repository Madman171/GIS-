# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 后端服务
# 本文件为平台核心业务代码，受软件著作权保护

from pathlib import Path
from typing import Iterable

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


ROOT_DIR = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT_DIR / "release"
SCREENSHOT_DIR = RELEASE_DIR / "screenshots"
DOCUMENT_PATH = (
    ROOT_DIR
    / "GIS交通路网教学知识图谱平台-V1.0-软件使用说明书.docx"
)

SOFTWARE_NAME = "GIS交通路网教学知识图谱平台"
VERSION = "V1.0"
PUBLIC_URL = "http://123.207.246.112:8080"


def set_run_font(run, name="宋体", size=10.5, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def set_paragraph_font(paragraph, size=10.5, bold=False):
    for run in paragraph.runs:
        set_run_font(run, size=size, bold=bold)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, end])
    set_run_font(run, size=10.5)


def add_toc(document):
    paragraph = document.add_paragraph()
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = ' TOC \\o "1-3" \\h \\z \\u '
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "在Word中右键此处并选择“更新域”生成目录"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, separate, placeholder, end])


def configure_document(document):
    section = document.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.header_distance = Cm(1.5)
    section.footer_distance = Cm(1.5)

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_run = header.add_run(
        "{0} {1}".format(SOFTWARE_NAME, VERSION)
    )
    set_run_font(header_run, size=10.5)

    footer = section.footer.paragraphs[0]
    footer.add_run("第 ")
    add_page_number(footer)
    footer.add_run(" 页")
    set_paragraph_font(footer, size=10.5)

    normal = document.styles["Normal"]
    normal.font.name = "宋体"
    normal.font.size = Pt(10.5)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    normal.paragraph_format.line_spacing = 1.25
    normal.paragraph_format.space_after = Pt(4)

    heading_sizes = {1: 16, 2: 14, 3: 12}
    for level, size in heading_sizes.items():
        style = document.styles["Heading {0}".format(level)]
        style.font.name = "宋体"
        style.font.size = Pt(size)
        style.font.bold = True
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


def add_cover(document):
    for _ in range(4):
        document.add_paragraph()

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(SOFTWARE_NAME)
    set_run_font(run, name="黑体", size=22, bold=True)

    version = document.add_paragraph()
    version.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = version.add_run("{0} 软件使用说明书".format(VERSION))
    set_run_font(run, name="黑体", size=18, bold=True)

    for _ in range(8):
        document.add_paragraph()

    info = [
        ("软件名称", SOFTWARE_NAME),
        ("软件版本", VERSION),
        ("文档版本", VERSION),
        ("编写日期", "2026年9月21日"),
        ("著作权人", "待确认"),
        ("公开访问地址", PUBLIC_URL),
    ]
    table = document.add_table(rows=0, cols=2)
    table.style = "Table Grid"
    for label, value in info:
        cells = table.add_row().cells
        cells[0].text = label
        cells[1].text = value
        for cell in cells:
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for paragraph in cell.paragraphs:
                set_paragraph_font(paragraph, size=11)
    document.add_page_break()


def add_bullet_list(document, items: Iterable[str]):
    for item in items:
        paragraph = document.add_paragraph(style="List Bullet")
        paragraph.add_run(item)
        set_paragraph_font(paragraph, size=10.5)


def add_table(document, headers, rows):
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.text = header
        for paragraph in cell.paragraphs:
            set_paragraph_font(paragraph, size=10.5, bold=True)
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            cells[index].text = str(value)
            for paragraph in cells[index].paragraphs:
                set_paragraph_font(paragraph, size=10.5)
    document.add_paragraph()
    return table


def add_screenshot(document, filename, title, description):
    document.add_page_break()
    document.add_heading(title, level=2)
    paragraph = document.add_paragraph(description)
    set_paragraph_font(paragraph, size=10.5)
    image_path = SCREENSHOT_DIR / filename
    if image_path.exists():
        image_paragraph = document.add_paragraph()
        image_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        image_paragraph.add_run().add_picture(
            str(image_path),
            width=Cm(15.5),
        )
        caption = document.add_paragraph(
            "{0} 软件界面示意图".format(title)
        )
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_font(caption, size=10.5)


def build_manual():
    document = Document()
    configure_document(document)
    add_cover(document)

    document.add_heading("目录", level=1)
    add_toc(document)
    document.add_page_break()

    document.add_heading("1 引言", level=1)
    document.add_heading("1.1 编写目的", level=2)
    document.add_paragraph(
        "本说明书用于介绍GIS交通路网教学知识图谱平台的软件功能、运行环境、"
        "安装部署方式、操作方法和常见问题，帮助教师、学生和项目管理人员"
        "快速理解并正确使用本软件。"
    )
    document.add_heading("1.2 术语与缩略语", level=2)
    add_table(
        document,
        ["术语", "解释"],
        [
            ["GIS", "地理信息系统，用于采集、存储、分析、展示空间数据。"],
            ["知识图谱", "以节点和关系表达知识点及其关联结构的图数据模型。"],
            ["Module", "课程模块或教学章节。"],
            ["KnowledgePoint", "可独立学习、查询和关联的教学知识点。"],
            ["拓扑校验", "检测伪节点、断头路、跨层连接和端点衔接问题。"],
            ["AI问答", "结合知识图谱上下文生成教学回答的问答功能。"],
        ],
    )
    document.add_page_break()

    document.add_heading("2 软件概述", level=1)
    document.add_heading("2.1 软件名称与版本", level=2)
    document.add_paragraph(
        "软件全称：GIS交通路网教学知识图谱平台；版本号：V1.0。"
    )
    document.add_heading("2.2 开发环境", level=2)
    add_table(
        document,
        ["项目", "内容"],
        [
            ["开发操作系统", "Windows"],
            ["开发工具", "Visual Studio Code、Neo4j Browser、PowerShell"],
            ["开发语言", "Python、JavaScript、Vue、CSS、Cypher"],
            ["后端框架", "Python 3.12.10、FastAPI"],
            ["前端框架", "Node.js 24、Vue 3、Vite、D3.js"],
            ["数据库", "Neo4j 5.x"],
        ],
    )
    document.add_heading("2.3 运行环境", level=2)
    add_table(
        document,
        ["类别", "建议配置"],
        [
            ["服务器", "2核CPU、4GB内存、40GB磁盘"],
            ["操作系统", "Ubuntu Server 24.04/26.04 LTS"],
            ["浏览器", "Microsoft Edge、Chrome等现代浏览器"],
            ["网络", "公网访问需开放8080端口，AI问答需可访问外部模型服务"],
        ],
    )
    document.add_heading("2.4 应用领域", level=2)
    document.add_paragraph(
        "本软件适用于GIS、交通工程、道路勘测、空间分析和智慧交通课程教学，"
        "可服务于高校教师、学生、课程建设人员及知识图谱研究人员。"
    )
    document.add_page_break()

    document.add_heading("3 功能描述", level=1)
    document.add_heading("3.1 功能模块划分", level=2)
    add_table(
        document,
        ["模块名称", "功能描述"],
        [
            ["知识目录模块", "按模块展示全部知识点，支持展开和目录检索。"],
            ["知识图谱可视化模块", "使用D3.js展示模块、知识点和关系。"],
            ["知识点详情模块", "展示定义、难度、重要性、分类和关联知识。"],
            ["教学资源模块", "展示并打开视频、PDF、PPT或PPTX资源。"],
            ["教学问答模块", "结合图谱上下文调用DeepSeek生成回答。"],
            ["学习路径模块", "基于前置关系生成知识点学习路线。"],
            ["拓扑校验模块", "执行伪节点、断头路和跨层连接检查。"],
            ["数据导入模块", "校验并导入知识图谱快照数据。"],
        ],
    )
    document.add_heading("3.2 核心功能详述", level=2)
    add_bullet_list(
        document,
        [
            "模块总览：启动后展示九个教学模块及其支撑关系。",
            "知识点展开：点击模块后加载该模块的知识点子图。",
            "知识点详情：点击节点显示描述、难度、重要性和关联知识。",
            "智能问答：用户输入自然语言问题，系统返回教学回答和知识来源。",
            "媒体资源：在知识点详情中播放视频或打开课件。",
            "学习路径：通过前置依赖关系生成从基础到进阶的学习顺序。",
        ],
    )
    document.add_heading("3.3 业务流程图", level=2)
    document.add_paragraph(
        "用户访问平台 → 浏览知识目录 → 选择模块 → 展开知识点 → "
        "查看详情与资源 → 发起智能问答 → 点击引用继续学习。"
    )
    document.add_page_break()

    document.add_heading("4 技术特点与创新点", level=1)
    document.add_heading("4.1 技术架构", level=2)
    document.add_paragraph(
        "平台采用前后端分离架构：前端使用Vue 3、Vite和D3.js；"
        "后端使用FastAPI；Neo4j保存知识图谱；Nginx提供静态资源和反向代理。"
    )
    document.add_heading("4.2 关键技术与创新点", level=2)
    add_bullet_list(
        document,
        [
            "构建GIS交通路网专属知识关系体系。",
            "实现伪节点、断头路、跨层连接和端点衔接四类拓扑校验。",
            "实现基于PREREQUISITE_OF的前置依赖链和学习路径推理。",
            "使用四类教学问答Prompt模板控制回答场景和引用来源。",
            "采用参数化只读Cypher和接口限流保证平台稳定运行。",
        ],
    )
    document.add_page_break()

    document.add_heading("5 开发过程", level=1)
    add_table(
        document,
        ["角色", "姓名", "职责"],
        [
            ["项目负责人", "待确认", "需求分析、总体设计、进度管理"],
            ["后端开发", "待确认", "知识图谱、接口和问答引擎"],
            ["前端开发", "待确认", "页面、图谱和交互实现"],
            ["测试人员", "待确认", "功能测试、接口测试和验收"],
        ],
    )
    document.add_paragraph(
        "开发周期：待确认。开发过程包括需求分析、架构设计、编码、测试、"
        "腾讯云部署和软著材料整理。"
    )
    document.add_page_break()

    document.add_heading("6 软件使用说明", level=1)
    document.add_heading("6.1 安装与部署", level=2)
    document.add_paragraph(
        "普通用户无需安装客户端，只需使用现代浏览器访问公网地址：{0}。"
        "管理员使用Docker Compose部署前端、后端和Neo4j，并使用Nginx"
        "提供统一入口。".format(PUBLIC_URL)
    )
    document.add_heading("6.2 操作指南", level=2)
    add_bullet_list(
        document,
        [
            "打开平台：浏览器输入公网地址。",
            "浏览目录：在左侧选择模块并展开知识点。",
            "查看图谱：点击模块，观察知识节点和关系。",
            "查看详情：点击知识点，阅读属性、说明和关联知识。",
            "使用问答：在右侧输入问题并发送。",
            "跳转引用：点击回答下方的知识点引用继续学习。",
        ],
    )
    add_screenshot(
        document,
        "01-overview.png",
        "6.3 平台首页",
        "首页展示左侧知识目录、中间模块图谱和右侧教学问答窗口。",
    )
    add_screenshot(
        document,
        "02-directory-module.png",
        "6.4 模块与知识点展开",
        "点击模块后，目录和中间图谱同步展开知识点。",
    )
    add_screenshot(
        document,
        "03-knowledge-detail.png",
        "6.5 知识点详情",
        "详情面板展示难度、重要性、分类、所属模块和关联知识。",
    )
    add_screenshot(
        document,
        "04-deepseek-chat.png",
        "6.6 教学智能问答",
        "输入问题后，平台结合知识图谱上下文生成回答和知识点引用。",
    )
    add_screenshot(
        document,
        "05-mobile.png",
        "6.7 移动端访问",
        "窄屏设备使用抽屉式目录和问答面板，保持图谱可操作。",
    )

    document.add_page_break()
    document.add_heading("7 系统维护与数据备份", level=1)
    document.add_heading("7.1 服务启动与停止", level=2)
    document.add_paragraph(
        "管理员进入服务器项目目录后，使用Docker Compose统一管理服务。"
        "平台使用Neo4j、FastAPI和Nginx三个主要容器，数据保存在Docker卷中。"
    )
    add_table(
        document,
        ["操作", "命令"],
        [
            ["查看状态", "docker compose ps"],
            ["查看日志", "docker compose logs -f"],
            ["重启服务", "docker compose restart"],
            ["停止服务", "docker compose down"],
            ["备份数据", "./deploy/backup.sh"],
        ],
    )
    document.add_heading("7.2 数据备份", level=2)
    document.add_paragraph(
        "平台数据由Neo4j图谱卷和media媒体目录组成。管理员应定期执行备份"
        "脚本，并将备份文件保存到独立磁盘或对象存储。"
    )
    document.add_heading("7.3 安全建议", level=2)
    add_bullet_list(
        document,
        [
            "不要将Neo4j的7474和7687端口暴露到公网。",
            "API Key和数据库密码只保存在服务器环境文件中。",
            "定期检查问答接口调用日志和访问频率。",
            "维护前先完成数据库和媒体备份。",
        ],
    )
    document.add_page_break()

    document.add_heading("8 常见问题解答", level=1)
    add_table(
        document,
        ["问题", "解决方法"],
        [
            ["网页无法打开", "检查服务器是否运行、8080端口是否开放。"],
            ["目录为空", "检查Neo4j数据是否导入及后端是否连接数据库。"],
            ["图谱不显示", "刷新页面，检查浏览器控制台和后端接口。"],
            ["问答提示未配置", "检查服务器环境变量中的模型API Key。"],
            ["问答提示频繁", "默认每个IP每分钟最多提问5次，请稍后重试。"],
            ["视频或PPT无法打开", "检查媒体文件路径及文件扩展名。"],
        ],
    )

    document.add_page_break()
    document.add_heading("9 著作权声明", level=1)
    document.add_paragraph(
        "本软件著作权归著作权人所有，受《中华人民共和国著作权法》保护。"
        "未经权利人书面许可，不得复制、传播、修改本软件或用于商业用途。"
        "著作权人信息以正式申请表为准。"
    )
    document.add_paragraph(
        "文档编写日期：2026年9月21日。正式提交前应确认该日期早于软件"
        "开发完成日期。"
    )

    document.add_page_break()
    document.add_heading("10 附录", level=1)
    add_table(
        document,
        ["接口", "用途"],
        [
            ["/api/health", "检查后端和数据库状态"],
            ["/api/directory", "读取模块和知识点目录"],
            ["/api/modules/{id}/graph", "读取模块知识点图谱"],
            ["/api/knowledge-points/{id}", "读取知识点详情"],
            ["/api/knowledge-points/{id}/learning-path", "查询前置学习链"],
            ["/api/topology/check", "执行拓扑完整性校验"],
            ["/api/chat", "执行教学智能问答"],
        ],
    )

    document.core_properties.title = (
        "{0} {1} 软件使用说明书".format(SOFTWARE_NAME, VERSION)
    )
    document.core_properties.author = "GIS交通路网教学知识图谱平台"
    DOCUMENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    document.save(DOCUMENT_PATH)
    print("USER_MANUAL_CREATED", DOCUMENT_PATH)
    print("BYTES", DOCUMENT_PATH.stat().st_size)


if __name__ == "__main__":
    build_manual()
