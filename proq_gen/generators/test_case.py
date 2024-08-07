from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableAssign
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

import json
import random

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a test case creator. Generate {n_testcases} test cases for the given problem statement in {lang}.
Each test case should include input and expected output.
Respond only in JSON format. Do not include any additional text.
"""),
    ("human", "Problem: Given two integers a and b, find their sum.\nn_testcases: 3"),
    ("ai", """
[
    input: [1, 2], output: 3,
    input: [-5, 10], output: 5,
    input: [0, 0], output: 0
]
"""),
    ("human", "Problem: {problem_statement}\nn_testcases: {n_testcases}")
])

model = ChatGroq(temperature=0.7, model="llama3-70b-8192")

test_case_processor = model | StrOutputParser()

def get_test_case_chain(lang, n_testcases):
    return (
        RunnableAssign(
            {
                "n_testcases": lambda x: n_testcases,
                "lang": lambda x: lang
            }
        )
        | prompt
        | test_case_processor
    )


# test_case_chain = get_test_case_chain(
#     lang="Python",
#     n_testcases=4
# )


# result = test_case_chain.invoke({"problem_statement":"Write a function that takes a string and returns its reverse."})
# print(json.dumps(result, indent=2))