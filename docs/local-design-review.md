# 本地界面重设计 · 2026-10-30

仅在本地修改。未提交、推送、创建发布或部署。数据文件未修改；后端新增了全课程图谱的只读查询接口。

## 方向与范围

使用 design-taste-frontend 的应用界面流程。方向为 Framed sheet，seed 1370576991，无重抽。
框架取低饱和蓝灰、阅读面取白色；图谱数据使用蓝绿与中性色。
英文使用本地 IBM Plex Sans，中文使用本地 Noto Sans SC 课程字库子集（约 319 KB），均保留 OFL 许可。
中文字体是对抽签字体中文覆盖不足的补充，不增加装饰性字体。

项目清单：9 个模块、344 个知识点、10 个工具、目录搜索、模块子图、节点关系、难度与重要性、
前置路径、视频与课件、知识点前后导航、AI 精灵拖动及聊天。这些真实内容决定布局。
首页的问题：从哪个模块开始学习、知识点怎样相连？主画面回答：课程知识网络。
详情页的问题：这个知识点是什么、先学什么、还能看什么？阅读面按现有内容回答。
概念：九个课程模块及其前置关系成为课程地图，知识点成为旁边可阅读的资料页。
交互主体：真实目录、图谱节点、视图模式、关系筛选、学习路径、详情导航和现有精灵问答。

## 本地预览

```powershell
cd E:\gis-knowledge-platform\frontend
npm run preview:design
```

打开 http://127.0.0.1:5181 ，示例详情为 http://127.0.0.1:5181/?knowledge=M1-007 。
预览读取 data/graph-snapshot.json，不连接 Neo4j，不调用 AI，不写入数据。
浏览器明确标记“本地快照预览”。聊天操作由现有 E2E 模拟验证，不代表真实模型已连接。
预览服务仅监听本机。端口 5181 不影响生产服务。

## 检查与对照

- 重设计前生产构建/真实快照检查：7 FAIL、2 WARN。
- 重设计后首页与详情：各在 1440、768、390 三个宽度检查；报告及截图在 .taste-skill/。
- 原有 Playwright 主流程通过，覆盖目录、图谱、详情、刷新、精灵、发送消息及引用。
- 本地额外检查覆盖三种宽度的模块、详情、教学资源、聊天；无横向溢出或页面脚本异常。
- data/、backend/、deploy/ 均无修改；所有知识点共用重设计后的详情组件。
- 活跃组件 lint 无 FAIL。少量 WARN：应用允许的小标签，以及仅用于悬浮提示和聊天窗的阴影。
  两个未被应用引用的旧版图谱组件未改动，因此扫描整个历史目录仍会命中它们的旧样式。
- 构建仍有原有 three.js 大分包提示，精灵依旧按需加载，未在视觉改版中升级依赖。

## 视觉检查记录

ROUND 1
Seen in one second: 紫色节点与背景网格，字体偏小，平板侧栏挤压图谱。
Idea (one sentence): 让真实课程网络成为主体，目录和知识资料作为安静的框架。
Live thing: 原有图谱探索与知识点导航。
Layout words by section: shell=L-frame / graph=canvas / detail=reading sheet
Scores: design 5.8 · usability 6.2 · creativity 6.0 · content 8.5 → overall 6.2
Caps applied: 重设计前检查存在 FAIL。
Top three problems:
1. before-snapshot/desktop-fold.jpg：网格、光环和多色强调抢占视觉，改为平面表面与收敛配色。
2. before-snapshot/tablet-fold.jpg：侧栏挤压画布，平板改为可展开目录。
3. before-snapshot/mobile-fold.jpg：小字号、控件拥挤，改为可读字号与分行工具栏。

ROUND 2
Seen in one second: 清晰的课程图和独立阅读页，中文长段落可读。
Idea (one sentence): 课程地图与资料阅读面共享一个低饱和框架。
Live thing: 可点击课程模块、关系筛选、学习路径和前后知识点。
Layout words by section: shell=L-frame / graph=canvas / detail=reading sheet
Scores: design 7.6 · usability 7.6 · creativity 7.0 · content 8.5 → overall 7.6
Caps applied: 应用界面不采用营销页图片/动效数量要求。
Top three problems:
1. 第一轮详情图：手机重复显示知识点标题和全套工具栏。修复为独立阅读层，关闭后返回图谱工具。
2. 第一轮详情图：窄图谱中图例和导航图叠放。修复为上下分区。
3. 第一轮首页：精灵默认覆盖右侧导航图。修复为桌面默认停靠目录底部，保留用户已保存的位置与拖动。

