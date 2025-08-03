import logging
from server import mcp
from tools.space_tools import find_space
from config.log_config import setup_logging
from config.database_config import initialize_database

logger = logging.getLogger(__name__)
setup_logging()


if __name__ == "__main__":
    try:
        initialize_database()

        mcp.run(transport="streamable-http")
    except Exception as e:
        logger.error(f"Error starting the server: {e}")
        raise e
