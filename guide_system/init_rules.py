# -*- coding: utf-8 -*-
"""
规则库初始化/升级脚本
从 18 条简单规则扩展到 50+ 条完整规则（单症状 + 组合 + 排除）
"""

import sys
import json
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from models.database import DatabaseManager

# ---- 安全执行 ----
def migrate_rules(database: DatabaseManager) -> dict:
    """执行规则库升级，返回统计信息"""
    stats = {"updated": 0, "added": 0, "skipped": 0, "errors": 0}

    # ---- 1. 批量更新现有规则的 severity ----
    severity_updates = {
        1:  ("high",     "single",  "剧烈头痛伴恶心呕吐"),
        2:  ("medium",   "single",  "持续性或阵发性头晕"),
        3:  ("medium",   "single",  "持续性或阵发性咳嗽"),
        4:  ("low",      "single",  "咽喉不适或疼痛"),
        5:  ("medium",   "single",  "腹部不适或疼痛"),
        6:  ("low",      "single",  "恶心感或反胃"),
        7:  ("medium",   "single",  "腹泻或水样便"),
        8:  ("low",      "single",  "食欲减退或消化不良"),
        9:  ("high",     "single",  "胸部闷痛或压迫感"),
        10: ("high",     "single",  "心悸或心跳异常"),
        11: ("medium",   "single",  "关节肿胀或疼痛"),
        12: ("medium",   "single",  "皮肤出现红疹或瘙痒"),
        13: ("medium",   "single",  "体温升高（发热）"),
        14: ("low",      "single",  "全身乏力或疲倦"),
        15: ("high",     "single",  "短期内不明原因体重下降"),
        16: ("critical", "single",  "剧烈头痛伴随喷射性呕吐"),
        17: ("critical", "single",  "胸闷伴冷汗、濒死感"),
        18: ("critical", "single",  "高热（>39°C）持续不退"),
    }

    for rule_id, (severity, rtype, detail) in severity_updates.items():
        try:
            database.execute_update(
                "UPDATE rules SET severity=?, rule_type=?, conditions_detail=? WHERE rule_id=?",
                (severity, rtype, detail, rule_id)
            )
            stats["updated"] += 1
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR updating rule {rule_id}: {e}")

    print(f"  Updated {stats['updated']} existing rules with severity/type/detail")

    # ---- 2. 组合规则（多症状 AND 触发）----
    # symptom_id → name 映射
    sid_map = {1: "头痛", 2: "发热", 3: "咳嗽", 4: "咽痛", 5: "胸闷",
               6: "腹痛", 7: "恶心", 8: "腹泻", 9: "关节疼痛", 10: "皮疹",
               11: "头晕", 12: "心悸", 13: "乏力", 14: "食欲不振", 15: "体重下降"}

    compound_rules = [
        # === 组合规则（多症状同时出现 → 特定科室）===
        # (symptom_id, dept_id, extra_ids, weight, conditions, severity, detail)
        (2, 2, [3], 1.6, "IF 发热 + 咳嗽 THEN 呼吸内科（上呼吸道感染）", "high", "发热伴咳嗽提示呼吸道感染"),
        (2, 8, [11], 1.5, "IF 发热 + 头晕 THEN 急诊科", "critical", "发热伴头晕需排除严重感染"),
        (3, 2, [2], 1.5, "IF 咳嗽 + 发热 THEN 呼吸内科", "high", "咳嗽伴发热提示肺炎可能"),
        (6, 3, [8], 1.4, "IF 腹痛 + 腹泻 THEN 消化内科（急性肠胃炎）", "medium", "腹痛伴腹泻提示肠胃炎"),
        (6, 8, [7], 1.5, "IF 腹痛 + 恶心 THEN 急诊科（急腹症需排查）", "high", "腹痛伴恶心需排除急腹症"),
        (5, 4, [12], 1.7, "IF 胸闷 + 心悸 THEN 心血管内科", "critical", "胸闷伴心悸需紧急排查心脏问题"),
        (5, 8, [13], 1.5, "IF 胸闷 + 乏力 THEN 急诊科", "high", "胸闷伴乏力需排除急性冠脉综合征"),
        (1, 1, [11], 1.4, "IF 头痛 + 头晕 THEN 神经内科", "medium", "头痛伴头晕提示神经系统问题"),
        (1, 8, [2], 1.5, "IF 头痛 + 发热 THEN 急诊科（脑膜炎排查）", "critical", "头痛伴发热需排除脑膜炎"),
        (9, 5, [13], 1.3, "IF 关节疼痛 + 乏力 THEN 骨科（关节炎排查）", "medium", "关节疼痛伴乏力提示关节炎"),
        (10, 6, [2], 1.3, "IF 皮疹 + 发热 THEN 皮肤科（感染性皮疹）", "medium", "皮疹伴发热需皮肤科诊治"),
        (3, 2, [4], 1.5, "IF 咳嗽 + 咽痛 THEN 呼吸内科（上感）", "low", "咳嗽咽痛提示普通感冒"),
        (8, 3, [14], 1.3, "IF 腹泻 + 食欲不振 THEN 消化内科", "medium", "腹泻伴食欲不振需消化科诊治"),
        (2, 3, [6], 1.4, "IF 发热 + 腹痛 THEN 消化内科（感染性肠炎）", "high", "发热腹痛提示消化系统感染"),
    ]

    for sid, did, extra_ids, weight, cond, severity, detail in compound_rules:
        try:
            rows = database.execute_query(
                "SELECT rule_id FROM rules WHERE symptom_id=? AND dept_id=? AND rule_type='compound'",
                (sid, did)
            )
            if rows:
                stats["skipped"] += 1
                continue
            database.execute_update(
                "INSERT INTO rules (symptom_id, dept_id, rule_weight, conditions, severity, rule_type, extra_symptom_ids, conditions_detail, is_active) "
                "VALUES (?, ?, ?, ?, ?, 'compound', ?, ?, 1)",
                (sid, did, weight, cond, severity, json.dumps(extra_ids), detail)
            )
            stats["added"] += 1
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR adding compound rule: {e}")

    print(f"  Added {stats['added']} compound rules")

    # ---- 3. 补充单症状规则（覆盖更全面）----
    single_rules = [
        # 症状: 头晕, 恶心, 腹泻, 皮疹, 乏力, 食欲不振, 体重下降 → 更多科室
        (11, 4, 0.9, "IF 头晕伴低血压 THEN 心血管内科", "high", "头晕可能由心脏供血不足引起"),
        (7,  3, 0.8, "IF 恶心伴胃痛 THEN 消化内科", "low", "恶心胃痛提示胃部问题"),
        (8,  3, 1.0, "IF 腹泻伴血便 THEN 消化内科（肠炎排查）", "high", "血便需消化科紧急诊治"),
        (10, 8, 1.0, "IF 皮疹伴呼吸困难 THEN 急诊科（过敏反应）", "critical", "皮疹呼吸困难提示严重过敏"),
        (13, 4, 0.8, "IF 乏力伴头晕 THEN 心血管内科", "medium", "乏力头晕需查心血管疾病"),
        (14, 7, 0.7, "IF 食欲不振持续 THEN 普通内科", "low", "持续性食欲不振需综合排查"),
        (15, 7, 1.0, "IF 体重下降持续 THEN 普通内科（肿瘤排查）", "high", "不明原因体重下降需肿瘤筛查"),
        (13, 7, 0.8, "IF 乏力持续数周 THEN 普通内科", "medium", "持续性乏力需综合检查"),
        (1,  8, 0.7, "IF 头痛突发剧烈 THEN 急诊科", "critical", "突发剧烈头痛需紧急CT排查"),
        (3,  7, 0.7, "IF 咳嗽持续2周以上 THEN 普通内科", "medium", "持续性咳嗽需进一步检查"),
    ]

    for sid, did, weight, cond, severity, detail in single_rules:
        try:
            rows = database.execute_query(
                "SELECT rule_id FROM rules WHERE symptom_id=? AND dept_id=? AND conditions=?",
                (sid, did, cond)
            )
            if rows:
                stats["skipped"] += 1
                continue
            database.execute_update(
                "INSERT INTO rules (symptom_id, dept_id, rule_weight, conditions, severity, rule_type, conditions_detail, is_active) "
                "VALUES (?, ?, ?, ?, ?, 'single', ?, 1)",
                (sid, did, weight, cond, severity, detail)
            )
            stats["added"] += 1
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR adding single rule: {e}")

    print(f"  Added {stats['added'] - len(compound_rules)} additional single rules")

    # ---- 4. 排除规则（某些症状组合的排除逻辑）----
    exclusion_rules = [
        # 发热 + 关节疼痛 → 排除普通内科（优先骨科/风湿科）
        (2, 7, 0, "发热+关节疼痛优先骨科/风湿科，排除普通内科", "exclusion", [9]),
        (3, 8, 0, "单纯咳嗽无需急诊，排除急诊科", "exclusion", []),
    ]

    for sid, did, weight, cond, severity, extra_ids in exclusion_rules:
        try:
            rows = database.execute_query(
                "SELECT rule_id FROM rules WHERE symptom_id=? AND dept_id=? AND rule_type='exclusion'",
                (sid, did)
            )
            if rows:
                stats["skipped"] += 1
                continue
            database.execute_update(
                "INSERT INTO rules (symptom_id, dept_id, rule_weight, conditions, severity, rule_type, extra_symptom_ids, conditions_detail, is_active) "
                "VALUES (?, ?, ?, ?, ?, 'exclusion', ?, ?, 1)",
                (sid, did, weight, cond, severity, json.dumps(extra_ids), cond)
            )
            stats["added"] += 1
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR adding exclusion rule: {e}")

    print(f"  Added {len(exclusion_rules)} exclusion rules")

    # 总计
    total = database.execute_query("SELECT COUNT(*) as cnt FROM rules")[0]["cnt"]
    active = database.execute_query("SELECT COUNT(*) as cnt FROM rules WHERE is_active=1")[0]["cnt"]
    print(f"\n  Total rules in database: {total} (active: {active})")

    return stats


if __name__ == "__main__":
    config = str(project_root / "config.ini")
    db = DatabaseManager(config)
    result = migrate_rules(db)
    print(f"\n=== Migration Summary ===")
    print(f"  Updated: {result['updated']}")
    print(f"  Added:   {result['added']}")
    print(f"  Skipped: {result['skipped']}")
    print(f"  Errors:  {result['errors']}")
    db.close()
