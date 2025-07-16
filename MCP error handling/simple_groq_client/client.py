from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

import os

load_dotenv()

async def call_client():

    model = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
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
    
    prompt = """
    Você é um assistente especializado em análise de dados.
        
        REGRAS IMPORTANTES:
        1. Use APENAS o nome exato do arquivo mencionado pelo usuário
        2. Se o arquivo não for CSV ou Parquet, informe que não pode analisar
        3. Se a ferramenta retornar erro, aceite e explique ao usuário
        4. NÃO invente nomes de arquivos
        5. NÃO tente novamente após erro
        6. Responda sempre em português, de forma clara e direta
        """

    agent = create_react_agent(
        model,
        tools
    )

    messages = [
            SystemMessage(content=prompt),
            HumanMessage(content="Resuma o arquivo sample.csv")
        ]
    try:
        response = await agent.ainvoke(
            {"messages": messages},
            config={
                "configurable": {
                    "max_iterations": 1,
                    "max_execution_time": 30
                }
            }
        )
        
        print(response["messages"][-1].content)
    except Exception as e:
        print(e)
