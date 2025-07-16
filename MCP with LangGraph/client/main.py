from graph import create_graph
from langchain_core.messages import HumanMessage
import asyncio

async def main():
    graph = create_graph()

    config = {
        "configurable": {
            "thread_id": "123"
        }
    }

    while True:
        try:
            user_input = str(input("User: "))
            response = await graph.ainvoke(
                {"messages": [HumanMessage(content=user_input)]}, 
                config
            )
            print("AI:", response["messages"][-1].content)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
