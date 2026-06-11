const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, HeadingLevel, AlignmentType, LevelFormat,
  TableOfContents, BorderStyle, WidthType, ShadingType, PageBreak
} = require("docx");

// ---------- helpers ----------
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };
const headerShading = { fill: "D5E8F0", type: ShadingType.CLEAR };
const altShading = { fill: "F5F5F5", type: ShadingType.CLEAR };

function p(text, opts = {}) {
  return new Paragraph({ spacing: { after: 80 }, ...opts, children: [new TextRun({ text, size: 22, font: "Microsoft YaHei", ...opts.run })] });
}
function bold(text) { return new TextRun({ text, bold: true, size: 22, font: "Microsoft YaHei" }); }
function run(text, opts = {}) { return new TextRun({ text, size: 22, font: "Microsoft YaHei", ...opts }); }

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 }, children: [run(text, { size: 32, bold: true })] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 }, children: [run(text, { size: 28, bold: true })] });
}
function h3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 200, after: 120 }, children: [run(text, { size: 26, bold: true })] });
}

function makeTable(headers, rows) {
  const colW = Math.floor(9026 / headers.length);
  const cols = Array(headers.length).fill(colW);
  const headerRow = new TableRow({
    children: headers.map(h => new TableCell({ borders, shading: headerShading, width: { size: colW, type: WidthType.DXA }, margins: cellMargins, children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 20, font: "Microsoft YaHei" })] })] }))
  });
  const dataRows = rows.map((row, ri) => new TableRow({
    children: row.map(c => new TableCell({ borders, shading: ri % 2 ? altShading : undefined, width: { size: colW, type: WidthType.DXA }, margins: cellMargins, children: [new Paragraph({ children: [new TextRun({ text: String(c), size: 20, font: "Microsoft YaHei" })] })] }))
  }));
  return new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: cols, rows: [headerRow, ...dataRows] });
}

function code(line) {
  return new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: line, size: 18, font: "Consolas" })] });
}
function codeBlock(lines) {
  const table = new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [9026],
    rows: [new TableRow({ children: [new TableCell({
      borders, margins: { top: 80, bottom: 80, left: 120, right: 120 },
      shading: { fill: "F8F8F8", type: ShadingType.CLEAR },
      children: lines.map(l => code(l))
    })] })]
  });
  return [table];
}

function img(name, w_inch = 5.8) {
  const data = fs.readFileSync(`images/${name}`);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({ type: "png", data, transformation: { width: Math.round(w_inch * 1440), height: Math.round(w_inch * 1440 * 0.7) }, altText: { title: name, description: name, name } })]
  });
}

const imgDir = "C:/Users/LiangYaoHui/Desktop/课程设计";

function loadImg(name) {
  return fs.readFileSync(`${imgDir}/images/${name}`);
}

function imageP(name, caption, w = 5.8) {
  const data = loadImg(name);
  const imgW = Math.round(w * 1440);
  const imgH = Math.round(imgW * 0.75);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160, after: 40 }, children: [new ImageRun({ type: "png", data, transformation: { width: imgW, height: imgH }, altText: { title: name, description: caption, name } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: caption, italics: true, size: 20, color: "666666", font: "Microsoft YaHei" })] }),
  ];
}

// ========== BUILD DOCUMENT ==========
const children = [];

