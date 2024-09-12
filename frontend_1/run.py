import gradio as gr
import os
import json
import ast
import requests
from PythonQuestionMaker import QuestionMaker
from difflib import Differ
from jinja2 import Template, Environment

from template import output_template, testcases_template


def update_question(selected_question, data):
            if data is None or not data:
                return "", "", "", "", "", ""
            selected_data = next(d for d in data if d['question'] == selected_question)
            function_template = selected_data['question_template'].replace("\\n", "\n")
            return (selected_data["question"],
                    testcases_template.render(testcases = selected_data['testcases']),
                    function_template)








import json

def run_code(code_snippet, selected_question, test_data):
    actual_output_messages = []
    expected_output_messages = []

    try:
        if test_data is None or not test_data:
            return ["No data available.", "No data available.", "", ""]


        selected_test_data = next((item for item in test_data if item['question'] == selected_question), None)
        if not selected_test_data:
            return ["Selected question not found.", "Selected question not found.", "", ""]

        function_name = selected_test_data["function_name"]
        execution_code = f"""
if __name__ == "__main__":
    import sys
    import json
    from inspect import signature

    # Read parameters from stdin
    parameters = json.loads(sys.stdin.read())

    sig = signature({function_name})
    if len(sig.parameters) == 1:
        result = {function_name}(parameters)  # Pass the list as a single argument
    elif isinstance(parameters, dict):
        result = {function_name}(**parameters)  # Use **params to unpack dictionary
    else:
        result = {function_name}(*parameters)  # Use *params to unpack list
    print(result)
"""

        # Combine the provided code and the execution code
        complete_code = code_snippet + execution_code

        # Loop through each test case
        for test_case in selected_test_data['testcases']:
            input_data = json.dumps(test_case["input"])  # Ensure inputs are in JSON string format
            expected_output = test_case["output"]

            # Prepare the payload for the Piston API
            payload = {
                "language": "python",
                "version": "3.10.0",
                "files": [{
                    "name": "script.py",
                    "content": complete_code
                }],
                "stdin": input_data  # Pass input data via stdin
            }

            # Send the request to the Piston API
            response = requests.post("https://emkc.org/api/v2/piston/execute", json=payload)
            execution_result = response.json()

            # Extract the output from the API response
            actual_output = execution_result['run']['output'].strip() if 'run' in execution_result and 'output' in execution_result['run'] else ""
            actual_output_messages.append(actual_output)
            match_flag = (str(expected_output).strip() == actual_output)

            # Format the output message based on whether the result matches the expected output
          
            expected_output_messages.append(expected_output)

          

    except Exception as e:
        # Handle exceptions by returning an error message
        output_messages = [f"An error occurred: {str(e)}"] * 2


    output_json = {"actual_output": actual_output_messages, "expected_output":expected_output_messages }
    # return output_json
    return output_template.render(output_json=output_json)
