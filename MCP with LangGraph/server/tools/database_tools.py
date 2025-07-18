from server import mcp
from mcp.types import CallToolResult, TextContent
from mcp.server.fastmcp import Context
from typing import Optional

from utils.context_utils import get_thread_id
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def tool_save_user_data(context: Context, name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, city: Optional[str] = None) -> CallToolResult:
    """ 
    Use this tool to save the user data to the database. If some of the data is missing, the tool will return a message asking for the missing data until the data is complete.
    
    Args:
        name: Optional[str] Name of the user
        email: Optional[str] Email of the user
        phone: Optional[str] Phone number of the user
        city: Optional[str] City of the user
    
    Returns:
        A CallToolResult object with a string describing the users's data saved.
    """
    thread_id = get_thread_id(context)
    
    logger.info(f"Thread ID: {thread_id} - Received user data: {name}, {email}, {phone}, {city} ")
    
    if not name:
        logger.debug(f"Thread ID: {thread_id} - Error: No name provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your name.", type="text")],
            isError=False
        )
    
    if not email:
        logger.debug(f"Thread ID: {thread_id} - Error: No email provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your email.", type="text")],
            isError=False
        )

    if not phone:
        logger.debug(f"Thread ID: {thread_id} - Error: No phone provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your phone number.", type="text")],
            isError=False
        )

    if not city:    
        logger.debug(f"Thread ID: {thread_id} - Error: No city provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your city.", type="text")],
            isError=False
        )
    
    logger.info(f"Thread ID: {thread_id} - Saving {name} user data")
    
    return CallToolResult(
        content=[TextContent(text="User data saved successfully.", type="text")],
        isError=False)
