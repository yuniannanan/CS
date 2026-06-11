# -*- coding: utf-8 -*-
"""
深度学习文本分类器模块（辅助症状识别）
"""

import jieba
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Classifier:
    """深度学习文本分类器（辅助症状识别）"""

    def __init__(self):
        """初始化分类器"""
        self.vectorizer = None
        self.model = None
        self.label_map = {}
        self.id_to_label = {}
        logger.info("分类器初始化完成")

    def train(self, X: list, y: list) -> bool:
        """
        训练文本分类器

        Args:
            X: 文本列表，格式为 ["症状描述1", "症状描述2", ...]
            y: 标签列表，格式为 ["发烧", "咳嗽", ...]

        Returns:
            bool: 训练成功返回True，否则返回False
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.naive_bayes import MultinomialNB

            # 构建标签映射
            unique_labels = list(set(y))
            self.label_map = {label: idx for idx, label in enumerate(unique_labels)}
            self.id_to_label = {idx: label for label, idx in self.label_map.items()}

            # 文本向量化（TF-IDF）
            self.vectorizer = TfidfVectorizer(
                tokenizer=lambda x: list(jieba.cut(x)),
                lowercase=False
            )
            X_vec = self.vectorizer.fit_transform(X)

            # 训练朴素贝叶斯分类器
            y_encoded = [self.label_map[label] for label in y]
            self.model = MultinomialNB()
            self.model.fit(X_vec, y_encoded)

            logger.info("分类器训练完成，共 %d 个类别", len(unique_labels))
            return True
        except ImportError:
            logger.warning("scikit-learn 未安装，分类器不可用")
            return False
        except Exception as e:
            logger.error("分类器训练失败: %s", e)
            return False

    def predict(self, text: str) -> dict:
        """
        预测文本所属的症状类别

        Args:
            text: 输入文本

        Returns:
            dict: {
                "success": True,
                "data": {
                    "symptom": str,
                    "confidence": float,
                    "top3": [{"symptom": str, "confidence": float}]
                },
                "message": str
            }
        """
        if self.model is None or self.vectorizer is None:
            return {
                "success": False,
                "data": None,
                "message": "分类器未训练，请先调用 train()"
            }

        try:
            # 向量化
            text_vec = self.vectorizer.transform([text])

            # 预测概率
            probabilities = self.model.predict_proba(text_vec)[0]
            top_indices = np.argsort(probabilities)[::-1][:3]

            top3 = []
            for idx in top_indices:
                label = self.id_to_label.get(idx, "未知")
                conf = float(probabilities[idx])
                top3.append({"symptom": label, "confidence": round(conf, 4)})

            best_idx = top_indices[0]
            best_symptom = self.id_to_label.get(best_idx, "未知")
            best_confidence = float(probabilities[best_idx])

            return {
                "success": True,
                "data": {
                    "symptom": best_symptom,
                    "confidence": round(best_confidence, 4),
                    "top3": top3
                },
                "message": "预测完成"
            }
        except Exception as e:
            logger.error("预测失败: %s", e)
            return {
                "success": False,
                "data": None,
                "message": "预测失败: {}".format(e)
            }

    def load_model(self, path: str) -> bool:
        """
        加载预训练模型

        Args:
            path: 模型文件路径

        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            import pickle
            with open(path, "rb") as f:
                saved = pickle.load(f)
                self.vectorizer = saved["vectorizer"]
                self.model = saved["model"]
                self.label_map = saved["label_map"]
                self.id_to_label = saved["id_to_label"]
            logger.info("模型加载成功: %s", path)
            return True
        except Exception as e:
            logger.error("模型加载失败: %s", e)
            return False

    def save_model(self, path: str) -> bool:
        """
        保存训练好的模型

        Args:
            path: 模型保存路径

        Returns:
            bool: 保存成功返回True，否则返回False
        """
        try:
            import pickle
            with open(path, "wb") as f:
                pickle.dump({
                    "vectorizer": self.vectorizer,
                    "model": self.model,
                    "label_map": self.label_map,
                    "id_to_label": self.id_to_label
                }, f)
            logger.info("模型保存成功: %s", path)
            return True
        except Exception as e:
            logger.error("模型保存失败: %s", e)
            return False
