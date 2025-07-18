from controller.chat_controller import router
from fastapi import FastAPI
import uvicorn
from config.log_config import setup_logging

setup_logging()

app = FastAPI()
app.include_router(router, tags=["chat"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)