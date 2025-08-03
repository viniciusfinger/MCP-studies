import logging

from server import mcp
from mcp.types import CallToolResult, TextContent
from mcp.server.fastmcp import Context

from utils.context_utils import get_thread_id

logger = logging.getLogger(__name__)


@mcp.tool()
def find_space(context: Context, city: str, state: str, bathrooms: int, bedrooms: int) -> CallToolResult:
    """
    Use this tool to find spaces by city.
    
    Args:
        city: The city to search for spaces.
        state: The state to search for spaces.
        bathrooms: The number of bathrooms to search for spaces.
        bedrooms: The number of bedrooms to search for spaces.

    Returns:
        A list of spaces that match the criteria.
    """
    #TODO: implement the database query

    thread_id = get_thread_id(context)
    logging.info(f"Thread_id: {thread_id} - Finding space in {city}, {state}, {bathrooms} bathrooms, {bedrooms} bedrooms")

    return []
