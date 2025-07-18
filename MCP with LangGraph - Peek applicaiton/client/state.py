from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class State(TypedDict):
    thread_id: str
    messages: Annotated[list[AnyMessage], add_messages]
    current_answer: str