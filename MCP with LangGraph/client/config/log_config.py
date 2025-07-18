import logging
import contextvars
from typing import Optional

thread_id_context = contextvars.ContextVar('thread_id', default=None)


class RobustFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'thread_id'):
            thread_id = thread_id_context.get()
            record.thread_id = thread_id if thread_id else "N/A"
        return super().format(record)


class ThreadIdFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'thread_id'):
            thread_id = thread_id_context.get()
            if thread_id:
                record.thread_id = thread_id
            else:
                record.thread_id = "N/A"
        return True


def setup_logging():
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    handler = logging.StreamHandler()
    
    formatter = RobustFormatter(
        '%(levelname)s: %(asctime)s - %(name)s - [thread_id: %(thread_id)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler.addFilter(ThreadIdFilter())
    handler.setFormatter(formatter)
    
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    mcp_loggers = [
        "mcp",
        "mcp.client",
        "mcp.client.streamable_http"
    ]
    
    for logger_name in mcp_loggers:
        mcp_logger = logging.getLogger(logger_name)
        mcp_logger.setLevel(logging.INFO)
        for handler in mcp_logger.handlers[:]:
            mcp_logger.removeHandler(handler)
        mcp_handler = logging.StreamHandler()
        mcp_handler.addFilter(ThreadIdFilter())
        mcp_handler.setFormatter(formatter)
        mcp_logger.addHandler(mcp_handler)
        mcp_logger.propagate = False


def set_thread_id(thread_id: str):
    thread_id_context.set(thread_id)


def get_thread_id() -> Optional[str]:
    return thread_id_context.get()