from fastapi import APIRouter
from graph import create_graph
from langchain_core.messages import HumanMessage

router = APIRouter()
graph = create_graph()

#TODO: create a chat interaction model or use a existing one
@router.post("/chat")
async def chat(message: str):
    config = {
        "configurable": {
            "thread_id": "123"
        }
    
    }

    response = await graph.ainvoke(
                {
                    "messages": [HumanMessage(content=message)]
                }, 
                config
            )
    
    print("AI:", response["messages"][-1].content)

    return {"message": response["messages"][-1].content}