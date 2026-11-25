from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
    
def chatbot(state: State):
    print(f"State in chatbot node: {state}")
    return {"messages": "Hi, This is a message from chatbot node!"}


def sampleNode(state: State):
    print(f"State in sampleNode node: {state}")
    return {"messages": "Message from sample node!"}
    
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleNode", sampleNode)

#  state = { "messages": ["Hey there"]}
#  Node runs - chatbot(state: ["hey there"]) -> ["Hi, this is a message from chatbot"]
#  state = { "messages": ["Hey there", "Hi, this is a message from chatbot"]}

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleNode")
graph_builder.add_edge("sampleNode", END)

# (START) -> (chatbot) -> (sampleNode) -> (END)


graph = graph_builder.compile()


updated_state = graph.invoke({"messages": ["Hey there"]})
print(f"Updated state after graph invocation: {updated_state}")