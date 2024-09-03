
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Now you can access the GROQ_API_KEY
groq_api_key = os.getenv('GROQ_API_KEY')

# If needed, pass the key explicitly
# Example:
# model = ChatGroq(temperature=.7, model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

model = ChatGroq(temperature=.7,model="llama-3.1-8b-instant")

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

