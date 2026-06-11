#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main entry point for Intelligent Medical Guide System.

This module initializes the application, sets up the database connection,
and launches the main GUI window.

Attributes:
    APP_NAME: Name of the application.
    VERSION: Current version of the application.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from gui.main_window import MainWindow
from utils.logger import setup_logger


APP_NAME = "智能导医系统"
VERSION = "1.0.0"


def main() -> int:
    """Initialize and run the Intelligent Medical Guide System.
    
    Returns:
        int: Application exit code.
    """
    # Setup logger
    logger = setup_logger()
    logger.info(f"Starting {APP_NAME} v{VERSION}")
    
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(VERSION)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create and show main window
    main_window = MainWindow()
    main_window.show()
    
    logger.info("Application started successfully")
    
    # Run application event loop
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
