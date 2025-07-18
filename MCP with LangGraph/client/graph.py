from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import StateGraph, CompiledStateGraph, START, END
from state import State
from agent.attendance_agent import attendance_agent

def create_graph() -> CompiledStateGraph:

    checkpointer = MemorySaver()

    graph = StateGraph(State)

    graph.add_node("attendance", attendance_agent)

    graph.add_edge(START, "attendance")
    graph.add_edge("attendance", END)

    return graph.compile(checkpointer=checkpointer)