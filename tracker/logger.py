import sys
from loguru import logger


class Logger:
    def __init__(self):
        self.logger = logger
        self.logger.add("log.log", format="{time} {level} {message}", level="WARNING")
        self.logger.add(sys.stdout, format="{message}", level="INFO")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    def log_info(self, message: str):
        self.logger.info(message)