from server import mcp
from mcp.types import CallToolResult, TextContent
from typing import Optional
import logging

@mcp.tool()
def tool_save_user_data(name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, city: Optional[str] = None) -> CallToolResult:
    logging.debug(f"Received user data: {name}, {email}, {phone}, {city}")
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
    if not name:
        logging.debug("Error: No name provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your name.", type="text")],
            isError=False
        )
    
    if not email:
        logging.debug("Error: No email provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your email.", type="text")],
            isError=False
        )

    if not phone:
        logging.debug("Error: No phone provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your phone number.", type="text")],
            isError=False
        )

    if not city:    
        logging.debug("Error: No city provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your city.", type="text")],
            isError=False
        )
    
    logging.debug(f"Saving user data: {name}, {email}, {phone}, {city}")
    return CallToolResult(
        content=[TextContent(text="User data saved successfully.", type="text")],
        isError=False)
