# 入门知识点澄清与本地修订

日期：2026-11-02。已处理9类问题，修订16个知识点，包含6个同主题相邻条目。本文按“怎样理解—例子—修订正文—依据”说明。

## 处理范围

本轮修订本地知识点快照和配套Cypher，保留全部知识点ID、难度、重要性、排序和图谱关系。未写入运行中的Neo4j，未上传或发布。未重做全图344个知识点的审计。

## 九项澄清概览

| 问题 | 涉及知识点 | 核心澄清 |
| --- | --- | --- |
| ERR-01 | M1-014、M7-014 | 尽端不是错误的同义词；要检查的是“不该断却断了”的位置。 |
| ERR-02 | M4-006、M4-007 | 比较的是从起点累积到候选节点的成本；首次看到终点时还不能停。 |
| ERR-03 | M3-017、M7-010 | 坐标的参考说明、地图显示和坐标转换是三件事；不能用改标签代替转换。 |
| ERR-04 | M1-015 | 画在一起、网络接上、车辆能走，分别是不同层次的判断。 |
| ERR-05 | M3-021 | 设计参数、允许开多快、实际怎么跑不能混为一谈；运行速度的统计指标也不必然是全程平均速率。 |
| ERR-06 | M3-024 | 时间成本既可以直接给出，也可以按明确假设推算；“固定”不等于“用设计速度”。 |
| ERR-07 | M1-002、M1-013 | 不是把“矢量”和“路网”对立起来，而是确认数据和规则是否足以回答交通问题。 |
| ERR-08 | M1-004、M1-005、M1-006 | 数据模型决定表达方式，不单独决定数据是否准确。 |
| ERR-09 | M7-013、M7-011 | 先使用已明确版本和参数的原生算法；不要把不存在具体说明的插件当成必装条件。 |

## ERR-01 · M1-014、M7-014

### M1-014 · 路网连通性拓扑规则

**怎样理解：** 尽端不是错误的同义词；要检查的是“不该断却断了”的位置。

**教学例子（自拟）：** 一条通往小区尽头的道路可正常保留；本应接入路口却少画一小段的道路则需核查修复。

**原文：**

> 路网连通性拓扑规则是保障路网可进行网络分析的基础规则，要求所有道路边必须通过节点实现连接，禁止出现线段悬空、端点不重合等情况；同一条道路的分段端点必须共享同一节点，确保交通流可以在路网中连续传递。

**修订后的完整正文：**

路网连通性应依据真实道路及建网规则建立，重点检查本应连接却断开的路段、端点错接等非预期错误。真实尽端路可以只有一条路段接入，隔离路段也不一定属于数据错误；不能为消除悬挂端点而虚构连接。使用“不得有悬挂”等拓扑检查规则时，应按数据规范审核并记录合法例外。节点是否连接还须结合端点或顶点连接策略、容差及层级等条件判断。

**直接依据：**

