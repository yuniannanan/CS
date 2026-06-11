# -*- coding: utf-8 -*-
"""为PRD文档生成专业图表：系统架构、用户流程、专家系统推理、UI线框、甘特图"""

import os

OUTPUT = "C:/Users/LiangYaoHui/Desktop/课程设计/images"

# ===========================
# 1. 系统架构图 SVG
# ===========================
def gen_architecture_svg():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 620" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs>
    <linearGradient id="gLayer" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E6F7FF"/><stop offset="100%" stop-color="#BAE7FF"/>
    </linearGradient>
    <linearGradient id="gCore" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFF7E6"/><stop offset="100%" stop-color="#FFD591"/>
    </linearGradient>
    <linearGradient id="gData" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F6FFED"/><stop offset="100%" stop-color="#B7EB8F"/>
    </linearGradient>
    <filter id="shadow"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/></filter>
    <marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6 Z" fill="#1890FF"/>
    </marker>
  </defs>

  <!-- 标题 -->
  <text x="450" y="35" text-anchor="middle" font-size="22" font-weight="bold" fill="#333">智能导医系统 - 混合架构图</text>
  <line x1="100" y1="48" x2="800" y2="48" stroke="#1890FF" stroke-width="2"/>

  <!-- 表示层 -->
  <rect x="30" y="65" width="840" height="100" rx="10" fill="url(#gLayer)" stroke="#1890FF" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="90" text-anchor="middle" font-size="15" font-weight="bold" fill="#096DD9">表示层 (Presentation Layer)</text>
  <rect x="60" y="105" width="150" height="45" rx="6" fill="white" stroke="#1890FF" stroke-width="1"/>
  <text x="135" y="133" text-anchor="middle" font-size="12" fill="#333">语音输入模块</text>
  <rect x="240" y="105" width="150" height="45" rx="6" fill="white" stroke="#1890FF" stroke-width="1"/>
  <text x="315" y="133" text-anchor="middle" font-size="12" fill="#333">文字输入模块</text>
  <rect x="420" y="105" width="150" height="45" rx="6" fill="white" stroke="#1890FF" stroke-width="1"/>
  <text x="495" y="133" text-anchor="middle" font-size="12" fill="#333">分诊结果展示</text>
  <rect x="600" y="105" width="150" height="45" rx="6" fill="white" stroke="#1890FF" stroke-width="1"/>
  <text x="675" y="133" text-anchor="middle" font-size="12" fill="#333">楼层导航展示</text>

  <!-- 箭头1 -->
  <line x1="450" y1="168" x2="450" y2="195" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- 业务逻辑层 -->
  <rect x="30" y="200" width="840" height="150" rx="10" fill="url(#gCore)" stroke="#FA8C16" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="225" text-anchor="middle" font-size="15" font-weight="bold" fill="#D46B08">业务逻辑层 (Expert System + NLP)</text>
  <rect x="60" y="240" width="180" height="45" rx="6" fill="white" stroke="#FA8C16" stroke-width="1"/>
  <text x="150" y="260" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">语音识别引擎</text>
  <text x="150" y="275" text-anchor="middle" font-size="9" fill="#888">Whisper / 百度API</text>
  <rect x="260" y="240" width="180" height="45" rx="6" fill="white" stroke="#FA8C16" stroke-width="1"/>
  <text x="350" y="260" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">症状提取引擎</text>
  <text x="350" y="275" text-anchor="middle" font-size="9" fill="#888">jieba分词 + 同义词匹配</text>
  <rect x="460" y="240" width="180" height="45" rx="6" fill="white" stroke="#FA8C16" stroke-width="1"/>
  <text x="550" y="260" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">专家系统推理机</text>
  <text x="550" y="275" text-anchor="middle" font-size="9" fill="#888">IF-THEN规则 + 组合推理</text>
  <rect x="660" y="240" width="180" height="45" rx="6" fill="white" stroke="#FA8C16" stroke-width="1"/>
  <text x="750" y="260" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">路径规划引擎</text>
  <text x="750" y="275" text-anchor="middle" font-size="9" fill="#888">医院场景模型寻路</text>

  <!-- 箭头2 -->
  <line x1="450" y1="353" x2="450" y2="380" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- 数据层 -->
  <rect x="30" y="385" width="840" height="100" rx="10" fill="url(#gData)" stroke="#52C41A" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="410" text-anchor="middle" font-size="15" font-weight="bold" fill="#389E0D">数据层 (Data Layer)</text>
  <rect x="100" y="425" width="140" height="45" rx="6" fill="white" stroke="#52C41A" stroke-width="1"/>
  <text x="170" y="448" text-anchor="middle" font-size="11" fill="#333">症状知识库</text>
  <rect x="270" y="425" width="140" height="45" rx="6" fill="white" stroke="#52C41A" stroke-width="1"/>
  <text x="340" y="448" text-anchor="middle" font-size="11" fill="#333">规则库 (51条)</text>
  <rect x="440" y="425" width="140" height="45" rx="6" fill="white" stroke="#52C41A" stroke-width="1"/>
  <text x="510" y="448" text-anchor="middle" font-size="11" fill="#333">科室信息库</text>
  <rect x="610" y="425" width="140" height="45" rx="6" fill="white" stroke="#52C41A" stroke-width="1"/>
  <text x="680" y="448" text-anchor="middle" font-size="11" fill="#333">医院场景模型</text>

  <!-- 左边标签 -->
  <rect x="5" y="60" width="20" height="510" rx="3" fill="#1890FF" opacity="0.15"/>
  <text x="15" y="320" text-anchor="middle" font-size="10" fill="#1890FF" transform="rotate(-90,15,320)">三层架构 MVC</text>

  <!-- 技术栈 -->
  <rect x="30" y="505" width="840" height="55" rx="8" fill="#FAFAFA" stroke="#D9D9D9" stroke-width="1"/>
  <text x="450" y="525" text-anchor="middle" font-size="12" fill="#666">技术栈: Python 3.13 | Flask Web框架 | PyQt5 GUI | SQLite数据库 | Whisper语音识别 | jieba分词 | 专家系统推理机</text>
  <text x="450" y="545" text-anchor="middle" font-size="10" fill="#999">部署: 自签名HTTPS | 响应式Web设计 | 移动端适配 | 完全离线语音识别</text>

  <!-- 底部说明 -->
  <text x="450" y="595" text-anchor="middle" font-size="11" fill="#BBB">图1: 智能导医系统整体架构图 — 三层MVC架构 + 混合AI技术栈</text>
