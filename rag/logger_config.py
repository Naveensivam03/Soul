"""
Soul Logging Configuration
Centralized logging setup for all components
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    """Set up a logger with the given name and log file."""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create file handler with rotation (10MB max, keep 5 files)
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, log_file),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Add file handler
    logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

# Initialize all loggers
def init_all_loggers():
    """Initialize all loggers for different components"""
    
    loggers = {
        'chroma': setup_logger('chroma', 'chroma_retrieval.log'),
        'valkey': setup_logger('valkey', 'valkey_cache.log'),
        'gemini': setup_logger('gemini', 'gemini_ai.log'),
        'database': setup_logger('database', 'database_operations.log'),
        'ui': setup_logger('ui', 'user_interface.log'),
        'workflow': setup_logger('workflow', 'workflow.log'),
        'embeddings': setup_logger('embeddings', 'embeddings.log'),
        'system': setup_logger('system', 'system.log')
    }
    
    return loggers

# Global logger instances
LOGGERS = init_all_loggers()

# Convenience functions to get specific loggers
def get_chroma_logger():
    return LOGGERS['chroma']

def get_valkey_logger():
    return LOGGERS['valkey']

def get_gemini_logger():
    return LOGGERS['gemini']

def get_database_logger():
    return LOGGERS['database']

def get_ui_logger():
    return LOGGERS['ui']

def get_workflow_logger():
    return LOGGERS['workflow']

def get_embeddings_logger():
    return LOGGERS['embeddings']

def get_system_logger():
    return LOGGERS['system']

def log_user_interaction(user_input, ai_response):
    """Log user interactions for analysis"""
    interaction_logger = setup_logger('interactions', 'user_interactions.log')
    interaction_logger.info(f"USER: {user_input}")
    interaction_logger.info(f"ANIMA: {ai_response}")
    interaction_logger.info("=" * 80)
