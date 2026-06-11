#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logging utility for Intelligent Medical Guide System.

This module provides logging setup and configuration for the
entire application.

Attributes:
    DEFAULT_LOG_LEVEL: Default logging level.
    DEFAULT_LOG_FILE: Default log file name.
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
import sys
from typing import Optional

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FILE = "guide_system.log"
DEFAULT_MAX_BYTES = 10485760  # 10MB
DEFAULT_BACKUP_COUNT = 5


def setup_logger(
    name: str = "guide_system",
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT
) -> logging.Logger:
    """Setup application logger with file and console handlers.
    
    Args:
        name: Logger name.
        log_level: Logging level string (DEBUG, INFO, WARNING, ERROR).
        log_file: Log file path.
        max_bytes: Maximum log file size in bytes.
        backup_count: Number of backup files to keep.
    
    Returns:
        Configured logger instance.
    """
    # Read configuration if available
    if log_level is None or log_file is None:
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read("config.ini", encoding="utf-8")
            log_level = log_level or config.get(
                "Logging", "log_level", fallback="INFO"
            )
            log_file = log_file or config.get(
                "Logging", "log_file", fallback=DEFAULT_LOG_FILE
            )
            max_bytes = config.getint(
                "Logging", "max_log_size", fallback=DEFAULT_MAX_BYTES
            )
            backup_count = config.getint(
                "Logging", "backup_count", fallback=DEFAULT_BACKUP_COUNT
            )
        except Exception:
            log_level = log_level or "INFO"
            log_file = log_file or DEFAULT_LOG_FILE
    
    # Convert log level string to constant
    level = getattr(logging, log_level.upper(), DEFAULT_LOG_LEVEL)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.info("Logger initialized: %s (level=%s)", name, log_level)
    
    return logger


def get_logger(name: str = "guide_system") -> logging.Logger:
    """Get an existing logger instance.
    
    Args:
        name: Logger name.
    
    Returns:
        Logger instance.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Logger not initialized, setup with defaults
        return setup_logger(name)
    
    return logger
