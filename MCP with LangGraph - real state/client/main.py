from controller.chat_controller import router
from fastapi import FastAPI
import uvicorn
from config.log_config import setup_logging
from config.thread_id_middleware import ThreadIdMiddleware
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(ThreadIdMiddleware)
app.include_router(router, tags=["chat"])

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Error starting the server: {e}")
        raise e