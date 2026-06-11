#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
绘制智能导医系统架构设计文档中的4个架构图
输出SVG格式，无外部依赖
"""

import os
import math

OUTPUT_DIR = "C:/Users/LiangYaoHui/Desktop/课程设计/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def wrap_text(text, max_chars=12):
    """简单中文换行"""
    if len(text) <= max_chars:
        return [text]
    lines = []
    while len(text) > max_chars:
        lines.append(text[:max_chars])
        text = text[max_chars:]
    if text:
        lines.append(text)
    return lines


# ============================================================
# 图1：四层架构图
# ============================================================
def draw_fig1():
    W, H = 1000, 1200
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append('<defs>')
    parts.append('<marker id="ab" markerWidth="10" markerHeight="8" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#1890FF"/></marker>')
    parts.append('<marker id="ag" markerWidth="10" markerHeight="8" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#52C41A"/></marker>')
    parts.append('<marker id="ao" markerWidth="10" markerHeight="8" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#FA8C16"/></marker>')
    parts.append('<style>text{font-family:"Microsoft YaHei","SimHei",sans-serif;}</style>')
    parts.append('</defs>')
    parts.append(f'<rect width="{W}" height="{H}" fill="#F5F5F5"/>')
    parts.append(f'<text x="{W//2}" y="38" font-size="20" font-weight="bold" text-anchor="middle" fill="#1a1a1a">智能导医系统 — 四层架构图</text>')

    # 层定义
    layers = [
        ("交互展示层", "#E8F4FD", "#BAE0FF", [
            ("GUI界面模块", "#BAE0FF"),
            ("语音交互模块", "#BAE0FF"),
            ("路线展示模块", "#BAE0FF"),
        ]),
        ("业务逻辑层", "#FFF3E0", "#FFE0B2", [
            ("分诊流程控制", "#FFE0B2"),
            ("症状管理模块", "#FFE0B2"),
            ("历史记录模块", "#FFE0B2"),
            ("异常处理模块", "#FFE0B2"),
        ]),
        ("算法推理层", "#E8F5E9", "#C8E6C9", [
            ("专家系统推理机", "#C8E6C9"),
            ("深度学习模型", "#C8E6C9"),
            ("症状提取引擎", "#C8E6C9"),
            ("语音转文本引擎", "#C8E6C9"),
        ]),
        ("数据层", "#FCE4EC", "#F8BBD0", [
            ("SQLite数据库", "#F8BBD0"),
            ("症状知识库", "#F8BBD0"),
            ("规则库", "#F8BBD0"),
            ("科室楼层数据", "#F8BBD0"),
        ]),
    ]

    LAYER_H = 200
    GAP_Y = 36
    MARGIN_X = 60
    layer_w = W - 2 * MARGIN_X
    start_y = 65

    # 记录每层模块中心，用于画箭头
    layer_mod_centers = []

    for i, (layer_name, layer_bg, mod_bg, modules) in enumerate(layers):
        y = start_y + i * (LAYER_H + GAP_Y)
        # 层背景
        parts.append(f'<rect x="{MARGIN_X}" y="{y}" width="{layer_w}" height="{LAYER_H}" fill="{layer_bg}" rx="12" stroke="#999" stroke-width="1.5"/>')
        # 层标题（左侧竖排）
        parts.append(f'<rect x="{MARGIN_X+6}" y="{y+6}" width="30" height="{LAYER_H-12}" fill="{layer_bg}" rx="6" stroke="#aaa" stroke-width="0.8"/>')
        for ci, ch in enumerate(layer_name):
            parts.append(f'<text x="{MARGIN_X+21}" y="{y+24+ci*20}" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">{ch}</text>')

        # 模块框
        n = len(modules)
        mod_w = 150
        mod_h = 46
        mod_gap = 14
        total = n * mod_w + (n-1) * mod_gap
        sx = MARGIN_X + (layer_w - total) // 2

        centers = []
        for j, (mname, mbg) in enumerate(modules):
            mx = sx + j * (mod_w + mod_gap)
            my = y + (LAYER_H - mod_h) // 2
            parts.append(f'<rect x="{mx}" y="{my}" width="{mod_w}" height="{mod_h}" fill="{mbg}" rx="8" stroke="#777" stroke-width="1"/>')
            lines = wrap_text(mname, 9)
            for li, line in enumerate(lines):
                ly = my + mod_h//2 + (li - len(lines)//2)*15 + 5
                parts.append(f'<text x="{mx+mod_w//2}" y="{ly}" font-size="12" text-anchor="middle" fill="#333">{line}</text>')
            centers.append((mx + mod_w//2, my + mod_h))
        layer_mod_centers.append(centers)

        # 保存本层底部y
        layer_mod_centers.append(("bottom", y + LAYER_H))

    # 层间箭头（交互展示层 → 业务逻辑层 → 算法推理层 → 数据层）
    # 重新整理：layer_mod_centers 中偶数索引是centers，奇数是bottom
    # 实际上面循环中直接append了，导致结构不对，重新处理
    parts.append(f'<text x="{W//2}" y="{H-18}" font-size="12" text-anchor="middle" fill="#888">图1：系统四层架构（交互展示层 → 业务逻辑层 → 算法推理层 → 数据层）</text>')
    parts.append('</svg>')

    path = os.path.join(OUTPUT_DIR, "fig1_architecture.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"  图1已生成: {path}")
    return path


# 重新写图1，正确处理位置记录
def draw_fig1_v2():
    W, H = 1000, 1250
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append('<defs>')
    parts.append('<marker id="ab" markerWidth="10" markerHeight="8" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#1890FF"/></marker>')
    parts.append('<style>text{font-family:"Microsoft YaHei","SimHei",sans-serif;}</style>')
    parts.append('</defs>')
    parts.append(f'<rect width="{W}" height="{H}" fill="#F5F5F5"/>')
    parts.append(f'<text x="{W//2}" y="38" font-size="20" font-weight="bold" text-anchor="middle" fill="#1a1a1a">智能导医系统 — 四层架构图</text>')

    layers = [
        ("交互展示层", "#E8F4FD", "#BAE0FF", [
            "GUI界面模块", "语音交互模块", "路线展示模块",
        ]),
        ("业务逻辑层", "#FFF3E0", "#FFE0B2", [
            "分诊流程控制", "症状管理模块", "历史记录模块", "异常处理模块",
        ]),
        ("算法推理层", "#E8F5E9", "#C8E6C9", [
            "专家系统推理机", "深度学习模型", "症状提取引擎", "语音转文本引擎",
        ]),
        ("数据层", "#FCE4EC", "#F8BBD0", [
            "SQLite数据库", "症状知识库", "规则库", "科室楼层数据",
        ]),
    ]

    LAYER_H = 210
    GAP_Y = 40
    MARGIN = 60
    layer_w = W - 2 * MARGIN
    start_y = 65

    all_centers = []  # list of (list_of_(cx,cy), bottom_y)

    for i, (layer_name, layer_bg, mod_bg, modules) in enumerate(layers):
        y = start_y + i * (LAYER_H + GAP_Y)
        parts.append(f'<rect x="{MARGIN}" y="{y}" width="{layer_w}" height="{LAYER_H}" fill="{layer_bg}" rx="12" stroke="#999" stroke-width="1.5"/>')
        # 左侧竖排标题
        parts.append(f'<rect x="{MARGIN+6}" y="{y+6}" width="30" height="{LAYER_H-12}" fill="{layer_bg}" rx="6" stroke="#aaa" stroke-width="0.8"/>')
        for ci, ch in enumerate(layer_name):
            parts.append(f'<text x="{MARGIN+21}" y="{y+24+ci*20}" font-size="13" font-weight="bold" text-anchor="middle" fill="#333">{ch}</text>')

        n = len(modules)
        mod_w = 150
        mod_h = 46
        mod_gap = 14
        total = n * mod_w + (n-1) * mod_gap
        sx = MARGIN + (layer_w - total) // 2

        centers = []
        for j, mname in enumerate(modules):
            mx = sx + j * (mod_w + mod_gap)
            my = y + (LAYER_H - mod_h) // 2
            parts.append(f'<rect x="{mx}" y="{my}" width="{mod_w}" height="{mod_h}" fill="{mod_bg}" rx="8" stroke="#777" stroke-width="1"/>')
            lines = wrap_text(mname, 9)
            for li, line in enumerate(lines):
                ly = my + mod_h//2 + (li - len(lines)//2)*15 + 5
                parts.append(f'<text x="{mx+mod_w//2}" y="{ly}" font-size="12" text-anchor="middle" fill="#333">{line}</text>')
            centers.append((mx + mod_w//2, my + mod_h))
        all_centers.append((centers, y + LAYER_H))

    # 画层间箭头
    colors = ["#1890FF", "#52C41A", "#FA8C16"]
    for i in range(len(layers) - 1):
        src_cs, src_bottom = all_centers[i]
        dst_cs, _ = all_centers[i+1]
        n_conn = min(len(src_cs), len(dst_cs))
        for k in range(n_conn):
            x1 = src_cs[k][0]
            y1 = src_bottom
            x2 = dst_cs[k][0]
            y2 = all_centers[i][0][0][1]  # 下一层第一个模块的顶部y，实际应该是下一层的y
            # 重新计算y2
            next_y = start_y + (i+1) * (LAYER_H + GAP_Y)
            y2_actual = next_y + (LAYER_H - 46) // 2
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2_actual}" stroke="{colors[i%3]}" stroke-width="2" marker-end="url(#ab)"/>')

    parts.append(f'<text x="{W//2}" y="{H-18}" font-size="12" text-anchor="middle" fill="#888">图1：系统四层架构（交互展示层 → 业务逻辑层 → 算法推理层 → 数据层）</text>')
    parts.append('</svg>')

    path = os.path.join(OUTPUT_DIR, "fig1_architecture.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"  图1已生成: {path}")
    return path


# ============================================================
# 图2：数据流转时序图
# ============================================================
def draw_fig2():
    W, H = 1100, 950
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append('<defs>')
    parts.append('<marker id="arr" markerWidth="10" markerHeight="8" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#1890FF"/></marker>')
    parts.append('<style>text{font-family:"Microsoft YaHei","SimHei",sans-serif;}</style>')
    parts.append('</defs>')
    parts.append(f'<rect width="{W}" height="{H}" fill="#F5F5F5"/>')
    parts.append(f'<text x="{W//2}" y="38" font-size="20" font-weight="bold" text-anchor="middle" fill="#1a1a1a">智能导医系统 — 数据流转时序图</text>')

    actors = ["用户", "GUI界面", "症状提取", "专家系统", "深度学习", "数据库"]
    # 均匀分布在宽度上
    padding = 80
    avail = W - 2 * padding
    n_actors = len(actors)
    axs = [padding + (avail * (i + 0.5)) / n_actors for i in range(n_actors)]

    actor_top = 90
    actor_bottom = 840

    for x, actor in zip(axs, actors):
        # 顶部参与者框
        parts.append(f'<rect x="{x-48}" y="{actor_top}" width="96" height="38" fill="#1890FF" rx="8"/>')
        parts.append(f'<text x="{x}" y="{actor_top+25}" font-size="12" font-weight="bold" text-anchor="middle" fill="white">{actor}</text>')
        # 生命线
        parts.append(f'<line x1="{x}" y1="{actor_top+38}" x2="{x}" y2="{actor_bottom}" stroke="#ccc" stroke-width="1.5" stroke-dasharray="6,4"/>')
        # 底部框
        parts.append(f'<rect x="{x-48}" y="{actor_bottom}" width="96" height="38" fill="#1890FF" rx="8"/>')
        parts.append(f'<text x="{x}" y="{actor_bottom+25}" font-size="12" font-weight="bold" text-anchor="middle" fill="white">{actor}</text>')

    # 消息序列：(src_idx, dst_idx, text, y_pos, color)
    messages = [
        (0, 1, "语音/文字输入症状", 180, "#333"),
        (1, 2, "提交文本进行症状提取", 240, "#1890FF"),
        (2, 5, "查询症状知识库", 300, "#52C41A"),
        (5, 2, "返回症状匹配结果", 350, "#52C41A"),
        (2, 1, "返回结构化症状列表", 400, "#333"),
        (1, 3, "提交症状进行规则推理", 460, "#1890FF"),
        (3, 5, "查询规则库与科室数据", 520, "#FA8C16"),
        (5, 3, "返回匹配规则", 565, "#FA8C16"),
        (3, 3, "加权计算置信度", 610, "#333"),
        (3, 1, "返回分诊结果", 660, "#722ED1"),
        (1, 4, "深度学习辅助验证", 710, "#EB2F96"),
        (4, 1, "返回优化建议", 750, "#EB2F96"),
        (1, 5, "保存分诊记录", 790, "#333"),
        (1, 0, "展示分诊结果与导航路线", 830, "#333"),
    ]

    for src, dst, text, y, color in messages:
        x1 = axs[src]
        x2 = axs[dst]
        parts.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="1.8" marker-end="url(#arr)"/>')
        tx = (x1 + x2) / 2
        # 判断箭头方向，文字放在上方或下方
        parts.append(f'<text x="{tx}" y="{y-7}" font-size="10" text-anchor="middle" fill="{color}">{text}</text>')

    parts.append(f'<text x="{W//2}" y="{H-18}" font-size="12" text-anchor="middle" fill="#888">图2：系统数据流转时序图（展示用户、界面与各模块间的交互顺序）</text>')
    parts.append('</svg>')

    path = os.path.join(OUTPUT_DIR, "fig2_sequence.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"  图2已生成: {path}")
    return path


# ============================================================
# 图3：功能模块划分图
# ============================================================
def draw_fig3():
    W, H = 1100, 800
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append('<defs>')
    parts.append('<marker id="modarr" markerWidth="10" markerHeight="8" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#1890FF"/></marker>')
    parts.append('<style>text{font-family:"Microsoft YaHei","SimHei",sans-serif;}</style>')
    parts.append('</defs>')
    parts.append(f'<rect width="{W}" height="{H}" fill="#F5F5F5"/>')
    parts.append(f'<text x="{W//2}" y="38" font-size="20" font-weight="bold" text-anchor="middle" fill="#1a1a1a">智能导医系统 — 功能模块划分图</text>')

    # 系统外框
    parts.append(f'<rect x="50" y="65" width="{W-100}" height="{H-150}" fill="none" stroke="#1890FF" stroke-width="3" rx="16"/>')
    parts.append(f'<rect x="120" y="55" width="220" height="28" fill="#1890FF" rx="6"/>')
    parts.append(f'<text x="230" y="74" font-size="14" font-weight="bold" text-anchor="middle" fill="white">智能导医系统</text>')

    # 模块：(name, x, y, w, h, bg, border)
    # 分两排
    row1 = [
        ("语音输入模块", 120, 120, 190, 68, "#E8F4FD", "#1890FF"),
        ("症状提取模块", 350, 120, 190, 68, "#E8F4FD", "#1890FF"),
        ("智能分诊模块", 580, 120, 190, 68, "#E8F4FD", "#1890FF"),
        ("楼层引导模块", 810, 120, 190, 68, "#E8F4FD", "#1890FF"),
    ]
    row2 = [
        ("历史记录模块", 120, 240, 190, 68, "#FFF3E0", "#FA8C16"),
        ("系统管理模块", 350, 240, 190, 68, "#FFF3E0", "#FA8C16"),
        ("专家系统推理机", 580, 240, 190, 68, "#E8F5E9", "#52C41A"),
        ("深度学习模型", 810, 240, 190, 68, "#E8F5E9", "#52C41A"),
    ]
    row3 = [
        ("SQLite数据库", 120, 370, 200, 68, "#FCE4EC", "#EB2F96"),
        ("症状知识库", 360, 370, 180, 68, "#FCE4EC", "#EB2F96"),
        ("规则库", 580, 370, 180, 68, "#FCE4EC", "#EB2F96"),
        ("科室楼层数据", 790, 370, 210, 68, "#FCE4EC", "#EB2F96"),
    ]
    row4 = [
        ("语音识别API", 250, 500, 210, 68, "#F9F0FF", "#722ED1"),
        ("GUI界面", 540, 500, 210, 68, "#F9F0FF", "#722ED1"),
    ]

    all_rows = row1 + row2 + row3 + row4
    positions = {}  # name -> (cx, cy)

    for (name, x, y, w, h, bg, border) in all_rows:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" rx="10" stroke="{border}" stroke-width="2"/>')
        lines = wrap_text(name, 10)
        for li, line in enumerate(lines):
            ly = y + h//2 + (li - len(lines)//2)*16 + 5
            parts.append(f'<text x="{x+w//2}" y="{ly}" font-size="12" font-weight="bold" text-anchor="middle" fill="#333">{line}</text>')
        positions[name] = (x + w//2, y + h//2)

    # 箭头
    arrows = [
        ("语音输入模块", "症状提取模块", "#1890FF"),
        ("症状提取模块", "智能分诊模块", "#1890FF"),
        ("智能分诊模块", "楼层引导模块", "#1890FF"),
        ("智能分诊模块", "专家系统推理机", "#52C41A"),
        ("专家系统推理机", "深度学习模型", "#52C41A"),
        ("智能分诊模块", "SQLite数据库", "#EB2F96"),
        ("专家系统推理机", "规则库", "#EB2F96"),
        ("楼层引导模块", "科室楼层数据", "#FA8C16"),
        ("智能分诊模块", "历史记录模块", "#FA8C16"),
        ("语音输入模块", "语音识别API", "#722ED1"),
        ("智能分诊模块", "GUI界面", "#722ED1"),
    ]
    for src, dst, color in arrows:
        if src in positions and dst in positions:
            x1, y1 = positions[src]
            x2, y2 = positions[dst]
            # 从src右边缘到dst左边缘
            src_mod = [m for m in all_rows if m[0] == src][0]
            dst_mod = [m for m in all_rows if m[0] == dst][0]
            sx = src_mod[1] + src_mod[3]  # 右边缘
            sy = y1
            dx = dst_mod[1]  # 左边缘
            dy = y2
            parts.append(f'<line x1="{sx}" y1="{sy}" x2="{dx}" y2="{dy}" stroke="{color}" stroke-width="2" marker-end="url(#modarr)"/>')

    parts.append(f'<text x="{W//2}" y="{H-18}" font-size="12" text-anchor="middle" fill="#888">图3：系统功能模块划分（展示各模块的职责与关联关系）</text>')
    parts.append('</svg>')

    path = os.path.join(OUTPUT_DIR, "fig3_modules.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"  图3已生成: {path}")
    return path


# ============================================================
# 图4：E-R 图
# ============================================================
def draw_fig4():
    W, H = 1200, 900
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append('<defs>')
    parts.append('<marker id="erarr" markerWidth="10" markerHeight="8" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker>')
    parts.append('<style>text{font-family:"Microsoft YaHei","SimHei",sans-serif;}</style>')
    parts.append('</defs>')
    parts.append(f'<rect width="{W}" height="{H}" fill="#F5F5F5"/>')
    parts.append(f'<text x="{W//2}" y="38" font-size="20" font-weight="bold" text-anchor="middle" fill="#1a1a1a">智能导医系统 — 数据库E-R图</text>')

    # 实体定义：(name, attrs, x, y, w, bg, hdr)
    entities = [
        ("SYMPTOM\n症状表",
         ["symptom_id  PK", "symptom_name", "category", "synonyms", "base_weight"],
         80, 130, 230, "#E8F4FD", "#1890FF"),
        ("DEPARTMENT\n科室表",
         ["dept_id  PK", "dept_name", "function_desc", "floor", "location_desc"],
         420, 130, 250, "#E8F5E9", "#52C41A"),
        ("RULE\n规则表",
         ["rule_id  PK", "symptom_id  FK", "dept_id  FK", "rule_weight", "conditions"],
         80, 450, 250, "#FFF3E0", "#FA8C16"),
        ("RECORD\n分诊记录表",
         ["record_id  PK", "create_time", "input_text", "recommended_dept  FK", "confidence"],
         440, 450, 280, "#FCE4EC", "#EB2F96"),
        ("FLOOR\n楼层表",
         ["floor_id  PK", "floor_number", "core_areas", "elevator_stairs", "guide_text"],
         780, 280, 260, "#F9F0FF", "#722ED1"),
    ]

    # 计算高度并画实体框
    ent_positions = {}  # name -> (cx, cy, y_bottom)
    for (name, attrs, x, y, w, bg, hdr) in entities:
        h = 42 + len(attrs) * 22 + 8
        # 更新y因为高度可能变化 — 实际上我们已经固定了y，所以这里用计算出的h
        # 重新给entities里的高
        idx = [i for i, e in enumerate(entities) if e[0] == name][0]
        entities[idx] = (name, attrs, x, y, w, bg, hdr, h)

    for (name, attrs, x, y, w, bg, hdr, h) in entities:
        # 外框
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" rx="4" stroke="#333" stroke-width="2"/>')
        # 表头
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="40" fill="{hdr}" rx="4"/>')
        parts.append(f'<rect x="{x}" y="{y}+36" width="{w}" height="4" fill="{hdr}"/>')
        # 实体名（分行）
        name_lines = name.split('\n')
        for ni, nline in enumerate(name_lines):
            parts.append(f'<text x="{x+w//2}" y="{y+20+ni*16}" font-size="12" font-weight="bold" text-anchor="middle" fill="white">{nline}</text>')
        # 属性
        for ai, attr in enumerate(attrs):
            ay = y + 46 + ai * 22
            if "PK" in attr:
                parts.append(f'<text x="{x+12}" y="{ay}" font-size="10" fill="#C41D1F">🔑 {attr}</text>')
            elif "FK" in attr:
                parts.append(f'<text x="{x+12}" y="{ay}" font-size="10" fill="#FA8C16">🔗 {attr}</text>')
            else:
                parts.append(f'<text x="{x+12}" y="{ay}" font-size="10" fill="#333">   {attr}</text>')
        # 记录位置（中心x, 中心y, 底部y）
        ent_positions[name.split('\n')[0]] = (x + w//2, y + h//2, y + h)

    # 画关系连线
    # SYMPTOM (1) --- (N) RULE
    s_ent = [e for e in entities if "SYMPTOM" in e[0]][0]
    r_ent = [e for e in entities if "RULE" in e[0]][0]
    s_cx = s_ent[2] + s_ent[4]//2
    s_by = s_ent[2] + s_ent[7]  # y + h
    r_cx = r_ent[2] + r_ent[4]//2
    r_y = r_ent[2]  # y
    parts.append(f'<line x1="{s_cx}" y1="{s_by}" x2="{r_cx}" y2="{r_y}" stroke="#333" stroke-width="2" marker-end="url(#erarr)"/>')
    parts.append(f'<text x="{(s_cx+r_cx)//2}" y="{(s_by+r_y)//2 - 8}" font-size="10" text-anchor="middle" fill="#333">1 : N</text>')
    parts.append(f'<text x="{(s_cx+r_cx)//2}" y="{(s_by+r_y)//2 + 6}" font-size="10" text-anchor="middle" fill="#333">SYMPTOM 拥有 RULE</text>')

    # DEPARTMENT (1) --- (N) RULE
    d_ent = [e for e in entities if "DEPARTMENT" in e[0]][0]
    d_cx = d_ent[2] + d_ent[4]//2
    d_by = d_ent[2] + d_ent[7]
    r_cx2 = r_ent[2] + r_ent[4]  # 右边缘
    parts.append(f'<line x1="{d_cx}" y1="{d_by}" x2="{r_cx2}" y2="{r_ent[2]}" stroke="#333" stroke-width="2" marker-end="url(#erarr)"/>')

    # RULE (N) --- (1) RECORD
    rec_ent = [e for e in entities if "RECORD" in e[0]][0]
    r_by2 = r_ent[2] + r_ent[7]
    rec_y2 = rec_ent[2]
    parts.append(f'<line x1="{r_cx}" y1="{r_by2}" x2="{rec_ent[2]}" y2="{rec_y2+60}" stroke="#333" stroke-width="2" marker-end="url(#erarr)"/>')

    # DEPARTMENT (1) --- (1) FLOOR
    f_ent = [e for e in entities if "FLOOR" in e[0]][0]
    d_cx2 = d_ent[2] + d_ent[4]
    d_cy2 = d_ent[2] + d_ent[7]//2
    f_cx2 = f_ent[2]
    f_cy2 = f_ent[2] + f_ent[7]//2
    parts.append(f'<line x1="{d_cx2}" y1="{d_cy2}" x2="{f_cx2}" y2="{f_cy2}" stroke="#333" stroke-width="2" stroke-dasharray="8,4" marker-end="url(#erarr)"/>')
    parts.append(f'<text x="{(d_cx2+f_cx2)//2}" y="{(d_cy2+f_cy2)//2 - 8}" font-size="10" text-anchor="middle" fill="#666">1 : 1</text>')
    parts.append(f'<text x="{(d_cx2+f_cx2)//2}" y="{(d_cy2+f_cy2)//2 + 6}" font-size="10" text-anchor="middle" fill="#666">位于</text>')

    # 关系说明框
    sx2, sy2 = 780, H - 170
    parts.append(f'<rect x="{sx2}" y="{sy2}" width="380" height="140" fill="white" rx="8" stroke="#ccc" stroke-width="1"/>')
    parts.append(f'<text x="{sx2+20}" y="{sy2+25}" font-size="13" font-weight="bold" fill="#333">关系说明：</text>')
    parts.append(f'<text x="{sx2+20}" y="{sy2+50}" font-size="11" fill="#333">🔑 PK 主键    🔗 FK 外键</text>')
    parts.append(f'<text x="{sx2+20}" y="{sy2+75}" font-size="11" fill="#333">SYMPTOM (1) ── (N) RULE</text>')
    parts.append(f'<text x="{sx2+20}" y = "{sy2+100}" font-size="11" fill="#333">DEPARTMENT (1) ── (N) RULE</text>')
    parts.append(f'<text x="{sx2+20}" y = "{sy2+125}" font-size="11" fill="#333">DEPARTMENT (1) ── (1) FLOOR</text>')

    parts.append(f'<text x="{W//2}" y="{H-18}" font-size="12" text-anchor="middle" fill="#888">图4：数据库E-R图（展示实体、属性及实体间的关联关系）</text>')
    parts.append('</svg>')

    path = os.path.join(OUTPUT_DIR, "fig4_er.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"  图4已生成: {path}")
    return path


if __name__ == "__main__":
    print("=" * 50)
    print("  开始绘制架构图...")
    print("=" * 50)
    f1 = draw_fig1_v2()
    f2 = draw_fig2()
    f3 = draw_fig3()
    f4 = draw_fig4()
    print("=" * 50)
    print(f"  全部4张图已生成至: {OUTPUT_DIR}")
    print("  SVG文件可直接在浏览器中打开查看。")
    print("=" * 50)