- [S12 · Esri：Add Rule To Topology](https://pro.arcgis.com/en/pro-app/3.4/tool-reference/data-management/add-rule-to-topology.htm)；ArcGIS Pro 3.4；Must Not Have Dangles (Line)；访问：2026-11-02。
- [S28 · QGIS：Topology Checker Plugin](https://docs.qgis.org/3.44/en/docs/user_manual/plugins/core_plugins/plugins_topology_checker.html)；QGIS 3.44；25.2.5 开头规则适用性说明；Line rules；访问：2026-11-02。
- [S11 · Esri：Understanding connectivity](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/understanding-connectivity.html)；ArcGIS Pro 在线文档，访问日版本；Connectivity policies；Using elevation fields；访问：2026-11-02。
### M7-014 · QGIS路网拓扑清洗批量操作

**怎样理解：** 清洗是修复不符合真实道路和规范的错误，不是把所有检查标记都消掉。

**教学例子（自拟）：** 捕捉距离过大时，相邻却不连通的道路可能被错接；批量处理后必须检查这种变化。

**原文：**

> 使用几何处理工具，批量执行删除重复几何、合并线段、捕捉节点，批量修复悬挂节点、重复线段等拓扑问题。

**修订后的完整正文：**

QGIS路网清洗应先按数据规范识别重复几何、非预期断裂、错接等问题，再选择适合的修复方法。删除重复、合并或捕捉会改变数据，批量操作前应保留原始数据并设定合理容差，处理后抽查实际连接和属性。真实尽端路可能是合法悬挂，不应全部自动连接或删除；桥上桥下、平行道路等也不能仅因位置接近就被捕捉为可通行连接。拓扑检查输出是待核实的问题线索，不等于每条记录都应采用同一种自动修复。

**直接依据：**

- [S28 · QGIS：Topology Checker Plugin](https://docs.qgis.org/3.44/en/docs/user_manual/plugins/core_plugins/plugins_topology_checker.html)；QGIS 3.44；25.2.5 开头规则适用性说明；Line rules；访问：2026-11-02。
- [S12 · Esri：Add Rule To Topology](https://pro.arcgis.com/en/pro-app/3.4/tool-reference/data-management/add-rule-to-topology.htm)；ArcGIS Pro 3.4；Must Not Have Dangles (Line)；访问：2026-11-02。
- [S11 · Esri：Understanding connectivity](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/understanding-connectivity.html)；ArcGIS Pro 在线文档，访问日版本；Connectivity policies；Using elevation fields；访问：2026-11-02。

## ERR-02 · M4-006、M4-007

### M4-006 · Dijkstra最短路径算法原理与路网适配

**怎样理解：** 比较的是从起点累积到候选节点的成本；首次看到终点时还不能停。

**教学例子（自拟）：** S→T耗时10分钟，S→A和A→T各2分钟：先发现的10分钟可被更新为4分钟。

**原文：**

> Dijkstra算法是经典单源最短路径算法，原理是从起点出发，采用贪心策略逐步扩展距离最短的节点，直到到达终点，得到起点到所有节点的最短路径。路网适配时将节点作为图顶点、路段阻抗作为边权重，是路网路径分析的基础算法。

**修订后的完整正文：**

Dijkstra是单源最短路径算法。本课采用边权固定且全部非负的模型，边权可以为0；“最短”指累计成本最小，成本可为距离或时间。算法从源点成本0开始，每次确定累计暂定成本最小的未确定节点，再检查经该节点到邻点是否更便宜，若更便宜便更新暂定值（松弛）。首次发现终点不等于已得到最优答案。只求一个目标时，可在该目标被按最小暂定成本取出并确定后结束；求全部可达节点时须继续处理，直到没有可达候选。不可达节点没有有限的最短成本，等成本最优路线也可能不唯一。

**直接依据：**

- [S18 · NetworkX：Dijkstra](https://networkx.org/documentation/stable/reference/algorithms/shortest_paths/dijkstra.html)；NetworkX 3.7 在线 stable；Dijkstra’s algorithm；访问：2026-11-02。
- [S19 · NetworkX：single_source_dijkstra](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.single_source_dijkstra.html)；NetworkX 3.7 在线 stable；Parameters / Returns / Notes；访问：2026-11-02。
- [S27 · MIT 6.006：Lecture 13, Dijkstra’s Algorithm](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/d819e7f4568aced8d5b59e03db6c7b67_MIT6_006S20_lec13.pdf)；2020 春季课程；第1页 Non-negative Edge Weights；第2–4页算法与正确性；访问：2026-11-02。
### M4-007 · Dijkstra算法在大规模路网的优化要点

**怎样理解：** 使用堆通常能改进选点效率，但不能直接承诺任何网络都近似线性。

**教学例子（自拟）：** 报告算法性能时应说明节点数、边数和实现方式，而不是只写“优化后O(n)”。

**原文：**

> 大规模路网下Dijkstra算法优化要点包括：采用优先队列（堆）优化节点提取效率、建立空间索引减少搜索范围、双向搜索降低搜索规模、分层次路网分级搜索。通过优化可将算法复杂度从O(n²)降至近似O(n)，支撑城市级以上路网计算。

**修订后的完整正文：**

Dijkstra的效率取决于图规模、数据结构和查询范围。设V为节点数、E为边数，朴素选点实现通常为O(V²+E)，常见二叉堆实现为O((V+E)log V)，不能概括成对任意路网都从O(n²)降为近似O(n)。空间索引可辅助定位或候选检索；双向、分层等路由方法还需各自明确适用前提、预处理及正确停止条件。本课仅要求理解固定非负成本的基本算法，不把高级优化方法当作无需验证的性能或正确性保证。

**直接依据：**

- [S18 · NetworkX：Dijkstra](https://networkx.org/documentation/stable/reference/algorithms/shortest_paths/dijkstra.html)；NetworkX 3.7 在线 stable；Dijkstra’s algorithm；访问：2026-11-02。
- [S27 · MIT 6.006：Lecture 13, Dijkstra’s Algorithm](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/d819e7f4568aced8d5b59e03db6c7b67_MIT6_006S20_lec13.pdf)；2020 春季课程；第1页 Non-negative Edge Weights；第2–4页算法与正确性；访问：2026-11-02。

## ERR-03 · M3-017、M7-010

### M3-017 · 路网坐标属性与空间定位规则

**怎样理解：** 坐标的参考说明、地图显示和坐标转换是三件事；不能用改标签代替转换。

**教学例子（自拟）：** 把经纬度图层的标签直接改成米制投影，不会让经纬度数字自动变成正确的米制坐标。

**原文：**

> 路网坐标属性存储道路的空间坐标信息，需遵循对应坐标系的定位规则，保证坐标精度与投影一致性。空间定位规则要求同一数据集采用统一坐标系，节点坐标精确重合，避免坐标偏移导致的拓扑错误与空间匹配误差。

**修订后的完整正文：**

道路坐标必须连同正确的坐标参考系（CRS）、单位及必要元数据解释，不能只凭坐标数值或视觉重合判断定位正确。经纬度采用角度，投影坐标采用线性单位，但不一定是米。QGIS中指定图层CRS是说明现有坐标属于什么系统，不改变源几何坐标数值；修改项目CRS主要改变显示参考；重投影才执行坐标转换。不同已知CRS的数据可动态叠加显示。空间分析前还须按工具要求确认分析CRS、单位及平面或椭球测量方法；建网连接也须遵循容差和层级规则，不是二维坐标重合就一定可通行。

**直接依据：**

- [S05 · QGIS：Working with Projections](https://docs.qgis.org/3.44/en/docs/user_manual/working_with_projections/working_with_projections.html)；QGIS 3.44；6.2 Layer CRS、6.3 Project CRS；访问：2026-11-02。
- [S06 · Esri：Coordinate systems and projections](https://doc.esri.com/en/arcgis-pro/latest/help/mapping/properties/coordinate-systems-and-projections.html)；ArcGIS Pro 在线文档，访问日版本；Coordinate systems；访问：2026-11-02。
- [S07 · PROJ：Cartographic projection / Units](https://proj.org/en/stable/usage/projections.html)；PROJ 9.9.0 在线 stable；Units；访问：2026-11-02。
- [S08 · QGIS：2D Map View / Measuring](https://docs.qgis.org/3.44/en/docs/user_manual/map_views/map_view.html#measuring)；QGIS 3.44；7.1.8.1–7.1.8.2；访问：2026-11-02。
- [S24 · QGIS：Vector general / Reproject layer](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#reproject-layer)；QGIS 3.44；24.1.25.1 Assign projection；24.1.25.16 Find projection；24.1.25.25 Reproject layer；访问：2026-11-02。
- [S26 · Esri：Define Projection](https://pro.arcgis.com/en/pro-app/3.3/tool-reference/data-management/define-projection.htm)；ArcGIS Pro 3.3；Usage；访问：2026-11-02。
- [S11 · Esri：Understanding connectivity](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/understanding-connectivity.html)；ArcGIS Pro 在线文档，访问日版本；Connectivity policies；Using elevation fields；访问：2026-11-02。
### M7-010 · QGIS路网数据加载与坐标系配置

**怎样理解：** 加载后先核实参考；只有任务需要时才转换数据，并检查具体分析参数。

**教学例子（自拟）：** 一份经纬度图层和一份投影图层可以共同显示；计算距离前仍须确认测量方法和单位。

**原文：**

> 导入路网矢量图层；设置项目CRS坐标系；执行坐标转换，保证全部路网图层空间参考统一。

**修订后的完整正文：**

在QGIS加载路网图层后，先核实数据来源、图层CRS和坐标单位；如果CRS未知或标错，先查证真实CRS，再纠正指定。项目CRS控制共同显示参考，已知CRS的图层可通过动态投影叠加，无须仅为显示而重写所有源文件。需要统一分析参考或输出坐标时，使用重投影执行转换，并检查适用范围、坐标转换及输出单位。显示叠加成功不代表测量或网络分析参数已经正确，还应核实具体工具的CRS、椭球和平面设置、方向字段及成本策略。

**直接依据：**

- [S05 · QGIS：Working with Projections](https://docs.qgis.org/3.44/en/docs/user_manual/working_with_projections/working_with_projections.html)；QGIS 3.44；6.2 Layer CRS、6.3 Project CRS；访问：2026-11-02。
- [S08 · QGIS：2D Map View / Measuring](https://docs.qgis.org/3.44/en/docs/user_manual/map_views/map_view.html#measuring)；QGIS 3.44；7.1.8.1–7.1.8.2；访问：2026-11-02。
- [S24 · QGIS：Vector general / Reproject layer](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#reproject-layer)；QGIS 3.44；24.1.25.1 Assign projection；24.1.25.16 Find projection；24.1.25.25 Reproject layer；访问：2026-11-02。
- [S13 · QGIS：Network analysis](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html)；QGIS 3.44；Shortest path (point to point) / Strategy、Direction、Speed；访问：2026-11-02。

## ERR-04 · M1-015

### M1-015 · 路网几何相邻与拓扑连通的区别

**怎样理解：** 画在一起、网络接上、车辆能走，分别是不同层次的判断。

**教学例子（自拟）：** 两段道路共享路口，但题设禁止左转时，该左转动作仍不可用。

**原文：**

> 几何相邻指两条道路在空间位置上靠近、重叠或交叉，但未建立节点连接关系，不具备交通连通性；拓扑连通指两条道路通过共同节点建立了逻辑连接关系，车辆可在二者之间通行。二者的核心区别在于是否存在节点级的逻辑连接与通行语义。

**修订后的完整正文：**

道路在二维图面上接近、重叠或交叉，属于几何位置关系，不自动证明网络中存在连接。拓扑连接需按照实际连接和建网策略建立节点或其他逻辑连接；例如无匝道的桥上、桥下道路不能仅因图面交叉而互相转入。即使两条边已经共享逻辑节点，判断某车辆能否从一条转入另一条，还须同时满足通行方向、转向、出行方式及其他适用限制。因此，几何交叉、逻辑连接和合法通行应分别检查。

**直接依据：**

- [S10 · Esri：Network elements](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/network-elements.html)；ArcGIS Pro 在线文档，访问日版本；Edges、Junctions、Turns；访问：2026-11-02。
- [S11 · Esri：Understanding connectivity](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/understanding-connectivity.html)；ArcGIS Pro 在线文档，访问日版本；Connectivity policies；Using elevation fields；访问：2026-11-02。
- [S15 · Esri：Restriction attributes](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/restriction-attributes.html)；ArcGIS Pro 在线文档，访问日版本；Restriction usage、Parameters；访问：2026-11-02。

## ERR-05 · M3-021

### M3-021 · 设计速度、限速与运行速度的区别

**怎样理解：** 设计参数、允许开多快、实际怎么跑不能混为一谈；运行速度的统计指标也不必然是全程平均速率。

**教学例子（自拟）：** 题目另给平均行驶速率30千米/小时，即应据此计算；不能自行替换为路牌上的另一个数值。

**原文：**

> 设计限速是道路工程设计的最高时速标准，由道路等级与线形条件决定；实际限速是交通管制设定的实时限速值，可能因施工、天气、管制等低于设计限速。二者需分字段存储，分别适配路网规划与实际运行分析场景。

**修订后的完整正文：**

设计速度是道路设计采用的技术参数；限速是在适用条件下对车辆通行速度的约束；运行速度描述车辆在规定观测或分析条件下的运行特征，使用时应说明统计口径。三者不能互作同义词，限速也不等于车辆每次行程的实际平均速率。建库时应区分设计速度、适用限速及其时段和车型条件、观测或估计速度；观测速度还应记录采样时段、车辆范围、统计方法和单位。计算旅行时间时，使用与任务匹配的平均行驶速率或旅行时间数据，不应无条件代入设计速度或限速。具体道路的限速及例外须依国内现行适用规定和现场条件核定，本知识点不提供统一的真实限速数值。

**直接依据：**

- [CN01 · 交通运输部：《公路限速标志设计规范》解读](https://xxgk.mot.gov.cn/jigou/glj/202007/t20200722_3436356.html)；2020-07-22；JTG/T 3381-02—2020的官方解读；三、主要内容（一）及（二）至（四）；访问：2026-11-02。
- [S22 · OpenStax Physics：Speed and Velocity](https://openstax.org/books/physics/pages/2-2-speed-and-velocity)；Physics 在线教材，访问日版本；2.2 Speed，平均速度与距离/时间关系；访问：2026-11-02。
- [S23 · FHWA：Relationship between Design Speed and Posted Speed](https://www.fhwa.dot.gov/design/standards/151007.cfm)；2015-10-07 备忘录；页面更新2017-09-18；Design speed / operating speed / posted speed；访问：2026-11-02。

## ERR-06 · M3-024

### M3-024 · 道路通行时间阻抗属性定义

**怎样理解：** 时间成本既可以直接给出，也可以按明确假设推算；“固定”不等于“用设计速度”。

**教学例子（自拟）：** 2千米、平均速率40千米/小时，对应3分钟；若另有一次1分钟等待且前值未含等待，总计4分钟。

**原文：**

> 通行时间阻抗指车辆通过路段所需的时间，由路段长度与行驶车速决定，是路网路径分析最常用的阻抗形式。静态时间阻抗基于设计限速计算，动态时间阻抗结合实时路况更新。该属性是最优路径规划、交通分配的核心参数。

**修订后的完整正文：**

通行时间阻抗表示通过路段或完成网络动作所需的时间，是时间最优路径的成本。固定教学模型可用给定路程除以与该路程匹配的平均行驶速率计算，也可直接采用经核实的固定耗时。路线总时间应累计各段耗时及明确计入的等待、转向等延误，统一单位，并避免把已包含在耗时中的延误再次加入。静态成本是本次分析中视为固定的成本，不要求一律根据设计速度或限速计算；随时段或交通状态变化的成本，应另说明历史估计、实时观测或预测等来源及其时间条件。

**直接依据：**

- [S14 · Esri：Cost attributes](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/cost-attributes.html)；ArcGIS Pro 在线文档，访问日版本；Cost attributes；访问：2026-11-02。
- [S17 · Esri：Historical traffic](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/historical-traffic.html)；ArcGIS Pro 在线文档，访问日版本；Historical traffic profiles；访问：2026-11-02。
- [S22 · OpenStax Physics：Speed and Velocity](https://openstax.org/books/physics/pages/2-2-speed-and-velocity)；Physics 在线教材，访问日版本；2.2 Speed，平均速度与距离/时间关系；访问：2026-11-02。
- [CN01 · 交通运输部：《公路限速标志设计规范》解读](https://xxgk.mot.gov.cn/jigou/glj/202007/t20200722_3436356.html)；2020-07-22；JTG/T 3381-02—2020的官方解读；三、主要内容（一）及（二）至（四）；访问：2026-11-02。

## ERR-07 · M1-002、M1-013

### M1-002 · 道路几何展示与交通网络分析的区别

**怎样理解：** 不是把“矢量”和“路网”对立起来，而是确认数据和规则是否足以回答交通问题。

**教学例子（自拟）：** 同样的道路线几何，若没有方向和成本说明，不能直接据此承诺得到合法最快驾车路线。

**原文：**

> 普通地理矢量数据仅表达道路的几何形态与基础属性，侧重空间位置呈现；GIS交通路网在此基础上新增了拓扑关系、通行规则、阻抗属性等交通专属语义，支持路径规划、连通性分析、交通分配等专业运算。二者的核心差异在于是否具备完整的交通语义与网络分析能力。

**修订后的完整正文：**

道路几何展示主要回答道路在哪里、形态如何；可求解的交通网络还需具备并正确解释连接、通行方向、转向或车辆限制及距离、时间等成本。矢量数据本身可以承载这些属性，也可以参与拓扑和网络建模，不能仅凭“矢量”二字断定其只有几何或缺少交通语义。能否开展可靠路径分析，取决于信息是否完整、规则是否适用及建网配置是否正确，而不是地图看起来是否像路网。

**直接依据：**

- [S02 · QGIS：Vector Data](https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/vector_data.html)；QGIS 3.44；3.1、3.2、3.5；访问：2026-11-02。
- [S10 · Esri：Network elements](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/network-elements.html)；ArcGIS Pro 在线文档，访问日版本；Edges、Junctions、Turns；访问：2026-11-02。
- [S13 · QGIS：Network analysis](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html)；QGIS 3.44；Shortest path (point to point) / Strategy、Direction、Speed；访问：2026-11-02。
- [S14 · Esri：Cost attributes](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/cost-attributes.html)；ArcGIS Pro 在线文档，访问日版本；Cost attributes；访问：2026-11-02。
### M1-013 · 交通路网拓扑关系的核心定义

**怎样理解：** 几何可用于判断如何建网；建好网络后，还要按逻辑连接及通行规则分析。

**教学例子（自拟）：** 桥上桥下的线可以相交，但没有实际连接时，不应仅凭交叉新增转向。

**原文：**

> 交通路网拓扑关系是指路网要素之间基于连接性的空间逻辑关系，不依赖具体坐标位置，核心包括节点与边的关联关系、边与边的连通关系、转向约束关系等。拓扑关系是路网区别于普通道路矢量数据的核心特征，是所有网络分析的基础。

**修订后的完整正文：**

路网拓扑以节点与边的关联等逻辑关系表达网络连接。建网时可结合几何端点、顶点、连接容差及高程或层级规则判断应有连接；网络建立后，路径分析按这些连接关系求解，不能把二维线条交叉直接当成连接。合法通行还需结合方向、转向和车辆等规则。拓扑和交通属性可以由矢量数据及其配套结构承载，不宜笼统认定普通矢量不能表达拓扑。

**直接依据：**

- [S10 · Esri：Network elements](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/network-elements.html)；ArcGIS Pro 在线文档，访问日版本；Edges、Junctions、Turns；访问：2026-11-02。
- [S11 · Esri：Understanding connectivity](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/understanding-connectivity.html)；ArcGIS Pro 在线文档，访问日版本；Connectivity policies；Using elevation fields；访问：2026-11-02。
- [S15 · Esri：Restriction attributes](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/restriction-attributes.html)；ArcGIS Pro 在线文档，访问日版本；Restriction usage、Parameters；访问：2026-11-02。
- [S02 · QGIS：Vector Data](https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/vector_data.html)；QGIS 3.44；3.1、3.2、3.5；访问：2026-11-02。

## ERR-08 · M1-004、M1-005、M1-006

### M1-004 · 路网空间数据的两大核心载体：矢量模型、栅格模型

**怎样理解：** 数据模型决定表达方式，不单独决定数据是否准确。

**教学例子（自拟）：** 站点位置可用点，道路中心线可用线，高程可用像元网格；三者都仍需检查采集质量及适用尺度。

**原文：**

> 矢量模型以点、线、面几何要素表达路网，精度高、属性丰富，适合拓扑分析与精细化建模；栅格模型以像元网格表达路网空间，计算简便、适合叠加分析与宏观模拟。二者是路网空间数据的基础表达形式，分别适配不同尺度与不同类型的交通分析场景。

**修订后的完整正文：**

矢量与栅格是两种常见空间表达模型。矢量用点、线、面及属性表达离散要素，常用于道路中心线、节点及其关系建模；栅格用规则行列像元及其值表达影像、连续表面或空间成本等信息。应根据对象、比例尺、分辨率、数据质量和分析任务选择，不能笼统认定矢量永远更准确或栅格只适合低精度工作。同一现实对象也可随表达目的和尺度采用不同模型或几何。

**直接依据：**

- [S02 · QGIS：Vector Data](https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/vector_data.html)；QGIS 3.44；3.1、3.2、3.5；访问：2026-11-02。
- [S03 · QGIS：Raster Data](https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/raster_data.html)；QGIS 3.44；6.1–6.2；访问：2026-11-02。
### M1-005 · 矢量路网模型的优势与适用场景

**怎样理解：** 矢量便于管理路段及其关系，但不会自动获得高精度和正确拓扑。

**教学例子（自拟）：** 一条偏移明显的道路即使保存为矢量线，位置仍可能不准确。

**原文：**

> 矢量路网模型采用节点-线段的离散化表达，优势在于定位精度高、属性存储灵活、拓扑关系清晰，可精准表达道路等级、车道数、限速等属性。适用于城市级精细化路网建模、路径规划、拓扑检查、交通设施管理等需要高精度空间表达的场景。

**修订后的完整正文：**

矢量路网可用线要素表示道路中心线，以属性表记录道路等级、长度、方向等信息，并通过节点关联或建网规则组织连接。它便于逐路段属性管理、路径分析和拓扑检查；但定位精度取决于原始采集质量、比例尺和处理过程，不由“矢量”模型自动保证。道路画成线也不意味着连接、方向和通行规则已经正确，使用前仍需核实。

**直接依据：**

- [S02 · QGIS：Vector Data](https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/vector_data.html)；QGIS 3.44；3.1、3.2、3.5；访问：2026-11-02。
- [S10 · Esri：Network elements](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/network-elements.html)；ArcGIS Pro 在线文档，访问日版本；Edges、Junctions、Turns；访问：2026-11-02。
- [S13 · QGIS：Network analysis](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html)；QGIS 3.44；Shortest path (point to point) / Strategy、Direction、Speed；访问：2026-11-02。
### M1-006 · 栅格路网模型的优势与适用场景

**怎样理解：** 栅格不是低精度的同义词；要检查像元尺度是否能表达本次问题。

**教学例子（自拟）：** 使用高程栅格分析道路周边地形时，应核实分辨率和高程质量，而不是仅因它是栅格就否定。

**原文：**

> 栅格路网模型将路网空间划分为规则像元网格，用像元值表达道路通行状态，优势在于计算逻辑简单、易于与遥感影像叠加、适合批量栅格运算。适用于区域宏观路网密度分析、可达性栅格计算、灾害损毁路网模拟等大尺度、低精度需求的分析场景。

**修订后的完整正文：**

栅格路网及相关环境数据用规则像元记录通行状态、空间成本、高程或其他值，便于与影像、连续表面进行叠加和栅格运算，可用于可达性、成本表面及灾害影响等任务。是否适用取决于分析目标、像元分辨率和数据质量，不能把栅格简单等同于低精度或仅适用于宏观分析。需要细分路段方向、转向或车辆约束时，应另行说明模型如何表达这些条件。

**直接依据：**

- [S03 · QGIS：Raster Data](https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/raster_data.html)；QGIS 3.44；6.1–6.2；访问：2026-11-02。
- [S02 · QGIS：Vector Data](https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/vector_data.html)；QGIS 3.44；3.1、3.2、3.5；访问：2026-11-02。

## ERR-09 · M7-013、M7-011

### M7-013 · QGIS原生网络分析与节点—边模型应用

**怎样理解：** 先使用已明确版本和参数的原生算法；不要把不存在具体说明的插件当成必装条件。

**教学例子（自拟）：** 同一网络分别选择距离最短和时间最少，结果可以不同；错误的方向编码也可能让路线不可用。

**原文：**

> 利用Graph插件读取路网图层；构建节点‑边图模型；配置阻抗字段，执行网络路径计算。

**修订后的完整正文：**

QGIS 3.44可使用处理工具箱中的原生网络分析算法，例如Shortest path (point to point)，以道路线图层为网络输入，指定起终点，并按字段及对应编码解释通行方向。选择距离最短或时间最少策略，时间策略还须正确配置速度字段及其单位或合理默认值；同时核实连接容差、测量设置及数据是否表达实际连通。算法结果应结合已知路线与约束验证，不能只凭软件成功输出就认定正确。此流程不要求安装一个未指明的“Graph插件”；若另用插件，应另列插件全名、版本、来源和用途。

**直接依据：**

- [S13 · QGIS：Network analysis](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html)；QGIS 3.44；Shortest path (point to point) / Strategy、Direction、Speed；访问：2026-11-02。
- [S08 · QGIS：2D Map View / Measuring](https://docs.qgis.org/3.44/en/docs/user_manual/map_views/map_view.html#measuring)；QGIS 3.44；7.1.8.1–7.1.8.2；访问：2026-11-02。
- [S11 · Esri：Understanding connectivity](https://doc.esri.com/en/arcgis-pro/latest/help/analysis/networks/understanding-connectivity.html)；ArcGIS Pro 在线文档，访问日版本；Connectivity policies；Using elevation fields；访问：2026-11-02。
### M7-011 · QGIS网络分析工具与可选插件的选择

**怎样理解：** 原生功能和可选插件应分清；插件必须能明确识别和复现。

**教学例子（自拟）：** 本课用原生点到点路径算法时，无须为了开始计算而安装一个只被笼统称为Graph的插件。

**原文：**

> 安装Graph、NetworkAnalysis等第三方插件；借助插件实现最短路径、服务区等路网网络分析功能。

**修订后的完整正文：**

QGIS 3.44提供原生网络分析处理算法，可用于最短或最快路径和服务区等任务，不必先安装未明确名称的第三方“Graph”或“NetworkAnalysis”插件。先根据教学任务核对原生工具是否满足需求。确需额外插件时，应给出插件全名、版本、可靠安装来源、与QGIS版本的兼容性及其补充功能，再按具体插件文档安装和验证；不能把模糊插件称呼作为统一的学习前提。

**直接依据：**

- [S13 · QGIS：Network analysis](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html)；QGIS 3.44；Shortest path (point to point) / Strategy、Direction、Speed；访问：2026-11-02。

## 习题对齐与验证

- 本轮修订落实原题库使用的正确限定结论，54道题的答案无需改动，23个定量/路线模型已另行复算通过。
- M1-002标题改为“道路几何展示与交通网络分析的区别”。题库对齐版已同步L01-E03的名称引用；ID和考查目标不变。
- M3-021、M7-011、M7-013标题一并澄清。它们未被原题库直接绑定为主辅知识点，不影响现有题号或判题。
- 原题库与原核查报告保留为编制时的历史记录；其中“未修订”的状态在当时成立。本轮最新处理状态见本文及结构化清单，不修改旧指纹冒充重新发布。
- 原图谱完整备份保存在本轮artifacts的before目录，可核对修订前后的事实及原题库基线。

## 文件与后续使用

- 当前本地知识点：[data/graph-snapshot.json](E:/gis-knowledge-platform/data/graph-snapshot.json)。
- 配套导入文件：[data/knowledge-points.cypher](E:/gis-knowledge-platform/data/knowledge-points.cypher)。
- 逐条原文、修订、来源和验证清单：[data/knowledge-clarifications-2026-11-02.json](E:/gis-knowledge-platform/data/knowledge-clarifications-2026-11-02.json)。
- 题库对齐版（1.0.1，仅同步知识点名称、来源及本地处理状态）：[artifacts/knowledge-clarifications/2026-11-02/question-bank-aligned.json](E:/gis-knowledge-platform/artifacts/knowledge-clarifications/2026-11-02/question-bank-aligned.json)。
- 本轮没有对实际限速值、国内具体坐标系统适用性或完整时变路由算法作新增判题承诺；涉及这些内容还需另行核查具体任务及现行规则。
- 后续发布时需将经审定的数据更新到运行中的数据库；仅提交快照不等于Neo4j内容已同步。再次从旧Excel导入可能覆盖澄清正文，应先按清单同步源表。

修订前快照SHA-256：`3169c5485e2b8e21d714368fd8c9f92fa61ad1f3e086e2ad66366248271782f9`。

修订后快照SHA-256：`ca8e64c6657ab10bdb1af3a9e5cb5ce82e2437451e0780142dd51e10e69e4736`。
