from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
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

                Para isso, você deve utilizar as seguintes ferramentas disponíveis para coletar as informações necessárias para salvar o cliente:

                1. **tool_save_user_data**: 
                Utilize esta ferramenta para coletar informações básicas do cliente, como nome, email, telefone e cidade e salvar os dados do cliente.
                    - **Argumentos:**  
                        - `name`: (Opcional): Nome do cliente.
                        - `phone`: (Opcional): O telefone do cliente.
                        - `email`: (Opcional): O email do cliente.
                        - `city`: (Opcional): A cidade do cliente.        

                    - **Comportamento esperado:**
                        Se solicitado, a ferramenta pode retornar mensagens para pedir mais informações ou fornecer as informações já obtidas.        
                        Caso necessário, peça mais informações para extrair um entendimento robusto e adequado. 
                        Seja claro, legal e gentil.
                        Responda na língua portuguesa do Brasil, não use markdown.
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
