from fastapi import APIRouter
from graph import create_graph
from langchain_core.messages import HumanMessage
from model.chat_message import ChatMessage
from datetime import datetime
from model.message_role import MessageRole
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
graph = create_graph()

@router.post("/chat")
async def chat(chat_message: ChatMessage) -> ChatMessage:
    logger.info(f"Received chat message: {chat_message.content}")
    
    config = {
        "configurable": {
            "thread_id": chat_message.thread_id
        }
    }

    response = await graph.ainvoke(
                {
                    "messages": [HumanMessage(content=chat_message.content)]
                },
                config
            )
    
    last_ai_message = response["messages"][-1]
    logger.info(f"AI answer: {last_ai_message.content}")
    
    return ChatMessage(
        thread_id=chat_message.thread_id,
            content=last_ai_message.content,
            role=MessageRole.from_str(last_ai_message.type),
            timestamp=datetime.now()
        )