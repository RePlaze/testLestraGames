import structlog
import logging
from typing import Dict, Any
from datetime import datetime

def configure_logging(level: str = "INFO") -> None:
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True
    )

    logging.basicConfig(
        format="%(message)s",
        level=level,
        handlers=[logging.StreamHandler()]
    )

def get_logger(name: str) -> structlog.BoundLogger:
    return structlog.get_logger(name)

class PerformanceLogger:
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger
        self.start_time: Dict[str, datetime] = {}

    def start_timer(self, operation: str) -> None:
        self.start_time[operation] = datetime.utcnow()

    def end_timer(self, operation: str, **kwargs: Any) -> None:
        if operation in self.start_time:
            duration = (datetime.utcnow() - self.start_time[operation]).total_seconds()
            self.logger.info(
                "operation_completed",
                operation=operation,
                duration_seconds=duration,
                **kwargs
            )
            del self.start_time[operation] 