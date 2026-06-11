# -*- coding: utf-8 -*-
"""
专家系统推理机模块（符号主义规则推理）
"""

from models.database import DatabaseManager
from models.rule import Rule
from models.department import Department
import logging

logger = logging.getLogger(__name__)


class ExpertSystem:
    """专家系统推理机（符号主义规则推理）"""

    def __init__(self, database: "DatabaseManager"):
        """
        初始化专家系统

        Args:
            database: DatabaseManager对象，用于加载规则库

        Raises:
            ValueError: 如果database为None
        """
        if database is None:
            raise ValueError("database cannot be None")
        self.database = database
        self.rules = []
        self.departments = {}

    def load_rules(self) -> bool:
        """
        从数据库加载所有规则

        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            rules_data = self.database.execute_query(
                "SELECT * FROM rules ORDER BY rule_id"
            )
            self.rules = [Rule.from_dict(r) for r in rules_data]

            dept_data = self.database.execute_query(
                "SELECT * FROM departments ORDER BY dept_id"
            )
            self.departments = {d["dept_id"]: Department.from_dict(d) for d in dept_data}

            logger.info("专家系统规则加载完成，共 %d 条规则", len(self.rules))
            return True
        except Exception as e:
            logger.error("规则加载失败: %s", e)
            return False

    def diagnose(self, symptoms: list) -> dict:
        """
        基于症状列表进行智能分诊（增强版：支持组合规则+严重度+共识加权）

        Args:
            symptoms: 症状列表，格式为 [{"name": str, "confidence": float}]

        Returns:
            dict: {
                "success": True,
                "data": {
                    "primary": {"dept_id": int, "dept_name": str, "confidence": float, "reason": str, "severity": str},
                    "alternatives": [...],
                    "matched_rules": [...],
                    "symptom_summary": {...}
                },
                "message": str
            }
        """
        if not symptoms:
            return {"success": False, "data": None, "message": "未提供症状列表"}

        if not self.rules:
            if not self.load_rules():
                return {"success": False, "data": None, "message": "规则库加载失败"}

        symptom_map = self._get_symptom_name_to_id()

        # 构建本次输入的症状ID集合
        matched_symptom_ids = set()
        symptom_confidences = {}  # symptom_id → confidence
        for s in symptoms:
            sid = symptom_map.get(s.get("name", ""))
            if sid is not None:
                matched_symptom_ids.add(sid)
                symptom_confidences[sid] = max(
                    symptom_confidences.get(sid, 0),
                    s.get("confidence", 1.0)
                )

        if not matched_symptom_ids:
            return {"success": False, "data": None, "message": "症状与规则库不匹配"}

        dept_scores = {}
        matched_rules = []
        matched_critical = []  # 严重规则命中
        exclusion_depts = set()  # 排除科室

        for rule in self.rules:
            if not rule.is_active:
                continue

            # ---- 处理排除规则 ----
            if rule.rule_type == "exclusion":
                if rule.symptom_id in matched_symptom_ids:
                    exclusion_depts.add(rule.dept_id)
                    matched_rules.append({
                        "symptom": self._get_symptom_name(rule.symptom_id),
                        "dept_id": rule.dept_id,
                        "dept_name": self._get_dept_name(rule.dept_id),
                        "confidence": 0.0,
                        "condition": rule.conditions,
                        "rule_type": "exclusion"
                    })
                continue

            # ---- 单症状规则匹配 ----
            if rule.rule_type == "single":
                if rule.symptom_id in matched_symptom_ids:
                    self._apply_rule(rule, matched_symptom_ids, symptom_confidences,
                                     dept_scores, matched_rules)

                    if rule.is_critical():
                        matched_critical.append(rule)

            # ---- 组合规则匹配 ----
            elif rule.rule_type == "compound":
                required_ids = set(rule.extra_symptom_ids) | {rule.symptom_id}
                if required_ids.issubset(matched_symptom_ids):
                    # 所有必要症状都命中，组合规则触发
                    self._apply_compound_rule(rule, matched_symptom_ids,
                                              symptom_confidences, dept_scores,
                                              matched_rules)
                    if rule.is_critical():
                        matched_critical.append(rule)

        if not dept_scores:
            return {
                "success": False,
                "data": None,
                "message": "未匹配到任何分诊规则，请补充更多症状描述"
            }

        # ---- 严重度升级逻辑 ----
        severity_label = "normal"
        if matched_critical:
            severity_label = "critical"
            # 严重规则的科室额外加分
            critical_dept_ids = {r.dept_id for r in matched_critical}
            for dept_id in critical_dept_ids:
                if dept_id in dept_scores:
                    dept_scores[dept_id]["total_score"] *= 1.2
                    dept_scores[dept_id]["reasons"].append(
                        "[紧急] 症状匹配严重度规则"
                    )

        # ---- 排除规则过滤 ----
        for eid in exclusion_depts:
            if eid in dept_scores:
                del dept_scores[eid]

        if not dept_scores:
            return {
                "success": False,
                "data": None,
                "message": "所有候选科室被排除规则过滤，请重新描述"
            }

        # ---- 综合评分计算 ----
        results = []
        for dept_id, score_info in dept_scores.items():
            rule_count = score_info["rule_count"]
            total_score = score_info["total_score"]

            # 多规则命中微幅加分（共识效应）
            combo_bonus = 1.0 + 0.02 * max(rule_count - 1, 0)
            # 症状数量稀释惩罚（输入症状越多，科室匹配特异性越低）
            dilution = 1.0 / (1.0 + 0.18 * max(len(symptoms) - 1, 0))
            # 规则竞争惩罚：多科室竞争时，置信度自然下降
            competition = 1.0 / max(1, len(dept_scores) ** 0.4)
            # 综合置信度
            normalized = total_score / max(rule_count, 1)
            final_confidence = normalized * combo_bonus * dilution * competition
            # 软上限：超过90%需要极强证据
            if final_confidence > 0.90:
                final_confidence = 0.90 + (final_confidence - 0.90) * 0.15
            final_confidence = min(final_confidence, 0.95)

            dept_name = self._get_dept_name(dept_id)

            results.append({
                "dept_id": dept_id,
                "dept_name": dept_name,
                "confidence": round(final_confidence, 4),
                "reasons": score_info["reasons"],
                "rule_count": rule_count,
                "total_score": round(total_score, 4),
            })

        results.sort(key=lambda x: x["confidence"], reverse=True)

        # ---- 删除重复原因并格式化 ----
        primary = results[0]
        alternatives = results[1:4]

        primary_reasons = list(dict.fromkeys(primary["reasons"]))  # 去重保序

        return {
            "success": True,
            "data": {
                "primary": {
                    "dept_id": primary["dept_id"],
                    "dept_name": primary["dept_name"],
                    "confidence": primary["confidence"],
                    "reason": "；".join(primary_reasons),
                    "severity": severity_label
                },
                "alternatives": [
                    {
                        "dept_id": alt["dept_id"],
                        "dept_name": alt["dept_name"],
                        "confidence": alt["confidence"]
                    } for alt in alternatives
                ],
                "matched_rules": matched_rules,
                "symptom_summary": {
                    "total_symptoms": len(symptoms),
                    "matched_count": len(matched_symptom_ids),
                    "severity": severity_label,
                    "has_critical_rules": len(matched_critical) > 0
                }
            },
            "message": "分诊完成"
        }

    # ---- 辅助方法 ----

    def _apply_rule(self, rule, matched_ids, confidences, dept_scores, matched_rules):
        """应用单条规则并更新分数"""
        symptom_confidence = min(confidences.get(rule.symptom_id, 1.0), 1.0)
        severity_mul = rule.get_severity_multiplier()
        rule_confidence = round(min(symptom_confidence * rule.rule_weight * severity_mul, 0.92), 4)

        dept_id = rule.dept_id
        if dept_id not in dept_scores:
            dept_scores[dept_id] = {"total_score": 0.0, "rule_count": 0, "reasons": []}

        dept_scores[dept_id]["total_score"] += rule_confidence
        dept_scores[dept_id]["rule_count"] += 1
        dept_scores[dept_id]["reasons"].append(
            f"{rule.conditions} [权重:{rule.rule_weight}]"
        )

        matched_rules.append({
            "symptom": self._get_symptom_name(rule.symptom_id),
            "dept_id": dept_id,
            "dept_name": self._get_dept_name(dept_id),
            "confidence": rule_confidence,
            "condition": rule.conditions,
            "rule_type": rule.rule_type,
            "severity": rule.severity
        })

    def _apply_compound_rule(self, rule, matched_ids, confidences, dept_scores, matched_rules):
        """应用组合规则：所有额外症状命中时额外加分"""
        all_ids = [rule.symptom_id] + rule.extra_symptom_ids
        avg_confidence = sum(confidences.get(sid, 0.8) for sid in all_ids) / len(all_ids)
        severity_mul = rule.get_severity_multiplier()
        # 组合规则额外加权1.2
        compound_boost = 1.2
        rule_confidence = round(avg_confidence * rule.rule_weight * severity_mul * compound_boost, 4)

        dept_id = rule.dept_id
        if dept_id not in dept_scores:
            dept_scores[dept_id] = {"total_score": 0.0, "rule_count": 0, "reasons": []}

        dept_scores[dept_id]["total_score"] += rule_confidence
        dept_scores[dept_id]["rule_count"] += 1

        symptom_names = [self._get_symptom_name(sid) for sid in all_ids]
        dept_scores[dept_id]["reasons"].append(
            f"组合规则: {'+'.join(symptom_names)} → {rule.conditions}"
        )

        matched_rules.append({
            "symptom": "+".join(symptom_names),
            "dept_id": dept_id,
            "dept_name": self._get_dept_name(dept_id),
            "confidence": rule_confidence,
            "condition": rule.conditions,
            "rule_type": "compound",
            "severity": rule.severity
        })

    def calculate_confidence(self, symptom_confidence: float, rule_weight: float) -> float:
        """计算单条规则的置信度"""
        return round(symptom_confidence * rule_weight, 4)

    def _resolve_conflicts(self, results: list) -> dict:
        """解决多科室冲突（加权投票机制）"""
        if not results:
            return {"primary": None, "alternatives": []}
        results.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        primary = results[0]
        alternatives = []
        for r in results[1:]:
            if (primary["confidence"] - r["confidence"]) < 0.15:
                alternatives.append(r)
        return {"primary": primary, "alternatives": alternatives[:2]}

    def _get_symptom_name_to_id(self) -> dict:
        """获取症状名称→ID映射"""
        try:
            symptoms = self.database.execute_query(
                "SELECT symptom_id, symptom_name FROM symptoms"
            )
            return {s["symptom_name"]: s["symptom_id"] for s in symptoms}
        except Exception:
            return {}

    def _get_symptom_name(self, symptom_id: int) -> str:
        """根据ID获取症状名称"""
        for s_name, s_id in self._get_symptom_name_to_id().items():
            if s_id == symptom_id:
                return s_name
        return f"症状#{symptom_id}"

    def _get_dept_name(self, dept_id: int) -> str:
        """根据ID获取科室名称"""
        dept = self.departments.get(dept_id)
        return dept.dept_name if dept else f"科室#{dept_id}"
