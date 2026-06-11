# -*- coding: utf-8 -*-
"""
规则数据模型模块
"""

import json
from typing import Dict, Optional, List
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Severity(Enum):
    """严重度等级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RuleType(Enum):
    """规则类型枚举"""
    SINGLE = "single"
    COMPOUND = "compound"
    EXCLUSION = "exclusion"


class Rule:
    """分诊规则数据模型（符号主义IF-THEN规则）"""

    def __init__(
        self,
        rule_id: Optional[int] = None,
        symptom_id: int = 0,
        dept_id: int = 0,
        rule_weight: float = 1.0,
        conditions: str = "",
        severity: str = "medium",
        rule_type: str = "single",
        extra_symptom_ids: str = "[]",
        conditions_detail: str = "",
        is_active: int = 1,
    ) -> None:
        """
        初始化规则对象

        Args:
            rule_id: 规则唯一标识
            symptom_id: 主触发症状ID
            dept_id: 推荐科室ID
            rule_weight: 规则权重 (0.0 ~ 2.0)
            conditions: IF条件描述文本
            severity: 严重度 (low/medium/high/critical)
            rule_type: 规则类型 (single/compound/exclusion)
            extra_symptom_ids: 附加症状ID列表JSON
            conditions_detail: 详细触发条件说明
            is_active: 是否启用 (0/1)
        """
        self.rule_id = rule_id
        self.symptom_id = symptom_id
        self.dept_id = dept_id
        self.rule_weight = max(0.1, min(2.0, rule_weight))
        self.conditions = conditions
        self.severity = severity
        self.rule_type = rule_type
        self.conditions_detail = conditions_detail
        self.is_active = bool(is_active)

        # 解析额外症状ID
        try:
            self.extra_symptom_ids = (
                json.loads(extra_symptom_ids)
                if isinstance(extra_symptom_ids, str)
                else extra_symptom_ids
            )
        except (json.JSONDecodeError, TypeError):
            self.extra_symptom_ids = []

        logger.debug("Rule created: symptom_id=%d, dept_id=%d, type=%s, severity=%s",
                     symptom_id, dept_id, rule_type, severity)

    @classmethod
    def from_dict(cls, data: Dict) -> "Rule":
        """
        从字典创建Rule实例

        Args:
            data: 包含规则数据的字典

        Returns:
            Rule实例
        """
        return cls(
            rule_id=data.get("rule_id"),
            symptom_id=data.get("symptom_id", 0),
            dept_id=data.get("dept_id", 0),
            rule_weight=data.get("rule_weight", 1.0),
            conditions=data.get("conditions", ""),
            severity=data.get("severity", "medium"),
            rule_type=data.get("rule_type", "single"),
            extra_symptom_ids=data.get("extra_symptom_ids", "[]"),
            conditions_detail=data.get("conditions_detail", ""),
            is_active=data.get("is_active", 1),
        )

    def to_dict(self) -> Dict:
        """
        将Rule实例转换为字典

        Returns:
            规则数据字典
        """
        return {
            "rule_id": self.rule_id,
            "symptom_id": self.symptom_id,
            "dept_id": self.dept_id,
            "rule_weight": self.rule_weight,
            "conditions": self.conditions,
            "severity": self.severity,
            "rule_type": self.rule_type,
            "extra_symptom_ids": (
                json.dumps(self.extra_symptom_ids, ensure_ascii=False)
                if isinstance(self.extra_symptom_ids, list)
                else self.extra_symptom_ids
            ),
            "conditions_detail": self.conditions_detail,
            "is_active": 1 if self.is_active else 0,
        }

    def is_compound(self) -> bool:
        """是否为组合规则"""
        return self.rule_type == "compound" and len(self.extra_symptom_ids) > 0

    def is_critical(self) -> bool:
        """是否为严重级别"""
        return self.severity in ("critical", "high")

    def get_severity_multiplier(self) -> float:
        """获取严重度加权系数"""
        multipliers = {
            "low": 0.75,
            "medium": 0.90,
            "high": 1.10,
            "critical": 1.25,
        }
        return multipliers.get(self.severity, 1.0)

    def validate(self) -> tuple:
        """
        验证规则数据合法性

        Returns:
            (is_valid, error_message)
        """
        if self.symptom_id <= 0:
            return False, "症状ID必须大于0"
        if self.dept_id <= 0:
            return False, "科室ID必须大于0"
        if self.rule_weight <= 0:
            return False, "规则权重必须大于0"
        if self.severity not in ("low", "medium", "high", "critical"):
            return False, "严重度无效"
        if self.rule_type not in ("single", "compound", "exclusion"):
            return False, "规则类型无效"
        return True, ""

    def __repr__(self) -> str:
        return (
            f"Rule(id={self.rule_id}, "
            f"type={self.rule_type}, "
            f"severity={self.severity}, "
            f"dept_id={self.dept_id}, "
            f"weight={self.rule_weight})"
        )
