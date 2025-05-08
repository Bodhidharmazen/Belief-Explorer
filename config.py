"""
Configuration utilities for the Belief Explorer backend.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

def configure_logging():
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    
    # Create file handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'belief_explorer.log'),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def get_gemini_api_key():
    """Get the Gemini API key from environment variables."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        logging.warning("GEMINI_API_KEY not found in environment variables")
    return api_key
