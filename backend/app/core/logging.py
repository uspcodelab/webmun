import logging


def configure_logging(level: str) -> logging.Logger:
    """Configure the application logger once during startup."""
    logger = logging.getLogger("webmun")
    logger.setLevel(level.upper())
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        )
        logger.addHandler(handler)

    return logger
