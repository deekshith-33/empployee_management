import json
import logging
import sys
from datetime import datetime, timezone


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Include any extra structured fields attached to the log record
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_payload.update(record.extra_data)

        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_payload)


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("emp_mgmt")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)

    logger.propagate = False
    return logger


logger = setup_logging()