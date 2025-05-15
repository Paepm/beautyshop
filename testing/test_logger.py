from beautyshop.logging_config import setup_logger

logger = setup_logger(__name__)

logger.debug("[DEBUG]  This is a debug message")
logger.info("[INFO]   This is an info message")
logger.warning("[WARNING] This is a warning message")
logger.error("[ERROR]  This is an error message")
logger.critical("[CRITICAL] This is a critical message")