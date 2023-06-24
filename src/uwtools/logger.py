"""
Logger
"""

import functools
import logging
import sys
from pathlib import Path
from typing import List, Optional, Union


class ColoredFormatter(logging.Formatter):
    """
    Logging colored formatter
    adapted from https://stackoverflow.com/a/56944256/3638629
    """

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.formats = {
            logging.DEBUG: self.blue + self.fmt + self.reset,
            logging.INFO: self.grey + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    """
    Improved logging
    """

    DEFAULT_FORMAT = "%(asctime)s - %(levelname)-8s - %(name)-12s: %(message)s"
    DEFAULT_LEVEL = "INFO"
    LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def __init__(
        self,
        name: Optional[str] = None,
        level: str = DEFAULT_LEVEL,
        fmt: Optional[str] = DEFAULT_FORMAT,
        colored_log: bool = False,
        log_file: Optional[Union[str, Path]] = None,
        quiet: bool = False,
    ):
        """
        Constructor for Logger
        """

        self.name = name
        self.level = level.upper()
        self.fmt = fmt or self.DEFAULT_FORMAT
        self.colored_log = colored_log

        if self.level not in Logger.LOG_LEVELS:
            raise LookupError(
                "{self.level} is unknown logging level\n"
                + "Currently supported log levels are:\n"
                + f'{" | ".join(Logger.LOG_LEVELS)}'
            )

        # Get the named logger (or the root logger if no name is specified),
        # set its log level, then attach console and file handlers if not in
        # quiet mode.

        self._logger = logging.getLogger(name) if name else logging.getLogger()
        self._logger.setLevel(self.level)
        if not quiet:
            self._logger.addHandler(
                Logger.add_stream_handler(
                    level=self.level,
                    fmt=self.fmt,
                    colored_log=self.colored_log,
                )
            )
            if log_file:
                self._logger.addHandler(
                    Logger.add_file_handler(log_file, level=self.level, fmt=self.fmt)
                )

    def __getattr__(self, attribute):
        """
        Allows calling logging module methods directly
        """
        return getattr(self._logger, attribute)

    def get_logger(self):
        """
        Return the logging object
        """
        return self._logger

    @classmethod
    def add_handlers(cls, logger: logging.Logger, handlers: List[logging.Handler]):
        """
        Add a list of handlers to a logger
        Parameters
        ----------
        logger
        logger
        handlers

        Returns
        -------
        logger
        """
        for handler in handlers:
            logger.addHandler(handler)

        return logger

    @classmethod
    def add_stream_handler(
        cls,
        level: str = DEFAULT_LEVEL,
        fmt: str = DEFAULT_FORMAT,
        colored_log: bool = False,
    ):
        """
        Create stream handler
        This classmethod will allow setting a custom stream handler on children
        """

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(ColoredFormatter(fmt) if colored_log else logging.Formatter(fmt))
        return handler

    @classmethod
    def add_file_handler(
        cls,
        logfile_path: Union[str, Path],
        level: str = DEFAULT_LEVEL,
        fmt: str = DEFAULT_FORMAT,
    ):
        """
        Create file handler.
        This classmethod will allow setting custom file handler on children
        """

        logfile_path = Path(logfile_path)

        # Create the directory containing the logfile_path
        if not logfile_path.parent.is_dir():
            logfile_path.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(str(logfile_path), mode="w")
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(fmt))

        return handler


def verbose(_func=None):
    """Logs the caller and args to a function."""

    def log_decorator_info(func):
        @functools.wraps(func)
        def log_decorator_wrapper(self, *args, **kwargs):
            log = logging.getLogger(self.log.name)

            # Gather the args passed into the function
            args_passed_in_function = [repr(a) for a in args]

            # Gather the keyword args passed into the function
            kwargs_passed_in_function = [f"{k}={v!r}" for k, v in kwargs.items()]

            # Format the output a little
            formatted_arguments = "\n".join(args_passed_in_function + kwargs_passed_in_function)

            func_name = f"{self.__class__.__name__}.{func.__name__}"
            log.debug("%s INPUT Args:", func_name)
            log.debug("\t%s", formatted_arguments)
            try:
                # Capture the return value from the decorated function
                value = func(self, *args, **kwargs)
                log.debug("%s RETURNED %s", func_name, value)
            except:
                log.error("Exception: %s", str(sys.exc_info()[1]))
                raise
            return value

        return log_decorator_wrapper

    if _func is None:
        return log_decorator_info
    return log_decorator_info(_func)
