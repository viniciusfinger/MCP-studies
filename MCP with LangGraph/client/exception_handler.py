from langchain_core.messages import AnyMessage
from httpx import ConnectError
from langchain_core.messages import SystemMessage
from logging import Logger
from langchain_core.tools import ToolException


def handle_agent_exception(e: Exception, logger: Logger) -> AnyMessage:
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
        logger.error(f"Tool error: {e.tool_name}")
    else:
        logger.error(f"Unexpected error: {e}")
    return SystemMessage(content="Sorry, I have an internal problem. Please try again later.")