// ---- 封面 ----
children.push(
  new Paragraph({ spacing: { before: 3000 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [run("智能导医系统", { size: 52, bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [run("架构设计文档", { size: 40, bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [run("文档版本：V1.0    修订日期：2026-05-28", { size: 24, color: "888888" })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [run("产品名称：智能导医系统    撰写人：课程设计小组", { size: 24, color: "888888" })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---- 目录 ----
children.push(
  h1("目录"),
  new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---- 第1章 项目概述 ----
children.push(
  h1("1. 项目概述"),
  h2("1.1 项目背景"),
  p("当前医院就诊流程繁琐，人工导诊人员工作压力大，患者常因不熟悉科室布局、不清楚症状对应科室，出现分诊错误、就诊延误等问题。据统计，85%的首诊患者不知该挂何科室，平均候诊时间达1.8小时。大型医院楼层多、科室分散，院内导航困难，信息不对称问题突出。"),
  p("在\"健康中国2030\"战略推进与老龄化加剧的背景下，智慧医疗市场规模预计在2025年达300亿元，年复合增长率35%。《互联网诊疗管理办法》等政策的出台，为智能导医类产品提供了广阔的发展空间。"),
  h2("1.2 产品定位"),
  p("面向医院门诊场景的 AI 智能导医原型系统，基于符号主义专家系统规则推理 + 深度学习技术混合架构，为患者提供语音问诊、症状智能识别、自动分诊、科室楼层导航一站式服务，替代/辅助人工导诊，简化就诊流程，提升医院门诊服务效率。"),
  h2("1.3 核心目标"),
  makeTable(["目标维度", "短期目标", "长期目标"], [
    ["功能范围", "支持18种常见症状、10个科室智能分诊", "扩展症状库至50+种，支持多轮对话式问诊"],
    ["分诊准确率", "≥ 90%", "≥ 95%"],
    ["导航准确率", "楼层引导路线100%准确", "支持AR实景导航"],
    ["交互方式", "语音输入、文字输入双模式", "增加人脸识别、多语言支持"],
    ["稳定性", "连续运行30分钟无崩溃", "对接医院HIS挂号系统，实现分诊-挂号一体化"],
  ]),
  h2("1.4 核心价值"),
  p("患者端价值：快速分诊（AI自动匹配科室，避免分诊错误）、精准导航（明确科室位置与就诊路线）、便捷操作（支持语音输入，降低中老年用户操作门槛）、减少等待（自助导诊无需排队）。"),
  p("医院端价值：降本增效（减轻人工导诊人员工作压力）、提升流转（优化门诊就诊流程）、服务升级（智能化服务提升医院整体形象与患者满意度）。"),
  p("教学价值：验证经典AI（专家系统）与现代深度学习技术在医疗场景的融合应用，通过完整产品开发流程，提升团队工程实践与协作能力。"),
  h2("1.5 适用场景"),
  ...["首次就医场景：患者首次到院，不了解医院科室设置",
    "多症状复杂场景：患者同时出现多种症状，无法判断优先就诊科室",
    "寻路导航场景：患者已知就诊科室，但找不到具体楼层与位置",
    "高峰繁忙场景：门诊高峰时段人工导诊排队，患者需快速自助导诊",
    "中老年就医场景：老年患者不擅长文字输入，需要语音交互"].map(t => p("· " + t)),
);

// ---- 第2章 需求分析 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("2. 需求分析"),
  h2("2.1 功能需求"),
  h3("2.1.1 核心功能清单"),
  makeTable(["功能模块", "功能描述", "优先级", "备注"], [
    ["语音问诊模块", "支持语音输入症状，自动转换为文字", "高", "调用语音识别API实现"],
    ["文字输入模块", "支持键盘文字输入症状描述", "高", "语音识别失败时的备用方案"],
    ["症状提取模块", "从输入文本中自动识别核心症状与伴随症状", "高", "基于规则匹配 + 文本分类"],
    ["智能分诊模块", "基于症状推理给出最优科室建议", "高", "专家系统规则库 + 正向推理机"],
    ["楼层引导模块", "生成从导诊台到目标科室的详细文字路线", "高", "基于科室楼层数据库"],
    ["多症状综合推理", "支持同时输入多种症状进行加权分诊", "高", "多规则加权计算"],
    ["模糊症状追问", "症状信息不全时主动提示补充", "中", "提升分诊准确率"],
    ["分诊历史记录", "查看近期分诊记录与就诊建议", "中", "便于复诊参考"],
    ["异常场景处理", "识别失败/无匹配症状时给出友好提示", "中", "引导至人工导诊"],
    ["科室信息查询", "查看各科室简介、出诊医生信息", "低", "扩展功能"],
  ]),
  h2("2.2 非功能需求"),
  h3("2.2.1 性能需求"),
  makeTable(["性能指标", "要求标准", "备注"], [
    ["单次分诊响应时间", "≤ 3秒", "从提交症状到显示分诊结果"],
    ["语音识别响应时间", "≤ 2秒", "从松开按钮到显示文字"],
    ["路线生成响应时间", "≤ 1秒", "点击查看路线到显示结果"],
    ["系统稳定性", "连续运行30分钟无崩溃", "满足课程设计演示要求"],
    ["并发支持", "支持单人连续操作无卡顿", "原型系统单用户使用"],
    ["内存占用", "≤ 500MB", "确保在普通PC上流畅运行"],
  ]),
  h3("2.2.2 兼容性需求"),
  makeTable(["兼容维度", "要求标准"], [
    ["操作系统", "Windows 10及以上版本"],
    ["运行环境", "Python 3.8+，JDK 1.8+"],
    ["屏幕分辨率", "1920×1080及以上，支持自适应缩放"],
    ["硬件要求", "普通PC即可，需配备麦克风"],
    ["网络要求", "语音识别需联网，基础分诊功能可离线运行"],
  ]),
  h3("2.2.3 安全性需求"),
  makeTable(["安全维度", "要求标准"], [
    ["用户隐私", "不存储患者姓名、身份证号等敏感隐私数据"],
    ["数据存储", "分诊历史记录仅本地缓存，不上传云端"],
    ["离线能力", "基础专家系统分诊可离线使用，不依赖网络"],
    ["数据备份", "知识库、规则库定期备份，防止数据丢失"],
    ["访问控制", "管理员配置功能需密码验证，防止误操作"],
  ]),
);

// ---- 第3章 系统总体架构 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("3. 系统总体架构"),
  h2("3.1 架构设计原则"),
  p("本项目采用\"专家系统 + 深度学习\"混合架构，兼顾经典AI方法与现代深度学习技术，既降低开发难度，又提升系统智能化水平。架构设计遵循以下原则："),
  ...["分层解耦：各层职责清晰，层间通过标准接口通信",
    "模块化设计：功能模块独立开发、独立测试、易于扩展",
    "混合推理：符号主义规则推理与深度学习模型协同工作",
    "离线优先：核心分诊功能不依赖网络，确保系统可用性"].map(t => p("· " + t)),
  h2("3.2 四层架构设计"),
  p("系统采用四层架构设计，从下到上依次为："),
  ...imageP("fig1_architecture.png", "图1：系统四层架构（交互展示层 → 业务逻辑层 → 算法推理层 → 数据层）", 5.8),
  h3("3.3 核心架构说明"),
  p("数据层：SQLite数据库存储科室信息、楼层布局、分诊历史记录；症状知识库包含18种核心症状及其属性定义；规则库为IF-THEN格式的医疗分诊规则集；科室楼层数据包含10个科室的位置信息与楼层分布。"),
  p("算法推理层：专家系统推理机基于正向推理机制实现规则匹配与加权计算；深度学习模型为症状文本分类模型，提升模糊症状识别准确率；症状提取引擎基于分词与模糊匹配；语音转文本引擎调用第三方语音识别API。"),
  p("业务逻辑层：分诊流程控制协调各模块完成\"输入→提取→推理→输出\"全流程；症状管理模块管理症状的生命周期与状态；历史记录模块实现分诊记录的存储、查询与展示；异常处理模块统一处理无匹配、识别失败等异常场景。"),
  p("交互展示层：GUI界面模块基于PyQt5的桌面应用程序；语音交互模块实现语音按钮交互与识别状态管理；路线展示模块实现文字路线生成与可视化展示。"),
  h2("3.4 数据流转图"),
  ...imageP("fig2_sequence.png", "图2：系统数据流转时序图（展示用户、界面与各模块间的交互顺序）", 5.8),
);

// ---- 第4章 功能模块设计 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("4. 功能模块设计"),
  h2("4.1 模块划分总览"),
  ...imageP("fig3_modules.png", "图3：系统功能模块划分（展示各模块的职责与关联关系）", 5.8),
  h2("4.2 模块详细设计"),
  h3("4.2.1 语音输入模块"),
  p("职责：提供语音与文字两种输入方式，将用户的症状描述转换为系统可处理的文本。核心组件：语音采集器（调用麦克风采集音频数据）、语音识别代理（封装第三方ASR API调用）、文字输入框（支持键盘输入的备用方案）、快捷症状按钮（发烧、咳嗽、头痛等常见症状一键输入）。输入：音频流/键盘文字，输出：结构化文本（症状描述）。"),
  h3("4.2.2 症状提取模块"),
  p("职责：从自然语言文本中识别并提取有效症状关键词。核心组件：中文分词器（jieba分词处理）、症状匹配器（与症状库进行精确/模糊匹配）、权重计算器（计算症状的置信度与优先级）、追问生成器（症状信息不足时生成补充问题）。输入：自然语言文本，输出：症状列表 [{症状名, 类型, 置信度}]。"),
  h3("4.2.3 智能分诊模块"),
  p("职责：基于提取的症状，通过专家系统推理得出最优科室建议。核心组件：规则加载器（加载IF-THEN规则库）、正向推理机（从症状出发匹配规则）、加权计算器（多规则冲突时的加权投票）、结果排序器（按置信度排序输出）。输入：症状列表，输出：分诊结果 [{科室, 置信度, 分诊依据, 备选科室}]。"),
  h3("4.2.4 楼层引导模块"),
  p("职责：根据分诊结果生成从导诊台到目标科室的文字导航路线。核心组件：科室定位器（查询科室楼层与位置）、路线生成器（基于楼层数据生成引导文本）、参照物提示器（提供标志性建筑辅助定位）。输入：目标科室ID，输出：文字导航路线 + 楼层位置信息。"),
  h3("4.2.5 历史记录模块"),
  p("职责：管理用户的分诊历史，支持查询与回顾。核心组件：记录存储器（将分诊结果持久化到SQLite）、记录查询器（按时间倒序查询历史记录）、详情展示器（展示单条记录的完整信息）。数据项：时间戳、输入症状、推荐科室、置信度、是否查看路线。"),
  h3("4.2.6 系统管理模块"),
  p("职责：提供知识库维护、规则管理、系统配置等管理功能。核心组件：知识库编辑器（增删改症状与科室数据）、规则管理器（编辑IF-THEN规则）、系统配置器（设置API密钥、阈值参数等）、数据备份器（知识库与规则库的导出/导入）。"),
);

// ---- 第5章 技术选型 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("5. 技术选型"),
  h2("5.1 技术选型总览"),
  makeTable(["技术领域", "选型方案", "版本要求", "选型理由"], [
    ["编程语言", "Python", "3.8+", "AI生态完善，专家系统与深度学习库丰富"],
    ["GUI框架", "PyQt5 / Tkinter", "5.15+", "跨平台、组件丰富、学习曲线适中"],
    ["数据库", "SQLite", "3.35+", "轻量级、零配置、内置于Python标准库"],
    ["语音识别", "百度语音API / 讯飞API", "-", "准确率高、中文支持好、有免费额度"],
    ["分词工具", "jieba", "0.42+", "中文分词首选，支持自定义词典"],
    ["深度学习", "scikit-learn / PyTorch", "1.0+", "适合文本分类任务，与专家系统互补"],
  ]),
  h2("5.2 前端/GUI技术"),
  p("PyQt5：优势是组件丰富（按钮、输入框、列表、对话框等完善），支持自定义样式，文档齐全；适用场景为桌面级GUI应用，需要复杂界面交互的场景；核心组件包括QMainWindow（主窗口）、QPushButton（按钮）、QTextEdit（文本输入）、QListWidget（列表展示）。"),
  p("备选Tkinter：优势是Python内置库，无需额外安装，轻量级；适用场景为简单界面、快速原型开发。决策：课程设计演示阶段使用PyQt5，确保界面美观度。"),
  h2("5.3 后端/算法技术"),
  p("专家系统引擎（自研）：知识表示基于产生式规则（IF-THEN），推理机制为正向推理（数据驱动），冲突消解采用加权投票机制、置信度优先，实现方式为Python字典存储规则、自定义推理机类。"),
  p("症状文本分类（深度学习辅助）：模型选择为朴素贝叶斯/SVM/浅层神经网络，特征提取采用TF-IDF + 词袋模型，训练数据基于18种症状的标注语料（可扩展），作用为辅助专家系统、提升模糊症状识别率。"),
  p("语音识别（第三方API）：候选方案为百度语音识别API、讯飞开放平台，调用方式为RESTful API，上传音频文件获取识别结果，容错设计为识别失败自动切换至文字输入。"),
  h2("5.4 数据库技术"),
  p("SQLite选型理由：零配置、单文件存储，便于课程设计交付与部署；内置于Python标准库（sqlite3模块），无需额外安装；支持标准SQL语法，满足本项目数据管理需求；性能足以支撑单用户原型系统。数据文件：guide_system.db（单文件，可随项目一起分发）。"),
  h2("5.5 AI技术栈"),
  makeTable(["AI技术", "具体实现", "作用"], [
    ["专家系统", "自研规则推理引擎", "核心分诊逻辑，可解释性强"],
    ["自然语言处理", "jieba分词 + 模糊匹配", "症状关键词提取"],
    ["机器学习", "scikit-learn文本分类", "辅助症状识别，提升准确率"],
    ["语音识别", "第三方ASR API", "语音输入转文字"],
  ]),
);

// ---- 第6章 数据库设计 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("6. 数据库设计"),
  h2("6.1 E-R图设计"),
  ...imageP("fig4_er.png", "图4：数据库E-R图（展示实体、属性及实体间的关联关系）", 5.8),
  h2("6.2 表结构设计"),
  h3("6.2.1 症状表（symptoms）"),
  makeTable(["字段名", "类型", "约束", "说明"], [
    ["symptom_id", "INTEGER", "PRIMARY KEY", "症状唯一标识"],
    ["symptom_name", "VARCHAR(50)", "NOT NULL", "症状名称"],
    ["category", "VARCHAR(30)", "NOT NULL", "症状分类（呼吸类/消化类等）"],
    ["synonyms", "VARCHAR(200)", "", "同义词，逗号分隔"],
    ["base_weight", "FLOAT", "DEFAULT 1.0", "症状基础权重"],
  ]),
  h3("6.2.2 科室表（departments）"),
  makeTable(["字段名", "类型", "约束", "说明"], [
    ["dept_id", "INTEGER", "PRIMARY KEY", "科室唯一标识"],
    ["dept_name", "VARCHAR(50)", "NOT NULL", "科室名称"],
    ["function_desc", "VARCHAR(200)", "", "核心职能描述"],
    ["floor", "INTEGER", "NOT NULL", "所在楼层"],
    ["location_desc", "VARCHAR(200)", "NOT NULL", "位置描述"],
  ]),
  h3("6.2.3 规则表（rules）"),
  makeTable(["字段名", "类型", "约束", "说明"], [
    ["rule_id", "INTEGER", "PRIMARY KEY", "规则唯一标识"],
    ["symptom_id", "INTEGER", "FOREIGN KEY", "关联症状"],
    ["dept_id", "INTEGER", "FOREIGN KEY", "关联科室"],
    ["rule_weight", "FLOAT", "DEFAULT 1.0", "规则权重"],
    ["conditions", "VARCHAR(500)", "", "规则条件描述"],
  ]),
  h3("6.2.4 分诊记录表（records）"),
  makeTable(["字段名", "类型", "约束", "说明"], [
    ["record_id", "INTEGER", "PRIMARY KEY AUTOINCREMENT", "记录唯一标识"],
    ["create_time", "DATETIME", "DEFAULT CURRENT_TIMESTAMP", "创建时间"],
    ["input_text", "VARCHAR(500)", "NOT NULL", "用户输入原文"],
    ["matched_symptoms", "VARCHAR(200)", "", "匹配到的症状列表"],
    ["recommended_dept", "INTEGER", "FOREIGN KEY", "推荐科室"],
    ["confidence", "FLOAT", "", "分诊置信度"],
    ["viewed_route", "BOOLEAN", "DEFAULT FALSE", "是否查看路线"],
  ]),
  h3("6.2.5 楼层表（floors）"),
  makeTable(["字段名", "类型", "约束", "说明"], [
    ["floor_id", "INTEGER", "PRIMARY KEY", "楼层唯一标识"],
    ["floor_number", "INTEGER", "NOT NULL", "楼层编号"],
    ["core_areas", "VARCHAR(200)", "", "核心区域/科室"],
    ["elevator_stairs", "VARCHAR(200)", "", "电梯/楼梯位置"],
    ["guide_text", "VARCHAR(500)", "", "引导说明文字"],
  ]),
);

// ---- 第7章 核心接口设计 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("7. 核心接口设计"),
  h2("7.1 接口设计规范"),
  p("接口风格：模块内部采用Python函数调用，模块间通过标准化数据格式（字典/JSON）交互。错误处理：统一返回格式 {\"success\": bool, \"data\": any, \"message\": str}。日志记录：关键接口调用记录输入参数与执行时间。"),
  h2("7.2 模块间核心接口"),
  h3("7.2.1 语音输入模块接口"),
  ...codeBlock([
    "# 语音识别接口",
    "def recognize_speech(audio_data: bytes) -> dict:",
    '    """将音频数据转换为文字"""',
    "    # 返回 {\"success\": True, \"data\": {\"text\": \"...\"}}",
    "",
    "# 文字输入接口",
    "def input_text(text: str) -> dict:",
    '    """接收用户文字输入"""',
    "    # 返回 {\"success\": True, \"data\": {\"text\": \"...\"}}",
  ]),
  h3("7.2.2 症状提取模块接口"),
  ...codeBlock([
    "def extract_symptoms(text: str) -> dict:",
    '    """从文本中提取症状关键词"""',
    "    # 返回 {",
    '    #   \"success\": True,',
    '    #   \"data\": {',
    '    #     \"symptoms\": [{\"name\": \"发烧\", \"type\": \"core\", \"confidence\": 1.0}],',
    '    #     \"need_clarify\": False',
    '    #   }',
    "    # }",
  ]),
  h3("7.2.3 智能分诊模块接口"),
  ...codeBlock([
    "def diagnose(symptoms: list) -> dict:",
    '    """基于症状列表进行智能分诊"""',
    "    # 返回 {",
    '    #   \"success\": True,',
    '    #   \"data\": {',
    '    #     \"primary\": {\"dept_id\": 1, \"dept_name\": \"呼吸内科\", \"confidence\": 0.95},',
    '    #     \"alternatives\": [...],',
    '    #     \"matched_rules\": [1, 2]',
    '    #   }',
    "    # }",
  ]),
  h3("7.2.4 楼层引导模块接口"),
  ...codeBlock([
    "def generate_route(dept_id: int) -> dict:",
    '    """生成到目标科室的导航路线"""',
    "    # 返回导航路线文字描述",
  ]),
  h2("7.3 外部API接口"),
  h3("7.3.1 语音识别API"),
  ...codeBlock([
    "# 百度语音识别API调用示例",
    "def call_baidu_asr(audio_data: bytes) -> str:",
    "    # POST https://vop.baidu.com/server_api",
    "    # Content-Type: audio/pcm;rate=16000",
    "    # 返回识别文本结果",
  ]),
);

// ---- 第8章 部署架构 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("8. 部署架构"),
  h2("8.1 运行环境要求"),
  makeTable(["环境项", "最低配置", "推荐配置"], [
    ["操作系统", "Windows 10", "Windows 11 / macOS / Linux"],
    ["CPU", "Intel i3 / AMD Ryzen 3", "Intel i5 / AMD Ryzen 5"],
    ["内存", "4GB", "8GB"],
    ["存储", "1GB可用空间", "2GB可用空间"],
    ["麦克风", "普通麦克风", "降噪麦克风"],
    ["网络", "可选（仅语音识别需联网）", "宽带网络"],
    ["屏幕分辨率", "1366×768", "1920×1080"],
  ]),
  h2("8.2 部署步骤"),
  p("1. 环境准备：安装Python 3.8+，创建虚拟环境 python -m venv venv"),
  p("2. 依赖安装：pip install -r requirements.txt（PyQt5、jieba、scikit-learn、requests等）"),
  p("3. 数据库初始化：python init_db.py"),
  p("4. 配置文件设置：编辑 config.ini，填入百度语音API密钥"),
  p("5. 启动系统：python main.py"),
  h2("8.3 文件目录结构"),
  ...codeBlock([
    "guide_system/",
    "├── main.py              # 程序入口",
    "├── config.ini           # 配置文件",
    "├── requirements.txt     # 依赖清单",
    "├── init_db.py           # 数据库初始化",
    "├── guide_system.db      # SQLite数据库",
    "├── core/                # 核心算法层",
    "│   ├── expert_system.py # 专家系统推理机",
    "│   ├── symptom_extractor.py",
    "│   ├── classifier.py    # 深度学习分类器",
    "│   └── speech_recognition.py",
    "├── gui/                 # 交互展示层",
    "│   ├── main_window.py",
    "│   ├── input_panel.py",
    "│   └── result_panel.py",
    "├── models/              # 数据模型层",
    "│   ├── database.py",
    "│   ├── symptom.py",
    "│   └── department.py",
    "└── data/                # 数据文件",
    "    ├── symptoms.json    # 症状知识库",
    "    ├── rules.json       # 分诊规则库",
    "    └── departments.json # 科室数据",
  ]),
);

// ---- 第9章 风险与扩展性 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("9. 风险与扩展性"),
  h2("9.1 风险分析与应对"),
  makeTable(["潜在风险", "影响程度", "应对措施"], [
    ["语音识别准确率低", "中", "使用成熟大厂API；提供文字输入备用方案；优化提示语引导用户清晰描述"],
    ["专家系统规则覆盖不足", "中", "基于18种核心症状构建完整规则；设计兜底规则引导人工导诊；预留规则扩展接口"],
    ["多症状分诊冲突", "低", "实现加权投票机制；设计冲突消解策略；冲突时给出备选建议"],
    ["模块集成困难", "中", "提前定义清晰的模块接口；输出标准化数据格式；每周小型集成验证"],
    ["开发进度滞后", "高", "制定详细周计划，每日站会同步；识别关键路径优先保障核心功能；预留1周缓冲"],
    ["演示时出现BUG", "中", "提前多轮演示彩排；准备备用演示环境与录屏；设计异常应对话术"],
  ]),
  h2("9.2 系统扩展性设计"),
  p("水平扩展方向：症状库可从18种扩展至50+种；科室数据独立存储可灵活增删；深度学习模块与专家系统解耦可独立升级；语音识别API可切换不同供应商；预留HIS系统对接接口。"),
  p("长期演进路线：V1.0（当前，18种症状、10个科室、单机运行、文字导航）→ V2.0（50+种症状、全科室覆盖、网络部署、室内地图）→ V3.0（多轮对话、个性化推荐、云端服务、AR实景导航）。"),
  h2("9.3 可维护性保障"),
  p("代码规范：遵循PEP 8编码规范，关键函数配备docstring。日志系统：分级日志记录（DEBUG/INFO/WARNING/ERROR），便于问题排查。单元测试：核心推理算法配备单元测试用例。文档完善：模块接口文档、数据库设计文档、部署手册齐全。"),
);

// ---- 附录 ----
children.push(
  new Paragraph({ children: [new PageBreak()] }),
  h1("附录：团队分工"),
  makeTable(["岗位", "负责人", "核心职责"], [
    ["项目组长", "梁耀辉", "统筹项目进度、协调各模块接口、组织团队讨论"],
    ["需求与架构组", "许欢、王志强、张若岩", "需求调研、PRD撰写、系统架构设计"],
    ["专家系统组", "邱良梓", "医疗知识库构建、规则库编写、推理机实现"],
    ["深度学习/算法组", "梁耀辉", "语音识别集成、症状提取算法、文本分类实现"],
    ["界面与交互组", "马一鹏、张治文", "GUI界面开发、交互逻辑实现"],
    ["测试与文档组", "朱益暄", "测试用例设计、功能测试、文档撰写"],
  ]),
  new Paragraph({ spacing: { before: 400 }, children: [new TextRun({ text: "本文档为智能导医系统课程设计架构设计文档，基于符号主义专家系统与深度学习混合架构，旨在完成可演示的原型系统。", italics: true, size: 20, color: "888888", font: "Microsoft YaHei" })] }),
);

// ========== FINAL ASSEMBLY ==========
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Microsoft YaHei", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Microsoft YaHei", color: "1A1A1A" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Microsoft YaHei", color: "2C2C2C" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Microsoft YaHei", color: "333333" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children,
  }],
});

const outPath = "C:/Users/LiangYaoHui/Desktop/课程设计/智能导医系统架构设计.docx";
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log("Word文档已生成: " + outPath);
  console.log("文件大小: " + (buf.length / 1024).toFixed(1) + " KB");
}).catch(err => {
  console.error("生成失败:", err);
});
