import logging
import json
import sys

from config import SERVICE_NAME


class JsonFormatter(logging.Formatter):
    """Structured JSON log formatter - Module 13.2.

    Every line is one JSON object so it can be shipped straight into
    ELK / Splunk / Loki without a parsing layer.
    """

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": SERVICE_NAME,
            "request_id": getattr(record, "request_id", None),
            "trace_id": getattr(record, "trace_id", None),
            "route": getattr(record, "route", None),
            "status_code": getattr(record, "status_code", None),
            "duration_ms": getattr(record, "duration_ms", None),
        }
        return json.dumps({k: v for k, v in payload.items() if v is not None})


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("orders_api")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = configure_logging()
