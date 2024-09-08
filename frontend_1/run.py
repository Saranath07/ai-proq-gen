import gradio as gr
import os
import json
import ast
import requests
from PythonQuestionMaker import QuestionMaker
from difflib import Differ
from jinja2 import Template, Environment
testcases_template = Template('''
{% for testcase in  testcases %}
### Input {{loop.index}}
```
{{testcase.input}}
```
### Expected Output {{loop.index}}
```
{{testcase.output}}
```  

                                                                  
{% endfor %}
''')



output_template = Template('''
{% for output in  outputs %}
### Actual Output {{loop.index}}
```
{{output}}                       
```
{% endfor %}


''')





diff_template = Template('''
{% for diff in  diffs %}
### Difference{{loop.index}}
```
({{diff}})                       
```
{% endfor %}


''')


"""
testcases = [{input: ... , output:...}]
testcases:{input:[], output:[]}

"""

"""
 "testcases": [
        {
            "input": "fruits.txt",
            "content" : "apple \\n mango \\n banana",
            "output": "['apple', 'mango', 'banana']"
        },
        {
            "input": "fruits.txt",
            "content" : "blueberry \\n strawberry \\n raspberry",
            "output": "['blueberry', 'strawberry', 'raspberry']"
        }
    ]
"""

def update_question(selected_question, data):
            if data is None or not data:
                return "", "", "", "", "", ""
            selected_data = next(d for d in data if d['question'] == selected_question)
            function_template = selected_data['question_template'].replace("\\n", "\n")
            return (selected_data["question"],
                    len(selected_data['testcases']),
                    selected_data['testcases'],
                    # str(selected_data['test_cases']),
                    testcases_template.render(testcases = selected_data['testcases']),
                    function_template)




import gradio as gr

def diff_texts(text1, text2):
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]

def run_code(code, selected_question, data):
    outputs = []
    diffs = []

    try:
        if data is None or not data:
            return ["No data available.", "No data available.", "", ""]

        selected_data = next(d for d in data if d['question'] == selected_question)
        function_name = selected_data["function_name"]

        # Create the execution code dynamically using string interpolation
        execution_code = f"""
if __name__ == "__main__":
    import sys
    import json
    from inspect import signature

    # Read parameters from stdin
    params = json.loads(sys.stdin.read())
    
    sig = signature({function_name})
    if len(sig.parameters) == 1:
        result = {function_name}(params)  # Pass the list as a single argument
    elif isinstance(params, dict):
        result = {function_name}(**params)  # Use **params to unpack dictionary
    else:
        result = {function_name}(*params)  # Use *params to unpack list
    print(result)       
"""

        # Combine the provided code and the execution code
        full_code = code + execution_code

        for test_case in selected_data['testcases']:
            inputs = json.dumps(test_case["input"])  # Ensure inputs are a JSON string
            expected_output = test_case["output"]

            payload = {
                "language": "python",
                "version": "3.10.0",
                "files": [{
                    "name": "script.py",
                    "content": full_code
                }],
                "stdin": inputs  # Pass input data via stdin
            }

            response = requests.post("https://emkc.org/api/v2/piston/execute", json=payload)
            result = response.json()

            output_o = result['run']['output'].strip() if 'run' in result and 'output' in result['run'] else ""
            match_flag = (str(expected_output).strip() == output_o)

            output = f"{output_o}\nMatch: {'✅' if match_flag else '❌'}\n"
            outputs.append(output)

            # Calculate the difference for displaying in the diff box
            diff = diff_texts(str(expected_output), output_o)
            diffs.append(diff)

    except Exception as e:
        outputs = [f"An error occurred: {str(e)}"] * 2
        diffs = [""] * 2

    # Ensure to return exactly four items
    return output_template.render(outputs=outputs), diff_template.render(diffs=diffs)