Remaining limitations: 全景子图在节点多且缩小到整图时标签仍较密；可使用缩放、重点/路径视图及目录阅读。
手机精灵仍可覆盖局部阅读内容，可拖动或关闭建议。用户已保存的位置不强制重置。
没有新增外部图片、视频、虚构数据或样例课文，精灵继续使用项目原有模型。

## 用户批注后的第二版

按浏览器四条批注调整，仍然仅保存在本地：

- 顶栏保持原高度，中文主标题从 20px 改为 28px，GIS 字标 36px，调整字距和字重。
- 移除标题、目录、工具栏、详情栏目和精灵上的装饰图标。导航使用文字，缩放使用加减符号。
  仅保留加载中的转圈状态与展开、关闭等基本操作符，不引入新的图标依赖。
- 移除顶栏和画布上的节点/关系/核心/进阶数量，以及模块副标题、目录汇总与列表尾部的数量。
  课程知识、难度、重要性、前置关系和教学资源仍完整保留。
- 移除所有节点圆环、白色中心点、同心圆轨道，采用名称直接置于节点内部的圆角矩形。
  知识点标题自动多行排版，难度使用侧边色标，模块使用浅色大节点。
- 使用可复现且无节点重叠的布局，全部连线仍来自原始数据；空间位置不暗示新的前置关系。
- 点击知识点后自动放大到所选节点附近，详情旁的图谱不再强制压缩成整幅缩略图。

参考来源：

- KeyLines 官方示例：https://developers.cambridge-intelligence.com/examples/keylines
- 节点内部标签与多行标签：https://developers.cambridge-intelligence.com/api/keylines/item-format
- Phosphor 图标库：https://phosphoricons.com/
- Tabler 图标库说明：https://docs.tabler.io/icons

这次选择文字导航与无装饰图标方案，没有下载或安装图标库。引用的是交互与节点文字组织方法，未复制第三方图片或素材。

验证新增：3 个图布局测试覆盖 9 个真实模块在 3 种画布宽度下的无重叠、标题保留、边界连接与布局稳定性；
额外浏览器检查加入用户批注的 1363px 宽度。原有 E2E 主流程继续通过。

ROUND 3 (user-feedback revision)
Seen in one second: 大字标题与名称可读的知识节点。
Idea (one sentence): 把知识点本身作为网络中的路标，界面只提供阅读和导航。
Live thing: 真实图谱连线、可拖动节点、关系筛选和知识点详情。
Layout words by section: header=wordmark / overview=linked modules / module=label network / detail=reading sheet
Scores: design 7.7 · usability 7.8 · creativity 7.0 · content 8.5 → overall 7.7
Caps applied: 用户要求更大字标，顶栏高度不增加；按应用界面规则评价。
Top three problems:
1. 原图标题过小：增大文字本身、移除标识图标、保留顶栏尺寸。
2. 原图圆点与外置标签密集：改为内部多行标签，自动测算节点高度，全部真实模块验证无重叠。
3. 原图统计和装饰图标占用注意力：移除重复计数与装饰，保留必要操作和教学信息。

Remaining limitations: 手机全景仍需放大阅读长知识点名称；详情视图会自动聚焦，适配按钮可返回全图。

## 用户确认后的圆形图谱版本

用户明确选择 Neo4j 的实心圆方向，并要求文字外置、总体圆形分布、总知识点居中且略大、箭头缩小。
本节取代上一版矩形节点方案；标题、字体、目录、详情和已移除的重复统计保持当前版本。

- 总览以基础理论模块为中心，其余真实模块围绕；模块子图以该模块为中心，知识点分层围绕。
- 使用纯色圆和略深的细描边，中心半径 42、外围知识点半径 23 或 29（随画布缩放）。
  没有中心白点、发光、渐变或多重套环。选中、悬停与键盘聚焦使用更明显的描边。
