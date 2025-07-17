from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import StateGraph, CompiledStateGraph, START, END
from state import State
from resource_agent import resource_agent

def create_graph() -> CompiledStateGraph:

    checkpointer = MemorySaver()

    graph = StateGraph(State)

    graph.add_node("resource", resource_agent)

    graph.add_edge(START, "resource")
    graph.add_edge("resource", END)

    return graph.compile(checkpointer=checkpointer)