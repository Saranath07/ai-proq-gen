import gradio as gr
import os
import json
import ast
import requests
from PythonQuestionMaker import QuestionMaker
from difflib import Differ
from jinja2 import Template, Environment

# from run import run_code

# output_json = {"actual_output": actual_output_messages, "expected_output":expected_output_messages }
# input,
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






def zip_filter(a, b):
    return zip(a, b)


env = Environment()
env.filters['zip'] = zip_filter


output_template = env.from_string('''
{% set list1 = output_json['actual_output'] %}
{% set list2 = output_json['expected_output'] %}
{% for item1, item2 in list1 | zip(list2) %}
    ### Actual Output {{loop.index}}                    
    {% if item1 == item2 %}
        Passed ✅
    {% else %}
        Expected: {{ item2 }}, but got: {{ item1 }} ❌
    {% endif %}                
{% endfor %}

''')