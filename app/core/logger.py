from pathlib import Path
import sys

from loguru import logger


LOG_DIR = Path(__file__).resolve().parents[2] / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logger():
    logger.remove()  # remove default logger

    fmt = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level} | "
        "{extra[fileName]} | "
        "{extra[data]} | "
        "{extra[request_id]} | "
        "{extra[task_id]} | "
        "{message}"
    )

    logger.add(
        sys.stdout,
        format=fmt,
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        LOG_DIR / "app_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        format=fmt,
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    return logger


class LogWrapper:
    def __init__(self, logger):
        self._logger = logger.bind(data="", fileName="", request_id="", task_id="")

    def _bind(self, data=None, fileName=None, request_id=None, task_id=None):
        extra = {}
        if data is not None:
            extra["data"] = data
        if fileName is not None:
            extra["fileName"] = fileName
        if request_id is not None:
            extra["request_id"] = request_id
        if task_id is not None:
            extra["task_id"] = task_id
        return self._logger.bind(**extra)

    def info(self, message=None, *, data=None, fileName=None, **kwargs):
        if message is None:
            message = data or ""
        return self._bind(data=data, fileName=fileName).info(message, **kwargs)

    def warning(self, message=None, *, data=None, fileName=None, **kwargs):
        if message is None:
            message = data or ""
        return self._bind(data=data, fileName=fileName).warning(message, **kwargs)

    def error(self, message=None, *, data=None, fileName=None, **kwargs):
        if message is None:
            message = data or ""
        return self._bind(data=data, fileName=fileName).error(message, **kwargs)

    def debug(self, message=None, *, data=None, fileName=None, **kwargs):
        if message is None:
            message = data or ""
        return self._bind(data=data, fileName=fileName).debug(message, **kwargs)

    def __getattr__(self, name):
        return getattr(self._logger, name)


# initialize global logger with default fields so output always includes them
log = LogWrapper(setup_logger())