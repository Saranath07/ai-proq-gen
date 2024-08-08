from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableAssign
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_groq import ChatGroq

import json
import random

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a test case creator. Generate {n_testcases} test cases for the given problem statement in {lang}.
Each test case should include input and expected output.
     Use the function template to generate the test cases. Input should have a suffix code to execute the function. print the repr of the object returned.
Respond only in JSON format. Do not include any additional text.
"""),
    ("human", "Problem: Given two integers a and b, find their sum.\nn_testcases: 3\n soltuion : def add(a, b):\n    return a + b\n"),
    ("ai", """[
        
    {{
        "input": "print(repr(add(5,7)))",
        "output": "12"
    }},
     {{
        "input": "print(repr(add(10,20)))",
        "output": "30"
     }}
]

"""),
    ("human", "Problem: {problem_statement}\nn_testcases: {n_testcases}\n solution: {solution}\n"),
])

model = ChatGroq(temperature=0.7, model="llama3-70b-8192")

test_case_processor = model | JsonOutputParser()



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


test_case_chain = get_test_case_chain(
    lang="Python",
    n_testcases=4
)


result = test_case_chain.invoke({"problem_statement":"Write a function that takes a string and returns its reverse.", "solution":"def reverse_string(s):\n    return s[::-1]"})
print(json.dumps(result, indent=2))