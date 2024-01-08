import logging
from enum import Enum, auto
from pathlib import Path


class LoggingLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Logger:
    logging_functions = [
        logging.debug,
        logging.info,
        logging.warning,
        logging.error,
        logging.critical,
    ]

    def __init__(self, app_name: str, logging_level: LoggingLevel) -> None:
        self.app_name = app_name
        self.logging_level = logging_level

        logging.basicConfig(
            level=self.logging_level,
            filename=Path(
                "./log.log",
                filemode="w",
                format="%(asctime)s - %(levelname)s - %(message)s"
            )
        )

    def log(self, message: str, level: LoggingLevel) -> None:
        if level < self.logging_level:
            return None

        self.logging_functions[self.logging_level](message)
