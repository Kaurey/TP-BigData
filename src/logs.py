import logging
import sys

def get_logger(name="BigDataTP"):
    """
    Creates and configures a logger for the application.
    Basic configuration to stdout with timestamp.
    """
    logger = logging.getLogger(name)
    
    # Check if handlers are already set to avoid duplicate logs in some environments
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        # Add formatter to handler
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
        
    return logger

# Create a default logger instance
logger = get_logger()
