from langgraph.checkpoint.memory import MemorySaver
from graph_builder import *

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Specify an ID for the thread
config = {"configurable": {"thread_id": "abc123"}}