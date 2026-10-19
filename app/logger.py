import logging
import os
from app.config import config


def setup_logger(name: str = "employee_app") -> logging.Logger:
    """Configures and returns a logger instance with file and console handlers."""
    logger = logging.getLogger(name)

    # Convert string level to logging attribute (e.g. "INFO" -> logging.INFO)
    log_level = getattr(logging, config.LOG_LEVEL, logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        # Ensure log directory exists
        os.makedirs(config.LOG_FILE.parent, exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File Handler (Persists logs to disk)
        file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

        # Stream Handler (Outputs logs to console)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()