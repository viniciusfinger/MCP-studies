from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import ToolException
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from state import State
import os
from httpx import ConnectError
try:
    import httpcore
    HttpCoreConnectError = httpcore.ConnectError
except ImportError:
    HttpCoreConnectError = None

load_dotenv()

async def attendance_agent(state: State) -> State:
    """
    Attendance agent is responsible for collecting the necessary information to save the client.
    It uses the tools available to collect the information.

    Args:
        state: State object containing the current state of the agent.

    Returns:
        State object containing the updated state of the agent.
    """

    # model = ChatGroq(
    #     model_name="llama-3.3-70b-versatile",
    #     temperature=0.5,
    #     api_key=os.getenv("GROQ_API_KEY")
    # )
    
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
        tools = await client.get_tools()
    #TODO: create a exception handler 
    except Exception as e:
        if hasattr(e, 'exceptions'):
            for exc in e.exceptions:
                if isinstance(exc, ConnectError) or isinstance(exc, HttpCoreConnectError):
                    print("Connection error: unable to connect to MCP service at http://localhost:8000/mcp.")
                    print("Check if the MCP service is running and accessible.")
                    
                    from langchain_core.messages import SystemMessage
                    state["messages"].append(
                        SystemMessage(content="Sorry, I have an internal problem. Please try again later.")
                    )
                    return state
                else:
                    print(f"Error: {e}")
                    raise e

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