- 外置标签按左右半圆分配，最多显示两行，完整原名保留在目录、悬浮提示、可访问名称和详情中。
  标签可点击；圆形分层只组织空间，不增加任何数据关系。
- 箭头为固定世界尺寸 4.5，不再随关系线宽放大。连线止于圆的边缘。
- 延续 Framed sheet（seed 1370576991），此次组件调整未重抽方向，也未增加图标、图片或依赖。

验证：生产构建通过；3 个图布局测试通过（全部 9 个真实模块、标题保留、标签间距、圆形轨道、圆边界连接）；
原有 Playwright 主流程通过。首页与详情在 1440 / 768 / 390 三种宽度的 inspector 均为 0 FAIL、0 WARN。
源码 lint 为 0 FAIL，保留的 3 个 WARN 是应用中的小标签以及悬浮提示/聊天层的阴影。
浏览器额外检查覆盖 9 个模块的实际标签包围盒，以及悬停、缩放、拖动、关系筛选、键盘打开详情。

ROUND 4 (confirmed circular nodes)
Seen in one second: 中心总知识点与外围实心圆网络，名称在节点外侧。
Idea (one sentence): 以总知识点为中心组织真实课程关系，使用圆的大小与位置表达层次。
Live thing: 圆形节点及名称可点击，保留拖动、缩放、关系筛选和知识点阅读。
Layout words by section: overview=circular modules / module=central topic and circular orbits / detail=reading sheet
Scores: design 7.8 · usability 7.6 · creativity 7.0 · content 8.5 → overall 7.7
Caps applied: 应用图谱遵循用户明确确认的圆形结构，不套用营销页图像数量要求。
Top three problems:
1. 前一版矩形节点违背用户预期：恢复纯色圆、外置名称和中心结构。
2. 等角度圆环顶部标签容易拥挤：按半圆均衡纵向间距，计算内外层间距，并检查实际浏览器标签。
3. 原箭头大小跟随线宽变化：使用固定 markerUnits 与小箭头，按圆边界截断连线。

Remaining limitations: 手机及节点较多的全图预览以结构为主，阅读长名称仍需缩放或打开知识点；
桌面打开详情时聚焦所选节点，因此周边网络可以超出画布，可拖动或使用“适配”。
检查截图在 .taste-skill/circular-*，未提交、推送或部署。

## 知识点详情恢复弹窗

按用户要求，详情从并排阅读区/窄屏全屏层改为居中的原生 dialog。
桌面宽度最多 880px，手机保留四周留白；标题栏固定，正文、关联知识、视频课件和前后导航在窗内滚动。
圆形图谱不再因详情打开而重排、缩放或自动居中，关闭后保留原来的图谱视口。
支持关闭按钮、Esc、点击遮罩；浏览器管理焦点范围和关闭后的焦点恢复。
加载中也可关闭，迟到的详情响应不会重新打开已关闭的弹窗。

生产构建与 Playwright 主流程通过。额外真实浏览器验证覆盖 1440、1363、768、390 四种宽度的
弹窗边距、图谱尺寸和变换不变、焦点限制、前后导航/返回、Esc 与遮罩关闭，以及加载中关闭后的响应竞争。
页面脚本错误为 0。Inspector 三种宽度为 0 FAIL、0 WARN，检查时只对真实模态窗口启用
`--allow covered-text,heavy-shadow`：原生 backdrop 会故意阻止背景标题交互，浮层本身允许有阴影；
这些是弹窗语义所需的局部例外，没有修改全局方向或跳过其他检查。

ROUND 5 (detail dialog)
Seen in one second: 图谱上方的独立知识点阅读窗口。
Idea (one sentence): 临时阅读知识点，关闭即继续原来的课程图谱探索。
Live thing: 弹窗内的前后知识点、学习路径、资源阅读与三种关闭方式。
Layout words by section: graph=unchanged canvas / detail=centered dialog
Scores: design 7.8 · usability 8.0 · creativity 7.0 · content 8.5 → overall 7.9
Caps applied: 原生模态窗口允许遮罩和浮层阴影；保留 Framed sheet，未重抽。
Top three problems:
1. 并排详情挤压图谱、手机直接铺满：改为所有尺寸均带边距的居中弹窗。
2. 选中知识点触发图谱跳转：取消自动居中，实际检查打开前后图谱变换一致。
3. 加载期间关闭后旧响应可能重开：使用请求序号使已关闭的请求结果失效。

