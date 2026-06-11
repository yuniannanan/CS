# -*- coding: utf-8 -*-
"""
语音识别代理模块（封装百度语音API）
"""

import requests
import json
import base64
import time
import logging

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """语音识别代理（封装百度AI开放平台语音识别API）"""

    def __init__(self, config_path: str = "config.ini"):
        """
        初始化语音识别器

        Args:
            config_path: 配置文件路径（包含API密钥）
        """
        self.config_path = config_path
        self.api_key = ""
        self.secret_key = ""
        self.token_url = "https://aip.baidu.com/oauth/2.0/token"
        self.speech_url = "https://vop.baidu.com/server_api"
        self.access_token = ""
        self.token_expires_at = 0
        self._load_config()

    def _load_config(self):
        """从配置文件加载API密钥"""
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read(self.config_path, encoding="utf-8")

            self.api_key = config.get("SpeechRecognition", "api_key", fallback="")
            self.secret_key = config.get("SpeechRecognition", "secret_key", fallback="")
            self.app_id = config.get("SpeechRecognition", "app_id", fallback="")

            if not self.api_key or self.api_key == "your_api_key":
                logger.warning("百度API密钥未配置，语音识别功能不可用")
        except Exception as e:
            logger.error("加载配置文件失败: %s", e)

    def recognize_speech(self, audio_data: bytes) -> dict:
        """
        将音频数据转换为文字

        Args:
            audio_data: 音频二进制数据（PCM格式，16000Hz，16bit，单声道）

        Returns:
            {
                "success": True,
                "data": {"text": str},
                "message": str
            }
        """
        if not self.api_key or self.api_key in ("YOUR_API_KEY_HERE", "your_api_key", ""):
            return {
                "success": False,
                "data": None,
                "message": "API密钥未配置，请先在config.ini中填写百度API密钥"
            }

        if not audio_data:
            return {
                "success": False,
                "data": None,
                "message": "音频数据为空"
            }

        try:
            token = self.get_access_token()
            if not token:
                return {
                    "success": False,
                    "data": None,
                    "message": "获取访问令牌失败，请检查API密钥"
                }

            # Base64编码音频数据
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")

            # 构造请求
            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "format": "pcm",
                "rate": 16000,
                "channel": 1,
                "cuid": "guide_system_client",
                "token": token,
                "speech": audio_base64,
                "len": len(audio_data)
            }

            response = requests.post(
                self.speech_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=10
            )

            result = response.json()

            if result.get("err_no") == 0:
                text = result.get("result", [""])[0]
                logger.info("语音识别成功: %s", text)
                return {
                    "success": True,
                    "data": {"text": text},
                    "message": "识别成功"
                }
            else:
                err_msg = result.get("err_msg", "未知错误")
                logger.error("语音识别失败: %s", err_msg)
                return {
                    "success": False,
                    "data": None,
                    "message": "识别失败: {}".format(err_msg)
                }

        except requests.Timeout:
            logger.error("语音识别请求超时")
            return {
                "success": False,
                "data": None,
                "message": "网络请求超时，请检查网络连接"
            }
        except Exception as e:
            logger.error("语音识别异常: %s", e)
            return {
                "success": False,
                "data": None,
                "message": "识别异常: {}".format(e)
            }

    def get_access_token(self) -> str:
        """
        获取百度AI开放平台访问令牌（带缓存）

        Returns:
            str: 访问令牌，失败返回空字符串
        """
        # 检查缓存的token是否还有效（提前60秒刷新）
        current_time = time.time()
        if self.access_token and current_time < self.token_expires_at - 60:
            return self.access_token

        try:
            params = {
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key
            }

            response = requests.get(
                self.token_url,
                params=params,
                timeout=5
            )

            result = response.json()

            if "access_token" in result:
                self.access_token = result["access_token"]
                # token有效期（秒），提前5分钟视为过期
                expires_in = result.get("expires_in", 2592000)
                self.token_expires_at = current_time + expires_in
                logger.info("获取访问令牌成功")
                return self.access_token
            else:
                logger.error("获取访问令牌失败: %s", result)
                return ""

        except Exception as e:
            logger.error("获取访问令牌异常: %s", e)
            return ""

    def preprocess_audio(self, audio_data: bytes) -> bytes:
        """
        预处理音频数据（格式校验与转换）

        Args:
            audio_data: 原始音频二进制数据

        Returns:
            bytes: 处理后的音频数据（PCM格式）
        """
        # 百度API要求：PCM格式，16000Hz，16bit，单声道
        # 这里只做基本校验，实际项目中需要完整的音频格式转换
        if not audio_data:
            return b""

        # 检查数据长度（至少有点数据）
        if len(audio_data) < 1024:
            logger.warning("音频数据过短，可能录制失败")

        logger.debug("音频预处理完成，数据长度: %d bytes", len(audio_data))
        return audio_data
