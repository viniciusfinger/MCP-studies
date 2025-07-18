import json
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from config.log_config import set_thread_id

logger = logging.getLogger(__name__)

class ThreadIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        thread_id = None
        
        if request.url.path == "/chat":
            try:
                body = await request.body()
                if body:
                    data = json.loads(body)
                    thread_id = data.get("thread_id")
                    
                    if thread_id:
                        set_thread_id(thread_id)
                        logger.debug(f"Thread ID extracted from request: {thread_id}")
                    else:
                        logger.warning("Thread ID not found in request")
                        
            except json.JSONDecodeError:
                logger.error("Error decoding JSON from request")
            except Exception as e:
                logger.error(f"Error processing request: {e}")
        
        response = await call_next(request)
        
        return response