Remaining limitations: 长内容需在窗内滚动；手机仍使用单列阅读。未上传或部署。

## 目录中的全部知识点总图

新增“全部知识点”入口，位于目录搜索框下方。原有模块总览和模块子图保留。
9 个真实模块组成中央大节点区域，344 个知识点按所属模块与课程顺序排在同一个外围圆环上。
外围节点缩小，圆环按知识点数量扩大；没有新增虚构节点或关系。

新增只读 `/api/graph/all`，查询所有 Module、KnowledgePoint 及它们之间的已定义关系，
包括跨模块关系和没有关系的孤立知识点；不把 Tool 或媒体节点混入课程总图。
本地设计服务器从同一项目快照提供对应接口，入口为 http://127.0.0.1:5181/?view=course 。
打开知识点、前后导航和关联知识时保留总图，关闭后继续原来的缩放位置。
“刷新数据”会重新读取总图；模块入口与“返回总览”仍可切回原来的视图。

总览默认显示模块名称；知识点名称在放大后按视口与碰撞情况显示，悬停仍可读完整名称。
全图适配取不遮挡节点的最大尺寸，逐项避开图例、缩放工具和导航图，而不是整条底边都留空。

验证：生产构建、4 个图布局测试、扩展后的 Playwright 主流程通过。
四种宽度 1440 / 1363 / 768 / 390 的浏览器检查确认 353 个节点完整、模块名称无重叠、
控件不遮挡初始节点、弹窗导航后保留总图和视口。额外验证滚轮放大后出现知识点标签、
标签不重叠、悬停提示、点击弹窗和适配复原。页面脚本错误为 0。
Inspector 在 1440 / 768 / 390 为 0 FAIL、0 WARN，无新增例外。
后端总图单元/API 测试 1 passed；Neo4j 实库集成测试 1 skipped，原因是当前本地没有连接可用的 Neo4j。
源码 lint 的 5 个 WARN 是原有目录小标签和真实悬浮层阴影；0 FAIL。

ROUND 6 (whole-course graph)
Seen in one second: 中央大模块与外围完整知识点圆环。
Idea (one sentence): 让全课程的真实知识点和跨模块联系组成一张可缩放的课程地图。
Live thing: 目录切换、总图探索、语义缩放、完整知识点弹窗和刷新。
Layout words by section: directory=course entry / center=module cluster / perimeter=knowledge circle
Scores: design 7.8 · usability 7.8 · creativity 7.2 · content 8.8 → overall 7.9
Caps applied: 沿用 Framed sheet，不重抽；图谱关系与节点均来自真实数据。
Top three problems:
1. 原来只能逐模块看：增加完整图谱接口，保留跨模块关系与孤立节点。
2. 数百个名称会互相遮挡：总览保留模块名，放大后对知识点标签进行碰撞筛选。
3. 圆环太大容易被角落控件挡住：按真实节点位置和控件边界计算最大可见适配比例。

Remaining limitations: 全图有数百个节点，需放大、悬停或使用目录阅读具体知识点。
Neo4j 实库联调尚未运行；本地可核对的画面和交互使用项目真实快照。未上传或部署。

## 莫兰迪配色、球形节点和彩色目录（用户参考图修订）

按用户四张参考图确定的新要求调整，仅本地保存，未操作 GitHub。
保留 Framed sheet 构图与 seed 1370576991，不重抽；配色、字体由用户明确要求覆盖原始方向。
方向记录标注 keep palette/type；本节取代前文旧版字体和纯色节点的说明。

- 知识点使用浅雾蓝、浅青绿、灰紫、浅灰粉等莫兰迪色，模块使用稳定的九组低饱和色。
  模块节点和目录框条共享颜色，难度颜色与图例一致；文字仍为深色保证阅读。
