"""
Logging Module for Email Automation & Reminder System.
Provides structured logging for both terminal console and persistent file logs.
"""

import logging
import sys
from pathlib import Path
from src.config import SYSTEM_LOG_FILE, DISPATCH_LOG_FILE

def setup_logger(name: str = "EmailAutomation", log_file: Path = SYSTEM_LOG_FILE, level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a robust logger instance.
    Prevents adding duplicate handlers if already configured.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers on multiple imports
    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

        # Stream / Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            fmt="[%(levelname)s] %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(level)
        logger.addHandler(console_handler)

    return logger

# Pre-initialized loggers
app_logger = setup_logger("AppEngine", SYSTEM_LOG_FILE)
dispatch_logger = setup_logger("EmailDispatcher", DISPATCH_LOG_FILE)
