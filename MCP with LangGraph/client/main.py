from controller.chat_controller import router
from fastapi import FastAPI
import uvicorn

app = FastAPI() 
app.include_router(router, tags=["chat"])

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8080)