- SVG 径向渐变形成左上受光、右下稍暗的圆球，不增加中心白点、套环、发光或额外 WebGL 场景。
- 图谱使用低对比点阵和轻微冷色渐变，正文阅读弹窗继续使用白色；总图连线减淡，外围小节点增加细边缘。
- 目录每个大模块变成带“模块”文字标记的浅色框条。侧栏 300px，减少长标题换行；搜索和展开逻辑保留。
- 标题使用本地 Noto Serif SC（600），正文和节点使用 Noto Sans SC，核心知识点字重加强。
  新增宋体课程字库约 207KB，含 OFL 许可证；常规构建和网页运行不依赖外部字体服务。
  字体来源为 Google Fonts 的 Noto Serif SC，许可证见 frontend/public/fonts/Noto-Serif-SC-LICENSE.txt。
- 不复制参考截图中的进度、完成率、考点标签或其他项目内容。未新增装饰图标和外部图片。

用户要求渐变、球形及彩色目录优先于技能默认的纯色限制，检查显式允许 gradient。
原生弹窗延续 covered-text、heavy-shadow 两个局部例外。标题 GIS 黑体字标与中文宋体名称保留为有意的字体分工，
因此 mixed-font-headline 的 1 个 WARN 有明确理由；字体总数仍为两个。

验证：构建、4 个布局测试、Playwright 主流程通过。9 个真实模块的实际标签不重叠；总图 353 节点完整，
四种宽度检查无脚本错误；缩放、拖动、筛选、弹窗导航、Esc/遮罩关闭、加载中关闭继续通过。
总图和弹窗的 inspector 在 1440 / 768 / 390 均为 0 FAIL、1 WARN（上述字标字体分工）。
完整记录与画面在 .taste-skill/morandi-*，字体生成脚本为 frontend/scripts/prepare-heading-font.mjs。

ROUND 7 (Morandi course atlas)
Seen in one second: 浅色球形课程网络与颜色对应的模块框条。
Idea (one sentence): 让课程模块在目录与图谱中共享柔和的识别色，背景作为轻量制图底纸。
Live thing: 原有目录、圆形图谱、全部知识点总图、关系筛选、详情弹窗和精灵问答。
Layout words by section: directory=tinted module strips / graph=spherical circular network / detail=serif-titled reading dialog
Scores: design 8.1 · usability 7.9 · creativity 7.5 · content 8.8 → overall 8.1
Caps applied: 用户明确授权浅渐变、球体明暗和彩色框条，保持正文对比度与两种字体。
Top three problems:
1. 旧节点深色且平：改为多数浅色的莫兰迪色与同一受光方向的球面明暗。
2. 纯白画布单调：增加稀疏低对比点阵与轻渐变，降低总图连线的存在感。
3. 目录和标题层级弱：目录与模块共享颜色，标题改用宋体，核心知识点字重加深。

Remaining limitations: 全部知识点总图中最小节点需放大查看球面和名称；手机总览以结构为主。
用户已保存的精灵位置仍然保留，可以拖动避开目录。未提交、推送或部署。

## 有样本依据的暖色阅读分区与单圈模块图

按本轮三条浏览器批注调整。先检索并读取真实样本，再实现，仍未提交、推送或部署。

参考与采用部分（未安装新 UI 库、未复制示例内容）：

- Radix Card：https://www.radix-ui.com/themes/docs/components/card
  采用把相关信息与操作组织进有边界容器的方式。详情元数据为四个浅暖色信息卡，
  说明、学习路径、关联知识、教学资源分别置于暖白内容框中，保留全部文字与资源。
- Radix Colors / Sand：https://www.radix-ui.com/colors
  色阶用途：https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale
  借鉴背景、组件底色、边框与文字分级用色的方法；本项目改为低饱和燕麦、暖灰、浅杏，
  具体色值按现有莫兰迪风格适配，没有把默认蓝色示例直接套入。
- Radix Callout：https://www.radix-ui.com/themes/docs/components/callout
  采用简短提示、操作按钮的结构；精灵建议增加“学习小提示”标题、浅杏底、暖色边框和操作按钮。
- AntV Circular：https://g6.antv.antgroup.com/manual/layout/circular-layout
  补充示例：https://x6.antv.vision/en/examples/layout/general/circle/
  采用相同半径上的外围节点布局，取消模块内原先的内外两圈。为中文外置标签保留纵向间距，
  顶部和底部增加对齐位置；模块居中，所有小知识点缩至半径 18/22，仍保留球面效果。

