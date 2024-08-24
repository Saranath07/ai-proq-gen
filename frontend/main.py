import gradio as gr
import os
import json
import ast
import requests
from difflib import Differ

def submit_first_page(name, roll_no):
        return f"Name: {name}, Roll Number: {roll_no}", gr.update(visible=False), gr.update(visible=True)

   
def submit_second_page(theme, topic):
        questionMaker = QuestionMaker(topic, theme)
        userQuestions = questionMaker.get_questions(5)
        new_data = []
        for i in range(len(userQuestions)):
            try:
                d = ast.literal_eval(userQuestions[i])
                new_data.append(d)
            except Exception as e:
                print(f"Failed to write question {i+1}: {e}")
        return new_data, gr.update(choices=[d['question'] for d in new_data])



        
def diff_texts(text1, text2):
    d = Differ()
    return [(token[2:], token[0] if token[0] != " " else None)for token in d.compare(text1, text2)]
               
               