import logging
from flask import Flask


app: Flask = Flask(__name__)
logger: logging.Logger = app.logger


def run_logging() -> None:
    clear_log_file()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s   (%(name)s)   %(message)s",
        filename='debug.log',
    )
    logger.propagate = False


def debug(msg: str, *args) -> None:
    logger.debug(msg, *args)


def inform(msg: str, *args) -> None:
    logger.info(msg, *args)


def warn(msg: str, *args) -> None:
    logger.warning(msg, *args)


def error(msg: str, *args) -> None:
    logger.error(msg, *args)


def exception(msg: str, *args) -> None:
    logger.exception(msg, *args)


def critical(msg: str, *args) -> None:
    logger.critical(msg, *args)


def clear_log_file() -> None:
    with open('debug.log', "w"):
        pass
