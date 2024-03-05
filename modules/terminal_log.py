import logging


log_file = "debug.log"


def run_logging() -> None:
    clear_log_file()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s   (%(name)s)   %(message)s",
        datefmt="[%m/%d/%y %h:%m:%s]",
        filename=log_file,
    )


def debug(msg: str, *args) -> None:
    logging.debug(msg, *args)


def inform(msg: str, *args) -> None:
    logging.info(msg, *args)


def warn(msg: str, *args) -> None:
    logging.warning(msg, *args)


def log_error(msg: str, *args) -> None:
    logging.error(msg, *args)


def log_exception(msg: str, *args) -> None:
    logging.exception(msg, *args)


def log_critical(msg: str, *args) -> None:
    logging.critical(msg, *args)


def clear_log_file() -> None:
    with open(log_file, "w"):
        pass


if __name__ == "__main__":
    run_logging()