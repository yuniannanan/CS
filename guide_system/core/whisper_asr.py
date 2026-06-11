# -*- coding: utf-8 -*-
"""
离线语音识别模块（基于 OpenAI Whisper tiny）
纯本地运行，零外部API依赖

支持输入格式：
- 原始 PCM 16-bit signed int, 16kHz mono
- WAV 文件格式（自动解析采样率和声道）
"""

import logging
import io
import numpy as np

logger = logging.getLogger(__name__)

_whisper_model = None


def _get_model():
    """获取 Whisper 模型（单例，延迟加载）"""
    global _whisper_model
    if _whisper_model is None:
        import whisper
        logger.info("Loading Whisper tiny model (~73MB, offline)...")
        _whisper_model = whisper.load_model("tiny")
        logger.info("Whisper model ready")
    return _whisper_model


def _pcm_to_float32(pcm_bytes: bytes, sample_width: int = 2) -> np.ndarray:
    """PCM bytes → float32 numpy array"""
    dtype = {1: np.int8, 2: np.int16, 4: np.int32}.get(sample_width, np.int16)
    audio = np.frombuffer(pcm_bytes, dtype=dtype)
    max_val = float(2 ** (8 * sample_width - 1))
    return audio.astype(np.float32) / max_val


def _read_wav(wav_bytes: bytes) -> np.ndarray:
    """解析 WAV 文件，返回 float32 numpy array"""
    import scipy.io.wavfile as wavfile
    f = io.BytesIO(wav_bytes)
    sr, data = wavfile.read(f)
    # 转为 mono
    if data.ndim > 1:
        data = data.mean(axis=1)
    # 归一化到 [-1, 1]
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    else:
        data = data.astype(np.float32)
    return data


def recognize(audio_bytes: bytes, fmt: str = "auto", language: str = "zh") -> dict:
    """
    识别语音文字

    Args:
        audio_bytes: 音频字节数据
        fmt: "pcm" | "wav" | "auto"（自动检测）
        language: 识别语言

    Returns:
        {"success": bool, "data": {"text": str}, "message": str}
    """
    if not audio_bytes or len(audio_bytes) < 400:
        return {"success": False, "data": None, "message": "音频太短，请长按说话至少1秒"}

    try:
        # 格式检测
        if fmt == "auto":
            fmt = "wav" if audio_bytes[:4] == b"RIFF" else "pcm"

        if fmt == "wav":
            audio = _read_wav(audio_bytes)
        else:
            audio = _pcm_to_float32(audio_bytes)

        # 至少0.3秒音频
        if len(audio) < 4800:
            return {"success": False, "data": None, "message": "音频太短，请长按说话"}

        model = _get_model()

        result = model.transcribe(
            audio,
            language=language,
            fp16=False,
            task="transcribe",
            verbose=False,
            no_speech_threshold=0.45,       # 降低阈值，更容易检测语音
            compression_ratio_threshold=2.4,
            condition_on_previous_text=False,
            temperature=0.0,                 # 贪婪解码，更稳定
        )

        text = result.get("text", "").strip()
        if not text:
            return {"success": False, "data": None,
                    "message": "未识别到语音，请清晰大声说话"}

        logger.info("Whisper: %s", text)
        return {"success": True, "data": {"text": text}, "message": "识别成功"}

    except Exception as e:
        logger.error("Whisper error: %s", e, exc_info=True)
        return {"success": False, "data": None,
                "message": "识别异常，请重试"}
