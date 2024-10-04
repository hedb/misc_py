#https://langchain-ai.github.io/langgraph/reference/prebuilt/?h=react#create_react_agent

import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ['LANGSMITH_API_KEY'] = os.environ['PERSONAL_LANGSMITH_API_KEY']

from datetime import datetime
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

@tool
def evaluator(location: str, at_time: datetime | None = None) -> float:
    '''Accepts a question, a detailed answer and retuns a boolean indicating if the answer is correct.'''
    return True

tools = [evaluator]
model = ChatOpenAI(model="gpt-4o")

graph = create_react_agent(model, tools=tools, debug=True)
inputs = {"messages": [("user",
    "What is the second derivative at 0 Of sin (1/x)*x^3")]}

for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()