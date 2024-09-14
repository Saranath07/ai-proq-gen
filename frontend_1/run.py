import gradio as gr
import os
import json
import ast
import requests
from PythonQuestionMaker import QuestionMaker
from difflib import Differ
from jinja2 import Template, Environment



def update_question(selected_question, data):
            # print(selected_data['testcases'])
            if data is None or not data:
                return "", "", "", "", "", ""
            selected_data = next(d for d in data if d['question'] == selected_question)
            function_template = selected_data['question_template'].replace("\\n", "\n")
            print(selected_data)
            return (selected_data["question"],
                    selected_data['testcases'],
                    function_template)





import json

def run_code(code_snippet,test_cases, input_type = "stdin"):
    if input_type == "code":
        code_snippet += "\nimport sys; exec(sys.stdin.read())" 
           
    
    # print(type(code_snippet))
    actual_output_messages = []
    expected_output_messages = []

    print(test_cases)
    for test_case in test_cases:
            
            print(test_case)
            input_data = test_case["input"]  # Ensure inputs are in JSON string format

   
            
            expected_output = test_case["output"]

            # Prepare the payload for the Piston API
            payload = {
                "language": "python",
                "version": "3.10.0",
                "files": [{
                    "name": "script.py",
                    "content": code_snippet
                }],
                "stdin": input_data  # Pass input data via stdin
            }

            # Send the request to the Piston API
            response = requests.post("https://emkc.org/api/v2/piston/execute", json=payload)
            execution_result = response.json()

    
            actual_output = execution_result['run']['output'].strip() if 'run' in execution_result and 'output' in execution_result['run'] else ""
            actual_output_messages.append(actual_output)
            match_flag = (str(expected_output).strip() == actual_output)

     
            expected_output_messages.append(expected_output)

          

 

    output_json = {"actual_output": actual_output_messages, "expected_output":expected_output_messages }
    return output_json
    return output_template.render(output_json=output_json)