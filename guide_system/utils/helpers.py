#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helper utility functions for Intelligent Medical Guide System.

This module provides common utility functions for text processing,
data validation, and other general operations.

Attributes:
    CHINESE_PUNCTUATION: Set of Chinese punctuation characters.
"""

import re
import hashlib
from typing import List, Optional, Any
from datetime import datetime
import difflib
import logging

logger = logging.getLogger(__name__)

CHINESE_PUNCTUATION = set(
    '，。！？；：""''【】（）《》、'
)


def format_time(dt: Optional[datetime] = None) -> str:
    """Format datetime to string.
    
    Args:
        dt: Datetime object to format.
    
    Returns:
        Formatted time string.
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def clean_text(text: str) -> str:
    """Clean and normalize text input.
    
    Args:
        text: Raw input text.
    
    Returns:
        Cleaned text string.
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters except Chinese, English, numbers
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text)
    
    return text.strip()


def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity between two strings.
    
    Args:
        str1: First string.
        str2: Second string.
    
    Returns:
        Similarity score between 0 and 1.
    """
    if not str1 or not str2:
        return 0.0
    
    return difflib.SequenceMatcher(None, str1, str2).ratio()


def validate_input(
    text: str, 
    min_length: int = 1, 
    max_length: int = 500
) -> tuple[bool, str]:
    """Validate user input text.
    
    Args:
        text: Input text to validate.
        min_length: Minimum allowed length.
        max_length: Maximum allowed length.
    
    Returns:
        Tuple of (is_valid, error_message).
    """
    if not text or not text.strip():
        return False, "输入不能为空"
    
    text = text.strip()
    
    if len(text) < min_length:
        return False, f"输入长度不能少于{min_length}个字符"
    
    if len(text) > max_length:
        return False, f"输入长度不能超过{max_length}个字符"
    
    return True, ""


def extract_keywords(text: str, top_k: int = 5) -> List[str]:
    """Extract keywords from text using jieba.
    
    Args:
        text: Input text.
        top_k: Number of top keywords to extract.
    
    Returns:
        List of keyword strings.
    """
    try:
        import jieba.analyse
        
        keywords = jieba.analyse.extract_tags(text, topK=top_k)
        return keywords
    except ImportError:
        logger.warning("jieba not installed, cannot extract keywords")
        return []
    except Exception as e:
        logger.error("Keyword extraction failed: %s", str(e))
        return []


def generate_id(seed: str) -> int:
    """Generate a numeric ID from string seed.
    
    Args:
        seed: String to generate ID from.
    
    Returns:
        Numeric ID value.
    """
    hash_obj = hashlib.md5(seed.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    # Take first 8 characters and convert to int
    id_value = int(hash_hex[:8], 16)
    return id_value % (10 ** 8)  # Limit to 8 digits


def format_confidence(confidence: float) -> str:
    """Format confidence score as percentage string.
    
    Args:
        confidence: Confidence score (0.0-1.0).
    
    Returns:
        Formatted percentage string.
    """
    percentage = confidence * 100
    return f"{percentage:.1f}%"


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis.
    
    Args:
        text: Text to truncate.
        max_length: Maximum length before truncation.
    
    Returns:
        Truncated text string.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def is_chinese(text: str) -> bool:
    """Check if text contains primarily Chinese characters.
    
    Args:
        text: Text to check.
    
    Returns:
        True if text is primarily Chinese.
    """
    if not text:
        return False
    
    chinese_count = sum(1 for char in text if '\u4e00' <= char <= '\u9fa5')
    return chinese_count > len(text) * 0.5
