# -*- coding: utf-8 -*-
"""
输入面板模块（语音按钮 + 文字输入 + 快捷症状）
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QMessageBox,
                             QGridLayout, QFrame)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import logging
import time

from core.speech_recognition import SpeechRecognizer
from core.symptom_extractor import SymptomExtractor
from core.expert_system import ExpertSystem
from models.database import DatabaseManager

logger = logging.getLogger(__name__)


class InputPanel(QWidget):
    """输入面板（语音/文字输入 + 快捷症状）"""

    def __init__(self, main_window):
        """
        初始化输入面板

        Args:
            main_window: 主窗口引用
        """
        super().__init__()
        self.main_window = main_window
        self.database = main_window.database
        self.speech_recognizer = None
        self.symptom_extractor = None
        self.expert_system = None
        self.is_recording = False
        self.init_ui()
        self.init_modules()

    def init_modules(self):
        """初始化算法模块"""
        try:
            import os
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config.ini"
            )
            self.speech_recognizer = SpeechRecognizer(config_path)
            self.symptom_extractor = SymptomExtractor(self.database)
            self.symptom_extractor.load_symptom_library()
            self.expert_system = ExpertSystem(self.database)
            self.expert_system.load_rules()
            logger.info("算法模块初始化完成")
        except Exception as e:
            logger.error("算法模块初始化失败: %s", e)

    def init_ui(self):
        """初始化UI界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # 标题区
        title_label = QLabel("请描述您的症状")
        title_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        title_label.setStyleSheet("color: #1890FF;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 语音输入区
        voice_frame = QFrame()
        voice_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #E8E8E8;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        voice_layout = QVBoxLayout(voice_frame)

        self.voice_btn = QPushButton("按住说话")
        self.voice_btn.setFixedSize(200, 60)
        self.voice_btn.setFont(QFont("微软雅黑", 14, QFont.Bold))
        self.voice_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890FF;
                color: white;
                border: none;
                border-radius: 30px;
            }
            QPushButton:pressed {
                background-color: #096DD9;
            }
            QPushButton:hover {
                background-color: #40A9FF;
            }
        """)
        self.voice_btn.pressed.connect(self.start_recording)
        self.voice_btn.released.connect(self.stop_recording)
        voice_layout.addWidget(self.voice_btn, 0, Qt.AlignCenter)

        self.voice_status = QLabel("点击按钮开始语音输入")
        self.voice_status.setFont(QFont("微软雅黑", 11))
        self.voice_status.setStyleSheet("color: #888888;")
        self.voice_status.setAlignment(Qt.AlignCenter)
        voice_layout.addWidget(self.voice_status)

        main_layout.addWidget(voice_frame)

        # 文字输入区
        text_label = QLabel("或文字输入:")
        text_label.setFont(QFont("微软雅黑", 12))
        text_label.setStyleSheet("color: #333333;")
        main_layout.addWidget(text_label)

        self.text_input = QTextEdit()
        self.text_input.setFixedHeight(80)
        self.text_input.setPlaceholderText("请详细描述您的症状，如：我发烧、咳嗽...")
        self.text_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid #1890FF;
            }
        """)
        main_layout.addWidget(self.text_input)

        # 按钮区
        btn_layout = QHBoxLayout()

        self.confirm_btn = QPushButton("确认")
        self.confirm_btn.setFixedSize(120, 44)
        self.confirm_btn.setFont(QFont("微软雅黑", 13, QFont.Bold))
        self.confirm_btn.setStyleSheet("""
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
        self.confirm_btn.clicked.connect(self.on_text_submit)
        btn_layout.addWidget(self.confirm_btn)

        self.clear_btn = QPushButton("清空")
        self.clear_btn.setFixedSize(120, 44)
        self.clear_btn.setFont(QFont("微软雅黑", 13))
        self.clear_btn.setStyleSheet("""
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
        self.clear_btn.clicked.connect(self.on_clear)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        # 快捷症状按钮区
        quick_label = QLabel("快捷症状（点击快速输入）:")
        quick_label.setFont(QFont("微软雅黑", 12))
        quick_label.setStyleSheet("color: #333333;")
        main_layout.addWidget(quick_label)

        self.quick_symptoms = [
            "发烧", "咳嗽", "头痛", "腹痛",
            "喉咙痛", "关节痛", "皮肤瘙痒", "胸痛"
        ]

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        row, col = 0, 0
        for symptom in self.quick_symptoms:
            btn = QPushButton(symptom)
            btn.setFixedSize(100, 40)
            btn.setFont(QFont("微软雅黑", 12))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E6F7FF;
                    color: #1890FF;
                    border: 1px solid #91D5FF;
                    border-radius: 20px;
                }
                QPushButton:hover {
                    background-color: #BAE7FF;
                }
            """)
            btn.clicked.connect(lambda checked, s=symptom: self.on_quick_symptom(s))
            grid_layout.addWidget(btn, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

    def start_recording(self):
        """开始录音"""
        self.is_recording = True
        self.voice_status.setText("录音中... 松开按钮结束")
        self.voice_btn.setText("松手结束")
        logger.info("开始录音")

    def stop_recording(self):
        """停止录音并识别"""
        if not self.is_recording:
            return
        self.is_recording = False
        self.voice_btn.setText("按住说话")
        self.voice_status.setText("识别中...")
        logger.info("停止录音，开始识别")

        # 模拟音频数据（实际项目中需要真实的音频采集）
        dummy_audio = b"\x00\x01" * 8000  # 模拟1秒音频

        if self.speech_recognizer:
            result = self.speech_recognizer.recognize_speech(dummy_audio)
            if result["success"]:
                text = result["data"]["text"]
                self.text_input.setText(text)
                self.voice_status.setText("识别成功: " + text)
                logger.info("语音识别成功: %s", text)
            else:
                self.voice_status.setText("识别失败: " + result["message"])
                logger.warning("语音识别失败: %s", result["message"])
        else:
            self.voice_status.setText("语音识别模块未初始化")

    def on_text_submit(self):
        """文字输入提交"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "提示", "请输入症状描述")
            return

        logger.info("提交症状描述: %s", text)

        # 提取症状
        if not self.symptom_extractor:
            QMessageBox.warning(self, "错误", "症状提取模块未初始化")
            return

        extract_result = self.symptom_extractor.extract_symptoms(text)
        if not extract_result["success"]:
            QMessageBox.warning(self, "提示", extract_result["message"])
            return

        symptoms = extract_result["data"]["symptoms"]
        if not symptoms:
            QMessageBox.warning(self, "提示", "未识别到有效症状")
            return

        # 保存记录到数据库
        try:
            symptoms_json = str([s["name"] for s in symptoms])
            self.database.execute_update(
                "INSERT INTO records (create_time, input_text, matched_symptoms, recommended_dept, confidence) "
                "VALUES (datetime('now'), ?, ?, NULL, 0)",
                (text, symptoms_json)
            )
        except Exception as e:
            logger.error("保存记录失败: %s", e)

        # 调用专家系统分诊
        if not self.expert_system:
            QMessageBox.warning(self, "错误", "专家系统未初始化")
            return

        diagnose_result = self.expert_system.diagnose(symptoms)
        if diagnose_result["success"]:
            # 更新记录中的推荐科室
            try:
                primary = diagnose_result["data"]["primary"]
                self.database.execute_update(
                    "UPDATE records SET recommended_dept = ?, confidence = ? "
                    "WHERE record_id = (SELECT MAX(record_id) FROM records)",
                    (primary["dept_id"], primary["confidence"])
                )
            except Exception as e:
                logger.error("更新记录失败: %s", e)

            # 回调主窗口显示结果
            self.main_window.on_diagnosis_complete(diagnose_result)
        else:
            QMessageBox.warning(self, "分诊失败", diagnose_result["message"])

    def on_clear(self):
        """清空输入"""
        self.text_input.clear()
        self.voice_status.setText("点击按钮开始语音输入")

    def on_quick_symptom(self, symptom_name):
        """
        快捷症状按钮点击

        Args:
            symptom_name: 症状名称
        """
        current_text = self.text_input.toPlainText().strip()
        if current_text:
            new_text = current_text + "、" + symptom_name
        else:
            new_text = symptom_name
        self.text_input.setText(new_text)
        logger.info("快捷输入症状: %s", symptom_name)
