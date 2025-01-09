from loguru import logger
import os
if not os.path.exists("logs"):
    os.makedirs("logs")
logger.add("logs/{time:YYYY-MM-DD}.log", rotation="00:00",encoding="utf-8", level="DEBUG")
