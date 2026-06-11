# -*- coding: utf-8 -*-
"""
历史记录面板模块
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QListWidget, QListWidgetItem,
                             QTextEdit, QFrame, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette
import logging
from datetime import datetime

from models.database import DatabaseManager
from models.record import TriageRecord
import json

logger = logging.getLogger(__name__)


class HistoryPanel(QWidget):
    """历史记录面板（记录列表 + 详情查看）"""

    def __init__(self, main_window):
        """
        初始化历史记录面板

        Args:
            main_window: 主窗口引用
        """
        super().__init__()
        self.main_window = main_window
        self.database = main_window.database
        self.init_ui()

    def init_ui(self):
        """初始化UI界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 30)
        main_layout.setSpacing(20)

        # 标题
        title = QLabel("分诊历史记录")
        title.setFont(QFont("微软雅黑", 18, QFont.Bold))
        title.setStyleSheet("color: #1890FF;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # 记录列表
        self.record_list = QListWidget()
        self.record_list.setFixedHeight(300)
        self.record_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #F0F0F0;
            }
            QListWidget::item:selected {
                background-color: #E6F7FF;
                color: #1890FF;
                border-radius: 6px;
            }
        """)
        self.record_list.itemClicked.connect(self.on_record_selected)
        main_layout.addWidget(self.record_list)

        # 详情显示区
        detail_label = QLabel("记录详情:")
        detail_label.setFont(QFont("微软雅黑", 12))
        detail_label.setStyleSheet("color: #333333;")
        main_layout.addWidget(detail_label)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setFixedHeight(200)
        self.detail_text.setStyleSheet("""
            QTextEdit {
                background-color: #F5F5F5;
                border: 1px solid #E8E8E8;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                line-height: 1.6;
            }
        """)
        main_layout.addWidget(self.detail_text)

        # 底部按钮区
        btn_layout = QHBoxLayout()

        self.back_btn = QPushButton("返回输入")
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

        self.clear_btn = QPushButton("清除历史")
        self.clear_btn.setFixedSize(140, 44)
        self.clear_btn.setFont(QFont("微软雅黑", 13))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4D4F;
                color: white;
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #FF7875;
            }
        """)
        self.clear_btn.clicked.connect(self.on_clear_history)
        btn_layout.addWidget(self.clear_btn)

        main_layout.addLayout(btn_layout)

    def load_history(self):
        """加载历史记录列表"""
        self.record_list.clear()
        self.detail_text.clear()

        try:
            config = self.main_window.config if hasattr(self.main_window, 'config') else {}
            max_records = config.get("max_history_records", 10)

            records = self.database.execute_query(
                "SELECT * FROM records ORDER BY create_time DESC LIMIT ?",
                (max_records,)
            )

            if not records:
                self.record_list.addItem("暂无分诊记录")
                return

            for record_data in records:
                record = TriageRecord.from_dict(record_data)

                # 格式化显示
                time_str = record.create_time.replace("T", " ").split(".")[0]
                dept_name = "未知科室"

                if record.recommended_dept:
                    dept_result = self.database.execute_query(
                        "SELECT dept_name FROM departments WHERE dept_id = ?",
                        (record.recommended_dept,)
                    )
                    if dept_result:
                        dept_name = dept_result[0]["dept_name"]

                conf_percent = int(record.confidence * 100)

                item_text = "{}\n症状: {}\n推荐: {} (置信度: {}%)".format(
                    time_str,
                    record.input_text[:30] + "..." if len(record.input_text) > 30 else record.input_text,
                    dept_name,
                    conf_percent
                )

                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, record.record_id)
                self.record_list.addItem(item)

            logger.info("加载了 %d 条历史记录", len(records))

        except Exception as e:
            logger.error("加载历史记录失败: %s", e)
            self.record_list.addItem("加载失败: {}".format(e))

    def on_record_selected(self, item):
        """
        点击某条记录，显示详情

        Args:
            item: 被点击的列表项
        """
        record_id = item.data(Qt.UserRole)
        if record_id is None:
            return

        try:
            record_data = self.database.execute_query(
                "SELECT * FROM records WHERE record_id = ?",
                (record_id,)
            )

            if not record_data:
                return

            record = TriageRecord.from_dict(record_data[0])

            # 获取科室信息
            dept_name = "未知科室"
            floor = ""
            location = ""
            if record.recommended_dept:
                dept_result = self.database.execute_query(
                    "SELECT dept_name, floor, location_desc FROM departments WHERE dept_id = ?",
                    (record.recommended_dept,)
                )
                if dept_result:
                    dept_name = dept_result[0]["dept_name"]
                    floor = str(dept_result[0]["floor"])
                    location = dept_result[0]["location_desc"]

            # 格式化详情
            time_str = record.create_time.replace("T", " ").split(".")[0]
            conf_percent = int(record.confidence * 100)

            detail = "分诊时间: {}\n".format(time_str)
            detail += "输入描述: {}\n".format(record.input_text)
            detail += "匹配症状: {}\n".format(", ".join(record.matched_symptoms))
            detail += "推荐科室: {}\n".format(dept_name)
            detail += "所在楼层: {}楼\n".format(floor)
            detail += "具体位置: {}\n".format(location)
            detail += "置信度: {}%\n".format(conf_percent)
            detail += "是否查看路线: {}\n".format("是" if record.viewed_route else "否")

            self.detail_text.setPlainText(detail)

        except Exception as e:
            logger.error("显示记录详情失败: %s", e)

    def on_back(self):
        """返回输入面板"""
        self.main_window.show_input_panel()

    def on_clear_history(self):
        """清除所有历史记录"""
        try:
            reply = QPushButton()
            from PyQt5.QtWidgets import QMessageBox
            confirm = QMessageBox.question(
                self,
                "确认清除",
                "确定要清除所有历史记录吗？此操作不可恢复。",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                self.database.execute_update("DELETE FROM records")
                self.load_history()
                self.detail_text.clear()
                logger.info("历史记录已清除")

        except Exception as e:
            logger.error("清除历史记录失败: %s", e)
