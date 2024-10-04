#https://langchain-ai.github.io/langgraph/reference/prebuilt/?h=react#create_react_agent

import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ['LANGSMITH_API_KEY'] = os.environ['PERSONAL_LANGSMITH_API_KEY']

from datetime import datetime
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

@tool
def evaluator(question: str, answer:str, calculation_steps: list[str]) -> bool:
    '''This is an evaluator tool.
It accepts a question,
a final answer,
and a list of calculation steps that brought to this answer.
It returns a boolean indicating if the answer is correct.

The actual verification is done on the calculation steps so the list needs to be exhaustive
'''
    return True


def request_for_verification(state):
    state["messages"][-1].content = state["messages"][-1].content + "\n please use the evaluator tool to verify the answer."
    return state["messages"]

tools = [evaluator]
model = ChatOpenAI(model="gpt-4o")

graph = create_react_agent(model, tools=tools, state_modifier=request_for_verification, debug=True)
inputs = {"messages": [("user",
"""
bike rider goes on a ramp of length 2 meters at a speed of 10 kmh and an angle of 30 degress of ground
there a barrier distance 1 meter from the ramp, assuming the rider passes the barrier - what's the maximum height of the barrier ?
""")]}

for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()