# -*- coding: utf-8 -*-
"""
结果展示面板模块
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QScrollArea,
                             QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette
import logging

logger = logging.getLogger(__name__)


class ResultPanel(QWidget):
    """结果展示面板（分诊建议 + 置信度）"""

    def __init__(self, main_window):
        """
        初始化结果面板

        Args:
            main_window: 主窗口引用
        """
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        """初始化UI界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 30)
        main_layout.setSpacing(20)

        # 标题
        title = QLabel("分诊建议")
        title.setFont(QFont("微软雅黑", 18, QFont.Bold))
        title.setStyleSheet("color: #1890FF;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        main_layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        self.detail_layout = QVBoxLayout(scroll_content)
        self.detail_layout.setContentsMargins(0, 0, 0, 0)
        self.detail_layout.setSpacing(16)

        # 推荐科室卡片（占位，show_result时填充）
        self.card_frame = None
        self.detail_layout.addStretch()

        # 底部按钮区
        btn_layout = QHBoxLayout()

        self.back_btn = QPushButton("返回修改")
        self.back_btn.setFixedSize(140, 44)
        self.back_btn.setFont(QFont("微软雅黑", 13))
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #666666;
                border: 2px solid #E8E8E8;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
        """)
        self.back_btn.clicked.connect(self.on_back)
        btn_layout.addWidget(self.back_btn)

        btn_layout.addStretch()

        self.route_btn = QPushButton("查看路线")
        self.route_btn.setFixedSize(140, 44)
        self.route_btn.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.route_btn.setStyleSheet("""
            QPushButton {
                background-color: #52C41A;
                color: white;
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #73D13D;
            }
        """)
        self.route_btn.clicked.connect(self.on_view_route)
        btn_layout.addWidget(self.route_btn)

        main_layout.addLayout(btn_layout)

    def show_result(self, data):
        """
        显示分诊结果

        Args:
            data: 分诊结果数据字典
        """
        # 清除旧卡片
        if self.card_frame:
            self.card_frame.deleteLater()
            self.card_frame = None

        primary = data.get("primary", {})
        alternatives = data.get("alternatives", [])
        matched_rules = data.get("matched_rules", [])

        dept_id = primary.get("dept_id", 0)
        dept_name = primary.get("dept_name", "未知")
        confidence = primary.get("confidence", 0.0)
        reason = primary.get("reason", "")

        # 创建推荐卡片
        self.card_frame = QFrame()
        self.card_frame.setStyleSheet("""
            QFrame {
                background-color: #E6F7FF;
                border: 2px solid #91D5FF;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(self.card_frame)

        # 推荐科室
        dept_label = QLabel("推荐科室: " + dept_name)
        dept_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        dept_label.setStyleSheet("color: #1890FF;")
        card_layout.addWidget(dept_label)

        # 所在楼层
        try:
            dept_data = self.main_window.database.execute_query(
                "SELECT floor, location_desc FROM departments WHERE dept_id = ?",
                (dept_id,)
            )
            if dept_data:
                floor = dept_data[0]["floor"]
                location = dept_data[0]["location_desc"]
                floor_label = QLabel("所在楼层: {}楼 ({})".format(floor, location))
                floor_label.setFont(QFont("微软雅黑", 13))
                floor_label.setStyleSheet("color: #333333;")
                card_layout.addWidget(floor_label)
        except Exception as e:
            logger.error("查询科室信息失败: %s", e)

        # 置信度
        conf_percent = int(confidence * 100)
        conf_label = QLabel("置信度: {}%".format(conf_percent))
        conf_label.setFont(QFont("微软雅黑", 13))
        if confidence >= 0.9:
            color = "#52C41A"
        elif confidence >= 0.7:
            color = "#1890FF"
        else:
            color = "#FAAD14"
        conf_label.setStyleSheet("color: {};".format(color))
        card_layout.addWidget(conf_label)

        # 分诊依据
        if reason:
            reason_label = QLabel("分诊依据: " + reason)
            reason_label.setFont(QFont("微软雅黑", 12))
            reason_label.setStyleSheet("color: #666666;")
            reason_label.setWordWrap(True)
            card_layout.addWidget(reason_label)

        # 备选科室
        if alternatives:
            alt_label = QLabel("备选科室:")
            alt_label.setFont(QFont("微软雅黑", 12, QFont.Bold))
            alt_label.setStyleSheet("color: #333333; margin-top: 8px;")
            card_layout.addWidget(alt_label)

            for alt in alternatives:
                alt_name = alt.get("dept_name", "未知")
                alt_conf = int(alt.get("confidence", 0) * 100)
                alt_text = "  - {} (置信度: {}%)".format(alt_name, alt_conf)
                alt_item = QLabel(alt_text)
                alt_item.setFont(QFont("微软雅黑", 11))
                alt_item.setStyleSheet("color: #888888;")
                card_layout.addWidget(alt_item)

        # 插入到布局中
        self.detail_layout.insertWidget(0, self.card_frame)

        # 保存dept_id供"查看路线"使用
        self.current_dept_id = dept_id

    def on_back(self):
        """返回输入面板"""
        self.main_window.show_input_panel()

    def on_view_route(self):
        """查看路线按钮回调"""
        if hasattr(self, "current_dept_id"):
            self.main_window.on_view_route(self.current_dept_id)
