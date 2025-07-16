from server import mcp
from utils.file_reader import read_csv_summary
from mcp.types import CallToolResult, TextContent
import os


@mcp.tool()
def summarize_csv_file(filename: str) -> CallToolResult:
    """
    Summarize a CSV file by reporting its number of rows and columns.
    Args:
        filename: Name of the CSV file in the /data directory (e.g., 'sample.csv')
    Returns:
        A CallToolResult object with a string describing the file's dimensions.
    """
    if not filename:
        print("Error: No filename provided.")
        return CallToolResult(
            content=[TextContent(text="Error: No filename provided.", type="text")],
            isError=True
        )
    
    if not filename.endswith(".csv"):
        print(f"Error: Invalid file extension: {filename}")
        return CallToolResult(
            content=[TextContent(text="Error: Invalid file extension. Please provide a CSV file.", type="text")],
            isError=True
        )

    file_path = os.path.join("data", filename)
    if not os.path.isfile(file_path):
        print(f"Error: The file '{filename}' does not exist in the 'data' directory.")
        return CallToolResult(
            content=[TextContent(text=f"Error: The file '{filename}' does not exist in the 'data' directory.", type="text")],
            isError=True
        )

    print(f"Reading CSV file: {filename}")
    response = read_csv_summary(filename)
    return CallToolResult(
        content=[TextContent(text=response, type="text")],
        isError=False
    )
