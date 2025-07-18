from server import mcp
import tools.database_tools
from config.log_config import setup_logging
import logging

logger = logging.getLogger(__name__)
setup_logging()

if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
        logger.info("Server started successfully")
    except Exception as e:
        logger.error(f"Error starting the server: {e}")
        raise e
