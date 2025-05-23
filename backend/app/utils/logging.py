import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """Set up a logger with consistent formatting and handlers.
    
    Args:
        name: Name of the logger
        
    Returns:
        Logger instance configured with consistent formatting
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create handlers if they don't exist
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger
