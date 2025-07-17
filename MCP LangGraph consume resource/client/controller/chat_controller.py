from fastapi import APIRouter
from graph import create_graph
from langchain_core.messages import HumanMessage
from chat_message import ChatMessage
from datetime import datetime
from message_role import MessageRole


router = APIRouter()
graph = create_graph()

@router.post("/chat")
async def chat(chat_message: ChatMessage) -> ChatMessage:
    config = {
        "configurable": {
            "thread_id": chat_message.session_id
        }
    }

    response = await graph.ainvoke(
                {
                    "messages": [HumanMessage(content=chat_message.message)]
                }, 
                config
            )
    
    last_message = response["messages"][-1]
    
    return ChatMessage(
        session_id=chat_message.session_id,
            message=last_message.content,
            role=MessageRole.from_str(last_message.type),
            timestamp=datetime.now()
        )