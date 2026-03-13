# utils/logger.py
import logging

def get_logger():
    """Returns the logger instance configured by the conftest.py session fixture."""
    return logging.getLogger("MyFrameworkLogger")