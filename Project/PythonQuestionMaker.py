# LangChain imports

from langchain.chains import SimpleSequentialChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from langchain_groq import ChatGroq

import ast
import random
import json
import os
import sys


with open("apiKeys.json", "r", encoding='utf-8') as f:
    apiKeys = json.load(f)





os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = apiKeys['LANGCHAIN_API_KEY']
os.environ["GROQ_API_KEY"] = apiKeys['GROQ_API_KEY']
class QuestionMaker:

    def __init__(self, topic, theme, model_name="llama3-8b-8192"):

        # self.userConcepts = userConcepts
        # self.userInterests = userInterests
        self.userConcept = topic
        self.userInterest = theme
        self.model = ChatGroq(model=model_name)


    def frame_a_question(self, userConcept, userInterest):
        
        
        parent_directory_2 = os.path.join("..", "example_jsons")
        with open(os.path.join(parent_directory_2, "template_1.json"), "r") as f:
            template_1 = str(json.load(f))
        
        # print(type(template_1))
        # parent_directory_3 = os.path.join("..", "example_jsons")
        # with open(os.path.join(parent_directory_3, "template_2.json"), "r") as f:
        #     template_2 = str(json.load(f))
        
        
        messages = [
            SystemMessage(content=f"""
            Generate a valid python programming question with 2 or more test cases for the given 
            concept and theme in json format strictly without any other extra sentances. STRICTLY USE DOUBLE QUOTES \"\" for JSON PARSABLE IN PYTHON.
            The template should have the function definition with docstring and type hints.
            Inputs and outputs in the testcases should be of the same type as the input and return types.          """),
            HumanMessage(content=f"Concept : functions, Theme : cricket"),
            AIMessage(content=template_1),
            # HumanMessage(content=f"Concept : file handling, Theme : fruits"),
            # AIMessage(content=template_2),
            HumanMessage(content=f"Concept : {userConcept}, Theme : {userInterest}")
        ]

        return self.model.invoke(messages).content

    def get_questions(self, n):

        questions = set()

        while len(questions) < n:
            # userConcept = random.choice(self.userConcepts)
            # userInterest = random.choice(self.userInterests)
            question = self.frame_a_question(self.userConcept, self.userInterest)
            questions.add(question)

        return list(questions)








          

        

        
        