#https://langchain-ai.github.io/langgraph/reference/prebuilt/?h=react#create_react_agent

import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ['LANGSMITH_API_KEY'] = os.environ['PERSONAL_LANGSMITH_API_KEY']

from datetime import datetime
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

@tool
def check_weather(location: str, at_time: datetime | None = None) -> float:
    '''Return the weather forecast for the specified location.'''
    return f"It's always sunny in {location}"

tools = [check_weather]
model = ChatOpenAI(model="gpt-4o")

def state_modifier(state):
    state["messages"] = ['whats going on here?']
    return state

graph = create_react_agent(model, tools=tools, debug=True
                           # , state_modifier=state_modifier
                           )
# inputs = {"messages": [("user", "what is the weather in sf")]}
inputs = {"messages": [("user", "I wonder if we could have a socker match today in sf")]}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()