验证：生产构建、4 个布局测试及 Playwright 主流程通过。布局测试增加“模块内全部小知识点同半径”断言；
全部 9 个模块的实际浏览器标签检查无重叠。四种宽度的弹窗边距、原图视口保留、前后导航、
焦点范围、Esc、遮罩关闭和加载中关闭验证继续通过，目录、资源、聊天检查无脚本异常或横向溢出。
Inspector 三种宽度为 0 FAIL、3 WARN：既有 GIS 与中文标题的字体分工；用户明确要求可见边框，
暖色边框对比约 1.45–1.59；以及弹窗/分区/内部卡片/控件各自的嵌套圆角。均为当前设计的明确取舍。
允许的 gradient、covered-text、heavy-shadow 延续此前用户授权；palette-cream 对应本轮明确要求暖色阅读面。

ROUND 8 (reference-led warm cards and single orbit)
Seen in one second: 暖色分区阅读弹窗、完整外围单圈与暖色提示卡。
Idea (one sentence): 用有边界的知识阅读卡组织学习内容，用单圈布局表达模块包含的全部知识点。
Live thing: 目录探索、单圈节点、学习路径、关联导航和精灵建议操作。
Layout words by section: detail=warm grouped cards / graph=one peripheral orbit / suggestion=warm callout
Scores: design 8.1 · usability 8.0 · creativity 7.5 · content 8.8 → overall 8.1
Caps applied: 明确借鉴上述样本的结构，按项目内容改写；保留暖色、边框与既有宋黑字体分工。
Top three problems:
1. 详情缺少分区边界：暖色底与卡片划分元数据、说明、路径和资源。
2. 模块图是两圈且密集：全部小知识点放在同一外围半径，减小尺寸并保留标签间距。
3. 精灵提示缺乏层次：采用 Callout 式标题、提示正文与浅暖色操作按钮。

Remaining limitations: 数十个长名称在全图缩小时字号仍小，需缩放、悬停或目录阅读。没有修改知识内容或关系数据。

## 加宽目录、标题与小迪命名

本轮继续沿用 Framed sheet 方向和莫兰迪色系。先查阅下列真实组件样本，再将结构用于现有课程内容：

- Element Plus Typography：https://element-plus.org/zh-CN/component/typography
  参考清晰的中文无衬线字阶和字重层次；主标题从宋体切换为本地 Noto Sans SC 600，
  桌面中文标题 32px，紧凑屏 28px。小屏按可用宽度调整，GIS 与中文统一字体。
- Radix Card：https://www.radix-ui.com/themes/docs/components/card
  参考同一卡片内的标题、次级描述层次。桌面目录由 300px 加宽到 332px，
  抽屉由 340px 加宽到最多 380px，每个模块新增一行与课程内容对应的简短介绍。
  标题 15px/600，简介 12px/400，沿用模块各自的柔和底色与深色文字。
- Radix Button：https://www.radix-ui.com/themes/docs/components/button
  参考 solid 按钮。紧凑屏“目录”改为与站点强调色一致的实心青灰色，保持 44px 点击目标。

精灵统一命名为“小迪”：模型下方加小名牌，学习提示、聊天工具栏、问答标题、
助手头像和首次问候共用一个名称常量。名字没有写进每条回复正文，不更改模型和知识数据。
聊天头像扩至 28px 并保持名字同一行。新增文字已补入自托管中文字体字库。

验证：生产构建及 Playwright 目录→图谱→弹窗→问答主流程通过。
额外在 1440×900、755×682（用户批注尺寸）、600×800、390×844 检查目录、标题和聊天，
九个模块简介均为一行，字体加载成功，未见脚本异常或页面横向溢出。
Inspector 总图在 1440/768/390 为 0 FAIL、0 WARN；暖色详情为 0 FAIL、2 WARN。
两个保留提醒是既有的暖色边框/选中目录强调线与分层容器圆角，对应用户要求可见框线和暖色分区。
截图：.taste-skill/xiaodi-directory-755.png、xiaodi-chat-390.png、xiaodi-course/、xiaodi-detail/。
全部修改仅在本地，未提交、推送或部署。

