from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import ToolException
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from state import State
import os
from exception_handler import handle_ai_exception

load_dotenv()

#TODO: adicionar logging no projeto

async def resource_agent(state: State) -> State:
    """
    Resource agent is responsible for using the resources available to the agent.
    It uses the resources available to the agent.

    Args:
        state: State object containing the current state of the agent.

    Returns:
        State object containing the updated state of the agent.
    """
    
    model = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0.5,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    client = MultiServerMCPClient(
        {
            "simple_server": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )

    try:
        resources = await client.get_resources("simple_server")
        tools = await client.get_tools()
    except Exception as e:
        state["messages"].append(handle_ai_exception(e))
        return state
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", """
                Você é um atendente de uma empresa de tecnologia e atende os clientes em seu primeiro contato.
                Você deve coletar as informações necessárias e persistir no banco de dados para que o vendedor entre em contato com o cliente.

                Para isso, você deve utilizar as ferramentas disponíveis para coletar as informações necessárias para salvar o cliente.
            """),
            ("placeholder", "{messages}")
        ]
    )

    agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=False,
        prompt=prompt_template
    )

    try:
        response = await agent.ainvoke(
            {"messages": state["messages"]},
            config={
                "configurable": {
                    "max_iterations": 1,
                    "max_execution_time": 10,
                    "max_retries": 3
                }
            }
        )

        state["messages"].append(response["messages"][-1])
        return state
    
    #TODO: adicionar o tratamento de exception aqui
    except ToolException as te:
        print("Tool error:")
        print(f"Error type: {type(te).__name__}")
        print(f"Error message: {te}")
        raise te
    except Exception as e:
        import traceback
        print("Error during agent execution:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        print("Stack trace:")
        traceback.print_exc()
        raise e
