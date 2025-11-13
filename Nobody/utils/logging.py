"""Logging utilities for the Nobody 3 application."""

import os
import sys
import logging
from .cache import resolve_writable_cache_dir


def setup_logging():
    """Configure the global logging stack."""
    log_dir = resolve_writable_cache_dir("Nobody 3")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "nobody3.log")

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    return logging.getLogger("Nobody 3")


# Global logger instance
logger = setup_logging()

