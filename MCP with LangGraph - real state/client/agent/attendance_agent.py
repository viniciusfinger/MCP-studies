from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from state import State
import os
from exception_handler import handle_agent_exception
import logging
from config.log_config import get_thread_id
from datetime import datetime


load_dotenv()
logger = logging.getLogger(__name__)

async def attendance_agent(state: State) -> State:
    """
    Attendance agent is responsible for collecting the necessary information to save the client.
    It uses the tools available to collect the information.

    Args:
        state: State object containing the current state of the agent.

    Returns:
        State object containing the updated state of the agent.
    """
    logger.debug(f"Starting attendance agent")
    model = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0.5,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    thread_id = get_thread_id()
    logger.debug(f"Thread ID obtained: {thread_id}")

    headers = {}
    if thread_id:
        headers["X-Thread-Id"] = thread_id
        logger.debug(f"Added thread_id to headers: {thread_id}")

    client = MultiServerMCPClient(
        {
            "simple_server": {
                "url": os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp"),
                "transport": "streamable_http",
                "headers": headers
            }
        }
    )

    try:
        tools = await client.get_tools()

        prompt = ChatPromptTemplate.from_messages(
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
            prompt=prompt
        )

        logger.debug(f"Invoking agent")
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
        logger.debug(f"Successfully invoked agent")

        state["messages"].append(response["messages"][-1])
        return state
    
    except Exception as e:
        treated_message = handle_agent_exception(e, logger)
        state["messages"].append(treated_message)
        return state
