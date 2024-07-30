from langchain.output_parsers import BooleanOutputParser
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

model = ChatGroq(temperature=0, model="llama-3.1-8b-instant")
prompt = ChatPromptTemplate.from_template(
    """
Check if the two given problem statements are exactly the same.
Respond with YES or NO and nothing else.

Statement 1: {statement1}
Statement 2: {statement2}
"""
)

equal_check_chain = prompt | model | BooleanOutputParser()

# TODO: implement batch prompt to reduce token usage.
prompt = ChatPromptTemplate.from_template(
    """
Check if the two given problem statements are exactly the same.
Respond with YES or NO and nothing else.

Statement 1: {statement1}
Statement 2: {statement2}
"""
)
