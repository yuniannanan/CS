# -*- coding: utf-8 -*-
"""
症状提取引擎模块
"""

import jieba
import re
from models.database import DatabaseManager
from models.symptom import Symptom
import logging

logger = logging.getLogger(__name__)


class SymptomExtractor:
    """症状提取引擎"""

    def __init__(self, database: "DatabaseManager"):
        """
        初始化症状提取器

        Args:
            database: DatabaseManager对象，用于加载症状库
        """
        self.database = database
        self.symptom_library = []
        self._init_jieba()

    def _init_jieba(self):
        """初始化jieba分词器，添加症状词到词典"""
        try:
            symptoms = self.database.execute_query(
                "SELECT symptom_name FROM symptoms"
            )
            for s in symptoms:
                jieba.add_word(s["symptom_name"])
        except Exception as e:
            logger.warning("初始化jieba词典失败: %s", e)

    def load_symptom_library(self) -> bool:
        """
        从数据库加载症状库

        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            data = self.database.execute_query(
                "SELECT * FROM symptoms ORDER BY symptom_id"
            )
            self.symptom_library = [Symptom.from_dict(d) for d in data]
            logger.info("症状库加载完成，共 %d 条症状", len(self.symptom_library))
            return True
        except Exception as e:
            logger.error("症状库加载失败: %s", e)
            return False

    def extract_symptoms(self, text: str) -> dict:
        """
        从文本中提取症状关键词

        Args:
            text: 用户输入的自然语言文本

        Returns:
            {
                "success": True,
                "data": {
                    "symptoms": [
                        {"name": str, "type": str, "confidence": float}
                    ],
                    "need_clarify": bool,
                    "clarify_question": str
                },
                "message": str
            }
        """
        if not text or not text.strip():
            return {
                "success": False,
                "data": None,
                "message": "输入文本为空"
            }

        if not self.symptom_library:
            if not self.load_symptom_library():
                return {
                    "success": False,
                    "data": None,
                    "message": "症状库加载失败"
                }

        # 分词
        words = list(jieba.cut(text))
        logger.debug("分词结果: %s", words)

        matched = []
        matched_names = set()

        # 1. 精确匹配（症状名称）
        for word in words:
            for symptom in self.symptom_library:
                if word == symptom.symptom_name:
                    if symptom.symptom_name not in matched_names:
                        matched.append({
                            "name": symptom.symptom_name,
                            "type": "exact",
                            "confidence": symptom.base_weight
                        })
                        matched_names.add(symptom.symptom_name)

        # 2. 同义词匹配
        for word in words:
            for symptom in self.symptom_library:
                if symptom.symptom_name in matched_names:
                    continue
                synonyms = symptom.synonym_list
                if word in synonyms:
                    if symptom.symptom_name not in matched_names:
                        matched.append({
                            "name": symptom.symptom_name,
                            "type": "synonym",
                            "confidence": symptom.base_weight * 0.9
                        })
                        matched_names.add(symptom.symptom_name)

        # 3. 模糊匹配（编辑距离）
        for word in words:
            if len(word) < 2:
                continue
            fuzzy_results = self.fuzzy_match(word, threshold=0.7)
            for result in fuzzy_results:
                symptom_name = result["symptom_name"]
                if symptom_name not in matched_names:
                    matched.append({
                        "name": symptom_name,
                        "type": "fuzzy",
                        "confidence": result["confidence"]
                    })
                    matched_names.add(symptom_name)

        if not matched:
            return {
                "success": False,
                "data": None,
                "message": "未识别到有效症状，请详细描述您的不适"
            }

        # 过滤低置信度症状
        matched = [m for m in matched if m["confidence"] >= 0.5]

        if not matched:
            return {
                "success": False,
                "data": None,
                "message": "症状置信度过低，请更清晰地描述症状"
            }

        # 按置信度降序排列
        matched.sort(key=lambda x: x["confidence"], reverse=True)

        # 判断是否需要追问
        need_clarify = len(matched) == 1 and matched[0]["confidence"] < 0.8
        clarify_question = ""
        if need_clarify:
            clarify_question = "您是否有「{}」以外的其他症状？请补充描述以便更准确分诊。".format(matched[0]["name"])

        return {
            "success": True,
            "data": {
                "symptoms": matched,
                "need_clarify": need_clarify,
                "clarify_question": clarify_question
            },
            "message": "成功识别 {} 个症状".format(len(matched))
        }

    def fuzzy_match(self, word: str, threshold: float = 0.8) -> list:
        """
        模糊匹配症状库

        Args:
            word: 待匹配词
            threshold: 相似度阈值

        Returns:
            list: 匹配到的症状列表 [{"symptom_name": str, "confidence": float}]
        """
        results = []
        for symptom in self.symptom_library:
            # 计算编辑距离相似度
            name = symptom.symptom_name
            distance = self._edit_distance(word, name)
            max_len = max(len(word), len(name))
            if max_len == 0:
                continue
            similarity = 1.0 - distance / max_len

            if similarity >= threshold:
                results.append({
                    "symptom_name": name,
                    "confidence": round(symptom.base_weight * similarity, 4)
                })

            # 同时检查同义词
            synonyms = symptom.synonym_list
            for syn in synonyms:
                distance = self._edit_distance(word, syn)
                max_len = max(len(word), len(syn))
                if max_len == 0:
                    continue
                similarity = 1.0 - distance / max_len
                if similarity >= threshold and symptom.symptom_name not in [r["symptom_name"] for r in results]:
                    results.append({
                        "symptom_name": symptom.symptom_name,
                        "confidence": round(symptom.base_weight * similarity * 0.9, 4)
                    })

        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results[:3]  # 最多返回3个匹配结果

    def _edit_distance(self, s1: str, s2: str) -> int:
        """
        计算两个字符串的编辑距离

        Args:
            s1: 字符串1
            s2: 字符串2

        Returns:
            int: 编辑距离
        """
        len1, len2 = len(s1), len(s2)
        if len1 == 0:
            return len2
        if len2 == 0:
            return len1

        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

        return dp[len1][len2]

    def calculate_confidence(self, match_type: str) -> float:
        """
        根据匹配类型计算置信度

        Args:
            match_type: 匹配类型 ("exact", "synonym", "fuzzy")

        Returns:
            float: 置信度 (0.0 ~ 1.0)
        """
        confidence_map = {
            "exact": 1.0,
            "synonym": 0.9,
            "fuzzy": 0.7
        }
        return confidence_map.get(match_type, 0.5)
