
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

model = ChatGroq(temperature=.7,model="llama3-70b-8192")

prompt = ChatPromptTemplate.from_messages([
    ('system', """
You are a problem statement creator. 
Rewrite the given idea for a problem statement for a programming question in simple terms 
clearly without ambiguity. Make it short and concise. 
"""),
    ('human',"add two numbers"),
    ('ai',"""
Given two integers a and b, find the sum of the two numbers.
"""),
    ('human',"{idea}")
])

idea2statement = prompt | model | StrOutputParser()

