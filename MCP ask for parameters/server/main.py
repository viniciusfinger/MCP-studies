from server import mcp
import tools.database_tools

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
