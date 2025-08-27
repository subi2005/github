from loguru import logger
import sys

logger.remove()  
logger.add(sys.stderr, level="INFO")
logger.add("logs/risk_model.log", rotation="10 MB", level="DEBUG")

__all__ = ["logger"]

