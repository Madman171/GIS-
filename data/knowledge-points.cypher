// GIS交通路网教学知识图谱平台 V1.0
// Generated node import file for KnowledgePoint.

MERGE (node:KnowledgePoint {kp_id: "M1-001"})
SET node = {`difficulty`: "入门", `importance`: "核心", `name`: "GIS交通路网的专业定义与核心研究范畴", `description`: "GIS交通路网是地理信息系统在交通领域的专项应用，以空间地理数据为载体，对道路、节点、交通设施等路网要素进行数字化建模、存储、分析与可视化表达。核心研究范畴涵盖路网拓扑构建、空间分析、动态交通模拟、多模态交通融合等，是交通规划、智慧交通、应急调度等领域的核心技术支撑。", `kp_id`: "M1-001", `sort_order`: 1};

MERGE (node:KnowledgePoint {kp_id: "M1-002"})
SET node = {`difficulty`: "入门", `importance`: "掌握", `name`: "GIS交通路网与普通地理矢量数据的核心区别", `description`: "普通地理矢量数据仅表达道路的几何形态与基础属性，侧重空间位置呈现；GIS交通路网在此基础上新增了拓扑关系、通行规则、阻抗属性等交通专属语义，支持路径规划、连通性分析、交通分配等专业运算。二者的核心差异在于是否具备完整的交通语义与网络分析能力。", `kp_id`: "M1-002", `sort_order`: 2};

MERGE (node:KnowledgePoint {kp_id: "M1-003"})
SET node = {`difficulty`: "入门", `importance`: "熟悉", `name`: "交通路网GIS的服务对象与行业应用边界", `description`: "交通路网GIS的服务对象覆盖交通运输管理部门、城市规划院、智慧交通企业、物流配送企业等主体。其应用边界聚焦于空间维度的交通相关分析，不包含纯交通流理论计算、车辆工程设计等非空间领域，是地理空间技术与交通工程的交叉应用方向。", `kp_id`: "M1-003", `sort_order`: 3};

