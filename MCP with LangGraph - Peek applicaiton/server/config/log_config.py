import logging
import sys


class RobustFormatter(logging.Formatter):
    def __init__(self, fmt: str = None, datefmt: str = None, style: str = '%'):
        super().__init__(fmt, datefmt, style)
    
    def format(self, record: logging.LogRecord) -> str:
        try:
            return super().format(record)
        except Exception as e:
            try:
                return f"LOGGING_ERROR: {record.levelname} - {record.getMessage()} (Format error: {e})"
            except Exception:
                return f"CRITICAL_LOGGING_ERROR: {record.levelname} - Unable to format log message"


def setup_logging() -> None:    
    formatter = RobustFormatter(
        '%(levelname)s: %(asctime)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    root_logger.addHandler(console_handler)
    
    logging.getLogger("mcp").setLevel(logging.INFO)
    logging.getLogger("tools").setLevel(logging.INFO)
    logging.getLogger("utils").setLevel(logging.INFO)

if __name__ != "__main__":
    setup_logging()
