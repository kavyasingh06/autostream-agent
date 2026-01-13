import operator
from typing import Annotated, TypedDict, Union
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver

from agent.intent import detect_intent
from agent.llm import llm
from agent.rag import load_rag
from agent.tools import mock_lead_capture

db = load_rag()

# 1. STATE DEFINITION
# We use 'add_messages' to handle the conversation history automatically
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str
    name: str
    email: str
    platform: str

# 2. NODES
''''
def intent_node(state: AgentState):
    last_msg = state["messages"][-1].content
    intent = detect_intent(last_msg, llm)
    return {"intent": intent}
    '''
# ... keep your imports ...

def intent_node(state: AgentState):
    last_msg = state["messages"][-1].content
    current_intent = state.get("intent")
    
    # --- FORM FILLING LOGIC ---
    # If we are already in 'high_intent' mode, the user is answering a question.
    # We must CAPTURE their answer before running detection again.
    if current_intent == "high_intent":
        # Check what is missing and fill it with the user's message
        if not state.get("name"):
            return {"name": last_msg, "intent": "high_intent"}
        elif not state.get("email"):
            return {"email": last_msg, "intent": "high_intent"}
        elif not state.get("platform"):
            return {"platform": last_msg, "intent": "high_intent"}

    # --- NORMAL DETECTION ---
    # If we are not in high_intent, run standard detection
    intent = detect_intent(last_msg, llm)
    return {"intent": intent}

# ... keep the rest of your graph.py the same ...

def rag_node(state: AgentState):
    query = state["messages"][-1].content
    docs = db.similarity_search(query, k=1)
    answer = docs[0].page_content if docs else "Check our website for details."
    return {"messages": [AIMessage(content=f"Here is what I found: {answer}")]}

def lead_node(state: AgentState):
    # Check what we already have
    name = state.get("name")
    email = state.get("email")
    platform = state.get("platform")

    if not name:
        msg = "I can help you get started! What is your full name?"
    elif not email:
        msg = f"Thanks {name}. What is your email address?"
    elif not platform:
        msg = "Which platform do you create content for (e.g., YouTube)?"
    else:
        # We have everything, run tool
        mock_lead_capture(name, email, platform)
        msg = "Success! I've captured your lead details."
    
    return {"messages": [AIMessage(content=msg)]}

def greeting_node(state: AgentState):
    return {"messages": [AIMessage(content="Hello! I'm the AutoStream assistant. How can I help?")]}

# 3. ROUTER
def router(state: AgentState):
    intent = state.get("intent")
    if intent == "product": return "rag"
    if intent == "high_intent": return "lead"
    return "greeting"

# 4. BUILD GRAPH
builder = StateGraph(AgentState)

builder.add_node("intent_node", intent_node)
builder.add_node("rag", rag_node)
builder.add_node("lead", lead_node)
builder.add_node("greeting", greeting_node)

# Connect Start to Intent
builder.add_edge(START, "intent_node")

# Connect Intent to Others
builder.add_conditional_edges("intent_node", router)

# Connect Others to End
builder.add_edge("rag", END)
builder.add_edge("lead", END)
builder.add_edge("greeting", END)

# Compile
memory = MemorySaver()
app = builder.compile(checkpointer=memory)