ROUND 9 (descriptive directory and Xiaodi)
Seen in one second: 加粗的大标题、带简介的彩色目录和有名字的小迪。
Idea (one sentence): 让课程目录直接解释模块学什么，让图谱精灵有稳定的称呼。
Live thing: 模块展开、圆形图谱、知识弹窗、精灵建议与问答。
Layout words by section: header=strong sans title / directory=title plus description / companion=named guide
Scores: design 8.1 · usability 8.1 · creativity 7.0 · content 8.8 → overall 7.95
Caps applied: 使用应用屏幕规则；较大标题、彩色模块卡和渐变球体为用户明确选择。
Top three problems:
1. 旧目录缺少模块解释：加宽后加入课程专属简介，不使用虚构进度或数量。
2. 旧主标题层次偏弱：采用更大、更有字重的中文无衬线，保留小号版本说明。
3. 精灵称呼不统一：统一为小迪，并修正窄聊天头像中的双字换行。

Remaining limitations: 窄屏目录需要滚动浏览；全部知识点总图仍需放大读取小节点名称。

## 二维小迪接入本地网页（2026-10-31）

用户确认第一批二维候选后，按要求接入网页，继续仅在本地预览，未上传 GitHub 或部署。
保留既有 Framed sheet、莫兰迪球形图谱、目录和知识点弹窗，不重新抽取设计方向。

- 使用用户确认的 `artifacts/xiaodi-2d/2026-10-31-stage1/xiaodi-static-draft-v3.png`，
  原样复制为 `frontend/public/assets/ai-pet/xiaodi-2d-v1.png`。SHA-256 检查一致，没有额外重绘或改变颜色。
- AIPet 改为透明 PNG 展示，桌面图片框高 200px，手机 180px；保留小迪名牌、拖动、位置记忆、
  点击问答、学习建议、建议开关和引用导航。当前是静态形象，没有宣称已完成眨眼、说话或分层动画。
- 移除组件的 Three.js 初始化、WebGL 渲染循环和模型加载。旧 GLB 文件保留；实际页面不请求它。
  构建产物现为单个应用 JS 和样式，不再生成三维渲染器、GLTF/Draco 的应用加载分块。
- 新默认位置避开目录与底部图例/导航图；保留用户已保存的位置并约束在可见区域。
  问答浮层根据视口定位；提示框测量实际高度，在窄屏缩窄并放在角色旁边。
  较矮手机默认把角色放到左侧。浮层仍会覆盖部分图谱内容，可关闭或拖动角色避让。
- 弹出问答支持 Escape 收起并把焦点还给小迪按钮；图片加载失败时显示“小迪”文字。

验证：生产构建及 Playwright 目录/图谱/详情/问答主流程通过。
额外真实浏览器检查 1440×900、1280×720、755×682、390×844、360×640：
图像请求与确认文件哈希一致，拖动不误开问答，位置刷新后恢复；手机触屏点击可打开问答；
问答框在屏幕内，Escape 关闭；无旧三维资源请求、脚本异常或横向溢出。
默认角色本身不覆盖目录、主工具栏、图例或导航图。
Inspector 总图为 0 FAIL、0 WARN，已查看桌面、平板和手机截图。
检查记录与截图保存在 `artifacts/xiaodi-2d/2026-10-31-integration/`。

ROUND 10 (approved 2D Xiaodi in the course atlas)
Seen in one second: 与确认稿一致的蓝发圆脸小迪，作为图谱旁的问答入口。
Idea (one sentence): 保留已认可的角色外观，让原有课程助手通过轻量二维图像承载。
Live thing: 拖动、位置记忆、问答、学习建议和知识引用。
Layout words by section: graph=unchanged circular atlas / companion=transparent portrait / chat=bounded floating panel
Scores: design 8.1 · usability 8.0 · creativity 7.0 · content 8.8 → overall 7.92
Caps applied: 当前仅接入静态确认稿，不加入新的视觉装饰或未经确认的动画。
Top three problems:
1. 原三维角色与确认形象不同：直接使用用户确认的 PNG 文件。
2. 角色增大后浮层可能遮挡工具栏或超出视口：按画布边界与浮层实际尺寸定位。
3. 手机沿用整体缩放导致聊天文字偏小：使用独立图片尺寸，问答文字保持正常字号。

Remaining limitations: 翅膀膜沿用已确认稿的偏不透明表现；尚未制作分层动画。小屏浮动助手和提示仍会遮住部分图谱，可拖动或关闭提示。
