import logging


LOG_FORMAT = (
    "%(asctime)s level=%(levelname)s logger=%(name)s "
    "message=\"%(message)s\""
)


def configure_logging(level_name: str = "INFO") -> None:
    level = getattr(logging, level_name.upper(), logging.INFO)

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root.addHandler(handler)
