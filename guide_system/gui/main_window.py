# -*- coding: utf-8 -*-
"""
主窗口模块（布局管理 + 面板切换）
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton,
                             QStackedWidget, QMessageBox, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import logging

from gui.input_panel import InputPanel
from gui.result_panel import ResultPanel
from gui.history_panel import HistoryPanel
from models.database import DatabaseManager

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """主窗口（管理各面板布局与切换）"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.database = DatabaseManager()
        self.init_ui()
        logger.info("主窗口初始化完成")

    def init_ui(self):
        """初始化UI界面"""
        # 窗口基本设置
        self.setWindowTitle("智能导医系统")
        self.setMinimumSize(900, 650)
        self.resize(1000, 700)

        # 设置医疗蓝主色调
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F8FF;
            }
            QStatusBar {
                background-color: #1890FF;
                color: white;
                padding: 4px;
            }
        """)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 顶部标题栏
        header = self._create_header()
        main_layout.addWidget(header)

        # 堆栈式面板（用于切换输入/结果/历史）
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # 创建各面板
        self.input_panel = InputPanel(self)
        self.result_panel = ResultPanel(self)
        self.history_panel = HistoryPanel(self)

        # 添加到堆栈
        self.stacked_widget.addWidget(self.input_panel)
        self.stacked_widget.addWidget(self.result_panel)
        self.stacked_widget.addWidget(self.history_panel)

        # 底部状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 默认显示输入面板
        self.show_input_panel()

    def _create_header(self):
        """
        创建顶部标题栏

        Returns:
            QWidget: 标题栏部件
        """
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            background-color: #1890FF;
            padding: 0px;
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        # 标题
        title = QLabel("智能导医系统")
        title.setFont(QFont("微软雅黑", 18, QFont.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        layout.addStretch()

        # 历史记录按钮
        history_btn = QPushButton("历史记录")
        history_btn.setFixedSize(100, 36)
        history_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1890FF;
                border: none;
                border-radius: 18px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E6F7FF;
            }
        """)
        history_btn.clicked.connect(self.show_history_panel)
        layout.addWidget(history_btn)

        return header

    def show_input_panel(self):
        """显示输入面板"""
        self.stacked_widget.setCurrentWidget(self.input_panel)
        self.status_bar.showMessage("请输入症状描述")

    def show_result_panel(self):
        """显示结果面板"""
        self.stacked_widget.setCurrentWidget(self.result_panel)
        self.status_bar.showMessage("分诊结果")

    def show_history_panel(self):
        """显示历史记录面板"""
        self.history_panel.load_history()
        self.stacked_widget.setCurrentWidget(self.history_panel)
        self.status_bar.showMessage("分诊历史记录")

    def on_diagnosis_complete(self, result):
        """
        分诊完成回调

        Args:
            result: 分诊结果字典
        """
        if result.get("success"):
            self.result_panel.show_result(result["data"])
            self.show_result_panel()
        else:
            QMessageBox.warning(
                self,
                "分诊提示",
                result.get("message", "分诊失败")
            )

    def on_view_route(self, dept_id):
        """
        查看路线按钮回调

        Args:
            dept_id: 科室ID
        """
        try:
            dept_data = self.database.execute_query(
                "SELECT * FROM departments WHERE dept_id = ?",
                (dept_id,)
            )
            if not dept_data:
                QMessageBox.warning(self, "提示", "未找到科室信息")
                return

            dept = dept_data[0]
            floor = dept["floor"]
            location = dept["location_desc"]
            dept_name = dept["dept_name"]

            # 生成路线指引
            from utils.helpers import calculate_route_guide
            dept_info = {
                "dept_id": dept_id,
                "dept_name": dept_name,
                "floor": floor,
                "location_desc": location
            }
            steps = calculate_route_guide(dept_info)

            route_text = "\n".join(steps)

            # 标记已查看路线
            self.database.execute_update(
                "UPDATE records SET viewed_route = 1 WHERE record_id = (SELECT MAX(record_id) FROM records)"
            )

            QMessageBox.information(self, "就诊导航", route_text)

        except Exception as e:
            logger.error("查看路线失败: %s", e)
            QMessageBox.warning(self, "错误", "生成路线失败")

    def closeEvent(self, event):
        """关闭窗口事件"""
        try:
            self.database.close()
            logger.info("数据库连接已关闭")
        except Exception:
            pass
        event.accept()
