"""Logging configuration."""

import logging
import sys
from loguru import logger as loguru_logger
import os


def setup_logging():
    """Setup application logging."""
    # Configure loguru
    log_level = os.getenv('API_LOG_LEVEL', 'INFO')
    
    loguru_logger.remove()  # Remove default handler
    loguru_logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level
    )
    
    # Also configure stdlib logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


logger = loguru_logger
