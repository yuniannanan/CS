# -*- coding: utf-8 -*-
"""生成PRD核心操作流程图 - 专业级可视化"""

import math

def gen_core_flow():
    # 配色体系（医疗蓝主色调）
    C = {
        "start_end": {"fill": "#1890FF", "stroke": "#096DD9", "text": "#FFFFFF"},
        "process":   {"fill": "#E6F7FF", "stroke": "#1890FF", "text": "#1D39C4"},
        "decision":  {"fill": "#FFF7E6", "stroke": "#FAAD14", "text": "#D48806"},
        "subflow":   {"fill": "#F6FFED", "stroke": "#52C41A", "text": "#389E0D"},
        "error":     {"fill": "#FFF1F0", "stroke": "#FF4D4F", "text": "#CF1322"},
        "data":      {"fill": "#F5F5F5", "stroke": "#8C8C8C", "text": "#595959"},
        "edge":      "#595959",
        "edge_yes":  "#52C41A",
        "edge_no":   "#FF4D4F",
    }

    def rect(cx, cy, w, h, rx, style, label, sub=""):
        x, y = cx - w//2, cy - h//2
        s = style
        svg = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{s["fill"]}" stroke="{s["stroke"]}" stroke-width="1.8" filter="url(#sh)"/>\n'
        svg += f'<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="12.5" fill="{s["text"]}" font-weight="bold">{label}</text>\n'
        if sub:
            svg += f'<text x="{cx}" y="{cy+13}" text-anchor="middle" font-size="9" fill="{s["text"]}" opacity="0.75">{sub}</text>\n'
        return svg

    def diamond(cx, cy, w, h, style, label):
        x, y = cx - w//2, cy - h//2
        pts = f"{cx},{y} {cx+w//2},{cy} {cx},{y+h} {cx-w//2},{cy}"
        svg = f'<polygon points="{pts}" fill="{style["fill"]}" stroke="{style["stroke"]}" stroke-width="1.8" filter="url(#sh)"/>\n'
        svg += f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="11" fill="{style["text"]}" font-weight="bold">{label}</text>\n'
        return svg

    def line(x1, y1, x2, y2, color="#595959", label=""):
        svg = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.8" marker-end="url(#arr_{color.replace("#","")})"/>\n'
        if label:
            mx, my = (x1+x2)//2, (y1+y2)//2
            svg += f'<text x="{mx+12}" y="{my-4}" font-size="9" fill="{color}" font-weight="600">{label}</text>\n'
        return svg

    def arrow_marker(name, color):
        return f'<marker id="arr_{name}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="{color}"/></marker>\n'

    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 750" font-family="PingFang SC, Microsoft YaHei, Arial, sans-serif">
<defs>
<filter id="sh"><feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-opacity="0.08"/></filter>
<linearGradient id="hdr" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#1890FF"/><stop offset="100%" stop-color="#096DD9"/></linearGradient>
'''

    # Arrow markers
    svg += arrow_marker("595959", "#595959")
    svg += arrow_marker("52C41A", "#52C41A")
    svg += arrow_marker("FF4D4F", "#FF4D4F")
    svg += arrow_marker("1890FF", "#1890FF")

    svg += '''</defs>
<rect x="0" y="0" width="1000" height="750" fill="#FAFBFC"/>

<!-- 标题栏 -->
<rect x="0" y="0" width="1000" height="50" fill="url(#hdr)"/>
<text x="500" y="22" text-anchor="middle" font-size="18" fill="white" font-weight="bold">智能导医系统 — 核心操作流程</text>
<text x="500" y="40" text-anchor="middle" font-size="11" fill="white" opacity="0.8">Core Operation Flow</text>
'''

    # ======== 主流程 (从左到右，从上到下) ========

    # Row 0: 阶段标识
    stages = [
        (130, "输入阶段"),
        (350, "识别阶段"),
        (570, "推理阶段"),
        (790, "输出阶段"),
    ]
    for x, name in stages:
        svg += f'<rect x="{x-55}" y="58" width="110" height="22" rx="11" fill="#F0F5FF" stroke="#BAE7FF"/>\n'
        svg += f'<text x="{x}" y="73" text-anchor="middle" font-size="10" fill="#1890FF" font-weight="bold">{name}</text>\n'

    # ---- 输入阶段 ----
    svg += rect(130, 110, 130, 42, 9, C["start_end"], "患者到达门诊", "")
    svg += line(130, 132, 130, 170, C["edge"])
    svg += rect(130, 190, 130, 42, 9, C["process"], "选择输入方式", "")
    svg += line(130, 212, 130, 250, C["edge"])

    # 语音/文字分支
    svg += rect(70, 270, 110, 50, 8, C["subflow"], "🎤 语音输入", "长按说话 · 松手识别")
    svg += rect(190, 270, 110, 50, 8, C["subflow"], "✏️ 文字输入", "键盘输入症状")
    svg += rect(130, 340, 130, 40, 8, C["subflow"], "快捷症状按钮", "点击常见症状标签")
    svg += line(130, 230, 70, 270, C["edge"])
    svg += line(130, 230, 190, 270, C["edge"])
    svg += line(130, 212, 130, 340, C["edge"])

    # 汇聚 → 症状识别
    svg += line(70, 295, 35, 295, C["edge"])
    svg += line(225, 295, 310, 295, C["edge"])
    svg += line(35, 295, 35, 395, C["edge"])
    svg += line(130, 360, 130, 395, C["edge"])
    svg += line(35, 395, 310, 395, C["edge"])

    # ---- 识别阶段 ----
    svg += line(310, 395, 310, 420, C["edge"])
    svg += rect(310, 440, 150, 48, 9, C["process"], "AI 症状提取", "jieba分词 · 同义词匹配")

    # 决策: 是否成功提取
    svg += line(310, 464, 310, 505, C["edge"])
    svg += diamond(310, 525, 100, 55, C["decision"], "提取成功?")

    # 失败分支 → 提示重试
    svg += line(310, 553, 310, 600, C["edge_no"], "否")
    svg += rect(310, 620, 130, 42, 9, C["error"], "提示重新描述", "引导补充症状细节")
    svg += line(310, 641, 310, 670, C["edge"])
    # 回到输入
    svg += line(310, 670, 310, 690, C["edge"])
    svg += line(310, 690, 130, 690, C["edge"])
    svg += line(130, 690, 130, 360, C["edge"])
    svg += '<text x="220" y="705" text-anchor="middle" font-size="9" fill="#FF4D4F" font-weight="600">↩ 重新描述症状</text>\n'

    # 成功分支 → 推理
    svg += line(400, 525, 465, 525, C["edge_yes"], "是")

    # ---- 推理阶段 ----
    svg += rect(470, 502, 160, 48, 9, C["process"], "专家系统推理", "51条规则 · 组合推理")

    # 决策: 是否匹配到规则
    svg += line(550, 527, 550, 570, C["edge"])
    svg += diamond(550, 585, 100, 50, C["decision"], "匹配到规则?")

    # 失败
    svg += line(550, 610, 550, 650, C["edge_no"], "否")
    svg += rect(550, 670, 130, 42, 9, C["error"], "引导人工导诊", "无匹配规则时兜底")

    # 成功
    svg += line(640, 585, 695, 585, C["edge_yes"], "是")

    # ---- 输出阶段 ----
    svg += rect(700, 562, 150, 48, 9, C["process"], "生成分诊结果", "推荐科室 · 置信度")

    # 严重度标签
    svg += '<rect x="695" y="560" width="55" height="18" rx="9" fill="#FFF7E6" stroke="#FFD591"/>\n'
    svg += '<text x="722" y="573" text-anchor="middle" font-size="9" fill="#D48806" font-weight="bold">🟠 紧急</text>\n'

    svg += line(775, 590, 775, 630, C["edge"])
    svg += rect(700, 650, 150, 48, 9, C["subflow"], "查看就诊路线", "楼层地图 · 路径指引")

    svg += line(775, 674, 775, 710, C["edge"])

    # 完成
    svg += rect(700, 710, 150, 42, 9, C["start_end"], "完成就诊", "")

    # ======== 右侧图例 ========
    legend_x = 885
    svg += f'<rect x="{legend_x}" y="100" width="100" height="260" rx="8" fill="white" stroke="#E8E8E8" filter="url(#sh)"/>\n'
    svg += f'<text x="{legend_x+50}" y="122" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">图例</text>\n'

    items = [
        (legend_x + 10, 140, "开始/结束", C["start_end"]),
        (legend_x + 10, 182, "处理步骤", C["process"]),
        (legend_x + 10, 224, "决策判断", C["decision"]),
        (legend_x + 10, 266, "子功能", C["subflow"]),
        (legend_x + 10, 308, "异常处理", C["error"]),
    ]
    for lx, ly, txt, st in items:
        svg += f'<rect x="{lx}" y="{ly}" width="28" height="22" rx="4" fill="{st["fill"]}" stroke="{st["stroke"]}" stroke-width="1.2"/>\n'
        svg += f'<text x="{lx+36}" y="{ly+16}" font-size="10" fill="#555">{txt}</text>\n'

    # 当前系统状态标注
    svg += f'<rect x="{legend_x}" y="380" width="100" height="180" rx="8" fill="#F0F5FF" stroke="#BAE7FF"/>\n'
    svg += f'<text x="{legend_x+50}" y="402" text-anchor="middle" font-size="10" fill="#1890FF" font-weight="bold">系统现状</text>\n'
    status_lines = [
        "15个症状", "8个科室", "51条规则",
        "4级严重度", "0.5秒语音", "5层医院模型",
    ]
    for i, txt in enumerate(status_lines):
        svg += f'<text x="{legend_x+50}" y="{422+i*22}" text-anchor="middle" font-size="9" fill="#666">✓ {txt}</text>\n'

    # 底部说明
    svg += '<text x="500" y="740" text-anchor="middle" font-size="10" fill="#BFBFBF">图: 智能导医系统核心操作流程图 — 从患者到达到完成就诊的端到端流程</text>\n'
    svg += '</svg>'
    return svg

if __name__ == "__main__":
    svg = gen_core_flow()
    out = "C:/Users/LiangYaoHui/Desktop/课程设计/images/prd_core_flow.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[OK] Generated: {out}")
