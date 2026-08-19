from typing import TypedDict
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from models import ChatRequest


load_dotenv()


# State shared between LangGraph nodes
class ChatState(TypedDict):
    user_message: str
    response: str


# Create the LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)


# Node 1: Validate the user's input
def validate_input(state: ChatState):
    request = ChatRequest(
        user_message=state["user_message"]
    )

    return {
        "user_message": request.user_message
    }


# Node 2: Send the validated message to the LLM
def call_llm(state: ChatState):
    response = llm.invoke(state["user_message"])

    return {
        "response": response.content
    }


# Create the graph
graph_builder = StateGraph(ChatState)


# Add nodes
graph_builder.add_node("validate", validate_input)
graph_builder.add_node("llm", call_llm)


# Connect nodes
graph_builder.add_edge(START, "validate")
graph_builder.add_edge("validate", "llm")
graph_builder.add_edge("llm", END)


# Compile the graph
graph = graph_builder.compile()


# Test the graph
if __name__ == "__main__":
    result = graph.invoke({
        "user_message": "Explain artificial intelligence in simple words.",
        "response": ""
    })

    print("AI:", result["response"])