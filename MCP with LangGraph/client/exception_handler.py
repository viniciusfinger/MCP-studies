from langchain_core.messages import BaseMessage
from httpx import ConnectError
from langchain_core.messages import SystemMessage

#TODO: rename this function 
def handle_ai_exception(e: Exception) -> BaseMessage:
    """
    Handle AI exceptions.

    Args:
        e: The exception to handle.

    Returns:
        A BaseMessage object with a treated message to return to the user.
    """

    if hasattr(e, 'exceptions'):
            for exc in e.exceptions:
                if isinstance(exc, ConnectError):
                    print("Connection error: unable to connect to MCP service at http://localhost:8000/mcp.")
                    print("Check if the MCP service is running and accessible.")
                    
                    return SystemMessage(content="Sorry, I have an internal problem. Please try again later.")
                else:
                    print("Add logs here")
                    return SystemMessage(content="Sorry, I have an internal problem. Please try again later.")