from langchain_core.messages import AnyMessage
from httpx import ConnectError
from langchain_core.messages import SystemMessage
import logging
from langchain_core.tools import ToolException

logger = logging.getLogger(__name__)

def handle_agent_exception(e: Exception) -> AnyMessage:
    """
    Log and handle AI agent exceptions.

    Args:
        e: The exception to handle.

    Returns:
        A Message object with a treated message to return to the user.
    """

    if hasattr(e, 'exceptions'):
        for exc in e.exceptions:
            if isinstance(exc, ConnectError):
                logger.error(f"Connection error: unable to connect to MCP service, please check if the MCP service is running and accessible: {exc.request.method} {exc.request.url}")
            else:
                logger.error(f"Unexpected error: {exc}")
    elif isinstance(e, ToolException):
        logger.error(f"Tool error: {e}")
    else:
        logger.error(f"Unexpected error: {e}")
    return SystemMessage(content="Sorry, I have an internal problem. Please try again later.")