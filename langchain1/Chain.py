import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

openai.api_key = os.environ['OPENAI_API_KEY']

import pandas as pd
df = pd.read_csv('/Users/hed-bar-nissan/Downloads/chain_tutorial_data.csv')
# print (df.head())

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(temperature=0.9)
prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe \
    a company that makes {product}?"
)

chain = LLMChain(llm=llm, prompt=prompt)

product = "A T-shirt that is made of recycled plastic bottles"
for i in range(5):
    res = chain.run(product)
    print(res)