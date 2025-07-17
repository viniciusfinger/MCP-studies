from server import mcp
from utils.file_reader import read_csv_summary
from mcp.types import CallToolResult, TextContent, ReadResourceResult, TextResourceContents
import os
from typing import Optional

@mcp.tool()
def tool_save_user_data(name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, city: Optional[str] = None) -> CallToolResult:
    print(f"Saving user data: {name}, {email}, {phone}, {city}")
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
        print("Error: No name provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your name.", type="text")],
            isError=False
        )
    
    if not email:
        print("Error: No email provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your email.", type="text")],
            isError=False
        )

    if not phone:
        print("Error: No phone provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your phone number.", type="text")],
            isError=False
        )

    if not city:    
        print("Error: No city provided.")
        return CallToolResult(
            content=[TextContent(text="Please provide your city.", type="text")],
            isError=False
        )
    
    print(f"Saving user data: {name}, {email}, {phone}, {city}")
    return CallToolResult(
        content=[TextContent(text="User data saved successfully.", type="text")],
        isError=False)

@mcp.resource("text://hello_world")
def resource_hello_world():
    return "Hello, world!"