MERGE (node:KnowledgePoint {kp_id: "M1-004"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网空间数据的两大核心载体：矢量模型、栅格模型", `description`: "矢量模型以点、线、面几何要素表达路网，精度高、属性丰富，适合拓扑分析与精细化建模；栅格模型以像元网格表达路网空间，计算简便、适合叠加分析与宏观模拟。二者是路网空间数据的基础表达形式，分别适配不同尺度与不同类型的交通分析场景。", `kp_id`: "M1-004", `sort_order`: 4};

MERGE (node:KnowledgePoint {kp_id: "M1-005"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "矢量路网模型的优势与适用场景", `description`: "矢量路网模型采用节点-线段的离散化表达，优势在于定位精度高、属性存储灵活、拓扑关系清晰，可精准表达道路等级、车道数、限速等属性。适用于城市级精细化路网建模、路径规划、拓扑检查、交通设施管理等需要高精度空间表达的场景。", `kp_id`: "M1-005", `sort_order`: 5};

MERGE (node:KnowledgePoint {kp_id: "M1-006"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "栅格路网模型的优势与适用场景", `description`: "栅格路网模型将路网空间划分为规则像元网格，用像元值表达道路通行状态，优势在于计算逻辑简单、易于与遥感影像叠加、适合批量栅格运算。适用于区域宏观路网密度分析、可达性栅格计算、灾害损毁路网模拟等大尺度、低精度需求的分析场景。", `kp_id`: "M1-006", `sort_order`: 6};

MERGE (node:KnowledgePoint {kp_id: "M1-007"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "交通路网Node-Edge节点边基础模型定义", `description`: "Node-Edge（节点-边）模型是路网图论表达的基础形式：Node（节点）代表道路交叉口、端点、枢纽等连接点；Edge（边）代表两个节点之间的道路路段。模型通过节点与边的连接关系表达路网拓扑结构，是所有路网空间分析、路径计算的底层数据模型。", `kp_id`: "M1-007", `sort_order`: 7};

MERGE (node:KnowledgePoint {kp_id: "M1-008"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网节点的定义、分类与核心作用", `description`: "路网节点是路网中道路的连接点或端点，按功能可分为交叉口节点、道路端点、匝道节点、枢纽节点等。核心作用是构建路网拓扑连接关系、承载转向规则与交通管制属性、作为路径计算的起止点与中转点，是路网拓扑完整性的关键控制要素。", `kp_id`: "M1-008", `sort_order`: 8};

MERGE (node:KnowledgePoint {kp_id: "M1-009"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网边的定义、分类与核心作用", `description`: "路网边是两个节点之间的道路路段，是路网的线性构成单元，按类型可分为主路、匝道、辅路、桥梁段、隧道段等。核心作用是承载道路长度、等级、限速、通行方向等属性，作为路径阻抗计算与交通流量分配的基本单元，连接节点形成完整路网。", `kp_id`: "M1-009", `sort_order`: 9};

MERGE (node:KnowledgePoint {kp_id: "M1-010"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "无向路网图模型的结构与适用场景", `description`: "无向路网图模型中，道路边不区分通行方向，节点间的连接是双向等价的。模型结构简单、计算量小，适用于步行路网、慢行系统、早期规划阶段的宏观路网连通性分析等不区分通行方向的场景，不适用于城市单向交通路网分析。", `kp_id`: "M1-010", `sort_order`: 10};

MERGE (node:KnowledgePoint {kp_id: "M1-011"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "有向路网图模型的结构与适用场景", `description`: "有向路网图模型中，每条道路边带有方向属性，区分上行与下行方向，可表达单向通行、双向通行等规则。是城市道路交通分析的标准模型，适用于机动车路径规划、交通分配、拥堵分析等需要区分通行方向的绝大多数城市交通场景。", `kp_id`: "M1-011", `sort_order`: 11};

MERGE (node:KnowledgePoint {kp_id: "M1-012"})
SET node = {`difficulty`: "进阶", `importance`: "核心", `name`: "加权路网图模型的权重定义逻辑", `description`: "加权路网图模型为每条路网边赋予权重值，权重可代表距离、通行时间、费用、拥堵程度等阻抗成本。权重定义逻辑需匹配分析目标：最短路径分析采用距离权重，最优时间路径采用时间权重，物流配送分析可采用综合费用权重，是路网分析贴合实际场景的核心设置。", `kp_id`: "M1-012", `sort_order`: 12};

MERGE (node:KnowledgePoint {kp_id: "M1-013"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "交通路网拓扑关系的核心定义", `description`: "交通路网拓扑关系是指路网要素之间基于连接性的空间逻辑关系，不依赖具体坐标位置，核心包括节点与边的关联关系、边与边的连通关系、转向约束关系等。拓扑关系是路网区别于普通道路矢量数据的核心特征，是所有网络分析的基础。", `kp_id`: "M1-013", `sort_order`: 13};

MERGE (node:KnowledgePoint {kp_id: "M1-014"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网连通性拓扑规则", `description`: "路网连通性拓扑规则是保障路网可进行网络分析的基础规则，要求所有道路边必须通过节点实现连接，禁止出现线段悬空、端点不重合等情况；同一条道路的分段端点必须共享同一节点，确保交通流可以在路网中连续传递。", `kp_id`: "M1-014", `sort_order`: 14};

MERGE (node:KnowledgePoint {kp_id: "M1-015"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网几何相邻与拓扑连通的区别", `description`: "几何相邻指两条道路在空间位置上靠近、重叠或交叉，但未建立节点连接关系，不具备交通连通性；拓扑连通指两条道路通过共同节点建立了逻辑连接关系，车辆可在二者之间通行。二者的核心区别在于是否存在节点级的逻辑连接与通行语义。", `kp_id`: "M1-015", `sort_order`: 15};

MERGE (node:KnowledgePoint {kp_id: "M1-016"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网方向性拓扑约束规则", `description`: "路网方向性拓扑约束是有向路网的核心规则，规定每条路网边的通行方向属性，包括双向通行、单向上行、单向下行三类。约束规则需与实际交通管制一致，直接影响路径规划的合法性，错误的方向约束会导致出现逆行路径等分析错误。", `kp_id`: "M1-016", `sort_order`: 16};

MERGE (node:KnowledgePoint {kp_id: "M1-017"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网转向拓扑约束规则", `description`: "路网转向拓扑约束定义了节点处不同进口道与出口道之间的通行权限，包括允许直行、左转、右转、禁止掉头等规则。约束规则存储于节点或节点-边关联关系中，是精细化路径规划、交叉口流量分析的必要条件，直接影响路径计算的真实性。", `kp_id`: "M1-017", `sort_order`: 17};

MERGE (node:KnowledgePoint {kp_id: "M1-018"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网节点重合拓扑规范", `description`: "路网节点重合拓扑规范要求，在同一物理位置的道路端点必须合并为同一个节点，不允许出现坐标接近但相互独立的重复节点。该规范保障路网连通性，避免出现伪节点与连通性断裂，是路网拓扑数据质量检查的基础项。", `kp_id`: "M1-018", `sort_order`: 18};

MERGE (node:KnowledgePoint {kp_id: "M1-019"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网线段无缝衔接拓扑规范", `description`: "路网线段无缝衔接拓扑规范要求，同一条道路的相邻线段端点必须精确重合于同一节点，线段之间无间隙、无重叠、无错位。该规范保障道路的几何连续性与拓扑连通性，避免出现路径断裂、长度计算误差等问题，是路网数据预处理的核心要求。", `kp_id`: "M1-019", `sort_order`: 19};

MERGE (node:KnowledgePoint {kp_id: "M1-020"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "伪节点的拓扑定义与产生原因", `description`: "伪节点是指在道路中间不必要地插入的节点，并非实际交叉口或道路端点，通常由数据采集误差、多源数据拼接、线段拆分操作不当产生。伪节点会增加路网数据冗余、干扰拓扑分析、降低路径计算效率，是路网拓扑清洗的主要处理对象。", `kp_id`: "M1-020", `sort_order`: 20};

MERGE (node:KnowledgePoint {kp_id: "M1-021"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "断头路的拓扑定义与路网缺陷特征", `description`: "断头路指末端节点没有连接其他道路边的孤立路段，属于路网拓扑缺陷。特征表现为路网悬挂节点、路径无法贯通、连通性中断。产生原因包括未建成道路、数据采集遗漏、拓扑连接错误等，会导致路径规划失败、可达性分析结果偏差。", `kp_id`: "M1-021", `sort_order`: 21};

MERGE (node:KnowledgePoint {kp_id: "M1-022"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "重复路网线段的拓扑特征", `description`: "重复路网线段指在同一空间位置存在两条或多条几何重叠、属性一致的道路边，通常由多源数据融合、重复采集产生。拓扑特征表现为同一对节点之间存在多条完全重合的边，会造成数据冗余、路径计算重复、统计结果偏大，需通过拓扑清洗去重。", `kp_id`: "M1-022", `sort_order`: 22};

MERGE (node:KnowledgePoint {kp_id: "M1-023"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "路网悬挂节点的定义与判定标准", `description`: "路网悬挂节点指仅连接一条道路边的节点，即度数为1的节点。判定标准为节点关联的边数量等于1，通常对应道路尽头、断头路端点。合理的悬挂节点是正常路网端点，异常悬挂节点则代表数据缺失或拓扑错误，是路网质量检查的指标之一。", `kp_id`: "M1-023", `sort_order`: 23};

MERGE (node:KnowledgePoint {kp_id: "M1-024"})
SET node = {`difficulty`: "进阶", `importance`: "核心", `name`: "交叉口拓扑建模核心规则", `description`: "交叉口拓扑建模需遵循节点唯一性、转向完整性、车道对应性三大核心规则：同一交叉口用单一节点表达；完整存储各进口道的转向约束；高等级建模需匹配车道级连接关系。模型精度直接决定路径规划、信号配时、交叉口流量分析结果的真实性。", `kp_id`: "M1-024", `sort_order`: 24};

MERGE (node:KnowledgePoint {kp_id: "M1-025"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "匝道与主路拓扑衔接规则", `description`: "匝道与主路拓扑衔接要求匝道端点必须与主路对应节点建立连接，明确驶入、驶出方向，禁止直接与主路路段中间连接。需区分入口匝道、出口匝道的单向属性，匹配主路的通行方向，保障快速路系统的拓扑连通性与通行规则正确性。", `kp_id`: "M1-025", `sort_order`: 25};

MERGE (node:KnowledgePoint {kp_id: "M1-026"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "桥梁路网拓扑独立建模逻辑", `description`: "桥梁路网拓扑独立建模指将桥梁段作为独立的路网边进行管理，单独标注桥梁属性（荷载、限高、桥名等），两端通过节点与普通道路连接。逻辑上与地面道路分层，避免与桥下道路产生错误拓扑连接，保障多层路网的拓扑正确性。", `kp_id`: "M1-026", `sort_order`: 26};

MERGE (node:KnowledgePoint {kp_id: "M1-027"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "隧道路网拓扑独立建模逻辑", `description`: "隧道路网拓扑独立建模将隧道段作为独立路网边，单独存储隧道属性（限高、限速、通风管制等），两端节点衔接地面道路。建模时需屏蔽隧道与地面其他道路的空间相交关系，避免产生虚假拓扑连接，保障地下路网的拓扑独立性。", `kp_id`: "M1-027", `sort_order`: 27};

MERGE (node:KnowledgePoint {kp_id: "M1-028"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "地面、高架、地下多层路网拓扑分层规则", `description`: "多层路网拓扑分层规则要求不同标高的道路系统分层建立拓扑关系，地面、高架、地下道路分别构建独立的节点-边体系，仅通过匝道、出入口节点实现层间连接。禁止不同标高道路在空间交叉处自动建立拓扑连接，避免出现“穿模”式的错误连通。", `kp_id`: "M1-028", `sort_order`: 28};

MERGE (node:KnowledgePoint {kp_id: "M1-029"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "单向通行路网拓扑构建要点", `description`: "单向通行路网拓扑构建需将对应道路边设置为单向属性，明确通行方向，匹配实际交通标志；同时在节点处对应设置转向约束，禁止逆向驶入。构建完成需进行方向校验，确保路径规划不会产生逆行路线，是城市老城区路网建模的重点内容。", `kp_id`: "M1-029", `sort_order`: 29};

MERGE (node:KnowledgePoint {kp_id: "M1-030"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "双向通行路网拓扑构建要点", `description`: "双向通行路网拓扑构建可采用双向边或两条反向单向边两种方式：双向边结构简单，适用于宏观分析；双单向边可分别存储上下行属性，适用于精细化分析。构建时需确保双向通行权限完整，匹配道路实际通行规则。", `kp_id`: "M1-030", `sort_order`: 30};

MERGE (node:KnowledgePoint {kp_id: "M1-031"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网拓扑完整性评价基础标准", `description`: "路网拓扑完整性评价基础标准包括：节点悬挂率、断头路比例、伪节点数量、线段重合率、节点连通度等指标。通过量化指标判定路网拓扑连接的完备程度，识别数据缺陷，是路网数据质量验收、拓扑修复效果评估的核心依据。", `kp_id`: "M1-031", `sort_order`: 31};

MERGE (node:KnowledgePoint {kp_id: "M1-032"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网拓扑一致性检查核心维度", `description`: "路网拓扑一致性检查核心维度包括：几何与拓扑一致性（坐标连接与逻辑连接匹配）、方向一致性（通行方向与实际规则匹配）、属性一致性（同等级道路属性统一）、分层一致性（多层路网无错误跨层连接），用于保障路网数据逻辑自洽。", `kp_id`: "M1-032", `sort_order`: 32};

MERGE (node:KnowledgePoint {kp_id: "M1-033"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网图论中度值的定义与计算逻辑", `description`: "路网图论中，度值指一个节点连接的道路边数量，反映节点的连通程度。无向图中节点度等于关联边数；有向图中分为入度（驶入边数）、出度（驶出边数），总度为二者之和。计算逻辑为统计节点关联的所有边的数量，是路网中心性分析的基础指标。", `kp_id`: "M1-033", `sort_order`: 33};

MERGE (node:KnowledgePoint {kp_id: "M1-034"})
SET node = {`difficulty`: "高阶", `importance`: "熟悉", `name`: "路网邻接矩阵的构建原理", `description`: "路网邻接矩阵是用矩阵形式表达节点间连接关系的方式，矩阵行与列对应路网节点，元素值为1表示两节点直接相连，为0表示不相连；加权邻接矩阵对应位置存储边的权重值。构建原理是基于节点编号与边连接关系映射为二维数组，是路网矩阵运算的基础。", `kp_id`: "M1-034", `sort_order`: 34};

MERGE (node:KnowledgePoint {kp_id: "M1-035"})
SET node = {`difficulty`: "高阶", `importance`: "了解", `name`: "路网关联矩阵的构建原理", `description`: "路网关联矩阵表达节点与边之间的关联关系，矩阵行对应节点、列对应边，元素值为1表示边以该节点为起点，-1表示以该节点为终点，0表示无关联。构建原理是基于边的起止节点映射矩阵元素，主要用于拓扑结构数学推导与图论算法开发。", `kp_id`: "M1-035", `sort_order`: 35};

MERGE (node:KnowledgePoint {kp_id: "M1-036"})
SET node = {`difficulty`: "高阶", `importance`: "了解", `name`: "路网聚类系数计算与网络结构特性", `description`: "路网聚类系数衡量节点的邻居节点之间相互连接的程度，反映路网的集聚特性。计算方式为节点邻居间实际连接数与最大可能连接数的比值。高聚类系数对应路网组团化特征明显，低聚类系数对应路网呈放射状结构，用于分析城市路网空间形态。", `kp_id`: "M1-036", `sort_order`: 36};

MERGE (node:KnowledgePoint {kp_id: "M1-037"})
SET node = {`difficulty`: "高阶", `importance`: "了解", `name`: "路网平均路径长度与小世界特性", `description`: "路网平均路径长度是所有节点对之间最短路径的平均值，反映路网整体通达性。小世界特性指路网同时具备较短的平均路径长度与较高的聚类系数，是城市路网的典型特征，意味着既有局部高集聚性，又有整体高效通达性。", `kp_id`: "M1-037", `sort_order`: 37};

MERGE (node:KnowledgePoint {kp_id: "M1-038"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "复杂交通场景下路网模型的拓展需求", `description`: "复杂交通场景（如车路协同、自动驾驶、多式联运）对基础路网模型提出拓展需求，包括车道级精细化建模、动态属性实时更新、多模态拓扑衔接、三维空间拓扑表达等。需在传统节点-边模型基础上扩展属性维度与时空维度，支撑高阶应用。", `kp_id`: "M1-038", `sort_order`: 38};

MERGE (node:KnowledgePoint {kp_id: "M2-001"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "线性参考系统（LRS）的定义与核心价值", `description`: "线性参考系统（LRS）是一种沿线性地物进行位置表达的空间参考体系，以道路中心线为基准，通过里程值（桩号）定位沿线地物与事件。核心价值在于将交通事件、设施与道路里程强绑定，适配交通行业“沿里程管理”的业务习惯，大幅提升沿线事件管理效率。", `kp_id`: "M2-001", `sort_order`: 1};

MERGE (node:KnowledgePoint {kp_id: "M2-002"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "LRS三大组成：交通网络、参照基准、线性参照方法", `description`: "LRS由三大核心部分构成：交通网络是承载线性参考的道路中心线数据；参照基准是里程起算点与桩号体系（如国道桩号基准）；线性参照方法是里程值与空间位置的映射规则。三者共同支撑“用里程描述位置”的线性定位模式。", `kp_id`: "M2-002", `sort_order`: 2};

MERGE (node:KnowledgePoint {kp_id: "M2-003"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "里程桩/桩号定位原理与中国公路桩号体系", `description`: "里程桩定位原理是以道路起点为零点，沿道路中心线按距离递增标注桩号，通过桩号数值唯一确定沿线位置。中国公路桩号体系以国道、省道、县道为单位独立编号，采用K+里程格式（如K123+450），是公路管理的标准定位方式。", `kp_id`: "M2-003", `sort_order`: 3};

MERGE (node:KnowledgePoint {kp_id: "M2-004"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "M值（Measure值）路线要素建模方法", `description`: "M值即测量值，是存储在道路线要素几何中的里程属性，每个折点都对应一个M值。建模方法是为道路中心线赋予起止桩号，通过线性插值计算沿线任意点的M值，实现空间坐标与里程值的双向映射，是LRS的核心数据实现方式。", `kp_id`: "M2-004", `sort_order`: 4};

MERGE (node:KnowledgePoint {kp_id: "M2-005"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "点事件数据模型：事故、标志、检测器等离散事件", `description`: "点事件数据模型用于表达发生在道路某一里程位置的离散事件，如交通事故、交通标志、车辆检测器、公交站点等。数据结构包含路线ID、里程值、事件类型、事件属性等字段，通过里程值映射到道路空间位置，是离散交通要素管理的基础模型。", `kp_id`: "M2-005", `sort_order`: 5};

MERGE (node:KnowledgePoint {kp_id: "M2-006"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "线事件数据模型：路面状况、限速区间、拥堵段等线性事件", `description`: "线事件数据模型用于表达沿道路一段里程范围持续存在的线性事件，如路面损坏段、限速区间、拥堵路段、施工路段等。数据结构包含路线ID、起始里程、终止里程、事件属性等字段，可对应到道路的具体线段，是带状交通要素管理的核心模型。", `kp_id`: "M2-006", `sort_order`: 6};

MERGE (node:KnowledgePoint {kp_id: "M2-007"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "事件表结构设计：路线ID + 测量值 + 属性值", `description`: "LRS事件表的标准结构由三部分构成：路线ID用于关联对应道路；测量值（点事件为单个M值，线事件为起止M值）用于定位；属性值存储事件的业务属性（如事故类型、限速值）。该结构实现了业务数据与空间数据的解耦，便于批量管理与更新。", `kp_id`: "M2-007", `sort_order`: 7};

MERGE (node:KnowledgePoint {kp_id: "M2-008"})
SET node = {`difficulty`: "进阶", `importance`: "核心", `name`: "动态分段技术原理：从测量值到几何位置的映射", `description`: "动态分段技术是LRS的核心技术，原理是基于道路的M值属性，将事件表中的里程测量值动态映射为空间几何要素，无需预先拆分道路线段。可根据不同事件的分段规则动态生成对应的空间线段，支持多维度事件的叠加分析，避免数据冗余。", `kp_id`: "M2-008", `sort_order`: 8};

MERGE (node:KnowledgePoint {kp_id: "M2-009"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "动态分段在路面管理中的应用", `description`: "在路面管理中，动态分段可根据路面性能指数（PCI）、损坏类型等属性，将道路按里程动态划分为不同路况段，生成路面状况空间图层。支持沿线路况分布统计、病害段定位、养护路段自动划分，提升公路养护管理的精细化水平。", `kp_id`: "M2-009", `sort_order`: 9};

MERGE (node:KnowledgePoint {kp_id: "M2-010"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "动态分段在交通事故分析中的应用", `description`: "在交通事故分析中，动态分段可将事故点数据按里程聚合为事故高发段，生成事故黑点空间分布。支持按路段统计事故率、识别事故多发区间、分析事故与道路线形的关联关系，为交通安全治理提供空间定位支撑。", `kp_id`: "M2-010", `sort_order`: 10};

MERGE (node:KnowledgePoint {kp_id: "M2-011"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "动态分段在限速管理中的应用", `description`: "在限速管理中，动态分段可将不同限速值的里程区间转换为空间限速路段，生成全路网限速分布图。支持限速规则可视化、超速点位匹配、限速区段统计，便于交通管制措施的空间化管理与校验。", `kp_id`: "M2-011", `sort_order`: 11};

MERGE (node:KnowledgePoint {kp_id: "M2-012"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "线性参考中的偏移量（Offset）建模", `description`: "偏移量建模用于表达道路横向位置，在里程值基础上增加横向偏移属性，区分左右侧、车道位置。可精准定位路侧设施、车道级事件的横向位置，解决传统LRS仅能表达中心线位置的局限，支撑车道级精细化管理。", `kp_id`: "M2-012", `sort_order`: 12};

MERGE (node:KnowledgePoint {kp_id: "M2-013"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "路线重合与分叉的线性参考处理", `description`: "路线重合段（共线）需建立主路线与副路线的里程映射关系，保证同一位置对应不同路线的桩号可相互转换；路线分叉点需设置里程基准节点，明确分支路线的起算桩号。处理核心是保障同一段物理道路在不同路线体系中的里程定位一致性。", `kp_id`: "M2-013", `sort_order`: 13};

MERGE (node:KnowledgePoint {kp_id: "M2-014"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "路线改线与桩号传递的线性参考维护", `description`: "道路改线后需进行桩号传递维护，通常采用断链处理方式，标注长链、短链位置与桩号差值，保证全线桩号体系的连续性与对应关系。维护需更新路线M值与事件表的对应里程，确保历史事件数据与新路线空间位置正确匹配。", `kp_id`: "M2-014", `sort_order`: 14};

MERGE (node:KnowledgePoint {kp_id: "M2-015"})
SET node = {`difficulty`: "进阶", `importance`: "了解", `name`: "ISO 19148线性参考国际标准解读", `description`: "ISO 19148是地理信息线性参考的国际标准，规定了线性参考的概念模型、数据结构、操作接口与交换格式。标准明确了M值建模、动态分段、事件表达的通用规则，是不同GIS平台间LRS数据互操作、跨系统数据共享的技术依据。", `kp_id`: "M2-015", `sort_order`: 15};

MERGE (node:KnowledgePoint {kp_id: "M2-016"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "ArcGIS Roads & Highways模块LRS工作流", `description`: "ArcGIS Roads & Highways是专门的LRS扩展模块，工作流包含：创建路线数据集、校准M值桩号、注册事件表、动态分段生成事件图层、发布LRS服务。提供了桩号校准、断链处理、事件编辑等专业工具，是行业内主流的LRS实现平台。", `kp_id`: "M2-016", `sort_order`: 16};

MERGE (node:KnowledgePoint {kp_id: "M2-017"})
SET node = {`difficulty`: "进阶", `importance`: "了解", `name`: "SuperMap动态分段功能与实现", `description`: "SuperMap的动态分段功能支持基于路由数据集创建事件表，实现点、线事件的空间映射，提供路由校准、事件叠加分析、里程查询等工具。适配国内交通行业需求，支持国产软件环境下的LRS应用开发与数据管理。", `kp_id`: "M2-017", `sort_order`: 17};

MERGE (node:KnowledgePoint {kp_id: "M2-018"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "多基准线性参考系统：公路桩号 vs 里程 vs GPS", `description`: "多基准LRS包含多种定位基准：公路桩号基于行政路线体系，适配行业管理；累计里程基于道路实际长度，适配工程计算；GPS坐标基于空间位置，适配外业采集。系统需建立多基准间的转换映射关系，支撑不同业务场景下的定位互通。", `kp_id`: "M2-018", `sort_order`: 18};

MERGE (node:KnowledgePoint {kp_id: "M2-019"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "线性参考数据质量校验方法", `description`: "LRS数据质量校验包含：M值连续性校验（无跳变、无逆行）、桩号与长度一致性校验（里程差与几何长度匹配）、事件里程合法性校验（不超出路线范围）、断链标注完整性校验。通过多维度校验保障线性参考定位的准确性。", `kp_id`: "M2-019", `sort_order`: 19};

MERGE (node:KnowledgePoint {kp_id: "M2-020"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "事件数据与路网空间叠加分析", `description`: "事件数据与路网空间叠加分析是将LRS事件图层与其他空间数据（如行政区、土地利用、人口）进行叠加，分析事件的空间分布规律。如分析事故与路网等级的关联、拥堵路段与人口分布的耦合，拓展线性参考数据的应用维度。", `kp_id`: "M2-020", `sort_order`: 20};

MERGE (node:KnowledgePoint {kp_id: "M2-021"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "事故黑点的线性参考识别方法", `description`: "基于LRS的事故黑点识别方法，是将事故点数据按里程进行滑动窗口统计，计算单位里程事故数，识别超出阈值的事故高发路段。通过线性参考可精准定位黑点段的桩号范围，支撑针对性的交通安全整治与道路优化。", `kp_id`: "M2-021", `sort_order`: 21};

MERGE (node:KnowledgePoint {kp_id: "M2-022"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路面性能沿线路网分布分析", `description`: "基于LRS的路面性能分布分析，是将路面检测数据按里程对应到道路，通过动态分段生成路面性能等级分布图。可分析路面损坏的空间分布规律、统计不同等级路面的里程占比，为公路养护计划制定提供数据支撑。", `kp_id`: "M2-022", `sort_order`: 22};

MERGE (node:KnowledgePoint {kp_id: "M2-023"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "交通标志标线的线性参考管理", `description`: "交通标志标线采用LRS管理，将标志位置、标线起止点以桩号形式存储，关联对应道路路线。可快速查询指定里程段的标志设置情况、统计标志密度、辅助标志合规性检查，提升交通设施精细化管理水平。", `kp_id`: "M2-023", `sort_order`: 23};

MERGE (node:KnowledgePoint {kp_id: "M2-024"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "沿线设施（加油站、服务区）线性参考定位", `description`: "沿线服务设施采用LRS进行里程定位，存储设施对应的路线ID与桩号，可快速查询指定里程范围内的设施分布、计算设施间距。适配公路出行服务、养护管理的业务需求，相比坐标定位更符合公路管理习惯。", `kp_id`: "M2-024", `sort_order`: 24};

MERGE (node:KnowledgePoint {kp_id: "M2-025"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "公交站点的线性参考定位与里程统计", `description`: "公交站点通过LRS定位到对应公交线路的里程位置，可统计站点间距、线路站点密度、计算任意两站间的里程。支持公交线网优化、站点布局分析，为公交运营管理提供线性维度的统计分析能力。", `kp_id`: "M2-025", `sort_order`: 25};

MERGE (node:KnowledgePoint {kp_id: "M2-026"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "交通拥堵事件的线性参考表达", `description`: "交通拥堵事件采用线事件模型表达，存储拥堵路段的起止桩号、拥堵程度、持续时间等属性。通过动态分段可实时生成拥堵空间分布，支持拥堵里程统计、拥堵演变分析，是动态交通信息管理的重要方式。", `kp_id`: "M2-026", `sort_order`: 26};

MERGE (node:KnowledgePoint {kp_id: "M2-027"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "施工占道事件的线性参考建模", `description`: "施工占道事件采用线事件模型，存储施工路段的起止里程、占道类型、施工时间、通行限制等属性。基于LRS可精准定位施工位置，自动生成施工警示空间范围，支撑交通导改方案制定与路网通行影响分析。", `kp_id`: "M2-027", `sort_order`: 27};

MERGE (node:KnowledgePoint {kp_id: "M2-028"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "LRS与传统坐标定位的优劣对比", `description`: "LRS定位优势在于贴合交通行业业务习惯、便于沿线统计、事件更新无需修改几何数据；缺点是依赖路线基准、横向定位精度有限。传统坐标定位优势是空间位置直观、通用性强；缺点是沿线关联分析不便、与业务管理维度脱节。", `kp_id`: "M2-028", `sort_order`: 28};

MERGE (node:KnowledgePoint {kp_id: "M2-029"})
SET node = {`difficulty`: "高阶", `importance`: "了解", `name`: "动态分段性能优化：大规模事件数据处理", `description`: "大规模事件数据的动态分段性能优化方法包括：建立路线M值索引、事件表分区存储、批量计算替代逐行计算、采用增量更新机制。通过优化可提升百万级事件数据的动态分段效率，满足省级、国家级路网的LRS应用需求。", `kp_id`: "M2-029", `sort_order`: 29};

MERGE (node:KnowledgePoint {kp_id: "M2-030"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "多源事件数据的线性参考融合", `description`: "多源事件数据融合需统一路线基准与桩号体系，将不同来源、不同格式的事件数据映射到同一LRS框架下，进行里程匹配与属性融合。需解决桩号基准差异、定位误差、数据冗余等问题，形成统一的沿线事件数据库。", `kp_id`: "M2-030", `sort_order`: 30};

MERGE (node:KnowledgePoint {kp_id: "M2-031"})
SET node = {`difficulty`: "基础", `importance`: "了解", `name`: "铁路线路的线性参考与里程管理", `description`: "铁路线路同样采用线性参考体系，以公里标为定位基准，管理沿线轨道、信号机、车站等设施。原理与公路LRS一致，但采用铁路专属的里程体系与断链规则，适配铁路工务管理、运输调度的业务需求。", `kp_id`: "M2-031", `sort_order`: 31};

MERGE (node:KnowledgePoint {kp_id: "M2-032"})
SET node = {`difficulty`: "基础", `importance`: "了解", `name`: "航道航段的线性参考定位方法", `description`: "航道航段采用线性参考定位，以航道中心线为基准，通过里程桩号定位航标、港口、浅滩等要素。适配内河航运管理需求，支持航道养护、通航管理的沿线分析，是水运交通GIS的重要技术方法。", `kp_id`: "M2-032", `sort_order`: 32};

MERGE (node:KnowledgePoint {kp_id: "M2-033"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "线性参考在资产管理中的应用", `description`: "交通资产管理中，LRS将道路、桥梁、沿线设施等资产按里程进行全生命周期管理，关联资产的建设时间、养护记录、技术状况等信息。可实现资产沿线路可视化、养护里程自动统计、资产状态演变分析，提升资产管理精细化水平。", `kp_id`: "M2-033", `sort_order`: 33};

MERGE (node:KnowledgePoint {kp_id: "M2-034"})
SET node = {`difficulty`: "高阶", `importance`: "熟悉", `name`: "历史事件的时空线性参考表达", `description`: "历史事件的时空LRS表达在传统里程维度基础上增加时间维度，存储事件发生的时间与对应里程位置。可追溯不同时期道路事件的时空分布，分析事件演变规律，支撑路网运行状态的时序分析与趋势预测。", `kp_id`: "M2-034", `sort_order`: 34};

MERGE (node:KnowledgePoint {kp_id: "M2-035"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "LRS数据模型的标准化与互操作", `description`: "LRS数据模型标准化指遵循ISO 19148等标准，统一路线建模、事件表结构、M值定义等规范。互操作指不同GIS平台、不同业务系统间可交换LRS数据，保障数据共享与业务协同，是跨部门交通数据整合的基础。", `kp_id`: "M2-035", `sort_order`: 35};

MERGE (node:KnowledgePoint {kp_id: "M2-036"})
SET node = {`difficulty`: "高阶", `importance`: "熟悉", `name`: "线性参考与知识图谱的事件实体关联", `description`: "将LRS事件数据映射为知识图谱中的事件实体，通过路线ID与里程值关联道路实体，建立“道路-包含-事件”的语义关系。实现线性参考数据与知识图谱的语义融合，支撑基于知识推理的事件关联分析与智能查询。", `kp_id`: "M2-036", `sort_order`: 36};

MERGE (node:KnowledgePoint {kp_id: "M3-001"})
SET node = {`difficulty`: "入门", `importance`: "掌握", `name`: "官方测绘路网数据的来源与权威属性", `description`: "官方测绘路网数据来源于自然资源部基础测绘、交通运输部公路普查等官方渠道，由专业测绘单位采集生产。具备法定权威性、标准统一、覆盖范围广的特点，是交通路网数据的基准数据源，可作为其他数据校正的参照。", `kp_id`: "M3-001", `sort_order`: 1};

MERGE (node:KnowledgePoint {kp_id: "M3-002"})
SET node = {`difficulty`: "入门", `importance`: "掌握", `name`: "交通运输部门路网普查数据特征", `description`: "交通运输部门路网普查数据由交通主管部门组织采集，聚焦公路与城市道路的交通属性，包含道路等级、路面类型、里程、桥梁隧道等丰富的交通专属字段。数据贴合交通业务需求，属性完备，但空间几何精度略低于基础测绘数据。", `kp_id`: "M3-002", `sort_order`: 2};

MERGE (node:KnowledgePoint {kp_id: "M3-003"})
SET node = {`difficulty`: "入门", `importance`: "掌握", `name`: "自然资源局国土路网矢量数据特征", `description`: "自然资源局国土路网矢量数据来源于基础地理信息数据库，几何精度高、坐标系规范、覆盖全域，包含各级道路的几何要素。优势是空间定位准确、现势性有保障；缺点是交通属性较少，缺乏限速、车道数等业务属性。", `kp_id`: "M3-003", `sort_order`: 3};

MERGE (node:KnowledgePoint {kp_id: "M3-004"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "基础地形图路网数据提取规则", `description`: "从基础地形图提取路网需遵循分级提取、属性映射、拓扑构建规则：按道路等级分层提取几何线要素；将地形图中的道路注记映射为属性字段；提取后进行节点连接与拓扑构建。需注意区分道路边线与中心线，保证提取结果符合路网建模要求。", `kp_id`: "M3-004", `sort_order`: 4};

MERGE (node:KnowledgePoint {kp_id: "M3-005"})
SET node = {`difficulty`: "入门", `importance`: "熟悉", `name`: "OSM开源路网数据的来源与优缺点", `description`: "OSM（OpenStreetMap）是众源开放路网数据，由全球志愿者共同贡献。优点是免费开源、更新快、覆盖全球、属性丰富；缺点是精度参差不齐、数据质量不稳定、部分区域属性缺失，适合作为研究与原型开发的数据源。", `kp_id`: "M3-005", `sort_order`: 5};

MERGE (node:KnowledgePoint {kp_id: "M3-006"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "高德地图路网数据的字段与精度特征", `description`: "高德地图路网数据覆盖全国，道路等级分类完善，包含实时路况、POI、交通事件等丰富属性，城市区域精度高。字段包含道路名称、等级、限速、车道数、通行方向等，适配导航与智慧交通应用，但商用需授权，原始数据获取难度较高。", `kp_id`: "M3-006", `sort_order`: 6};

MERGE (node:KnowledgePoint {kp_id: "M3-007"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "百度地图路网数据的字段与精度特征", `description`: "百度地图路网数据城市覆盖全面，城区道路细节丰富，支持车道级导航数据，配套有交通拥堵、事件等动态数据。字段体系与高德类似，在城市支路、步行路网等细节上各有优劣，同样需商业授权方可获取原始数据。", `kp_id`: "M3-007", `sort_order`: 7};

MERGE (node:KnowledgePoint {kp_id: "M3-008"})
SET node = {`difficulty`: "基础", `importance`: "了解", `name`: "腾讯地图路网数据的差异化特征", `description`: "腾讯地图路网数据在位置服务、LBS应用领域适配性强，侧重移动端场景的路网表达。差异化特征在于与社交、位置大数据结合紧密，步行、骑行路网数据完善，适合基于位置的交通分析与出行服务应用。", `kp_id`: "M3-008", `sort_order`: 8};

MERGE (node:KnowledgePoint {kp_id: "M3-009"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "车载GPS浮动车轨迹数据的路网适配价值", `description`: "浮动车轨迹数据由车辆GPS采集得到，通过地图匹配可反演路网的实际通行速度、拥堵状态、流量分布。核心价值在于可动态感知路网运行状态，补充静态路网数据的动态属性，是动态路网建模、交通状态识别的核心数据源。", `kp_id`: "M3-009", `sort_order`: 9};

MERGE (node:KnowledgePoint {kp_id: "M3-010"})
SET node = {`difficulty`: "基础", `importance`: "了解", `name`: "无人机航拍影像路网提取数据特征", `description`: "无人机航拍影像通过图像识别提取路网数据，具备高分辨率、灵活采集、现势性强的特点。可快速获取局部区域的最新路网形态，适合小范围路网更新、应急场景路网勘测，但大范围采集成本高，需进行后处理与拓扑构建。", `kp_id`: "M3-010", `sort_order`: 10};

MERGE (node:KnowledgePoint {kp_id: "M3-011"})
SET node = {`difficulty`: "进阶", `importance`: "了解", `name`: "车载激光点云路网采集数据特征", `description`: "车载激光点云通过移动测量系统采集道路三维点云数据，可高精度提取道路几何、车道线、交通标志、附属设施等信息。特征是精度高、三维信息丰富、可实现车道级建模，是高精地图、三维路网建模的核心数据源。", `kp_id`: "M3-011", `sort_order`: 11};

MERGE (node:KnowledgePoint {kp_id: "M3-012"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "交通卡口监测路网配套数据特征", `description`: "交通卡口数据包含过车记录、车牌、时间、车型等信息，对应路网的卡口点位。可用于统计路段流量、车速、OD出行分布，配套静态路网数据可实现交通运行状态监测，是城市动态交通数据的重要来源。", `kp_id`: "M3-012", `sort_order`: 12};

MERGE (node:KnowledgePoint {kp_id: "M3-013"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "铁路路网数据：线路、车站、枢纽数据特征", `description`: "铁路路网数据包含线路几何、车站位置、枢纽布局、道岔分布等要素，属性包含线路等级、速度目标值、牵引类型、车站等级等。数据标准性高、拓扑严谨，由铁路主管部门统一管理，是多模态综合交通网的重要组成部分。", `kp_id`: "M3-013", `sort_order`: 13};

MERGE (node:KnowledgePoint {kp_id: "M3-014"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "城市轨道交通数据：地铁、轻轨线路与站点", `description`: "城市轨道交通数据包含地铁、轻轨等线路的空间走向、站点位置、换乘站等要素，属性包含线路制式、运营时间、站间距、客流等。数据精度高、拓扑清晰，是城市公共交通网络的核心组成，支撑公交线网融合分析。", `kp_id`: "M3-014", `sort_order`: 14};

MERGE (node:KnowledgePoint {kp_id: "M3-015"})
SET node = {`difficulty`: "基础", `importance`: "了解", `name`: "水运航道与港口数据特征", `description`: "水运数据包含航道中心线、港口、码头、船闸、锚地等要素，属性包含航道等级、通航水深、港口吞吐量、码头泊位等。数据具有线性特征，适配线性参考系统管理，是综合立体交通网的水运分支数据。", `kp_id`: "M3-015", `sort_order`: 15};

MERGE (node:KnowledgePoint {kp_id: "M3-016"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "路网空间几何属性核心字段", `description`: "路网空间几何属性核心字段包括：道路长度、道路走向、坐标序列、曲率、坡度、高程等。这些字段描述了道路的空间几何特征，是路径计算、线形分析、行车视距分析的基础，直接影响路网空间分析的准确性。", `kp_id`: "M3-016", `sort_order`: 16};

MERGE (node:KnowledgePoint {kp_id: "M3-017"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网坐标属性与空间定位规则", `description`: "路网坐标属性存储道路的空间坐标信息，需遵循对应坐标系的定位规则，保证坐标精度与投影一致性。空间定位规则要求同一数据集采用统一坐标系，节点坐标精确重合，避免坐标偏移导致的拓扑错误与空间匹配误差。", `kp_id`: "M3-017", `sort_order`: 17};

MERGE (node:KnowledgePoint {kp_id: "M3-018"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网长度、曲率、坡度几何属性定义", `description`: "长度指道路路段的实际里程长度；曲率描述道路线形的弯曲程度，影响行车安全与限速；坡度指道路的纵坡大小，影响车辆通行效率与能耗。三者是道路线形的核心几何指标，也是路网阻抗计算的重要参数。", `kp_id`: "M3-018", `sort_order`: 18};

MERGE (node:KnowledgePoint {kp_id: "M3-019"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "道路等级属性分类标准（高速/国道/省道/县道/城市道路）", `description`: "我国道路按行政等级与功能分为高速公路、国道、省道、县道、乡道、城市道路（快速路、主干路、次干路、支路）等。不同等级对应不同的设计速度、车道数、通行能力，是路网分级管理、阻抗赋值、可视化表达的核心依据。", `kp_id`: "M3-019", `sort_order`: 19};

MERGE (node:KnowledgePoint {kp_id: "M3-020"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "道路车道数字段规范与录入标准", `description`: "道路车道数字段记录道路的机动车道数量，录入标准需区分单向车道数与双向车道数，明确是否包含辅路、匝道车道。高等级道路需分方向标注车道数，车道数变化处需设置节点分段。该字段是道路容量计算、通行能力分析的基础参数。", `kp_id`: "M3-020", `sort_order`: 20};

MERGE (node:KnowledgePoint {kp_id: "M3-021"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "道路设计限速、实际限速字段区分", `description`: "设计限速是道路工程设计的最高时速标准，由道路等级与线形条件决定；实际限速是交通管制设定的实时限速值，可能因施工、天气、管制等低于设计限速。二者需分字段存储，分别适配路网规划与实际运行分析场景。", `kp_id`: "M3-021", `sort_order`: 21};

MERGE (node:KnowledgePoint {kp_id: "M3-022"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "道路通行方向属性标注规则", `description`: "道路通行方向属性分为双向通行、单向上行、单向下行三类，标注需匹配实际交通管制。有向路网中每条边对应一个通行方向，双向道路可采用双单向边或双向边表达。标注错误会导致路径规划出现逆行，是路网属性质量检查的重点。", `kp_id`: "M3-022", `sort_order`: 22};

MERGE (node:KnowledgePoint {kp_id: "M3-023"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "路面材质属性分类与数据规范", `description`: "路面材质主要分为沥青混凝土、水泥混凝土、砂石路面等类型，不同材质对应不同的摩擦系数、养护成本、通行舒适度。数据规范要求统一分类标准，标注路面结构类型，是路面管理、养护决策、阻抗计算的参考属性。", `kp_id`: "M3-023", `sort_order`: 23};

MERGE (node:KnowledgePoint {kp_id: "M3-024"})
SET node = {`difficulty`: "进阶", `importance`: "核心", `name`: "道路通行时间阻抗属性定义", `description`: "通行时间阻抗指车辆通过路段所需的时间，由路段长度与行驶车速决定，是路网路径分析最常用的阻抗形式。静态时间阻抗基于设计限速计算，动态时间阻抗结合实时路况更新。该属性是最优路径规划、交通分配的核心参数。", `kp_id`: "M3-024", `sort_order`: 24};

MERGE (node:KnowledgePoint {kp_id: "M3-025"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "道路通行费用阻抗属性定义", `description`: "通行费用阻抗指车辆通过路段产生的经济成本，包括高速公路通行费、油费、时间成本折算等。可根据车型、里程计算费用值，作为物流配送、货运路径规划的阻抗权重，支撑经济成本最优的路径分析。", `kp_id`: "M3-025", `sort_order`: 25};

MERGE (node:KnowledgePoint {kp_id: "M3-026"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网转向限制属性录入规则", `description`: "转向限制属性存储交叉口的禁左、禁右、禁止掉头等规则，录入需对应具体进口道与行驶方向，明确限制时段与车型。可存储在节点属性或转向关系表中，录入后需进行路径验证，确保转向规则正确生效。", `kp_id`: "M3-026", `sort_order`: 26};

MERGE (node:KnowledgePoint {kp_id: "M3-027"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网限行规则（时段/车型）属性存储方式", `description`: "限行规则属性采用“路段+时段+车型”的结构化存储方式，分字段记录限行路段、限行时间段、受限车型、限行类型。支持时间依赖型路网分析，可根据查询时间动态判定路段通行权限，是精细化交通管制建模的必要属性。", `kp_id`: "M3-027", `sort_order`: 27};

MERGE (node:KnowledgePoint {kp_id: "M3-028"})
SET node = {`difficulty`: "进阶", `importance`: "了解", `name`: "GDF地理数据文件标准格式解读", `description`: "GDF（Geographic Data File）是国际通用的导航地理数据标准格式，规定了路网、POI、交通规则等数据的存储结构与交换规范。数据采用分层架构，支持拓扑关系与交通属性表达，是车载导航、高精地图领域的主流数据标准。", `kp_id`: "M3-028", `sort_order`: 28};

MERGE (node:KnowledgePoint {kp_id: "M3-029"})
SET node = {`difficulty`: "高阶", `importance`: "熟悉", `name`: "OpenDRIVE高精地图数据格式", `description`: "OpenDRIVE是自动驾驶领域的高精地图开放标准格式，采用XML结构描述道路几何、车道、标志、信号等要素，支持车道级拓扑与三维道路建模。格式定义了道路参考线、车道段、交叉口等核心元素，是自动驾驶路网建模的事实标准。", `kp_id`: "M3-029", `sort_order`: 29};

MERGE (node:KnowledgePoint {kp_id: "M3-030"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "CGCS2000坐标系路网适配规则", `description`: "CGCS2000是我国现行法定大地坐标系，路网数据适配需统一采用该坐标系的平面投影（通常为高斯-克吕格投影）。规则要求数据坐标精准匹配、投影参数一致、跨带数据需进行换带处理，保障全国路网数据的空间基准统一。", `kp_id`: "M3-030", `sort_order`: 30};

MERGE (node:KnowledgePoint {kp_id: "M3-031"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "WGS84坐标系路网适配规则", `description`: "WGS84是国际通用大地坐标系，广泛用于GPS数据与互联网地图。路网适配时需注意与国内坐标系的差异，涉及坐标偏移问题；互联网地图使用的是加密后的WGS84（火星坐标系），直接叠加会出现位置偏差。", `kp_id`: "M3-031", `sort_order`: 31};

MERGE (node:KnowledgePoint {kp_id: "M3-032"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "北京54、西安80老旧路网坐标转换方法", `description`: "北京54、西安80是我国历史坐标系，老旧路网数据需转换为CGCS2000坐标系。转换方法包括七参数布尔莎模型、四参数转换、格网插值法等，需根据区域精度要求选择转换方法，转换后进行精度验证。", `kp_id`: "M3-032", `sort_order`: 32};

MERGE (node:KnowledgePoint {kp_id: "M3-033"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网数据批量纠偏处理流程", `description`: "路网数据批量纠偏流程包括：确定偏移基准、选取控制点、计算偏移参数、批量坐标转换、拓扑修复、精度验证。针对互联网地图偏移数据采用专用纠偏算法，针对系统误差采用整体转换，针对局部误差采用局部校正。", `kp_id`: "M3-033", `sort_order`: 33};

MERGE (node:KnowledgePoint {kp_id: "M3-034"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网数据格式转换（shp/geojson/gdb/GPX）", `description`: "常见路网数据格式包括Shapefile、GeoJSON、FileGDB、GPX等，不同格式适配不同平台与应用场景。格式转换需保证几何信息不丢失、属性字段完整、拓扑关系不变，注意坐标系信息的同步转换，避免数据损失。", `kp_id`: "M3-034", `sort_order`: 34};

MERGE (node:KnowledgePoint {kp_id: "M3-035"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网数据裁剪、拼接、融合处理方法", `description`: "路网数据裁剪是按研究范围提取目标区域路网；拼接是将多幅相邻路网数据合并为一个数据集；融合是将多源路网数据合并去重、属性补充。处理过程需注意拓扑衔接、坐标统一、属性映射，保障结果数据的完整性与一致性。", `kp_id`: "M3-035", `sort_order`: 35};

MERGE (node:KnowledgePoint {kp_id: "M3-036"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网数据完整性质量评价指标", `description`: "路网数据完整性评价指标包括：道路覆盖率、等级完整性、属性字段缺失率、拓扑连通率、节点完整度等。用于衡量路网数据的覆盖程度与要素完备性，识别数据缺失、断头路、属性缺失等质量问题。", `kp_id`: "M3-036", `sort_order`: 36};

MERGE (node:KnowledgePoint {kp_id: "M3-037"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网数据精度质量评价指标", `description`: "路网数据精度评价指标包括：几何位置精度、属性精度、拓扑精度。几何精度衡量坐标与实际位置的偏差；属性精度衡量字段值的准确性；拓扑精度衡量连接关系的正确性。是路网数据质量的核心评价维度。", `kp_id`: "M3-037", `sort_order`: 37};

MERGE (node:KnowledgePoint {kp_id: "M3-038"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "路网数据时效性质量评价指标", `description`: "路网数据时效性评价指标包括：数据现势性、更新频率、历史版本完整性。衡量路网数据与当前实际道路状况的吻合程度，新建道路、道路改线是否及时更新。时效性是动态路网与互联网地图数据的核心优势指标。", `kp_id`: "M3-038", `sort_order`: 38};

MERGE (node:KnowledgePoint {kp_id: "M3-039"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网数据一致性质量评价指标", `description`: "路网数据一致性评价包括：几何与拓扑一致性、属性逻辑一致性、多源数据一致性、分层一致性。衡量数据内部逻辑自洽程度，以及不同来源、不同图层数据之间的匹配程度，避免出现矛盾数据与错误关联。", `kp_id`: "M3-039", `sort_order`: 39};

MERGE (node:KnowledgePoint {kp_id: "M3-040"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "多源路网数据质量综合评价体系", `description`: "综合评价体系从完整性、精度、时效性、一致性、可用性五个维度构建指标体系，采用加权评分法对多源路网数据进行综合量化评估。用于数据源选型、数据质量验收、融合效果评估，指导路网数据质量提升。", `kp_id`: "M3-040", `sort_order`: 40};

MERGE (node:KnowledgePoint {kp_id: "M4-001"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "路网网络分析的核心逻辑：阻抗成本模型", `description`: "路网网络分析的核心是基于阻抗成本模型，将道路通行代价量化为权重值，通过图论算法寻找成本最优的路径或方案。阻抗可选择距离、时间、费用等单一指标，也可采用多指标综合权重，是所有路网分析算法的底层逻辑。", `kp_id`: "M4-001", `sort_order`: 1};

MERGE (node:KnowledgePoint {kp_id: "M4-002"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "距离阻抗模型的构建与计算规则", `description`: "距离阻抗模型以道路长度作为阻抗权重，构建规则是为每条路网边赋予长度属性值。计算规则为路径总阻抗等于所经路段长度之和，适用于最短路径分析、距离测算等对距离敏感的场景，计算简单但未考虑通行效率。", `kp_id`: "M4-002", `sort_order`: 2};

MERGE (node:KnowledgePoint {kp_id: "M4-003"})
SET node = {`difficulty`: "基础", `importance`: "核心", `name`: "时间阻抗模型的构建与计算规则", `description`: "时间阻抗模型以车辆通行时间作为阻抗权重，构建规则为路段通行时间 = 路段长度 / 行驶车速。计算规则为路径总时间等于各路段时间与转向时间之和，车速可采用设计车速或实时车速。是最常用的路网分析模型，适配最优时间路径规划。", `kp_id`: "M4-003", `sort_order`: 3};

MERGE (node:KnowledgePoint {kp_id: "M4-004"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "经济费用阻抗模型的构建与计算规则", `description`: "经济费用阻抗模型以通行经济成本作为阻抗权重，构建规则为总费用 = 油费 + 通行费 + 时间成本折算。计算规则为路径总费用等于各路段费用之和，可根据车型、运价进行参数配置。适用于物流配送、货运路径优化等成本敏感场景。", `kp_id`: "M4-004", `sort_order`: 4};

MERGE (node:KnowledgePoint {kp_id: "M4-005"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "多阻抗耦合路网模型的权重配比逻辑", `description`: "多阻抗耦合模型融合距离、时间、费用等多种阻抗，通过权重配比计算综合阻抗值。权重配比逻辑需根据业务目标确定各指标权重，采用加权求和或层次分析法计算综合成本。模型灵活性高，可适配不同决策偏好的路网分析需求。", `kp_id`: "M4-005", `sort_order`: 5};

MERGE (node:KnowledgePoint {kp_id: "M4-006"})
SET node = {`difficulty`: "进阶", `importance`: "核心", `name`: "Dijkstra最短路径算法原理与路网适配", `description`: "Dijkstra算法是经典单源最短路径算法，原理是从起点出发，采用贪心策略逐步扩展距离最短的节点，直到到达终点，得到起点到所有节点的最短路径。路网适配时将节点作为图顶点、路段阻抗作为边权重，是路网路径分析的基础算法。", `kp_id`: "M4-006", `sort_order`: 6};

MERGE (node:KnowledgePoint {kp_id: "M4-007"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "Dijkstra算法在大规模路网的优化要点", `description`: "大规模路网下Dijkstra算法优化要点包括：采用优先队列（堆）优化节点提取效率、建立空间索引减少搜索范围、双向搜索降低搜索规模、分层次路网分级搜索。通过优化可将算法复杂度从O(n²)降至近似O(n)，支撑城市级以上路网计算。", `kp_id`: "M4-007", `sort_order`: 7};

MERGE (node:KnowledgePoint {kp_id: "M4-008"})
SET node = {`difficulty`: "进阶", `importance`: "核心", `name`: "A*启发式路径算法原理与路网优势", `description`: "A*算法是启发式最短路径算法，原理是在Dijkstra基础上引入启发函数（估算当前点到终点的代价），优先搜索更接近终点的方向。路网应用优势是搜索效率远高于Dijkstra，计算速度快，适合点对点实时路径查询场景。", `kp_id`: "M4-008", `sort_order`: 8};

MERGE (node:KnowledgePoint {kp_id: "M4-009"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "双向A*算法的路网路径优化逻辑", `description`: "双向A*算法同时从起点和终点出发，分别向前与向后执行A*搜索，当两个搜索方向相遇时得到最短路径。优化逻辑是通过双向搜索大幅缩小搜索范围，进一步提升长距离路径计算效率，是导航软件的核心路径算法。", `kp_id`: "M4-009", `sort_order`: 9};

MERGE (node:KnowledgePoint {kp_id: "M4-010"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网OD成本矩阵的定义与构建场景", `description`: "OD成本矩阵是起点（Origin）到终点（Destination）的最短阻抗值二维表，记录所有节点对之间的最优路径成本。构建场景包括交通分配、设施选址、可达性分析、OD反推等，是宏观交通分析与网络规划的基础数据。", `kp_id`: "M4-010", `sort_order`: 10};

MERGE (node:KnowledgePoint {kp_id: "M4-011"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "多点对多点OD矩阵批量计算方法", `description`: "OD矩阵批量计算方法包括：全源最短路径法（适用于小规模路网）、分块并行计算法（适用于大规模路网）、抽样估算发（适用于超大规模路网）。可基于Dijkstra或A*算法并行实现，通过空间索引与分布式计算提升效率。", `kp_id`: "M4-011", `sort_order`: 11};

MERGE (node:KnowledgePoint {kp_id: "M4-012"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "路网几何缓冲区分析的原理与缺陷", `description`: "几何缓冲区分析原理是沿道路线按固定距离生成缓冲区域，统计区域内的要素。缺陷是仅考虑空间直线距离，未考虑路网拓扑连通性与实际通行路径，无法反映真实的路网可达范围，适用于粗略的空间范围分析。", `kp_id`: "M4-012", `sort_order`: 12};

MERGE (node:KnowledgePoint {kp_id: "M4-013"})
SET node = {`difficulty`: "进阶", `importance`: "核心", `name`: "路网网络缓冲区（可达范围）分析原理", `description`: "网络缓冲区分析又称服务区分析，原理是从起点出发，沿路网搜索所有阻抗成本不超过阈值的节点与路段，得到真实的路网可达范围。相比几何缓冲区，考虑了道路连通性、通行方向、阻抗成本，结果更贴合实际出行场景。", `kp_id`: "M4-013", `sort_order`: 13};

MERGE (node:KnowledgePoint {kp_id: "M4-014"})
SET node = {`difficulty`: "进阶", `importance`: "核心", `name`: "等时圈可达性分析模型构建方法", `description`: "等时圈模型构建方法为：以目标点为中心，基于时间阻抗路网，计算不同时间阈值下的路网可达边界，生成等时圈多边形。可分别构建5分钟、15分钟、30分钟等时圈，用于评价公共服务设施的交通可达性与服务覆盖范围。", `kp_id`: "M4-014", `sort_order`: 14};

MERGE (node:KnowledgePoint {kp_id: "M4-015"})
SET node = {`difficulty`: "基础", `importance`: "熟悉", `name`: "等距圈路网覆盖范围计算方法", `description`: "等距圈计算方法为：以目标点为中心，基于距离阻抗路网，搜索所有路网距离不超过阈值的区域，生成等距离覆盖范围。用于衡量设施的空间服务半径，相比直线缓冲区更贴合道路实际通行距离。", `kp_id`: "M4-015", `sort_order`: 15};

MERGE (node:KnowledgePoint {kp_id: "M4-016"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "公共设施路网服务区划分算法", `description`: "公共设施服务区划分算法基于网络服务区分析，采用距离或时间阻抗，划分每个设施的服务覆盖范围。常用方法有泰森多边形法（基于路网距离）、竞争型服务区划分（考虑设施等级与容量），支撑公共设施布局优化与资源配置。", `kp_id`: "M4-016", `sort_order`: 16};

MERGE (node:KnowledgePoint {kp_id: "M4-017"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "路网设施点空间分配模型原理（位置分配）", `description`: "位置分配模型原理是在给定候选设施点与需求点的情况下，基于路网阻抗，求解最优的设施选址与需求分配方案，实现总出行成本最小化。包含最小阻抗模型、最大覆盖模型等，是公共设施、物流网点选址的核心算法。", `kp_id`: "M4-017", `sort_order`: 17};

MERGE (node:KnowledgePoint {kp_id: "M4-018"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网转向延迟成本的算法嵌入逻辑", `description`: "转向延迟成本指车辆在交叉口转向产生的时间损耗，包括左转等待、减速等。算法嵌入逻辑是将转向延迟作为节点阻抗，叠加到路径总阻抗中，在路径计算时考虑转向代价。嵌入后可提升城市路网路径时间计算的准确性。", `kp_id`: "M4-018", `sort_order`: 18};

MERGE (node:KnowledgePoint {kp_id: "M4-019"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网禁行约束的路径筛选算法", `description`: "禁行约束路径筛选算法原理是在路径搜索过程中，校验路段通行权限与节点转向规则，过滤掉违反禁行规则的路径。算法需支持分时段、分车型的动态约束判断，保证输出路径符合交通管制规则，避免出现违法路径。", `kp_id`: "M4-019", `sort_order`: 19};

MERGE (node:KnowledgePoint {kp_id: "M4-020"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "时间依赖型动态路网算法原理", `description`: "时间依赖型动态路网算法原理是路网边的阻抗值随时间动态变化，不同时段对应不同的通行时间。路径计算时需根据出发时间匹配对应时段的阻抗值，考虑拥堵的时间分布规律，输出对应时间下的最优路径。", `kp_id`: "M4-020", `sort_order`: 20};

MERGE (node:KnowledgePoint {kp_id: "M4-021"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "早晚高峰路网阻抗动态更新机制", `description`: "早晚高峰阻抗更新机制是根据历史交通流数据，划分早高峰、晚高峰、平峰、夜间等时段，为每个时段配置对应的路段通行时间。在路径计算时根据查询时间自动切换阻抗值，模拟不同时段的路网运行状态。", `kp_id`: "M4-021", `sort_order`: 21};

MERGE (node:KnowledgePoint {kp_id: "M4-022"})
SET node = {`difficulty`: "基础", `importance`: "掌握", `name`: "路网密度单点计算与格网密度统计方法", `description`: "单点路网密度计算指定范围内的道路总长度与面积的比值；格网密度统计是将研究区划分为规则格网，逐个计算每个格网的路网密度，生成密度分布图。用于分析城市路网空间分布特征、识别路网稀疏区域。", `kp_id`: "M4-022", `sort_order`: 22};

MERGE (node:KnowledgePoint {kp_id: "M4-023"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "路网连接度β指数计算原理", `description`: "β指数是路网连接度评价指标，计算原理为β=边数/节点数，反映路网的整体连接水平。β值越高说明路网连接越密集，β=1对应树状路网，β>1说明存在环路。用于宏观评价区域路网的发育程度与连接水平。", `kp_id`: "M4-023", `sort_order`: 23};

MERGE (node:KnowledgePoint {kp_id: "M4-024"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "路网连通性γ指数计算原理", `description`: "γ指数是路网连通性评价指标，计算原理为γ=实际边数/最大可能边数，取值0-1，反映路网连通的完善程度。γ值越接近1说明路网连通性越好。用于对比不同区域路网的连通水平，评价路网规划方案的连通效率。", `kp_id`: "M4-024", `sort_order`: 24};

MERGE (node:KnowledgePoint {kp_id: "M4-025"})
SET node = {`difficulty`: "进阶", `importance`: "了解", `name`: "路网环度α指数计算原理", `description`: "α指数是路网环度评价指标，计算原理为α=实际环路数/最大可能环路数，反映路网的环路发育程度。高α指数对应路网备选路径多、容错性强。用于评价路网的可靠性与绕行能力，支撑路网韧性分析。", `kp_id`: "M4-025", `sort_order`: 25};

MERGE (node:KnowledgePoint {kp_id: "M4-026"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网节点度中心性计算方法", `description`: "节点度中心性通过节点的度值衡量其在路网中的重要程度，度值越高说明节点连接的道路越多、交通地位越重要。计算方法为节点的入度与出度之和，可进行归一化处理。用于识别路网中的关键交叉口与枢纽节点。", `kp_id`: "M4-026", `sort_order`: 26};

MERGE (node:KnowledgePoint {kp_id: "M4-027"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "路网介数中心性计算方法", `description`: "介数中心性衡量节点作为路网交通中介的重要程度，计算方法为所有最短路径中经过该节点的路径数量占比。介数高的节点是路网的交通咽喉，一旦失效会严重影响路网通行效率。用于识别路网瓶颈节点与关键通道。", `kp_id`: "M4-027", `sort_order`: 27};

MERGE (node:KnowledgePoint {kp_id: "M4-028"})
SET node = {`difficulty`: "高阶", `importance`: "熟悉", `name`: "路网接近中心性计算方法", `description`: "接近中心性衡量节点到达路网中所有其他节点的便捷程度，计算方法为节点到所有其他节点的最短路径平均值的倒数。值越高说明节点整体可达性越好，越靠近路网几何中心。用于评价节点的区位优势与整体通达性。", `kp_id`: "M4-028", `sort_order`: 28};

MERGE (node:KnowledgePoint {kp_id: "M4-029"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "交通分配模型：全有全无分配", `description`: "全有全无分配是最简单的交通分配方法，原理是将OD间的全部交通量全部分配到最短路径上，不考虑道路容量与拥堵效应。模型计算简单，适用于低密度交通流、路网规划初步方案，结果与实际交通状况偏差较大。", `kp_id`: "M4-029", `sort_order`: 29};

MERGE (node:KnowledgePoint {kp_id: "M4-030"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "交通分配模型：容量限制分配", `description`: "容量限制分配在全有全无基础上考虑道路容量约束，当路段流量达到容量上限时，剩余流量分配到次优路径。采用迭代分配方式逐步加载流量，更新路段阻抗。相比全有全无更贴合实际，是常用的平衡分配简化方法。", `kp_id`: "M4-030", `sort_order`: 30};

MERGE (node:KnowledgePoint {kp_id: "M4-031"})
SET node = {`difficulty`: "高阶", `importance`: "核心", `name`: "交通分配模型：用户平衡（UE）分配", `description`: "用户平衡分配模型基于Wardrop第一原理，即平衡状态下每个OD对的所有使用路径的出行时间相等且最小，未使用路径的时间大于等于该值。模型通过迭代收敛求解，结果最接近实际交通流分布，是交通规划的核心模型。", `kp_id`: "M4-031", `sort_order`: 31};

MERGE (node:KnowledgePoint {kp_id: "M4-032"})
SET node = {`difficulty`: "高阶", `importance`: "掌握", `name`: "交通分配模型：系统最优（SO）分配", `description`: "系统最优分配基于Wardrop第二原理，目标是使路网总出行时间最小，追求系统整体效益最优。模型结果中部分路径的个人出行时间并非最短，常用于交通管理政策评估、路网整体效益评价，代表理想管控状态。", `kp_id`: "M4-032", `sort_order`: 32};

MERGE (node:KnowledgePoint {kp_id: "M4-033"})
SET node = {`difficulty`: "高阶", `importance`: "熟悉", `name`: "OD矩阵反推与估计技术", `description`: "OD矩阵反推是基于路段观测流量、路网拓扑与路径选择模型，反向推算OD出行分布的技术。常用方法有最大熵模型、广义最小二乘法、贝叶斯估计等。可在缺乏出行调查数据时估算OD矩阵，支撑交通分析与规划。", `kp_id`: "M4-033", `sort_order`: 33};

MERGE (node:KnowledgePoint {kp_id: "M4-034"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网拥堵热点空间识别算法", `description`: "拥堵热点识别算法基于动态路网速度或流量数据，通过空间聚类、阈值筛选、时空密度分析等方法，识别持续性拥堵的路段与交叉口。可结合时间维度分析拥堵演化规律，定位路网瓶颈，支撑交通治堵方案制定。", `kp_id`: "M4-034", `sort_order`: 34};

MERGE (node:KnowledgePoint {kp_id: "M4-035"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "路网薄弱节点空间识别算法", `description`: "薄弱节点识别算法通过中心性分析、连通可靠性分析、故障模拟等方法，识别对路网连通性影响大的关键节点。采用节点移除法模拟节点失效后的路网连通度变化，变化越大节点越薄弱。用于路网韧性提升与应急管理。", `kp_id`: "M4-035", `sort_order`: 35};

MERGE (node:KnowledgePoint {kp_id: "M4-036"})
SET node = {`difficulty`: "进阶", `importance`: "掌握", `name`: "多路径择优分析算法（规避拥堵/最短时间）", `description`: "多路径择优算法可同时输出多条备选路径，综合考虑时间、距离、拥堵程度等因素。通过路径相似度过滤重复路径，提供规避拥堵、距离最短、红绿灯少等不同偏好的路径方案，适配导航与出行决策需求。", `kp_id`: "M4-036", `sort_order`: 36};

MERGE (node:KnowledgePoint {kp_id: "M4-037"})
SET node = {`difficulty`: "进阶", `importance`: "熟悉", `name`: "慢行路网（步行/骑行）专属分析算法", `description`: "慢行路网专属算法针对步行、骑行的交通特性，适配慢行专用路网、过街设施、坡度阻抗等特征。采用慢行专属阻抗模型（考虑步行速度、过街等待、坡度影响），支持慢行路径规划、慢行系统连通性评价、慢行设施覆盖分析。", `kp_id`: "M4-037", `sort_order`: 37};

MERGE (node:KnowledgePoint {kp_id: "M4-038"})
SET node = {`difficulty`: "高阶", `importance`: "了解", `name`: "大规模路网并行计算优化算法", `description`: "大规模路网并行计算优化采用分布式计算框架，将路网分区、算法任务拆分到多个计算节点并行执行。优化方向包括：路网图分割、并行最短路径算法、分布式OD矩阵计算、GPU加速等。支撑省级、国家级超大规模路网的高效分析。", `kp_id`: "M4-038", `sort_order`: 38};

MERGE (node:KnowledgePoint {kp_id: "M5-001"})
SET node = {`name`: "静态GIS交通路网的定义与核心特征", `kp_id`: "M5-001", `sort_order`: 1, `difficulty`: "入门", `importance`: "核心", `description`: "静态路网是刻画道路永久固有属性的GIS路网模型，路网几何形态、拓扑连接、道路等级等要素长期保持固定，不承载瞬时实时交通状态数据，可作为整套交通路网分析的基础基底数据，是动态路网的底层骨架。"};

MERGE (node:KnowledgePoint {kp_id: "M5-002"})
SET node = {`name`: "静态路网的核心构成要素与固定属性", `kp_id`: "M5-002", `sort_order`: 2, `difficulty`: "入门", `importance`: "掌握", `description`: "核心构成要素包含道路路段、交叉口节点两大单元；固定属性涵盖道路几何信息、道路等级、车道数、设计限速、路面材质、通行方向、拓扑连接关系；不存储瞬时拥堵、临时施工、临时管制这类随时间变化的动态信息。"};

MERGE (node:KnowledgePoint {kp_id: "M5-003"})
SET node = {`name`: "静态路网的适用分析场景", `kp_id`: "M5-003", `sort_order`: 3, `difficulty`: "入门", `importance`: "掌握", `description`: "适用于国土空间规划、中长期路网布局评估、路网结构统计分析、基础底图制图输出；主要用于不考虑短时交通波动的宏观、静态评价任务，不适合实时路径规划、短时交通仿真。"};

MERGE (node:KnowledgePoint {kp_id: "M5-004"})
SET node = {`name`: "静态路网模型的局限性", `kp_id`: "M5-004", `sort_order`: 4, `difficulty`: "基础", `importance`: "熟悉", `description`: "静态路网无法表达早晚高峰拥堵、临时施工占道、临时交通管制、恶劣天气带来的通行能力衰减；基于静态路网开展路径规划、交通仿真会和真实交通现状产生明显偏差，不能支撑实时交通调度、动态导航类业务。"};

MERGE (node:KnowledgePoint {kp_id: "M5-005"})
SET node = {`name`: "动态GIS交通路网的定义与核心特征", `kp_id`: "M5-005", `sort_order`: 5, `difficulty`: "基础", `importance`: "核心", `description`: "动态GIS交通路网以静态路网作为底层骨架，叠加随时间变化的交通通行状态；路网阻抗、局部拓扑约束可以随时间发生改变，引入时间维度标签，能够还原真实交通状态随时间演化的客观规律。"};

MERGE (node:KnowledgePoint {kp_id: "M5-006"})
SET node = {`name`: "动态路网与静态路网的核心差异对比", `kp_id`: "M5-006", `sort_order`: 6, `difficulty`: "基础", `importance`: "掌握", `description`: "静态路网：几何、拓扑、全部属性长期固定，无时间维度；动态路网：基础几何一般保持不变，主要变化阻抗参数、通行约束、临时拓扑变更，新增时间维度标签，支持按照时间做时序查询。"};

MERGE (node:KnowledgePoint {kp_id: "M5-007"})
SET node = {`name`: "实时路况数据的接入格式与解析规则", `kp_id`: "M5-007", `sort_order`: 7, `difficulty`: "进阶", `importance`: "掌握", `description`: "实时路况主流交换格式包含JSON、protobuf；核心存储字段包含路段ID、时间戳、路段车速、拥堵等级；数据解析流程需要完成路段ID匹配映射、时间戳对齐、异常噪声数据过滤，保证和路网路段一一对应。"};

MERGE (node:KnowledgePoint {kp_id: "M5-008"})
SET node = {`name`: "浮动车轨迹数据反演路网车速的方法", `kp_id`: "M5-008", `sort_order`: 8, `difficulty`: "进阶", `importance`: "核心", `description`: "采集海量车载GPS浮动车轨迹点，通过地图匹配算法将轨迹点映射绑定到路网对应路段；统计单位时间内该路段全部匹配车辆的平均行驶速度，输出路段实时通行车速，作为动态路网阻抗的输入数据源。"};

MERGE (node:KnowledgePoint {kp_id: "M5-009"})
SET node = {`name`: "卡口流量数据更新路网通行状态的逻辑", `kp_id`: "M5-009", `sort_order`: 9, `difficulty`: "进阶", `importance`: "掌握", `description`: "交通卡口设备统计单位时间内驶入、驶出断面的车流量；结合道路设计通行能力计算路段饱和度，推导得到路段拥堵等级，更新动态路网当中路段通行状态属性，补充动态路网的流量维度信息。"};

MERGE (node:KnowledgePoint {kp_id: "M5-010"})
SET node = {`name`: "节假日路网通行规则动态适配机制", `kp_id`: "M5-010", `sort_order`: 10, `difficulty`: "进阶", `importance`: "熟悉", `description`: "节假日会出现高速免费通行、车流暴涨、临时交通管控等变化；动态路网依靠时间标签切换阻抗参数，启用或者关闭限行管制规则，完成节假日特殊交通条件下路网模型的适配。"};

MERGE (node:KnowledgePoint {kp_id: "M5-011"})
SET node = {`name`: "恶劣天气路网阻抗动态修正模型", `kp_id`: "M5-011", `sort_order`: 11, `difficulty`: "进阶", `importance`: "掌握", `description`: "雨雪雾等恶劣天气会降低车辆行驶速度；根据天气等级构建速度修正系数，对原有时间阻抗做放大修正，更新动态路网当中路段通行代价，还原恶劣天气下实际通行效率。"};

MERGE (node:KnowledgePoint {kp_id: "M5-012"})
SET node = {`name`: "施工占道路网动态拓扑修改规则", `kp_id`: "M5-012", `sort_order`: 12, `difficulty`: "进阶", `importance`: "核心", `description`: "施工占道场景不修改原始静态路网几何数据；依靠临时标记将部分车道或者整条路段标记为不可通行，增加绕行阻抗，同时记录约束生效时间与结束时间，到期自动恢复原有路网通行状态。"};

MERGE (node:KnowledgePoint {kp_id: "M5-013"})
SET node = {`name`: "交通管制场景下动态路网建模方法", `kp_id`: "M5-013", `sort_order`: 13, `difficulty`: "进阶", `importance`: "掌握", `description`: "针对临时封路、单向管制、分车型限行场景；不改动基础拓扑结构，增加附带有效时间范围的约束条件；路径计算阶段过滤被管制的路段与转向，实现管制效果。"};

MERGE (node:KnowledgePoint {kp_id: "M5-014"})
SET node = {`name`: "时空路网数据模型的核心架构", `kp_id`: "M5-014", `sort_order`: 14, `difficulty`: "进阶", `importance`: "核心", `description`: "同时组织空间维度（路段、节点几何拓扑）与时间维度（不同时刻通行状态）；整体分为三层：静态基础层、动态状态层、时间索引层；支持空间‑时间联合查询，是动态路网存储的标准架构。"};

MERGE (node:KnowledgePoint {kp_id: "M5-015"})
SET node = {`name`: "时空立方体路网存储结构原理", `kp_id`: "M5-015", `sort_order`: 15, `difficulty`: "高阶", `importance`: "了解", `description`: "时空立方体将空间位置与时间切片组织为立方体单元；每一个单元存储该路网对象在对应时间切片下的通行参数，实现路网空间数据与时序通行数据一体化存储。"};

MERGE (node:KnowledgePoint {kp_id: "M5-016"})
SET node = {`name`: "路网时间序列数据的组织方式", `kp_id`: "M5-016", `sort_order`: 16, `difficulty`: "进阶", `importance`: "掌握", `description`: "以路段ID作为主键，单条记录绑定时间戳，存储对应时刻车速、流量、拥堵等级；按照小时或者日粒度做切片存储，构建每一条路段独立的交通状态时间序列数据表。"};

MERGE (node:KnowledgePoint {kp_id: "M5-017"})
SET node = {`name`: "路网小时级时空变化特征提取", `kp_id`: "M5-017", `sort_order`: 17, `difficulty`: "进阶", `importance`: "掌握", `description`: "按照小时时间切片统计各路段车速、拥堵时长指标；识别早高峰、晚高峰时段路网拥堵空间分布，提取小时粒度下路网交通状态的空间变化规律。"};

MERGE (node:KnowledgePoint {kp_id: "M5-018"})
SET node = {`name`: "路网日度、月度时空演变规律分析", `kp_id`: "M5-018", `sort_order`: 18, `difficulty`: "进阶", `importance`: "熟悉", `description`: "聚合日、月度维度的交通时序数据；分析工作日、周末、月度车流的差异性，识别路网长期周期性变化特征，为中长期交通规划评估提供依据。"};

MERGE (node:KnowledgePoint {kp_id: "M5-019"})
SET node = {`name`: "动态路网阻抗实时更新流程", `kp_id`: "M5-019", `sort_order`: 19, `difficulty`: "进阶", `importance`: "核心", `description`: "完整流程：实时数据接入→数据降噪校验→路段匹配映射→阻抗系数计算→覆盖更新动态阻抗字段；全程保留原始静态阻抗，方便业务需要时完成状态重置。"};

MERGE (node:KnowledgePoint {kp_id: "M5-020"})
SET node = {`name`: "动态路网拓扑临时变更记录方法", `kp_id`: "M5-020", `sort_order`: 20, `difficulty`: "进阶", `importance`: "掌握", `description`: "采用「时间区间+约束标记」方式记录临时拓扑变化；不删除原始连通关系，记录要素包含生效时间、失效时间、约束类型（封路、转向禁止等），到期自动恢复原始拓扑连接。"};

MERGE (node:KnowledgePoint {kp_id: "M5-021"})
SET node = {`name`: "宏观交通模型与GIS路网的耦合逻辑", `kp_id`: "M5-021", `sort_order`: 21, `difficulty`: "高阶", `importance`: "熟悉", `description`: "宏观交通模型输出区域OD矩阵、路段宏观流量结果；将流量结果回写至GIS路网路段属性字段；GIS负责空间可视化、空间统计分析，宏观模型负责交通总量推演计算，实现二者闭环。"};

MERGE (node:KnowledgePoint {kp_id: "M5-022"})
SET node = {`name`: "中观交通仿真模型的路网数据对接方式", `kp_id`: "M5-022", `sort_order`: 22, `difficulty`: "高阶", `importance`: "熟悉", `description`: "中观交通仿真以路段作为基础计算单元；将GIS路网的几何、拓扑、车道数、限速导出作为仿真输入；仿真输出流量、车速结果回写GIS路网图层开展空间分析。"};

MERGE (node:KnowledgePoint {kp_id: "M5-023"})
SET node = {`name`: "微观交通仿真的精细路网适配要求", `kp_id`: "M5-023", `sort_order`: 23, `difficulty`: "高阶", `importance`: "掌握", `description`: "微观仿真面向单车个体仿真，需要车道级细节；GIS路网数据需要拆解到车道实体，提供车道转向、车道宽度、交叉口车道分配信息，满足微观仿真精细输入条件。"};

MERGE (node:KnowledgePoint {kp_id: "M5-024"})
SET node = {`name`: "VISSIM仿真与GIS路网数据交互方法", `kp_id`: "M5-024", `sort_order`: 24, `difficulty`: "高阶", `importance`: "熟悉", `description`: "GIS平台完成路网预处理后导出*.inpx等交换格式，导入VISSIM开展仿真运算；VISSIM仿真输出速度、流量结果导出后，重新关联回GIS路网图层，完成空间分析与制图。"};

MERGE (node:KnowledgePoint {kp_id: "M5-025"})
SET node = {`name`: "TransCAD交通软件路网兼容规则", `kp_id`: "M5-025", `sort_order`: 25, `difficulty`: "高阶", `importance`: "熟悉", `description`: "TransCAD拥有自有路网存储格式，支持导入shp等通用GIS矢量路网；导入前GIS路网需要补齐阻抗、转向、车道相关属性；仿真运算输出结果可以导出回GIS平台继续分析。"};

MERGE (node:KnowledgePoint {kp_id: "M5-026"})
SET node = {`name`: "动态路网拥堵时空演化建模", `kp_id`: "M5-026", `sort_order`: 26, `difficulty`: "进阶", `importance`: "核心", `description`: "串联不同时刻拥堵空间分布状态，构建拥堵传播模型；模拟拥堵沿路段扩散、消散全过程，还原拥堵随时间、空间演变完整规律，定位拥堵传播路径。"};

MERGE (node:KnowledgePoint {kp_id: "M5-027"})
SET node = {`name`: "路网高峰时段时空特征聚类分析", `kp_id`: "M5-027", `sort_order`: 27, `difficulty`: "进阶", `importance`: "掌握", `description`: "对各路段时序拥堵数据执行聚类运算；划分多种拥堵模式类别，识别持续拥堵路段、间歇性拥堵路段，定位路网高峰时段的问题区域。"};

MERGE (node:KnowledgePoint {kp_id: "M5-028"})
SET node = {`name`: "静态路网批量更新动态数据的流程", `kp_id`: "M5-028", `sort_order`: 28, `difficulty`: "进阶", `importance`: "掌握", `description`: "加载静态路网底图层；接入时序动态数据表；基于路段ID属性做连接匹配；更新路网动态属性字段；生成同时具备静态基底、动态时序属性的完整路网数据集。"};

MERGE (node:KnowledgePoint {kp_id: "M5-029"})
SET node = {`name`: "时空路网数据的版本管理机制", `kp_id`: "M5-029", `sort_order`: 29, `difficulty`: "高阶", `importance`: "掌握", `description`: "按照时间快照生成路网版本；每一个时间切片保存一份路网状态快照；支持回溯历史任意时间点路网状态，方便不同时期交通状态对比分析。"};

MERGE (node:KnowledgePoint {kp_id: "M5-030"})
SET node = {`name`: "实时路网数据的降噪与纠错处理", `kp_id`: "M5-030", `sort_order`: 30, `difficulty`: "进阶", `importance`: "核心", `description`: "浮动车、卡口采集得到的实时原始数据存在大量异常值；采用阈值过滤、邻接路段平滑、时间窗口校验等方法剔除异常车速、流量，避免错误数据污染动态路网模型。"};

MERGE (node:KnowledgePoint {kp_id: "M5-031"})
SET node = {`name`: "动态路网路径规划的实时响应机制", `kp_id`: "M5-031", `sort_order`: 31, `difficulty`: "高阶", `importance`: "掌握", `description`: "路径计算读取当前时刻动态阻抗；当路况发生改变时实时刷新阻抗参数；用户发起路径查询时调用最新阻抗，输出适配当下真实交通状态的出行路线。"};

MERGE (node:KnowledgePoint {kp_id: "M5-032"})
SET node = {`name`: "突发事件下路网动态推演模型", `kp_id`: "M5-032", `sort_order`: 32, `difficulty`: "高阶", `importance`: "掌握", `description`: "模拟交通事故、灾害造成路段通行能力下降；输入事件发生时间、受影响路段，推演拥堵扩散范围、通行时间变化结果，为应急决策提供数据支撑。"};

MERGE (node:KnowledgePoint {kp_id: "M5-033"})
SET node = {`name`: "城市路网时空活力评价模型", `kp_id`: "M5-033", `sort_order`: 33, `difficulty`: "进阶", `importance`: "熟悉", `description`: "融合不同时段路网流量、车速、出行量多源数据；构建综合评价指标，量化城市不同片区路网交通活力高低，用于城市更新、国土空间规划评估。"};

MERGE (node:KnowledgePoint {kp_id: "M5-034"})
SET node = {`name`: "动态路网数据可视化表达规则", `kp_id`: "M5-034", `sort_order`: 34, `difficulty`: "进阶", `importance`: "掌握", `description`: "采用颜色分级渲染表达路段拥堵等级；配置时间轴控件切换不同时刻路网状态；严格区分道路永久固有属性与瞬时动态状态，避免把瞬时交通状态误展示为道路固有属性。"};

MERGE (node:KnowledgePoint {kp_id: "M5-035"})
SET node = {`name`: "时空路网分析结果的落地应用逻辑", `kp_id`: "M5-035", `sort_order`: 35, `difficulty`: "进阶", `importance`: "掌握", `description`: "时空路网分析输出拥堵热点、通行能力短板；输出结果对接规划、交管业务部门；定位问题路段，支撑信号配时、道路改造、交通管制方案制定落地。"};

MERGE (node:KnowledgePoint {kp_id: "M5-036"})
SET node = {`name`: "动静结合路网模型的搭建方法", `kp_id`: "M5-036", `sort_order`: 36, `difficulty`: "进阶", `importance`: "核心", `description`: "完整保留静态路网存储道路固有属性；建立独立动态数据表存储随时间变化的通行状态；依靠路段ID外键关联两张数据表，实现静态基底和动态状态解耦存储。"};

MERGE (node:KnowledgePoint {kp_id: "M6-001"})
SET node = {`name`: "综合立体交通网的概念与构成", `kp_id`: "M6-001", `sort_order`: 1, `difficulty`: "入门", `importance`: "核心", `description`: "综合立体交通网由公路、铁路、城市轨道交通、水运、航空、管道等多种运输网络共同组成；核心强调不同交通方式协同衔接，支撑多模式一体化客运出行与货物多式联运。"};

MERGE (node:KnowledgePoint {kp_id: "M6-002"})
SET node = {`name`: "铁路路网GIS建模：线路、车站、枢纽、道岔", `kp_id`: "M6-002", `sort_order`: 2, `difficulty`: "基础", `importance`: "掌握", `description`: "铁路线路抽象为网络边；车站、枢纽、道岔作为网络节点；道岔节点约束列车允许通行转向方向；枢纽节点承担多条线路交汇，记录线路之间换乘、转场关系。"};

MERGE (node:KnowledgePoint {kp_id: "M6-003"})
SET node = {`name`: "铁路线路等级与技术标准属性", `kp_id`: "M6-003", `sort_order`: 3, `difficulty`: "基础", `importance`: "掌握", `description`: "铁路属性包含高铁、客专、普速、货运线路等级；存储设计时速、限重、轨距等技术参数；参数作为铁路网络阻抗计算的基础输入。"};

MERGE (node:KnowledgePoint {kp_id: "M6-004"})
SET node = {`name`: "城市轨道交通路网建模：地铁、轻轨、有轨电车", `kp_id`: "M6-004", `sort_order`: 4, `difficulty`: "基础", `importance`: "掌握", `description`: "轨道线路作为网络边，站点作为网络节点；换乘站需要区分物理站点实体和多条逻辑线路节点；建模不同线路之间换乘连接关系、换乘步行距离。"};

MERGE (node:KnowledgePoint {kp_id: "M6-005"})
SET node = {`name`: "公交线网GIS建模：线路、站点、场站", `kp_id`: "M6-005", `sort_order`: 5, `difficulty`: "基础", `importance`: "掌握", `description`: "公交站点为网络节点；公交线路由若干道路路段有序组合而成；场站作为线路起终点实体；存储线路走向、发车间隔、运营时间核心属性。"};

MERGE (node:KnowledgePoint {kp_id: "M6-006"})
SET node = {`name`: "水运航道网络建模：航道、港口、船闸、锚地", `kp_id`: "M6-006", `sort_order`: 6, `difficulty`: "基础", `importance`: "熟悉", `description`: "航道抽象为网络边；港口、船闸、锚地作为网络节点；航道通行能力会受水位季节变化影响，需要纳入动态属性参与网络分析。"};

MERGE (node:KnowledgePoint {kp_id: "M6-007"})
SET node = {`name`: "航空航路与机场净空GIS分析", `kp_id`: "M6-007", `sort_order`: 7, `difficulty`: "基础", `importance`: "了解", `description`: "航路属于逻辑网络，不完全贴合地面几何实体；机场作为网络节点；GIS主要用于机场净空障碍物检测、航线空间分布统计分析。"};

MERGE (node:KnowledgePoint {kp_id: "M6-008"})
SET node = {`name`: "管道运输网络GIS建模：油气管道、泵站", `kp_id`: "M6-008", `sort_order`: 8, `difficulty`: "基础", `importance`: "了解", `description`: "管道作为网络边；泵站、阀室作为网络节点；构建管网拓扑关系，用于管线连通分析、风险蔓延模拟，属于广义交通物流网络。"};

MERGE (node:KnowledgePoint {kp_id: "M6-009"})
SET node = {`name`: "邮政快递网络建模：网点、分拣中心、投递路线", `kp_id`: "M6-009", `sort_order`: 9, `difficulty`: "进阶", `importance`: "了解", `description`: "分拣中心、网点作为网络节点；干线运输线路、末端投递路线作为网络边；支撑快递路径优化、网点可达性评估分析。"};

MERGE (node:KnowledgePoint {kp_id: "M6-010"})
SET node = {`name`: "多模式交通网络（Multimodal Network）融合架构", `kp_id`: "M6-010", `sort_order`: 10, `difficulty`: "进阶", `importance`: "核心", `description`: "各个交通子网保留自身独立拓扑；不直接将不同运输方式的边互相连接；仅在枢纽/换乘节点建立跨模式逻辑关联，以此完成多网络融合。"};

MERGE (node:KnowledgePoint {kp_id: "M6-011"})
SET node = {`name`: "多式联运枢纽的拓扑衔接建模", `kp_id`: "M6-011", `sort_order`: 11, `difficulty`: "进阶", `importance`: "核心", `description`: "在枢纽内部拆解不同交通子网络接入点；建立不同子网络节点之间换乘关系；记录换乘步行距离、换乘耗时，作为跨模式网络分析的阻抗参数。"};

MERGE (node:KnowledgePoint {kp_id: "M6-012"})
SET node = {`name`: "铁水联运网络阻抗模型", `kp_id`: "M6-012", `sort_order`: 12, `difficulty`: "进阶", `importance`: "掌握", `description`: "总阻抗包含铁路运输时间、水运航行时间；叠加港口装卸作业时间、两种交通模式之间中转等待时间，共同组成铁水联运完整通行代价。"};

MERGE (node:KnowledgePoint {kp_id: "M6-013"})
SET node = {`name`: "公铁联运网络路径规划", `kp_id`: "M6-013", `sort_order`: 13, `difficulty`: "进阶", `importance`: "掌握", `description`: "同时调用公路路网、铁路路网两套网络；在货运枢纽节点完成运输模式切换；路径算法综合公路短驳、铁路干线运输、中转等待综合代价求解最优方案。"};

MERGE (node:KnowledgePoint {kp_id: "M6-014"})
SET node = {`name`: "空铁联运网络可达性分析", `kp_id`: "M6-014", `sort_order`: 14, `difficulty`: "进阶", `importance`: "熟悉", `description`: "结合城市轨道交通、铁路、机场节点；计算各个地点到达机场全过程出行时间；评价空铁联运服务覆盖范围。"};

MERGE (node:KnowledgePoint {kp_id: "M6-015"})
SET node = {`name`: "多模式换乘节点建模与换乘时间计算", `kp_id`: "M6-015", `sort_order`: 15, `difficulty`: "进阶", `importance`: "掌握", `description`: "同一个物理枢纽内部，不同换乘通道具备不同步行距离；依据通道距离、人流拥堵系数计算换乘耗时，作为网络分析阻抗参数。"};

MERGE (node:KnowledgePoint {kp_id: "M6-016"})
SET node = {`name`: "综合交通枢纽客流集散GIS分析", `kp_id`: "M6-016", `sort_order`: 16, `difficulty`: "进阶", `importance`: "掌握", `description`: "以GIS路网为基础，统计枢纽周边道路、轨道、公交的客流供给能力；评估枢纽客流疏散能力，识别集散瓶颈点位。"};

MERGE (node:KnowledgePoint {kp_id: "M6-017"})
SET node = {`name`: "多模态网络数据标准与交换格式", `kp_id`: "M6-017", `sort_order`: 17, `difficulty`: "进阶", `importance`: "了解", `description`: "包含GTFS、NetCDF以及各类交通规划软件交换格式；实现公路、轨道、水运等多源异构交通数据统一交换。"};

MERGE (node:KnowledgePoint {kp_id: "M6-018"})
SET node = {`name`: "GTFS公共交通数据格式与GIS转换", `kp_id`: "M6-018", `sort_order`: 18, `difficulty`: "进阶", `importance`: "掌握", `description`: "GTFS是国际通用公交数据标准，存储线路、站点、时刻表信息；可以通过工具转换生成GIS点线矢量图层，构建公交网络模型。"};

MERGE (node:KnowledgePoint {kp_id: "M6-019"})
SET node = {`name`: "铁路时刻表数据与路网空间匹配", `kp_id`: "M6-019", `sort_order`: 19, `difficulty`: "进阶", `importance`: "熟悉", `description`: "时刻表存储列车到发时间信息；将车次运行站点序列匹配映射到铁路GIS路网节点，实现时间信息和空间路网实体关联。"};

MERGE (node:KnowledgePoint {kp_id: "M6-020"})
SET node = {`name`: "航班数据与航路网络空间分析", `kp_id`: "M6-020", `sort_order`: 20, `difficulty`: "进阶", `importance`: "了解", `description`: "包含航班起降时间、起终点机场数据；关联航路网络节点，统计航线密度，开展航空网络空间结构分析。"};

MERGE (node:KnowledgePoint {kp_id: "M6-021"})
SET node = {`name`: "内河航运水位与通行能力GIS分析", `kp_id`: "M6-021", `sort_order`: 21, `difficulty`: "进阶", `importance`: "熟悉", `description`: "将水位监测数据关联航道路网；水位变化改变航道通航等级，更新航道允许通行船舶吨位，完成水运网络动态评估。"};

MERGE (node:KnowledgePoint {kp_id: "M6-022"})
SET node = {`name`: "综合交通网连通性评价指标体系", `kp_id`: "M6-022", `sort_order`: 22, `difficulty`: "进阶", `importance`: "掌握", `description`: "指标包含全网连通度、不同模式之间衔接效率、枢纽可达性；量化整个多模态网络连通完备水平。"};

MERGE (node:KnowledgePoint {kp_id: "M6-023"})
SET node = {`name`: "多式联运路径优化算法", `kp_id`: "M6-023", `sort_order`: 23, `difficulty`: "高阶", `importance`: "掌握", `description`: "同时考虑多种运输模式，纳入中转切换代价；求解货运从起点至终点总时间或者总费用最优的联运方案。"};

MERGE (node:KnowledgePoint {kp_id: "M6-024"})
SET node = {`name`: "综合交通枢纽选址GIS模型", `kp_id`: "M6-024", `sort_order`: 24, `difficulty`: "高阶", `importance`: "掌握", `description`: "输入多模态路网、人口、产业分布数据；利用GIS可达性分析，筛选适合建设综合交通枢纽的候选点位。"};

MERGE (node:KnowledgePoint {kp_id: "M6-025"})
SET node = {`name`: "区域交通一体化路网协同分析", `kp_id`: "M6-025", `sort_order`: 25, `difficulty`: "进阶", `importance`: "熟悉", `description`: "跨行政区整合公路、轨道网络；分析省界、市界处路网衔接短板，支撑区域交通协同规划。"};

MERGE (node:KnowledgePoint {kp_id: "M6-026"})
SET node = {`name`: "城乡交通网络通达性对比分析", `kp_id`: "M6-026", `sort_order`: 26, `difficulty`: "进阶", `importance`: "掌握", `description`: "分别计算城市、乡村区域路网可达性指标；识别乡村路网通达短板，服务农村公路建设评估。"};

MERGE (node:KnowledgePoint {kp_id: "M6-027"})
SET node = {`name`: "边境口岸与国际通道GIS分析", `kp_id`: "M6-027", `sort_order`: 27, `difficulty`: "进阶", `importance`: "了解", `description`: "将口岸作为多模态网络关键节点；分析国际公路、铁路通道连通状态，评估跨境交通网络运行条件。"};

MERGE (node:KnowledgePoint {kp_id: "M6-028"})
SET node = {`name`: "综合交通网与国土空间规划耦合", `kp_id`: "M6-028", `sort_order`: 28, `difficulty`: "进阶", `importance`: "掌握", `description`: "把多模态路网和用地、城镇开发边界做叠加分析；校验交通网络布局是否匹配国土空间开发格局。"};

MERGE (node:KnowledgePoint {kp_id: "M6-029"})
SET node = {`name`: "多模态交通网络韧性评估", `kp_id`: "M6-029", `sort_order`: 29, `difficulty`: "高阶", `importance`: "熟悉", `description`: "模拟节点、线路损毁场景；计算网络连通能力下降幅度；衡量多模式网络抵御灾害、故障之后维持服务的能力。"};

MERGE (node:KnowledgePoint {kp_id: "M6-030"})
SET node = {`name`: "综合交通信息平台数据集成架构", `kp_id`: "M6-030", `sort_order`: 30, `difficulty`: "进阶", `importance`: "熟悉", `description`: "架构四层：数据源接入层、数据清洗融合层、网络模型层、服务输出层；汇聚公路、轨道、水运、航空多源交通数据。"};

MERGE (node:KnowledgePoint {kp_id: "M6-031"})
SET node = {`name`: "多源交通网络数据融合方法", `kp_id`: "M6-031", `sort_order`: 31, `difficulty`: "进阶", `importance`: "核心", `description`: "对不同来源多模态路网完成坐标统一、实体对齐、冲突检测；消除同名站点、线路ID不一致问题，融合形成统一综合网络。"};

MERGE (node:KnowledgePoint {kp_id: "M6-032"})
SET node = {`name`: "综合交通一张图数据规范", `kp_id`: "M6-032", `sort_order`: 32, `difficulty`: "进阶", `importance`: "掌握", `description`: "统一坐标系、图层命名、属性字段；规范公路、轨道、水运等图层要素，实现多模态交通数据可视化一张图展示。"};

MERGE (node:KnowledgePoint {kp_id: "M6-033"})
SET node = {`name`: "跨运输方式数据共享与互操作", `kp_id`: "M6-033", `sort_order`: 33, `difficulty`: "进阶", `importance`: "熟悉", `description`: "制定统一数据字典、接口规范；解决铁路、公路、水运不同部门数据格式不统一难题，实现跨行业数据调用共享。"};

MERGE (node:KnowledgePoint {kp_id: "M6-034"})
SET node = {`name`: "综合交通网络仿真模型对接", `kp_id`: "M6-034", `sort_order`: 34, `difficulty`: "高阶", `importance`: "了解", `description`: "将GIS构建的多模态网络导入交通仿真软件；仿真输出流量、运力结果回写GIS，实现仿真‑空间分析闭环。"};

MERGE (node:KnowledgePoint {kp_id: "M6-035"})
SET node = {`name`: "多模态交通网络知识图谱实体关系设计", `kp_id`: "M6-035", `sort_order`: 35, `difficulty`: "高阶", `importance`: "熟悉", `description`: "定义公路、铁路、轨道、港口、枢纽等实体；设计“换乘、途经、联运、属于”等跨模式关系；将多模态路网语义、拓扑存入知识图谱。"};

MERGE (node:KnowledgePoint {kp_id: "M7-001"})
SET node = {`name`: "ArcGIS路网基础数据导入与图层配置", `kp_id`: "M7-001", `sort_order`: 1, `difficulty`: "入门", `importance`: "掌握", `description`: "将shp等路网矢量数据导入ArcGIS软件；设置图层坐标系、字段别名；检查几何错误，完成路网分析前期数据准备。"};

MERGE (node:KnowledgePoint {kp_id: "M7-002"})
SET node = {`name`: "ArcGIS网络数据集创建完整流程", `kp_id`: "M7-002", `sort_order`: 2, `difficulty`: "基础", `importance`: "核心", `description`: "新建网络数据集，选取路网线要素；配置阻抗属性、通行方向规则、转向规则；执行拓扑构建，生成可供网络分析运算的网络数据集。"};

MERGE (node:KnowledgePoint {kp_id: "M7-003"})
SET node = {`name`: "ArcGIS路网阻抗属性赋值操作", `kp_id`: "M7-003", `sort_order`: 3, `difficulty`: "基础", `importance`: "掌握", `description`: "编辑属性表，填写距离、时间、费用阻抗字段；可使用字段计算器结合路段长度、限速字段自动计算通行时间阻抗。"};

MERGE (node:KnowledgePoint {kp_id: "M7-004"})
SET node = {`name`: "ArcGIS路网转向规则编辑配置", `kp_id`: "M7-004", `sort_order`: 4, `difficulty`: "进阶", `importance`: "掌握", `description`: "打开转向编辑器，在交叉口节点配置允许/禁止转向约束；记录转弯限制、转弯延迟时间，还原真实路口通行约束条件。"};

MERGE (node:KnowledgePoint {kp_id: "M7-005"})
SET node = {`name`: "ArcGIS最短路径分析工具实操", `kp_id`: "M7-005", `sort_order`: 5, `difficulty`: "基础", `importance`: "掌握", `description`: "使用网络分析模块的最短路径工具；录入起点终点，选择对应阻抗；执行计算输出最优路径结果。"};

MERGE (node:KnowledgePoint {kp_id: "M7-006"})
SET node = {`name`: "ArcGIS服务区与可达性分析实操", `kp_id`: "M7-006", `sort_order`: 6, `difficulty`: "基础", `importance`: "核心", `description`: "新建服务区图层；录入设施点位，设置时间/距离阈值；运算生成路网可达服务区面，表达沿道路可以到达的实际范围。"};

MERGE (node:KnowledgePoint {kp_id: "M7-007"})
SET node = {`name`: "ArcGIS OD成本矩阵生成方法", `kp_id`: "M7-007", `sort_order`: 7, `difficulty`: "进阶", `importance`: "掌握", `description`: "调用OD成本矩阵工具；输入多点起点、多点终点；批量计算每一对OD之间通行时间、距离代价，输出OD表格。"};

MERGE (node:KnowledgePoint {kp_id: "M7-008"})
SET node = {`name`: "ArcGIS路网拓扑检查与修复工具使用", `kp_id`: "M7-008", `sort_order`: 8, `difficulty`: "基础", `importance`: "核心", `description`: "使用拓扑工具集，配置拓扑规则（不能重叠、禁止悬挂、节点必须捕捉）；执行检查，输出拓扑错误，使用修复工具处理伪节点、悬挂节点等问题。"};

MERGE (node:KnowledgePoint {kp_id: "M7-009"})
SET node = {`name`: "ArcGIS线性参考与动态分段实操", `kp_id`: "M7-009", `sort_order`: 9, `difficulty`: "进阶", `importance`: "掌握", `description`: "建立LRS线性参考，为路网线要素添加M值；导入事件表，执行动态分段，将桩号事件转换为地图可视化要素。"};

MERGE (node:KnowledgePoint {kp_id: "M7-010"})
SET node = {`name`: "QGIS路网数据加载与坐标系配置", `kp_id`: "M7-010", `sort_order`: 10, `difficulty`: "入门", `importance`: "掌握", `description`: "导入路网矢量图层；设置项目CRS坐标系；执行坐标转换，保证全部路网图层空间参考统一。"};

MERGE (node:KnowledgePoint {kp_id: "M7-011"})
SET node = {`name`: "QGIS开源路网分析插件安装与使用", `kp_id`: "M7-011", `sort_order`: 11, `difficulty`: "基础", `importance`: "掌握", `description`: "安装Graph、NetworkAnalysis等第三方插件；借助插件实现最短路径、服务区等路网网络分析功能。"};

MERGE (node:KnowledgePoint {kp_id: "M7-012"})
SET node = {`name`: "QGIS OSM路网数据下载与解析方法", `kp_id`: "M7-012", `sort_order`: 12, `difficulty`: "基础", `importance`: "熟悉", `description`: "使用OSM下载插件获取开源路网；解析OSM标签，提取道路等级、通行方向、限速属性，生成标准矢量路网。"};

MERGE (node:KnowledgePoint {kp_id: "M7-013"})
SET node = {`name`: "QGIS Graph模型路网构建实操", `kp_id`: "M7-013", `sort_order`: 13, `difficulty`: "进阶", `importance`: "掌握", `description`: "利用Graph插件读取路网图层；构建节点‑边图模型；配置阻抗字段，执行网络路径计算。"};

MERGE (node:KnowledgePoint {kp_id: "M7-014"})
SET node = {`name`: "QGIS路网拓扑清洗批量操作", `kp_id`: "M7-014", `sort_order`: 14, `difficulty`: "进阶", `importance`: "掌握", `description`: "使用几何处理工具，批量执行删除重复几何、合并线段、捕捉节点，批量修复悬挂节点、重复线段等拓扑问题。"};

MERGE (node:KnowledgePoint {kp_id: "M7-015"})
SET node = {`name`: "GeoPandas路网数据读取与预处理代码实现", `kp_id`: "M7-015", `sort_order`: 15, `difficulty`: "进阶", `importance`: "掌握", `description`: "Python代码读取shp/geojson路网；完成投影转换、裁剪、要素筛选，实现路网批量预处理。"};

MERGE (node:KnowledgePoint {kp_id: "M7-016"})
SET node = {`name`: "GeoPandas路网几何修改与属性更新", `kp_id`: "M7-016", `sort_order`: 16, `difficulty`: "进阶", `importance`: "掌握", `description`: "调用GeoPandas几何API，完成线段合并、节点捕捉；修改DataFrame属性列，批量更新道路等级、限速等字段。"};

MERGE (node:KnowledgePoint {kp_id: "M7-017"})
SET node = {`name`: "NetworkX路网图模型构建代码逻辑", `kp_id`: "M7-017", `sort_order`: 17, `difficulty`: "进阶", `importance`: "掌握", `description`: "从GeoPandas路网当中提取节点、边要素；转换为NetworkX图对象；构建抽象图模型用于网络统计计算。"};

MERGE (node:KnowledgePoint {kp_id: "M7-018"})
SET node = {`name`: "NetworkX路网中心性指标计算代码实现", `kp_id`: "M7-018", `sort_order`: 18, `difficulty`: "高阶", `importance`: "掌握", `description`: "调用NetworkX内置函数，计算度中心性、介数中心性、接近中心性等路网拓扑指标，输出各节点指标计算结果。"};

MERGE (node:KnowledgePoint {kp_id: "M7-019"})
SET node = {`name`: "PyQGIS批量处理路网数据脚本开发", `kp_id`: "M7-019", `sort_order`: 19, `difficulty`: "高阶", `importance`: "熟悉", `description`: "编写PyQGIS Python脚本；自动化完成路网加载、拓扑清洗、网络分析，搭建大批量路网数据处理流水线。"};

MERGE (node:KnowledgePoint {kp_id: "M7-020"})
SET node = {`name`: "PostGIS空间数据库路网数据表创建", `kp_id`: "M7-020", `sort_order`: 20, `difficulty`: "进阶", `importance`: "掌握", `description`: "在PostgreSQL数据库中启用PostGIS扩展；创建路网数据表，设置几何字段、道路业务属性字段，存储路网矢量数据。"};

MERGE (node:KnowledgePoint {kp_id: "M7-021"})
SET node = {`name`: "PostGIS路网空间索引搭建方法", `kp_id`: "M7-021", `sort_order`: 21, `difficulty`: "进阶", `importance`: "核心", `description`: "针对路网geometry几何字段创建GIST空间索引；大幅加速空间查询、空间连接运算，提升大规模路网数据库查询性能。"};

MERGE (node:KnowledgePoint {kp_id: "M7-022"})
SET node = {`name`: "PostGIS路网拓扑查询SQL语句编写", `kp_id`: "M7-022", `sort_order`: 22, `difficulty`: "进阶", `importance`: "掌握", `description`: "编写SQL语句实现查询相邻路段、相交节点、查找悬挂节点；调用PostGIS空间函数完成路网拓扑检索。"};

MERGE (node:KnowledgePoint {kp_id: "M7-023"})
SET node = {`name`: "pgRouting插件安装与路网适配配置", `kp_id`: "M7-023", `sort_order`: 23, `difficulty`: "进阶", `importance`: "核心", `description`: "数据库安装pgRouting扩展；对路网表新增源节点、目标节点字段；执行拓扑生成，完成路网适配，支持网络路径分析。"};

MERGE (node:KnowledgePoint {kp_id: "M7-024"})
SET node = {`name`: "pgRouting最短路径SQL查询实现", `kp_id`: "M7-024", `sort_order`: 24, `difficulty`: "进阶", `importance`: "掌握", `description`: "调用pgRouting的Dijkstra函数，传入起点ID、终点ID、阻抗字段参数；直接在数据库SQL语句内部完成最短路径求解运算。"};

MERGE (node:KnowledgePoint {kp_id: "M7-025"})
SET node = {`name`: "超图SuperMap路网分析功能实操", `kp_id`: "M7-025", `sort_order`: 25, `difficulty`: "进阶", `importance`: "掌握", `description`: "SuperMap平台中构建网络数据集；配置阻抗、转向约束；执行路径分析、服务区、动态分段，适配国内CGCS2000坐标系。"};

MERGE (node:KnowledgePoint {kp_id: "M7-026"})
SET node = {`name`: "国产GIS平台（MapGIS）路网功能", `kp_id`: "M7-026", `sort_order`: 26, `difficulty`: "进阶", `importance`: "了解", `description`: "MapGIS支持网络数据集构建、拓扑检查修复、网络分析、动态分段；面向国内政务交通项目落地使用。"};

MERGE (node:KnowledgePoint {kp_id: "M7-027"})
SET node = {`name`: "开源路网批量分析自动化流程搭建", `kp_id`: "M7-027", `sort_order`: 27, `difficulty`: "高阶", `importance`: "掌握", `description`: "串联GeoPandas‑NetworkX‑PostGIS‑pgRouting工具链；构建脚本流水线，自动完成路网读取、清洗、分析、结果导出。"};

MERGE (node:KnowledgePoint {kp_id: "M7-028"})
SET node = {`name`: "路网大数据量存储优化方案", `kp_id`: "M7-028", `sort_order`: 28, `difficulty`: "高阶", `importance`: "熟悉", `description`: "建立空间索引、数据分块分区存储；为业务属性建立普通索引；裁剪无关区域数据，提升千万级路网读写查询性能。"};

MERGE (node:KnowledgePoint {kp_id: "M7-029"})
SET node = {`name`: "WebGIS路网矢量数据渲染规则", `kp_id`: "M7-029", `sort_order`: 29, `difficulty`: "基础", `importance`: "掌握", `description`: "按照道路等级设置不同线宽、颜色；配置缩放级别可见范围；避免低缩放级别加载全部精细路网造成前端页面卡顿。"};

MERGE (node:KnowledgePoint {kp_id: "M7-030"})
SET node = {`name`: "WebGIS路网分级显示配置", `kp_id`: "M7-030", `sort_order`: 30, `difficulty`: "基础", `importance`: "掌握", `description`: "设置比例尺分级；大比例尺下展示全部细节道路；小比例尺只展示高速、国道主干路网，实现LOD分级渲染。"};

MERGE (node:KnowledgePoint {kp_id: "M7-031"})
SET node = {`name`: "前端在线路网路径查询功能实现逻辑", `kp_id`: "M7-031", `sort_order`: 31, `difficulty`: "进阶", `importance`: "掌握", `description`: "前端接收起止点参数；把请求发送后端pgRouting / 网络分析服务；后端完成路径计算，返回路径几何给前端渲染展示。"};

MERGE (node:KnowledgePoint {kp_id: "M7-032"})
SET node = {`name`: "路网数据切片处理与发布方法", `kp_id`: "M7-032", `sort_order`: 32, `difficulty`: "进阶", `importance`: "熟悉", `description`: "将路网矢量数据生成矢量切片；发布地图服务；Web前端加载切片，实现大规模路网高效浏览。"};

MERGE (node:KnowledgePoint {kp_id: "M7-033"})
SET node = {`name`: "移动端GIS路网数据适配优化", `kp_id`: "M7-033", `sort_order`: 33, `difficulty`: "进阶", `importance`: "熟悉", `description`: "对路网做轻量化裁剪、几何简化；降低数据体积；配置缓存策略，适配移动端有限算力与网络带宽。"};

MERGE (node:KnowledgePoint {kp_id: "M7-034"})
SET node = {`name`: "多源路网数据在GIS平台的融合方法", `kp_id`: "M7-034", `sort_order`: 34, `difficulty`: "进阶", `importance`: "掌握", `description`: "统一坐标系；执行空间匹配；实体对齐；冲突检测；合并来自OSM、官方测绘、互联网地图的路网数据。"};

MERGE (node:KnowledgePoint {kp_id: "M7-035"})
SET node = {`name`: "三维GIS平台路网基础加载配置", `kp_id`: "M7-035", `sort_order`: 35, `difficulty`: "进阶", `importance`: "熟悉", `description`: "导入路网数据；匹配高程信息；对高架、隧道设置高度偏移，构建多层立体路网三维场景。"};

MERGE (node:KnowledgePoint {kp_id: "M7-036"})
SET node = {`name`: "GIS平台路网分析模板自定义搭建", `kp_id`: "M7-036", `sort_order`: 36, `difficulty`: "进阶", `importance`: "掌握", `description`: "把常用拓扑检查、路径分析、动态分段流程保存为模型/模板；重复用于多批次路网处理，减少重复操作。"};

MERGE (node:KnowledgePoint {kp_id: "M8-001"})
SET node = {`name`: "知识图谱基本概念：本体、实体、关系、属性", `kp_id`: "M8-001", `sort_order`: 1, `difficulty`: "入门", `importance`: "核心", `description`: "本体（Schema模式层）定义类别与约束规则；实体代表现实对象，例如路段、交叉口；关系表达实体之间联系；属性描述实体自身特征。基础表达单元为三元组(主语，关系，宾语)。"};

MERGE (node:KnowledgePoint {kp_id: "M8-002"})
SET node = {`name`: "交通路网知识图谱的定位与价值", `kp_id`: "M8-002", `sort_order`: 2, `difficulty`: "基础", `importance`: "核心", `description`: "将GIS路网几何拓扑、业务语义转化为图结构；融合道路、交通设施、交通事件、管理实体；支持语义查询、连通推理、多源路网知识融合，弥补传统GIS关系模型语义表达不足的短板。"};

MERGE (node:KnowledgePoint {kp_id: "M8-003"})
SET node = {`name`: "交通本体（Ontology）设计方法", `kp_id`: "M8-003", `sort_order`: 3, `difficulty`: "进阶", `importance`: "核心", `description`: "梳理交通领域业务概念；划分实体大类、子类；定义允许的关系类型、属性字段、取值约束；严格区分模式层本体与实例数据层。"};

MERGE (node:KnowledgePoint {kp_id: "M8-004"})
SET node = {`name`: "道路实体类型设计：道路、路段、车道、交叉口", `kp_id`: "M8-004", `sort_order`: 4, `difficulty`: "进阶", `importance`: "掌握", `description`: "实体分层：逻辑道路、路段（节点之间的边）、车道（车道级细分实体）、交叉口（路网节点实体）；设置父子包含关系。"};

MERGE (node:KnowledgePoint {kp_id: "M8-005"})
SET node = {`name`: "交通设施实体设计：标志、信号灯、护栏、路灯", `kp_id`: "M8-005", `sort_order`: 5, `difficulty`: "进阶", `importance`: "掌握", `description`: "道路附属设施作为独立实体；记录设施类型、空间位置、所属路段；建立“安装于路段”语义关系。"};

MERGE (node:KnowledgePoint {kp_id: "M8-006"})
SET node = {`name`: "交通事件实体设计：事故、拥堵、施工、管制", `kp_id`: "M8-006", `sort_order`: 6, `difficulty`: "进阶", `importance`: "掌握", `description`: "事件作为独立实体；包含事件类型、发生时间、持续时间；建立“发生于某路段”关系，区分瞬时事件与持续事件。"};

MERGE (node:KnowledgePoint {kp_id: "M8-007"})
SET node = {`name`: "管理实体设计：行政区、交通小区、管理部门", `kp_id`: "M8-007", `sort_order`: 7, `difficulty`: "进阶", `importance`: "掌握", `description`: "行政区、交通小区属于空间管理实体；交通局、交管支队作为管理部门实体；建立“管辖、包含”关系连接路网实体。"};

MERGE (node:KnowledgePoint {kp_id: "M8-008"})
SET node = {`name`: "拓扑关系类型设计：连通、相邻、上下游、相交", `kp_id`: "M8-008", `sort_order`: 8, `difficulty`: "进阶", `importance`: "掌握", `description`: "拓扑关系刻画路网空间连接；连通代表节点直接相连；上下游表达路段通行顺序；相交代表几何交汇；注意区分几何相交和拓扑连通。"};

MERGE (node:KnowledgePoint {kp_id: "M8-009"})
SET node = {`name`: "语义关系类型设计：属于、包含、导致、影响", `kp_id`: "M8-009", `sort_order`: 9, `difficulty`: "进阶", `importance`: "掌握", `description`: "属于：路段隶属于某条逻辑道路；包含：交叉口包含多条接入路段；导致：事故导致拥堵；影响：施工影响路段通行能力。"};

MERGE (node:KnowledgePoint {kp_id: "M8-010"})
SET node = {`name`: "空间关系类型设计：距离、方位、覆盖、邻近", `kp_id`: "M8-010", `sort_order`: 10, `difficulty`: "进阶", `importance`: "掌握", `description`: "表达非拓扑的空间关联；例如设施位于道路左侧；事件覆盖某段道路；两个实体空间邻近。"};

MERGE (node:KnowledgePoint {kp_id: "M8-011"})
SET node = {`name`: "时间关系类型设计：发生于、持续、先后、同步", `kp_id`: "M8-011", `sort_order`: 11, `difficulty`: "进阶", `importance`: "掌握", `description`: "面向动态交通事件；事件发生于某个时刻；事件持续一段时间；定义两个事件发生先后顺序；记录多事件同步发生关系。"};

MERGE (node:KnowledgePoint {kp_id: "M8-012"})
SET node = {`name`: "知识图谱三元组与五元组建模方法", `kp_id`: "M8-012", `sort_order`: 12, `difficulty`: "进阶", `importance`: "掌握", `description`: "三元组(s,p,o)表达基础事实；五元组拓展增加时间、空间维度(s,p,o,time,location)，适配交通路网时空特性。"};

MERGE (node:KnowledgePoint {kp_id: "M8-013"})
SET node = {`name`: "模式层（Schema）与数据层（Instance）分层设计", `kp_id`: "M8-013", `sort_order`: 13, `difficulty`: "进阶", `importance`: "核心", `description`: "模式层定义实体类别、关系、属性约束；数据层存储一条条真实实例；需要先完成模式层本体设计，再导入实例数据，不允许随意新增实体类别。"};

MERGE (node:KnowledgePoint {kp_id: "M8-014"})
SET node = {`name`: "结构化路网数据的知识抽取与直接映射", `kp_id`: "M8-014", `sort_order`: 14, `difficulty`: "进阶", `importance`: "掌握", `description`: "GIS属性表属于结构化数据；数据表行映射为实体；数据表字段映射为实体属性；外键关联映射为实体之间的关系，可自动化批量生成大量三元组。"};

MERGE (node:KnowledgePoint {kp_id: "M8-015"})
SET node = {`name`: "半结构化数据（CSV/JSON/XML）知识抽取", `kp_id`: "M8-015", `sort_order`: 15, `difficulty`: "进阶", `importance`: "掌握", `description`: "配置映射规则；解析JSON、CSV当中的事件、设施数据；提取实体、属性、关系，完成半结构化数据知识抽取。"};

MERGE (node:KnowledgePoint {kp_id: "M8-016"})
SET node = {`name`: "非结构化文本的交通实体与关系抽取", `kp_id`: "M8-016", `sort_order`: 16, `difficulty`: "高阶", `importance`: "熟悉", `description`: "针对交管新闻、事故报告文本；使用NLP命名实体识别、关系抽取技术；从自然语言当中提取事故、管制、路段实体以及相互关系。"};

MERGE (node:KnowledgePoint {kp_id: "M8-017"})
SET node = {`name`: "路网实体对齐与消歧方法", `kp_id`: "M8-017", `sort_order`: 17, `difficulty`: "高阶", `importance`: "掌握", `description`: "多源数据当中同一条道路存在不同ID、不同名称；通过几何空间匹配、名称相似度、属性特征，识别等价实体，完成实体合并消歧。"};

MERGE (node:KnowledgePoint {kp_id: "M8-018"})
SET node = {`name`: "多源路网知识融合与冲突检测", `kp_id`: "M8-018", `sort_order`: 18, `difficulty`: "高阶", `importance`: "掌握", `description`: "融合测绘、OSM、互联网地图来源的知识；对同一实体的冲突属性（限速、通行方向）开展冲突检测，依据数据源可信度完成取舍。"};

MERGE (node:KnowledgePoint {kp_id: "M8-019"})
SET node = {`name`: "基于规则的路网知识推理：连通性推理、路径推理", `kp_id`: "M8-019", `sort_order`: 19, `difficulty`: "高阶", `importance`: "掌握", `description`: "编写业务规则：若A节点与B节点连通，B与C连通，则A、C存在间接连通；依靠规则推理补全间接可达关系，推导路径可行性。"};

MERGE (node:KnowledgePoint {kp_id: "M8-020"})
SET node = {`name`: "基于嵌入表示的知识推理：TransE/RotatE", `kp_id`: "M8-020", `sort_order`: 20, `difficulty`: "高阶", `importance`: "了解", `description`: "知识表示学习方法，将实体、关系映射到向量空间；用于补全缺失的交通关系，预测设施、事件之间潜在关联。"};

MERGE (node:KnowledgePoint {kp_id: "M8-021"})
SET node = {`name`: "Neo4j图数据库路网数据存储设计", `kp_id`: "M8-021", `sort_order`: 21, `difficulty`: "进阶", `importance`: "掌握", `description`: "节点：路段、交叉口、事件、设施；关系存储连通、发生于、包含；索引建立在ID、名称字段；大尺度路网做好存储分区。"};

MERGE (node:KnowledgePoint {kp_id: "M8-022"})
SET node = {`name`: "Neo4j路网节点与关系建模最佳实践", `kp_id`: "M8-022", `sort_order`: 22, `difficulty`: "进阶", `importance`: "掌握", `description`: "路段和交叉口分开作为两类节点；连通关系建立在交叉口‑路段之间；不要把完整几何存入节点属性，复杂几何外置到PostGIS数据库。"};

MERGE (node:KnowledgePoint {kp_id: "M8-023"})
SET node = {`name`: "Cypher查询语言：路网连通性查询", `kp_id`: "M8-023", `sort_order`: 23, `difficulty`: "进阶", `importance`: "掌握", `description`: "编写Cypher语句，查询某个交叉口直接相连的所有路段；查询两个实体之间是否存在连通关系。"};

MERGE (node:KnowledgePoint {kp_id: "M8-024"})
SET node = {`name`: "Cypher查询语言：最短路径与可达性查询", `kp_id`: "M8-024", `sort_order`: 24, `difficulty`: "进阶", `importance`: "掌握", `description`: "调用Cypher最短路径函数，在图数据库中查询两节点之间路径；支持筛选带约束（排除施工封路路段）的可达路径。"};

MERGE (node:KnowledgePoint {kp_id: "M8-025"})
SET node = {`name`: "大规模路网图数据库性能优化", `kp_id`: "M8-025", `sort_order`: 25, `difficulty`: "高阶", `importance`: "掌握", `description`: "创建节点、关系索引；限制返回结果集；静态、动态数据做分离；避免无限制深度遍历，防止查询超时卡顿。"};

MERGE (node:KnowledgePoint {kp_id: "M8-026"})
SET node = {`name`: "路网知识图谱可视化工具与方法", `kp_id`: "M8-026", `sort_order`: 26, `difficulty`: "进阶", `importance`: "熟悉", `description`: "使用Neo4j Browser、Gephi等工具；展示路网节点关系图；支持筛选道路、事件实体，实现图谱交互可视化。"};

MERGE (node:KnowledgePoint {kp_id: "M8-027"})
SET node = {`name`: "交通知识图谱标准：T/CITSA 68‑2025解读", `kp_id`: "M8-027", `sort_order`: 27, `difficulty`: "进阶", `importance`: "了解", `description`: "国内交通知识图谱团体标准；规定交通本体、数据格式、实体关系规范，作为路网知识图谱建设参考依据。"};

MERGE (node:KnowledgePoint {kp_id: "M8-028"})
SET node = {`name`: "高精地图知识图谱：GDF/OpenDRIVE本体映射", `kp_id`: "M8-028", `sort_order`: 28, `difficulty`: "高阶", `importance`: "熟悉", `description`: "将高精地图GDF、OpenDRIVE当中车道、标识实体映射到交通知识图谱本体；实现高精地图语义向图模型转换。"};

MERGE (node:KnowledgePoint {kp_id: "M8-029"})
SET node = {`name`: "动态知识图谱：路网状态实时更新机制", `kp_id`: "M8-029", `sort_order`: 29, `difficulty`: "高阶", `importance`: "掌握", `description`: "静态实体（道路）很少改动；动态实体（拥堵、事故）支持新增、删除、属性更新；通过时间戳标记事实有效时间，实现动态图谱。"};

MERGE (node:KnowledgePoint {kp_id: "M8-030"})
SET node = {`name`: "交通大模型与知识图谱的融合应用", `kp_id`: "M8-030", `sort_order`: 30, `difficulty`: "高阶", `importance`: "熟悉", `description`: "知识图谱提供可信结构化交通知识；大模型负责自然语言问答、文本理解；图谱约束大模型输出，减少幻觉，用于交通智能问答、辅助决策。"};

MERGE (node:KnowledgePoint {kp_id: "M9-001"})
SET node = {`name`: "城市总体规划中路网布局合理性评估", `subcategory`: "应用场景", `kp_id`: "M9-001", `sort_order`: 1, `difficulty`: "进阶", `importance`: "掌握", `description`: "利用GIS路网指标、可达性分析；评估规划路网密度、连通性是否匹配城市总体发展需求。"};

MERGE (node:KnowledgePoint {kp_id: "M9-002"})
SET node = {`name`: "新区开发路网方案GIS比选分析", `subcategory`: "应用场景", `kp_id`: "M9-002", `sort_order`: 2, `difficulty`: "进阶", `importance`: "掌握", `description`: "多套新区路网规划方案输入GIS；计算路网连通度、可达性、出行代价，量化对比不同方案优劣。"};

MERGE (node:KnowledgePoint {kp_id: "M9-003"})
SET node = {`name`: "旧城改造路网优化空间分析", `subcategory`: "应用场景", `kp_id`: "M9-003", `sort_order`: 3, `difficulty`: "进阶", `importance`: "掌握", `description`: "针对老城区路网狭窄、连通差现状；GIS分析路网瓶颈、断头路；为旧城道路改造提供空间依据。"};

MERGE (node:KnowledgePoint {kp_id: "M9-004"})
SET node = {`name`: "国土空间规划中路网与用地耦合分析", `subcategory`: "应用场景", `kp_id`: "M9-004", `sort_order`: 4, `difficulty`: "进阶", `importance`: "掌握", `description`: "将路网图层与城镇用地、居住产业用地叠加；分析交通供给与土地开发匹配程度。"};

MERGE (node:KnowledgePoint {kp_id: "M9-005"})
SET node = {`name`: "公交线网与城市路网匹配优化", `subcategory`: "应用场景", `kp_id`: "M9-005", `sort_order`: 5, `difficulty`: "进阶", `importance`: "掌握", `description`: "基于路网可达性；评估公交站点覆盖、线路走向；识别公交服务薄弱片区，优化公交线网布局。"};

MERGE (node:KnowledgePoint {kp_id: "M9-006"})
SET node = {`name`: "慢行系统（步行/骑行）路网评估", `subcategory`: "应用场景", `kp_id`: "M9-006", `sort_order`: 6, `difficulty`: "进阶", `importance`: "掌握", `description`: "提取步行、骑行路网；计算慢行路网密度、连通性、慢行可达范围；评估非机动车出行环境短板。"};

MERGE (node:KnowledgePoint {kp_id: "M9-007"})
SET node = {`name`: "消防救援最优路径规划GIS应用", `subcategory`: "应用场景", `kp_id`: "M9-007", `sort_order`: 7, `difficulty`: "进阶", `importance`: "掌握", `description`: "以路网为基础，设置消防救援阻抗；计算消防站到达各地块最优通行路线，评估消防响应可达范围。"};

MERGE (node:KnowledgePoint {kp_id: "M9-008"})
SET node = {`name`: "应急避难场所路网覆盖范围测算", `subcategory`: "应用场景", `kp_id`: "M9-008", `sort_order`: 8, `difficulty`: "进阶", `importance`: "掌握", `description`: "利用网络服务区分析；测算避难场所沿路网能够服务覆盖的居民区，识别避难服务盲区。"};

MERGE (node:KnowledgePoint {kp_id: "M9-009"})
SET node = {`name`: "灾害场景下路网损毁模拟与连通分析", `subcategory`: "应用场景", `kp_id`: "M9-009", `sort_order`: 9, `difficulty`: "高阶", `importance`: "掌握", `description`: "模拟洪水、地震造成路段损毁；删除损毁路段，重新计算全网连通性；分析受灾区域通行隔绝情况。"};

MERGE (node:KnowledgePoint {kp_id: "M9-010"})
SET node = {`name`: "物流配送网点路网选址分析", `subcategory`: "应用场景", `kp_id`: "M9-010", `sort_order`: 10, `difficulty`: "进阶", `importance`: "掌握", `description`: "结合路网、订单分布；使用位置分配模型，筛选物流网点最优位置，保障配送可达效率。"};

MERGE (node:KnowledgePoint {kp_id: "M9-011"})
SET node = {`name`: "多车辆配送VRP路网路径优化", `subcategory`: "应用场景", `kp_id`: "M9-011", `sort_order`: 11, `difficulty`: "高阶", `importance`: "掌握", `description`: "基于路网距离时间阻抗；求解多车辆配送路径规划，最小化总行驶里程或配送时间。"};

MERGE (node:KnowledgePoint {kp_id: "M9-012"})
SET node = {`name`: "智慧城市路网拥堵时空监测分析", `subcategory`: "应用场景", `kp_id`: "M9-012", `sort_order`: 12, `difficulty`: "进阶", `importance`: "掌握", `description`: "接入动态路网时序数据；监测各路段拥堵发生时段、持续时长；输出城市拥堵空间分布报告。"};

MERGE (node:KnowledgePoint {kp_id: "M9-013"})
SET node = {`name`: "路网瓶颈路段识别与优化分析", `subcategory`: "应用场景", `kp_id`: "M9-013", `sort_order`: 13, `difficulty`: "进阶", `importance`: "掌握", `description`: "利用介数中心性、饱和度指标识别路网瓶颈交叉口、瓶颈路段；支撑道路拓宽、立交改造决策。"};

MERGE (node:KnowledgePoint {kp_id: "M9-014"})
SET node = {`name`: "学区、医疗配套路网可达性公平性分析", `subcategory`: "应用场景", `kp_id`: "M9-014", `sort_order`: 14, `difficulty`: "进阶", `importance`: "掌握", `description`: "计算居民点到达学校、医院路网通行时间；评估公共服务可达性在不同片区是否均衡，识别服务不公区域。"};

MERGE (node:KnowledgePoint {kp_id: "M9-015"})
SET node = {`name`: "新能源充电桩路网可达性布局分析", `subcategory`: "应用场景", `kp_id`: "M9-015", `sort_order`: 15, `difficulty`: "进阶", `importance`: "掌握", `description`: "使用网络服务区分析；评估现有充电桩路网覆盖；筛选适合新增充电桩的点位。"};

MERGE (node:KnowledgePoint {kp_id: "M9-016"})
SET node = {`name`: "自动驾驶普通路网适配评估应用", `subcategory`: "应用场景", `kp_id`: "M9-016", `sort_order`: 16, `difficulty`: "高阶", `importance`: "熟悉", `description`: "分析现有路网车道、标志、交叉口条件；评估普通道路是否满足自动驾驶运行基础条件。"};

MERGE (node:KnowledgePoint {kp_id: "M9-017"})
SET node = {`name`: "城际路网连通性与区域协同分析", `subcategory`: "应用场景", `kp_id`: "M9-017", `sort_order`: 17, `difficulty`: "进阶", `importance`: "掌握", `description`: "计算城市之间公路、轨道通行代价；评估城际通道连通短板，支撑区域协同发展规划。"};

MERGE (node:KnowledgePoint {kp_id: "M9-018"})
SET node = {`name`: "乡村路网通达性短板识别分析", `subcategory`: "应用场景", `kp_id`: "M9-018", `sort_order`: 18, `difficulty`: "进阶", `importance`: "掌握", `description`: "计算乡村居民点对外路网可达时间；识别断头路、通达性差村庄，服务农村公路建设评估。"};

MERGE (node:KnowledgePoint {kp_id: "M9-019"})
SET node = {`name`: "大型活动路网交通疏导规划分析", `subcategory`: "应用场景", `kp_id`: "M9-019", `sort_order`: 19, `difficulty`: "高阶", `importance`: "掌握", `description`: "大型赛事会展场景；利用路网仿真、可达性分析；评估周边路网承载能力，制定疏导管制方案。"};

MERGE (node:KnowledgePoint {kp_id: "M9-020"})
SET node = {`name`: "产业园区路网交通适配性评估", `subcategory`: "应用场景", `kp_id`: "M9-020", `sort_order`: 20, `difficulty`: "进阶", `importance`: "掌握", `description`: "统计产业园货运、通勤出行需求；分析园区内外路网通行能力，识别交通供需矛盾。"};

MERGE (node:KnowledgePoint {kp_id: "M9-021"})
SET node = {`name`: "景区路网通行承载力与疏导分析", `subcategory`: "应用场景", `kp_id`: "M9-021", `sort_order`: 21, `difficulty`: "进阶", `importance`: "掌握", `description`: "测算景区路网最大承载客流量；模拟高峰客流下拥堵点位，制定游览疏导方案。"};

MERGE (node:KnowledgePoint {kp_id: "M9-022"})
SET node = {`name`: "路网施工交通导改空间模拟分析", `subcategory`: "应用场景", `kp_id`: "M9-022", `sort_order`: 22, `difficulty`: "进阶", `importance`: "掌握", `description`: "模拟道路施工封闭；路网修改对应路段通行约束；推演绕行路线，评估施工带来周边路网影响。"};

MERGE (node:KnowledgePoint {kp_id: "M9-023"})
SET node = {`name`: "城市停车设施路网可达性分析", `subcategory`: "应用场景", `kp_id`: "M9-023", `sort_order`: 23, `difficulty`: "进阶", `importance`: "掌握", `description`: "计算城市各区域到达停车场路网通行代价；识别停车设施服务盲区，指导停车规划。"};

MERGE (node:KnowledgePoint {kp_id: "M9-024"})
SET node = {`name`: "交通公平性路网可达性评价模型", `subcategory`: "应用场景", `kp_id`: "M9-024", `sort_order`: 24, `difficulty`: "进阶", `importance`: "掌握", `description`: "综合不同社会群体出行可达条件；量化不同片区居民获取交通服务的公平程度。"};

MERGE (node:KnowledgePoint {kp_id: "M9-025"})
SET node = {`name`: "低碳路网通行效率分析模型", `subcategory`: "应用场景", `kp_id`: "M9-025", `sort_order`: 25, `difficulty`: "进阶", `importance`: "熟悉", `description`: "结合路网车速、行驶里程估算碳排放；评估路网运行的低碳水平，用于绿色交通评估。"};

MERGE (node:KnowledgePoint {kp_id: "M9-026"})
SET node = {`name`: "路网交叉口节点错位问题与修复", `subcategory`: "问题优化", `kp_id`: "M9-026", `sort_order`: 26, `difficulty`: "基础", `importance`: "掌握", `description`: "交叉口多条道路端点空间没有捕捉到同一点；会破坏拓扑连通；通过节点捕捉、拓扑编辑，把相交道路端点对齐至同一个节点。"};

MERGE (node:KnowledgePoint {kp_id: "M9-027"})
SET node = {`name`: "路网伪节点过多导致的分析误差", `subcategory`: "问题优化", `kp_id`: "M9-027", `sort_order`: 27, `difficulty`: "基础", `importance`: "掌握", `description`: "同一条连续道路中间产生多余节点，道路被错误切分成大量短边；会干扰路径分析、统计指标；需要合并同属性相邻线段消除伪节点。"};

MERGE (node:KnowledgePoint {kp_id: "M9-028"})
SET node = {`name`: "单向路网方向标注错误问题与修正", `subcategory`: "问题优化", `kp_id`: "M9-028", `sort_order`: 28, `difficulty`: "进阶", `importance`: "掌握", `description`: "路段通行方向属性填反，导致路径规划出现逆行路线；核查原始影像、交通资料修正方向字段；拓扑检查批量筛查单向错误。"};

MERGE (node:KnowledgePoint {kp_id: "M9-029"})
SET node = {`name`: "多层路网上下层拓扑混淆问题", `subcategory`: "问题优化", `kp_id`: "M9-029", `sort_order`: 29, `difficulty`: "进阶", `importance`: "核心", `description`: "高架、地面、隧道几何相交，错误建立拓扑连通，现实中车辆不能穿越；需要分层标记路网，禁止不同高程路网建立连通关系。"};

MERGE (node:KnowledgePoint {kp_id: "M9-030"})
SET node = {`name`: "路网坐标偏移带来的空间匹配误差", `subcategory`: "问题优化", `kp_id`: "M9-030", `sort_order`: 30, `difficulty`: "进阶", `importance`: "掌握", `description`: "路网图层坐标存在偏移，与POI、事件点位无法正确匹配；执行坐标纠偏、配准，统一空间参考基准。"};

MERGE (node:KnowledgePoint {kp_id: "M9-031"})
SET node = {`name`: "路网限速数据不准带来的时间阻抗误差", `subcategory`: "问题优化", `kp_id`: "M9-031", `sort_order`: 31, `difficulty`: "进阶", `importance`: "掌握", `description`: "限速属性与现实不符，造成时间阻抗计算偏差；结合浮动车实测车速、外业调研校正限速字段。"};

MERGE (node:KnowledgePoint {kp_id: "M9-032"})
SET node = {`name`: "大规模路网路径查询卡顿问题优化", `subcategory`: "问题优化", `kp_id`: "M9-032", `sort_order`: 32, `difficulty`: "高阶", `importance`: "掌握", `description`: "千万级路网直接遍历计算耗时巨大；采用路网分层分块、空间索引、剪枝算法，优化查询效率。"};

MERGE (node:KnowledgePoint {kp_id: "M9-033"})
SET node = {`name`: "路网空间索引搭建与计算提速", `subcategory`: "问题优化", `kp_id`: "M9-033", `sort_order`: 33, `difficulty`: "进阶", `importance`: "核心", `description`: "对路网几何字段构建GIST空间索引；加速空间连接、相交查询、缓冲区运算，显著提升批量分析速度。"};

MERGE (node:KnowledgePoint {kp_id: "M9-034"})
SET node = {`name`: "众源路网数据的噪声与冗余处理", `subcategory`: "问题优化", `kp_id`: "M9-034", `sort_order`: 34, `difficulty`: "进阶", `importance`: "掌握", `description`: "OSM等众源路网存在重复线段、错误连通、多余碎边；通过去重、合并、拓扑清洗剔除噪声冗余数据。"};

MERGE (node:KnowledgePoint {kp_id: "M9-035"})
SET node = {`name`: "跨坐标系路网融合的拓扑错乱问题", `subcategory`: "问题优化", `kp_id`: "M9-035", `sort_order`: 35, `difficulty`: "进阶", `importance`: "掌握", `description`: "多份路网原始坐标系不统一，直接叠加产生错位；先全部转换为同一坐标系，再执行路网融合与拓扑修复。"};

MERGE (node:KnowledgePoint {kp_id: "M9-036"})
SET node = {`name`: "路网阻抗权重设置不合理的分析偏差", `subcategory`: "问题优化", `kp_id`: "M9-036", `sort_order`: 36, `difficulty`: "进阶", `importance`: "掌握", `description`: "距离、时间、费用阻抗权重配比不合理，导致路径结果不符合业务预期；结合真实出行样本标定阻抗权重参数。"};

MERGE (node:KnowledgePoint {kp_id: "M9-037"})
SET node = {`name`: "多源路网数据融合纠错优化方案", `subcategory`: "问题优化", `kp_id`: "M9-037", `sort_order`: 37, `difficulty`: "进阶", `importance`: "核心", `description`: "统一坐标系→实体空间匹配→冲突检测→依据数据源可信度修正错误属性；输出一份融合后高质量路网。"};

MERGE (node:KnowledgePoint {kp_id: "M9-038"})
SET node = {`name`: "路网异常节点智能识别优化算法", `subcategory`: "问题优化", `kp_id`: "M9-038", `sort_order`: 38, `difficulty`: "进阶", `importance`: "掌握", `description`: "编写算法自动筛查悬挂节点、孤立节点、度数异常节点；批量定位拓扑错误点位，减少人工检查工作量。"};

MERGE (node:KnowledgePoint {kp_id: "M9-039"})
SET node = {`name`: "路网历史数据增量更新迭代机制", `subcategory`: "问题优化", `kp_id`: "M9-039", `sort_order`: 39, `difficulty`: "进阶", `importance`: "掌握", `description`: "不全部替换路网；识别新增道路、变更道路；只对发生变化要素做增量更新；保留历史版本快照。"};

MERGE (node:KnowledgePoint {kp_id: "M9-040"})
SET node = {`name`: "路网分析结果误差校正通用方法", `subcategory`: "问题优化", `kp_id`: "M9-040", `sort_order`: 40, `difficulty`: "进阶", `importance`: "掌握", `description`: "对比分析结果和真实观测数据（浮动车、卡口流量）；溯源误差来源（拓扑错误/属性错误/算法参数）；修复原始数据再重新运算。"};

MERGE (node:KnowledgePoint {kp_id: "M9-041"})
SET node = {`name`: "三维GIS交通路网与BIM+GIS融合建模", `subcategory`: "前沿技术", `kp_id`: "M9-041", `sort_order`: 41, `difficulty`: "高阶", `importance`: "熟悉", `description`: "道路BIM构件模型与GIS路网数据融合；把道路构件BIM信息接入GIS，实现路网几何、工程属性一体化三维建模。"};

MERGE (node:KnowledgePoint {kp_id: "M9-042"})
SET node = {`name`: "城市立体交通路网三维拓扑构建", `subcategory`: "前沿技术", `kp_id`: "M9-042", `sort_order`: 42, `difficulty`: "高阶", `importance`: "掌握", `description`: "为高架、隧道、地面道路增加高程维度；构建三维拓扑，区分空间相交和真实连通关系，解决多层路网建模难题。"};

MERGE (node:KnowledgePoint {kp_id: "M9-043"})
SET node = {`name`: "自动驾驶高精地图（HD Map）核心特征", `subcategory`: "前沿技术", `kp_id`: "M9-043", `sort_order`: 43, `difficulty`: "高阶", `importance`: "核心", `description`: "车道级粒度；包含车道线、交通标志、停止线、交叉口车道转向规则；几何精度达到厘米级，面向自动驾驶感知定位。"};

MERGE (node:KnowledgePoint {kp_id: "M9-044"})
SET node = {`name`: "高精路网车道级建模与交通标识建模", `subcategory`: "前沿技术", `kp_id`: "M9-044", `sort_order`: 44, `difficulty`: "高阶", `importance`: "掌握", `description`: "将路网拆解至单条车道实体；建模车道连接关系；完整存储交通标志、地面标线语义信息。"};

MERGE (node:KnowledgePoint {kp_id: "M9-045"})
SET node = {`name`: "AI遥感影像自动提取路网技术", `subcategory`: "前沿技术", `kp_id`: "M9-045", `sort_order`: 45, `difficulty`: "高阶", `importance`: "熟悉", `description`: "深度学习语义分割模型，从卫星、航拍影像自动识别提取道路几何；用于快速更新路网底图，补充偏远地区路网数据。"};

MERGE (node:KnowledgePoint {kp_id: "M9-046"})
SET node = {`name`: "机器学习预测路网交通流量变化", `subcategory`: "前沿技术", `kp_id`: "M9-046", `sort_order`: 46, `difficulty`: "高阶", `importance`: "熟悉", `description`: "使用时序机器学习模型，输入历史流量、天气、节假日特征；预测未来短时间内各路段车流量、拥堵等级。"};

MERGE (node:KnowledgePoint {kp_id: "M9-047"})
SET node = {`name`: "轨迹数据挖掘路网隐藏通行规则", `subcategory`: "前沿技术", `kp_id`: "M9-047", `sort_order`: 47, `difficulty`: "高阶", `importance`: "熟悉", `description`: "利用海量车辆GPS轨迹；挖掘现实中隐性转向限制、潮汐车道规则，补充路网属性表当中缺失通行约束。"};

MERGE (node:KnowledgePoint {kp_id: "M9-048"})
SET node = {`name`: "时空大数据路网演化规律挖掘技术", `subcategory`: "前沿技术", `kp_id`: "M9-048", `sort_order`: 48, `difficulty`: "高阶", `importance`: "熟悉", `description`: "多年份路网时空数据；挖掘城市路网扩张、道路新建拆除演化模式，用于城市历史交通研究。"};

MERGE (node:KnowledgePoint {kp_id: "M9-049"})
SET node = {`name`: "数字孪生城市路网实时映射与仿真", `subcategory`: "前沿技术", `kp_id`: "M9-049", `sort_order`: 49, `difficulty`: "高阶", `importance`: "核心", `description`: "将现实世界实时交通状态映射到数字孪生路网；支持仿真推演，模拟管制、施工带来路网状态变化，实现虚实联动。"};

MERGE (node:KnowledgePoint {kp_id: "M9-050"})
SET node = {`name`: "车路协同场景下GIS路网应用", `subcategory`: "前沿技术", `kp_id`: "M9-050", `sort_order`: 50, `difficulty`: "高阶", `importance`: "熟悉", `description`: "路网提供车道、交叉口、标志语义数据；支撑车路协同V2X业务，向路侧设备、车载终端输出道路静态语义信息。"};

MERGE (node:KnowledgePoint {kp_id: "M9-051"})
SET node = {`name`: "全域感知路网数据融合技术", `subcategory`: "前沿技术", `kp_id`: "M9-051", `sort_order`: 51, `difficulty`: "高阶", `importance`: "掌握", `description`: "融合摄像头、雷达、浮动车、卡口、物联网感知设备数据；生成全域感知动态路网，实现更精准实时状态更新。"};

MERGE (node:KnowledgePoint {kp_id: "M9-052"})
SET node = {`name`: "云端路网大数据分析架构", `subcategory`: "前沿技术", `kp_id`: "M9-052", `sort_order`: 52, `difficulty`: "高阶", `importance`: "了解", `description`: "基于云存储、分布式计算；对大规模城市级、省级路网做分布式并行分析，解决本地计算机算力不足问题。"};

MERGE (node:KnowledgePoint {kp_id: "M9-053"})
SET node = {`name`: "应急智慧路网智能调度技术", `subcategory`: "前沿技术", `kp_id`: "M9-053", `sort_order`: 53, `difficulty`: "高阶", `importance`: "熟悉", `description`: "灾害、突发事件场景；结合路网损毁分析、路径推演；自动生成应急救援通道、物资运输路线，支撑应急调度决策。"};

MERGE (node:KnowledgePoint {kp_id: "M9-054"})
SET node = {`name`: "城市更新中路网动态迭代技术", `subcategory`: "前沿技术", `kp_id`: "M9-054", `sort_order`: 54, `difficulty`: "高阶", `importance`: "熟悉", `description`: "伴随城市更新项目，持续迭代路网几何、属性；实现路网随城市建设动态更新，保持路网数据时效性。"};

MERGE (node:KnowledgePoint {kp_id: "M9-055"})
SET node = {`name`: "智慧路网未来技术发展趋势", `subcategory`: "前沿技术", `kp_id`: "M9-055", `sort_order`: 55, `difficulty`: "高阶", `importance`: "了解", `description`: "向车道级、实时动态、数字孪生、知识图谱语义化方向发展；融合AI感知、车路协同，实现路网从静态底图转向可感知、可推演的智慧交通底座。"};
