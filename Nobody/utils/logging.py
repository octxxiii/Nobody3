"""로깅 시스템 유틸리티"""

import os
import sys
import logging
from .cache import resolve_writable_cache_dir


def setup_logging():
    """로깅 시스템 초기화"""
    log_dir = resolve_writable_cache_dir("OctXXIII")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "octxxiii.log")
    
    # 로깅 포맷 설정
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 로깅 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger('OctXXIII')


# 전역 로거 인스턴스
logger = setup_logging()