</svg>'''
    with open(os.path.join(OUTPUT, "prd_architecture.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  [OK] prd_architecture.svg")

# ===========================
# 2. 用户使用流程图 SVG
# ===========================
def gen_user_flow_svg():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs>
    <marker id="arrow2" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1890FF"/></marker>
    <filter id="sh"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/></filter>
  </defs>

  <text x="450" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333">患者导诊使用流程</text>

  <!-- Start -->
  <ellipse cx="130" cy="80" rx="80" ry="25" fill="#52C41A" filter="url(#sh)"/>
  <text x="130" y="86" text-anchor="middle" font-size="13" fill="white" font-weight="bold">开始: 患者到达</text>

  <line x1="210" y1="80" x2="270" y2="80" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- 选择输入方式 -->
  <rect x="275" y="55" width="150" height="50" rx="8" fill="#1890FF" filter="url(#sh)"/>
  <text x="350" y="75" text-anchor="middle" font-size="12" fill="white" font-weight="bold">选择输入方式</text>
  <text x="350" y="93" text-anchor="middle" font-size="10" fill="white" opacity="0.8">语音 / 文字 / 快捷按钮</text>

  <line x1="425" y1="80" x2="485" y2="80" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- 描述症状 -->
  <rect x="490" y="55" width="140" height="50" rx="8" fill="#722ED1" filter="url(#sh)"/>
  <text x="560" y="75" text-anchor="middle" font-size="12" fill="white" font-weight="bold">描述症状</text>
  <text x="560" y="93" text-anchor="middle" font-size="10" fill="white" opacity="0.8">说出/输入不适</text>

  <line x1="630" y1="80" x2="690" y2="80" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- 症状提取 -->
  <rect x="695" y="55" width="150" height="50" rx="8" fill="#FA8C16" filter="url(#sh)"/>
  <text x="770" y="75" text-anchor="middle" font-size="12" fill="white" font-weight="bold">AI症状提取</text>
  <text x="770" y="93" text-anchor="middle" font-size="10" fill="white" opacity="0.8">分词 + 同义词匹配</text>

  <!-- Arrow down -->
  <line x1="770" y1="108" x2="770" y2="150" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- 专家系统推理 -->
  <rect x="595" y="155" width="200" height="55" rx="8" fill="#EB2F96" filter="url(#sh)"/>
  <text x="695" y="177" text-anchor="middle" font-size="13" fill="white" font-weight="bold">专家系统推理</text>
  <text x="695" y="195" text-anchor="middle" font-size="10" fill="white" opacity="0.8">规则库匹配 + 置信度计算</text>

  <line x1="695" y1="210" x2="695" y2="260" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- 分岔 -->
  <polygon points="695,260 665,270 725,270" fill="#FF4D4F" filter="url(#sh)"/>
  <text x="695" y="288" text-anchor="middle" font-size="10" fill="#FF4D4F" font-weight="bold">匹配成功?</text>

  <!-- 成功路径 -->
  <line x1="665" y1="270" x2="450" y2="270" stroke="#52C41A" stroke-width="2"/>
  <line x1="450" y1="270" x2="450" y2="330" stroke="#52C41A" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="580" y="263" text-anchor="middle" font-size="11" fill="#52C41A">✅ 是</text>

  <!-- 失败路径 -->
  <line x1="725" y1="270" x2="830" y2="270" stroke="#FF4D4F" stroke-width="2"/>
  <line x1="830" y1="270" x2="830" y2="410" stroke="#FF4D4F" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="780" y="263" text-anchor="middle" font-size="11" fill="#FF4D4F">❌ 否</text>

  <!-- 结果显示 -->
  <rect x="310" y="335" width="280" height="55" rx="8" fill="#52C41A" filter="url(#sh)"/>
  <text x="450" y="357" text-anchor="middle" font-size="13" fill="white" font-weight="bold">显示分诊结果 + 导航路线</text>
  <text x="450" y="375" text-anchor="middle" font-size="10" fill="white" opacity="0.8">科室建议 | 置信度 | 楼层指引 | 医院地图</text>

  <line x1="450" y1="393" x2="450" y2="445" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- End -->
  <ellipse cx="450" cy="465" rx="60" ry="20" fill="#1890FF" filter="url(#sh)"/>
  <text x="450" y="470" text-anchor="middle" font-size="13" fill="white" font-weight="bold">完成就诊</text>

  <!-- 失败处理 -->
  <rect x="730" y="415" width="150" height="50" rx="8" fill="#FF4D4F" filter="url(#sh)"/>
  <text x="805" y="437" text-anchor="middle" font-size="12" fill="white" font-weight="bold">引导人工导诊</text>
  <text x="805" y="455" text-anchor="middle" font-size="10" fill="white" opacity="0.8">补充症状描述</text>

  <line x1="805" y1="468" x2="805" y2="490" stroke="#1890FF" stroke-width="2"/>
  <line x1="805" y1="490" x2="550" y2="490" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="550" y1="490" x2="550" y2="185" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrow2)"/>
  <text x="695" y="495" text-anchor="middle" font-size="9" fill="#999">重新描述症状</text>
</svg>'''
    with open(os.path.join(OUTPUT, "prd_user_flow.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  [OK] prd_user_flow.svg")

# ===========================
# 3. 专家系统推理流程 SVG
# ===========================
def gen_expert_reasoning_svg():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 580" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs>
    <marker id="arrow3" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1890FF"/></marker>
    <filter id="sh2"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/></filter>
    <linearGradient id="ruleBg"><stop offset="0%" stop-color="#F0F5FF"/><stop offset="100%" stop-color="#D6E4FF"/></linearGradient>
  </defs>

  <text x="450" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333">专家系统推理机 — 工作流程</text>

  <!-- 输入 -->
  <rect x="60" y="55" width="200" height="45" rx="8" fill="#1890FF" filter="url(#sh2)"/>
  <text x="160" y="73" text-anchor="middle" font-size="12" fill="white" font-weight="bold">症状列表输入</text>
  <text x="160" y="90" text-anchor="middle" font-size="10" fill="white" opacity="0.85">[头痛:0.95, 发热:1.08, ...]</text>

  <line x1="260" y1="78" x2="320" y2="78" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow3)"/>

  <!-- 症状名→ID映射 -->
  <rect x="325" y="55" width="220" height="45" rx="8" fill="url(#ruleBg)" stroke="#597EF7" stroke-width="1.5" filter="url(#sh2)"/>
  <text x="435" y="73" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">症状名称 → ID 映射</text>
  <text x="435" y="90" text-anchor="middle" font-size="10" fill="#666">查询 symptoms 表获取ID</text>

  <line x1="545" y1="78" x2="605" y2="78" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow3)"/>

  <!-- 规则遍历 -->
  <rect x="610" y="55" width="220" height="45" rx="8" fill="#722ED1" filter="url(#sh2)"/>
  <text x="720" y="73" text-anchor="middle" font-size="11" fill="white" font-weight="bold">遍历规则库 (51条规则)</text>
  <text x="720" y="90" text-anchor="middle" font-size="10" fill="white" opacity="0.85">single / compound / exclusion</text>

  <!-- 向下分叉 -->
  <line x1="720" y1="102" x2="720" y2="140" stroke="#1890FF" stroke-width="2"/>
  <polygon points="720,140 680,155 760,155" fill="#FA8C16" filter="url(#sh2)"/>
  <text x="720" y="172" text-anchor="middle" font-size="10" fill="#FA8C16" font-weight="bold">规则类型判断</text>

  <!-- 三条分支 -->
  <!-- single -->
  <line x1="680" y1="155" x2="350" y2="155" stroke="#52C41A" stroke-width="2"/>
  <line x1="350" y1="155" x2="350" y2="195" stroke="#52C41A" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="520" y="148" text-anchor="middle" font-size="11" fill="#52C41A">single: 单症状匹配</text>

  <rect x="200" y="200" width="300" height="45" rx="6" fill="#F6FFED" stroke="#52C41A" stroke-width="1.5"/>
  <text x="350" y="218" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">规则置信度 = 症状置信度 × 规则权重 × 严重度系数</text>
  <text x="350" y="236" text-anchor="middle" font-size="9" fill="#888">上限 0.92 | severity: low 0.75 ~ critical 1.25</text>

  <!-- compound -->
  <line x1="760" y1="155" x2="760" y2="195" stroke="#EB2F96" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="800" y="175" font-size="11" fill="#EB2F96">compound: 多症状AND</text>

  <rect x="600" y="200" width="280" height="45" rx="6" fill="#FFF0F6" stroke="#EB2F96" stroke-width="1.5"/>
  <text x="740" y="218" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">所有必需症状命中 → 组合规则触发</text>
  <text x="740" y="236" text-anchor="middle" font-size="9" fill="#888">额外 ×1.2 加权 | extra_symptom_ids 全匹配</text>

  <!-- exclusion -->
  <line x1="80" y1="78" x2="80" y2="280" stroke="#FF4D4F" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="15" y="180" font-size="11" fill="#FF4D4F" transform="rotate(-90,15,180)">exclusion: 排除规则</text>

  <rect x="25" y="285" width="110" height="80" rx="6" fill="#FFF1F0" stroke="#FF4D4F" stroke-width="1.5"/>
  <text x="80" y="310" text-anchor="middle" font-size="10" fill="#333" font-weight="bold">触发生效</text>
  <text x="80" y="330" text-anchor="middle" font-size="9" fill="#FF4D4F">从候选科室</text>
  <text x="80" y="348" text-anchor="middle" font-size="9" fill="#FF4D4F">中移除</text>

  <!-- 汇聚 -->
  <line x1="350" y1="248" x2="350" y2="290" stroke="#999" stroke-width="1.5"/>
  <line x1="740" y1="248" x2="350" y2="290" stroke="#999" stroke-width="1.5"/>
  <line x1="350" y1="290" x2="350" y2="330" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow3)"/>

  <!-- 加权计算 -->
  <rect x="170" y="335" width="360" height="55" rx="8" fill="#13C2C2" filter="url(#sh2)"/>
  <text x="350" y="355" text-anchor="middle" font-size="12" fill="white" font-weight="bold">多规则综合置信度计算</text>
  <text x="350" y="375" text-anchor="middle" font-size="10" fill="white" opacity="0.85">归一化 × combo_bonus × dilution × competition → 软上限 95%</text>

  <line x1="350" y1="393" x2="350" y2="440" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow3)"/>

  <!-- 严重度升级 -->
  <rect x="170" y="445" width="360" height="45" rx="8" fill="#FF4D4F" filter="url(#sh2)"/>
  <text x="350" y="463" text-anchor="middle" font-size="12" fill="white" font-weight="bold">严重度升级 + 冲突消解 → 输出推荐科室</text>
  <text x="350" y="481" text-anchor="middle" font-size="10" fill="white" opacity="0.85">critical/high命中 → 自动升级 | 排除规则过滤</text>

  <line x1="530" y1="468" x2="590" y2="468" stroke="#1890FF" stroke-width="2" marker-end="url(#arrow3)"/>

  <!-- 输出 -->
  <rect x="595" y="445" width="220" height="45" rx="8" fill="#52C41A" filter="url(#sh2)"/>
  <text x="705" y="463" text-anchor="middle" font-size="12" fill="white" font-weight="bold">输出: 推荐科室 + 备选</text>
  <text x="705" y="481" text-anchor="middle" font-size="10" fill="white" opacity="0.85">primary + alternatives + reasons</text>

  <!-- 右侧标注 -->
  <rect x="840" y="55" width="45" height="435" rx="5" fill="#F5F5F5" stroke="#D9D9D9"/>
  <text x="863" y="280" text-anchor="middle" font-size="10" fill="#999" transform="rotate(-90,863,280)">51条规则 · 15个症状 · 4级严重度</text>

  <text x="450" y="560" text-anchor="middle" font-size="11" fill="#BBB">图3: 专家系统推理机完整工作流程 — 从症状输入到科室推荐的端到端推理链路</text>
