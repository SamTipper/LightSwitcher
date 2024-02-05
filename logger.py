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
    _logging_functions: list = [
        logging.debug,
        logging.info,
        logging.warning,
        logging.error,
        logging.critical,
    ]
    
    def __init__(self, app_name: str, logging_level: str) -> None:
        try:
            logging_level = int(logging_level)

        except ValueError as e:
            raise ValueError(
                "\"logging_level\" in the config file is not a valid integer.",
                e
            )

        self.app_name = app_name
        self.logging_level = logging_level
        self._misconfigured = logging_level not in range(len(self._logging_functions))

        logging.basicConfig(
            level=self.logging_level,
            filename=Path(
                "./log.log",
                filemode="w",
                format="%(asctime)s - %(levelname)s - %(message)s"
            )
        )

    def log(self, message: str, level: LoggingLevel) -> None:
        if self._misconfigured or level < self.logging_level:
            return None
        
        if level not in range(len(self._logging_functions)):
            self._logging_functions[LoggingLevel.ERROR](
                "Incorrect logging level given."
            )
            return None

        self._logging_functions[level](message)
