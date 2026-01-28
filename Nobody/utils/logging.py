"""Logging utilities for the Nobody 3 application."""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from .cache import resolve_writable_cache_dir


def setup_logging():
    """Configure the global logging stack with rotation.

    Log files are rotated when they reach 10MB, keeping up to 5 backup files.
    This prevents log files from growing indefinitely.

    Log level can be controlled via NOBODY3_LOG_LEVEL environment variable:
    - DEBUG: Detailed debugging information
    - INFO: General informational messages (default)
    - WARNING: Warning messages only
    - ERROR: Error messages only
    """
    log_dir = resolve_writable_cache_dir("Nobody 3")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "nobody3.log")

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Determine log level from environment variable or default to INFO
    log_level_str = os.getenv("NOBODY3_LOG_LEVEL", "INFO").upper()
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level = log_level_map.get(log_level_str, logging.INFO)

    # Use RotatingFileHandler to prevent log files from growing too large
    # Max size: 10MB, keep 5 backup files
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(
        logging.Formatter(log_format, datefmt=date_format)
    )

    # Console handler for immediate feedback
    # Console may use a different level (e.g., WARNING in production)
    console_level_str = os.getenv("NOBODY3_CONSOLE_LOG_LEVEL", "").upper()
    if console_level_str and console_level_str in log_level_map:
        console_level = log_level_map[console_level_str]
    else:
        # Default console level matches file level
        console_level = log_level

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(
        logging.Formatter(log_format, datefmt=date_format)
    )

    # Configure root logger
    root_logger = logging.getLogger("Nobody 3")
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()  # Clear any existing handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.propagate = False  # Prevent propagation to root logger

    # Log the configured log level
    root_logger.info(
        f"Logging initialized (level: {log_level_str}, "
        f"file: {log_file})"
    )

    return root_logger


# Global logger instance
logger = setup_logging()
