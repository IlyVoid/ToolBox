import logging
import os

# Setup logging configurations
def setup_logging():
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Error Logger
    error_handler = logging.FileHandler("logs/error.log")
    error_handler.setLevel(logging.ERROR)
    
    # Activity Logger
    activity_handler = logging.FileHandler("logs/activity.log")
    activity_handler.setLevel(logging.INFO)
    
    logger = logging.getLogger()
    logger.addHandler(error_handler)
    logger.addHandler(activity_handler)
    
    return logger