</svg>'''
    with open(os.path.join(OUTPUT, "prd_expert_reasoning.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  [OK] prd_expert_reasoning.svg")

# ===========================
# 4. UI线框图 SVG
# ===========================
def gen_ui_wireframe_svg():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 520" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs>
    <filter id="sh3"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.12"/></filter>
    <linearGradient id="headerGrad"><stop offset="0%" stop-color="#1890FF"/><stop offset="100%" stop-color="#096DD9"/></linearGradient>
  </defs>

  <text x="450" y="25" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">智能导医系统 — UI 界面线框图</text>

  <!-- ===== 页面1: 首页 ===== -->
  <g transform="translate(10, 38)">
    <rect x="0" y="0" width="275" height="470" rx="10" fill="white" stroke="#D9D9D9" stroke-width="1.5" filter="url(#sh3)"/>
    <!-- Header -->
    <rect x="0" y="0" width="275" height="40" rx="10" fill="url(#headerGrad)"/>
    <rect x="0" y="20" width="275" height="20" fill="url(#headerGrad)"/>
    <text x="138" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">智能导医系统</text>
    <!-- Voice -->
    <circle cx="138" cy="95" r="28" fill="#1890FF" filter="url(#sh3)"/>
    <text x="138" y="100" text-anchor="middle" font-size="16" fill="white">🎤</text>
    <text x="138" y="135" text-anchor="middle" font-size="9" fill="#888">按住说话</text>
    <!-- Input -->
    <rect x="15" y="155" width="200" height="30" rx="6" fill="#F5F5F5" stroke="#D9D9D9"/>
    <text x="115" y="175" text-anchor="middle" font-size="9" fill="#BBB">请描述您的症状…</text>
    <rect x="220" y="155" width="40" height="30" rx="6" fill="#52C41A"/>
    <text x="240" y="175" text-anchor="middle" font-size="9" fill="white" font-weight="bold">分诊</text>
    <!-- Tags -->
    <rect x="15" y="195" width="42" height="22" rx="11" fill="#E6F7FF" stroke="#91D5FF"/>
    <text x="36" y="210" text-anchor="middle" font-size="8" fill="#1890FF">发烧</text>
    <rect x="63" y="195" width="42" height="22" rx="11" fill="#E6F7FF" stroke="#91D5FF"/>
    <text x="84" y="210" text-anchor="middle" font-size="8" fill="#1890FF">咳嗽</text>
    <rect x="111" y="195" width="42" height="22" rx="11" fill="#E6F7FF" stroke="#91D5FF"/>
    <text x="132" y="210" text-anchor="middle" font-size="8" fill="#1890FF">头痛</text>
    <rect x="159" y="195" width="42" height="22" rx="11" fill="#E6F7FF" stroke="#91D5FF"/>
    <text x="180" y="210" text-anchor="middle" font-size="8" fill="#1890FF">腹痛</text>
    <!-- Result preview -->
    <rect x="15" y="235" width="245" height="80" rx="6" fill="#F6FFED" stroke="#B7EB8F" stroke-width="1"/>
    <text x="138" y="255" text-anchor="middle" font-size="11" fill="#52C41A" font-weight="bold">呼吸内科</text>
    <text x="138" y="272" text-anchor="middle" font-size="8" fill="#666">📍 1楼东侧</text>
    <rect x="30" y="280" width="215" height="6" rx="3" fill="#E8E8E8"/>
    <rect x="30" y="280" width="200" height="6" rx="3" fill="#52C41A"/>
    <text x="138" y="300" text-anchor="middle" font-size="8" fill="#999">置信度: 95% | 命中规则: 9条</text>
    <rect x="50" y="305" width="175" height="24" rx="6" fill="#FFF7E6" stroke="#FFD591"/>
    <text x="138" y="322" text-anchor="middle" font-size="9" fill="#D48806">查看就诊路线</text>
  </g>

  <text x="148" y="515" text-anchor="middle" font-size="10" fill="#999">首页 — 语音+文字输入</text>

  <!-- ===== 页面2: 医院导航 ===== -->
  <g transform="translate(310, 38)">
    <rect x="0" y="0" width="275" height="470" rx="10" fill="white" stroke="#D9D9D9" stroke-width="1.5" filter="url(#sh3)"/>
    <rect x="0" y="0" width="275" height="40" rx="10" fill="url(#headerGrad)"/>
    <rect x="0" y="20" width="275" height="20" fill="url(#headerGrad)"/>
    <text x="138" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">就诊导航</text>
    <!-- Floor tabs -->
    <rect x="15" y="50" width="32" height="20" rx="10" fill="#1890FF"/>
    <text x="31" y="64" text-anchor="middle" font-size="8" fill="white" font-weight="bold">1F</text>
    <rect x="52" y="50" width="32" height="20" rx="10" fill="white" stroke="#D9D9D9"/>
    <text x="68" y="64" text-anchor="middle" font-size="8" fill="#666">2F</text>
    <rect x="89" y="50" width="32" height="20" rx="10" fill="white" stroke="#D9D9D9"/>
    <text x="105" y="64" text-anchor="middle" font-size="8" fill="#666">3F</text>
    <rect x="126" y="50" width="32" height="20" rx="10" fill="white" stroke="#D9D9D9"/>
    <text x="142" y="64" text-anchor="middle" font-size="8" fill="#666">4F</text>
    <rect x="163" y="50" width="32" height="20" rx="10" fill="white" stroke="#D9D9D9"/>
    <text x="179" y="64" text-anchor="middle" font-size="8" fill="#666">5F</text>
    <!-- Hospital map -->
    <rect x="15" y="78" width="245" height="210" rx="6" fill="#FAFAFA" stroke="#E8E8E8"/>
    <!-- Walls -->
    <rect x="25" y="88" width="225" height="190" rx="4" fill="#F5F5F5" stroke="#D9D9D9" stroke-dasharray="4,2"/>
    <!-- Corridor -->
    <rect x="120" y="88" width="25" height="190" fill="#E8E8E8" stroke="#D9D9D9" stroke-dasharray="3,2"/>
    <text x="132" y="188" text-anchor="middle" font-size="7" fill="#999">走廊</text>
    <!-- Departments -->
    <rect x="35" y="100" width="70" height="35" rx="5" fill="#52C41A" opacity="0.2" stroke="#52C41A"/>
    <text x="70" y="122" text-anchor="middle" font-size="9" fill="#52C41A" font-weight="bold">普通内科</text>
    <rect x="155" y="100" width="65" height="35" rx="5" fill="#FF4D4F" opacity="0.2" stroke="#FF4D4F"/>
    <text x="187" y="122" text-anchor="middle" font-size="9" fill="#FF4D4F" font-weight="bold">急诊科</text>
    <!-- Facilities -->
    <rect x="55" y="180" width="55" height="28" rx="4" fill="#FAAD14" opacity="0.15" stroke="#FAAD14"/>
    <text x="82" y="198" text-anchor="middle" font-size="8" fill="#FAAD14">🏷 挂号处</text>
    <rect x="160" y="180" width="55" height="28" rx="4" fill="#1890FF" opacity="0.15" stroke="#1890FF"/>
    <text x="187" y="198" text-anchor="middle" font-size="8" fill="#1890FF">💊 药房</text>
    <!-- Entrance -->
    <circle cx="82" cy="255" r="6" fill="#52C41A"/>
    <text x="82" y="270" text-anchor="middle" font-size="7" fill="#52C41A">🚪 入口</text>
    <!-- Elevator -->
    <rect x="145" y="240" width="18" height="18" rx="4" fill="#1890FF" opacity="0.15" stroke="#1890FF"/>
    <text x="154" y="265" text-anchor="middle" font-size="7" fill="#1890FF">🛗</text>
    <!-- Path line -->
    <line x1="82" y1="250" x2="82" y2="195" stroke="#FF4D4F" stroke-width="2" stroke-dasharray="4,3"/>
    <line x1="82" y1="195" x2="70" y2="130" stroke="#FF4D4F" stroke-width="2" stroke-dasharray="4,3"/>
    <!-- Steps -->
    <text x="138" y="310" font-size="9" fill="#333" font-weight="bold">导航步骤:</text>
    <text x="20" y="328" font-size="8" fill="#666">1. 从正门进入1楼大厅</text>
    <text x="20" y="344" font-size="8" fill="#666">2. 前往导诊台确认挂号</text>
    <text x="20" y="360" font-size="8" fill="#666">3. 前往「普通内科」诊区</text>
    <text x="20" y="376" font-size="8" fill="#666">4. 向护士报到就诊</text>
  </g>
  <text x="448" y="515" text-anchor="middle" font-size="10" fill="#999">导航页 — 楼层地图+路线</text>

  <!-- ===== 页面3: 规则管理 ===== -->
  <g transform="translate(610, 38)">
    <rect x="0" y="0" width="275" height="470" rx="10" fill="white" stroke="#D9D9D9" stroke-width="1.5" filter="url(#sh3)"/>
    <rect x="0" y="0" width="275" height="40" rx="10" fill="url(#headerGrad)"/>
    <rect x="0" y="20" width="275" height="20" fill="url(#headerGrad)"/>
    <text x="138" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">⚙ 规则管理</text>
    <!-- Stats -->
    <rect x="15" y="50" width="80" height="35" rx="6" fill="#F6FFED"/>
    <text x="55" y="65" text-anchor="middle" font-size="14" fill="#52C41A" font-weight="bold">51</text>
    <text x="55" y="78" text-anchor="middle" font-size="8" fill="#888">规则总数</text>
    <rect x="100" y="50" width="52" height="35" rx="6" fill="#E6F7FF"/>
    <text x="126" y="65" text-anchor="middle" font-size="14" fill="#1890FF" font-weight="bold">36</text>
    <text x="126" y="78" text-anchor="middle" font-size="8" fill="#888">单症状</text>
    <rect x="157" y="50" width="52" height="35" rx="6" fill="#FFF7E6"/>
    <text x="183" y="65" text-anchor="middle" font-size="14" fill="#FA8C16" font-weight="bold">13</text>
    <text x="183" y="78" text-anchor="middle" font-size="8" fill="#888">组合</text>
    <rect x="214" y="50" width="46" height="35" rx="6" fill="#FFF1F0"/>
    <text x="237" y="65" text-anchor="middle" font-size="14" fill="#FF4D4F" font-weight="bold">2</text>
    <text x="237" y="78" text-anchor="middle" font-size="8" fill="#888">排除</text>
    <!-- Filter -->
    <rect x="15" y="95" width="35" height="18" rx="9" fill="#1890FF"/>
    <text x="32" y="108" text-anchor="middle" font-size="8" fill="white">全部</text>
    <rect x="55" y="95" width="52" height="18" rx="9" fill="white" stroke="#D9D9D9"/>
    <text x="81" y="108" text-anchor="middle" font-size="7" fill="#666">单症状</text>
    <rect x="112" y="95" width="40" height="18" rx="9" fill="white" stroke="#D9D9D9"/>
    <text x="132" y="108" text-anchor="middle" font-size="7" fill="#666">组合</text>
    <rect x="157" y="95" width="40" height="18" rx="9" fill="white" stroke="#D9D9D9"/>
    <text x="177" y="108" text-anchor="middle" font-size="7" fill="#666">排除</text>
    <!-- Table header -->
    <rect x="15" y="120" width="245" height="16" rx="3" fill="#FAFAFA"/>
    <text x="25" y="132" font-size="7" fill="#888">ID</text>
    <text x="52" y="132" font-size="7" fill="#888">条件</text>
    <text x="125" y="132" font-size="7" fill="#888">科室</text>
    <text x="155" y="132" font-size="7" fill="#888">严重度</text>
    <text x="185" y="132" font-size="7" fill="#888">类型</text>
    <text x="215" y="132" font-size="7" fill="#888">操作</text>
    <!-- Row 1 -->
    <rect x="15" y="138" width="245" height="22" fill="white" stroke="#F5F5F5"/>
    <text x="25" y="153" font-size="7" fill="#333">1</text>
    <text x="52" y="153" font-size="7" fill="#333">IF头痛THEN神经内科</text>
    <text x="125" y="153" font-size="7" fill="#1890FF">神经内科</text>
    <rect x="152" y="145" width="26" height="12" rx="6" fill="#FA8C16"/>
    <text x="165" y="154" font-size="6" fill="white">high</text>
    <text x="188" y="153" font-size="7" fill="#666">单症状</text>
    <text x="218" y="153" font-size="7" fill="#1890FF">编辑</text>
    <text x="240" y="153" font-size="7" fill="#FF4D4F">删</text>
    <!-- Row 2 -->
    <rect x="15" y="162" width="245" height="22" fill="#F9FBFF" stroke="#F5F5F5"/>
    <text x="25" y="177" font-size="7" fill="#333">2</text>
    <text x="52" y="177" font-size="7" fill="#333">IF头晕THEN神经内科</text>
    <text x="125" y="177" font-size="7" fill="#1890FF">神经内科</text>
    <rect x="152" y="169" width="26" height="12" rx="6" fill="#1890FF"/>
    <text x="165" y="178" font-size="6" fill="white">med</text>
    <text x="188" y="177" font-size="7" fill="#666">单症状</text>
    <text x="218" y="177" font-size="7" fill="#1890FF">编辑</text>
    <text x="240" y="177" font-size="7" fill="#FF4D4F">删</text>
    <!-- Row 3 -->
    <rect x="15" y="186" width="245" height="22" fill="white" stroke="#F5F5F5"/>
    <text x="25" y="201" font-size="7" fill="#333">3</text>
    <text x="52" y="201" font-size="7" fill="#333">IF咳嗽THEN呼吸内科</text>
    <text x="125" y="201" font-size="7" fill="#1890FF">呼吸内科</text>
    <rect x="152" y="193" width="26" height="12" rx="6" fill="#1890FF"/>
    <text x="165" y="202" font-size="6" fill="white">med</text>
    <text x="188" y="201" font-size="7" fill="#666">单症状</text>
    <text x="218" y="201" font-size="7" fill="#1890FF">编辑</text>
    <text x="240" y="201" font-size="7" fill="#FF4D4F">删</text>
    <!-- Add button -->
    <rect x="200" y="215" width="60" height="20" rx="10" fill="#52C41A"/>
    <text x="230" y="229" text-anchor="middle" font-size="8" fill="white">+ 新增</text>
  </g>
  <text x="748" y="515" text-anchor="middle" font-size="10" fill="#999">规则管理页 — CRUD</text>
</svg>'''
    with open(os.path.join(OUTPUT, "prd_ui_wireframe.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  [OK] prd_ui_wireframe.svg")

# ===========================
# 5. 甘特图 SVG
# ===========================
def gen_gantt_svg():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 410" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <text x="450" y="28" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">项目排期甘特图</text>

  <!-- 时间轴表头 -->
  <rect x="200" y="40" width="680" height="25" fill="#FAFAFA"/>
  <text x="200" y="57" font-size="9" fill="#999">第1周</text>
  <text x="313" y="57" font-size="9" fill="#999">第2周</text>
  <text x="426" y="57" font-size="9" fill="#999">第3周</text>
  <text x="540" y="57" font-size="9" fill="#999">第4周</text>
  <text x="653" y="57" font-size="9" fill="#999">第5周</text>
  <text x="766" y="57" font-size="9" fill="#999">第6周</text>

  <line x1="200" y1="40" x2="200" y2="390" stroke="#E8E8E8"/>
  <line x1="313" y1="40" x2="313" y2="390" stroke="#E8E8E8"/>
  <line x1="426" y1="40" x2="426" y2="390" stroke="#E8E8E8"/>
  <line x1="540" y1="40" x2="540" y2="390" stroke="#E8E8E8"/>
  <line x1="653" y1="40" x2="653" y2="390" stroke="#E8E8E8"/>
  <line x1="766" y1="40" x2="766" y2="390" stroke="#E8E8E8"/>

  <!-- 阶段1: PRD -->
  <rect x="10" y="75" width="180" height="38" rx="4" fill="#F0F5FF"/>
  <text x="100" y="90" text-anchor="middle" font-size="10" fill="#333" font-weight="bold">阶段1: 需求与PRD</text>
  <text x="100" y="105" text-anchor="middle" font-size="8" fill="#888">梁耀辉</text>
  <rect x="200" y="82" width="113" height="24" rx="6" fill="#1890FF"/>
  <text x="257" y="98" text-anchor="middle" font-size="9" fill="white" font-weight="bold">第1周</text>

  <!-- 阶段2: 架构设计 -->
  <rect x="10" y="125" width="180" height="38" rx="4" fill="#F6FFED"/>
  <text x="100" y="140" text-anchor="middle" font-size="10" fill="#333" font-weight="bold">阶段2: 架构设计</text>
  <text x="100" y="155" text-anchor="middle" font-size="8" fill="#888">许欢 王志强 张若岩</text>
  <rect x="200" y="132" width="113" height="24" rx="6" fill="#52C41A"/>
  <text x="257" y="148" text-anchor="middle" font-size="9" fill="white" font-weight="bold">第1周</text>

  <!-- 阶段3: 专家系统 -->
  <rect x="10" y="175" width="180" height="38" rx="4" fill="#FFF7E6"/>
  <text x="100" y="190" text-anchor="middle" font-size="10" fill="#333" font-weight="bold">阶段3: 专家系统</text>
  <text x="100" y="205" text-anchor="middle" font-size="8" fill="#888">邱良梓</text>
  <rect x="313" y="182" width="226" height="24" rx="6" fill="#FA8C16"/>
  <text x="426" y="198" text-anchor="middle" font-size="9" fill="white" font-weight="bold">第2-3周</text>

  <!-- 阶段4: 算法模块 -->
  <rect x="10" y="225" width="180" height="38" rx="4" fill="#F0F5FF"/>
  <text x="100" y="240" text-anchor="middle" font-size="10" fill="#333" font-weight="bold">阶段4: 算法模块</text>
  <text x="100" y="255" text-anchor="middle" font-size="8" fill="#888">梁耀辉</text>
  <rect x="313" y="232" width="226" height="24" rx="6" fill="#1890FF"/>
  <text x="426" y="248" text-anchor="middle" font-size="9" fill="white" font-weight="bold">第2-3周</text>

  <!-- 阶段5: GUI -->
  <rect x="10" y="275" width="180" height="38" rx="4" fill="#FFF0F6"/>
  <text x="100" y="290" text-anchor="middle" font-size="10" fill="#333" font-weight="bold">阶段5: GUI开发</text>
  <text x="100" y="305" text-anchor="middle" font-size="8" fill="#888">马一鹏 张治文</text>
  <rect x="426" y="282" width="226" height="24" rx="6" fill="#EB2F96"/>
  <text x="540" y="298" text-anchor="middle" font-size="9" fill="white" font-weight="bold">第3-4周</text>

  <!-- 阶段6: 集成测试 -->
  <rect x="10" y="325" width="180" height="38" rx="4" fill="#F6FFED"/>
  <text x="100" y="340" text-anchor="middle" font-size="10" fill="#333" font-weight="bold">阶段6: 集成测试</text>
  <text x="100" y="355" text-anchor="middle" font-size="8" fill="#888">朱益暄</text>
  <rect x="653" y="332" width="113" height="24" rx="6" fill="#52C41A"/>
  <text x="710" y="348" text-anchor="middle" font-size="9" fill="white" font-weight="bold">第5周</text>

  <!-- 阶段7: 优化验收 -->
  <rect x="10" y="375" width="180" height="30" rx="4" fill="#F0F5FF"/>
  <text x="100" y="393" text-anchor="middle" font-size="10" fill="#333" font-weight="bold">阶段7: 优化验收</text>
  <rect x="766" y="380" width="113" height="24" rx="6" fill="#1890FF"/>
  <text x="823" y="396" text-anchor="middle" font-size="9" fill="white" font-weight="bold">第6周</text>

  <!-- 里程碑 -->
  <line x1="766" y1="40" x2="766" y2="405" stroke="#FF4D4F" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="860" y="75" font-size="9" fill="#FF4D4F" font-weight="bold">答辩</text>
</svg>'''
    with open(os.path.join(OUTPUT, "prd_gantt.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  [OK] prd_gantt.svg")


if __name__ == "__main__":
    os.makedirs(OUTPUT, exist_ok=True)
    print("Generating PRD diagrams...")
    gen_architecture_svg()
    gen_user_flow_svg()
    gen_expert_reasoning_svg()
    gen_ui_wireframe_svg()
    gen_gantt_svg()
    print("\n  [OK] All 5 diagrams generated in images/")
