from server import mcp
from utils.file_reader import read_csv_summary
from mcp.types import CallToolResult, TextContent
import os


@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Summarize a CSV file by reporting its number of rows and columns.
    Args:
        filename: Name of the CSV file in the /data directory (e.g., 'sample.csv')
    Returns:
        A string describing the file's dimensions.
    """
    if not filename:
        print("Error: No filename provided.")
        return "Error: No filename provided."
    
    if not filename.endswith(".csv"):
        print(f"Error: Invalid file extension: {filename}")
        return "Error: Invalid file extension. Please provide a CSV file."

    print(f"Reading CSV file: {filename}")
    return read_csv_summary(filename)