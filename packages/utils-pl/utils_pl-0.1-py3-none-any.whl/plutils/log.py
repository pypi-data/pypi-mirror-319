from typing import Callable
import logging
import lutils.simple_log as base
from rich.logging import RichHandler

class LogHandler(RichHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            if record.levelno == logging.INFO:
                base.info(msg)
            elif record.levelno == logging.DEBUG:
                base.verbose(msg)
            elif record.levelno == logging.WARNING:
                base.warning(msg)
            elif record.levelno == logging.ERROR:
                base.error(msg)
            elif record.levelno == logging.CRITICAL:
                base.critical(msg)
        except Exception as e:
            base.exception(f"Error in logging: {e}")
            self.handleError(record)

class Logger:
    def __init__(self, name: str | None, color: str | None, _prefix_append: Callable | None = None, _logger_name: str = 'rich'):
        self.logger = logging.getLogger(_logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(LogHandler())
        self.name = name
        if name:
            if color:
                name = f"[{color}]{name}[/{color}]"
            self.name_prefix = f"[bold #5e5e5e][[/]{name}[bold #5e5e5e]][/] "
        else:
            self.name_prefix = ""
        self._prefix_append = _prefix_append

    def __prefix(self):
        if self._prefix_append:
            return f"{self.name_prefix}{self._prefix_append()}"
        return self.name_prefix

    def __render(self, message: str):
        return f"{self.__prefix()} {message}"

    def exception(self, message: str, **kwargs):
        self.logger.exception(self.__render(message))

    def critical(self, message: str, **kwargs):
        self.logger.critical(self.__render(message))

    def error(self, message: str, **kwargs):
        self.logger.error(self.__render(message))

    def success(self, message: str, **kwargs):
        self.logger.info(self.__render(message))

    def warning(self, message: str, **kwargs):
        self.logger.warning(self.__render(message))

    def info(self, message: str, **kwargs):
        self.logger.info(self.__render(message))

    def verbose(self, message: str, **kwargs):
        self.logger.debug(self.__render(message))

    def debug(self, message: str, **kwargs):
        self.logger.debug(self.__render(message))

    @property
    def log_level(self):
        return base.LOGLEVEL

    @log_level.setter
    def log_level(self, level):
        base.set_loglevel(level)
        self.logger.setLevel(level)

