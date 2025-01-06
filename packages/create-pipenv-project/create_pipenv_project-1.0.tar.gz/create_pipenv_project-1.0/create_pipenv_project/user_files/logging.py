import os
import time
import logging
import inspect
from typing import Optional, Union, Iterator, Any
from contextlib import contextmanager
from PACKAGE_NAME.environ import DEFAULT_LOGGING_LEVEL, DEFAULT_FILE_LOGGING

_formatter = logging.Formatter(
    "\033[93m%(levelname).1s\033[0m \033[95m%(asctime)s\033[0m "
    "\033[91m%(name)s\033[0m %(message)s",
    datefmt="%y%m%d-%H%M%S",
)


def get_logger(
    name: str,
    *,
    level: str = DEFAULT_LOGGING_LEVEL,
    file_logging: bool = DEFAULT_FILE_LOGGING,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(_formatter)
        logger.addHandler(stream_handler)

        if file_logging:
            os.makedirs("logs", exist_ok=True)
            file_handler = logging.FileHandler(os.path.join("logs", "all.txt"))
            file_handler.setFormatter(_formatter)
            logger.addHandler(file_handler)

    for handler in logger.handlers:
        handler.setLevel(level)

    return logger


def trace(msg: Any = None) -> None:
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    logger = get_logger(f"Trace {caller.filename}")

    if msg is None:
        logger.debug(f"Line {caller.lineno}")
    else:
        logger.debug(f"Line {caller.lineno}: {msg}")


class MeasureTime:
    @staticmethod
    @contextmanager
    def wall_clock(
        logger_name: Union[str, logging.Logger],
        block_name: Optional[str] = None,
    ) -> Iterator[dict[str, float | None]]:
        if isinstance(logger_name, logging.Logger):
            logger = logger_name
        else:
            logger = get_logger(logger_name)

        msg = block_name or logger.name
        logger.debug(f"Measuring wall clock time of {msg}...")

        start_time = time.time()
        res: dict[str, float | None] = {
            "start_time": start_time,
            "end_time": None,
            "delta": None,
        }
        yield res

        end_time = time.time()
        delta = end_time - start_time

        res["end_time"] = end_time
        res["delta"] = delta

        logger.debug(f"Wall clock time of {msg}: {round(delta, 2)}s")

    @staticmethod
    @contextmanager
    def cpu(
        logger_name: Union[str, logging.Logger],
        block_name: Optional[str] = None,
    ) -> Iterator[dict[str, float | None]]:
        if isinstance(logger_name, logging.Logger):
            logger = logger_name
        else:
            logger = get_logger(logger_name)

        msg = block_name or logger.name
        logger.debug(f"Measuring CPU time of {msg}...")

        start_time = time.perf_counter()
        res: dict[str, float | None] = {
            "start_time": start_time,
            "end_time": None,
            "delta": None,
        }
        yield res

        end_time = time.perf_counter()
        delta = end_time - start_time

        res["end_time"] = end_time
        res["delta"] = delta

        logger.debug(f"CPU time of {msg}: {round(delta, 2)}s")
