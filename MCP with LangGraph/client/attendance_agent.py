from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from state import State
import asyncio
import os

load_dotenv()

async def attendance_agent(state: State):

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

    tools = await client.get_tools()

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
                    "max_execution_time": 30
                }
            }
        )

        state["messages"].append(response["messages"][-1])

        return state
    except Exception as e:
        print(e)
