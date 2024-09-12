import gradio as gr
import ast
from proq_gen.generators.chroma import get_db_store
import json
from proq_gen.convert_to_json import data_to_json
from run import update_question, run_code
from difflib import Differ

from template import make_template_outputs, make_template_testcases
def print_n_value(n_value):
    global no_tests
    no_tests = n_value  # Store the value in the global variable
    # print(f"Value of n stored in no_tests: {no_tests}")
    return n_value  # Return the value if needed for further processing

def submit_second_page(topic):
    db_store = get_db_store("python-questions")
    questions = db_store.similarity_search(topic)

    questions_json = json.loads(data_to_json(questions))

    # print(questions_json)
    # Update the dropdown with questions
    return questions_json, gr.update(choices=[d['question'] for d in questions_json])

def create_third_page(data_state):
    with gr.Column(visible=True) as page3:
        gr.Markdown("# Programming in Python")
        with gr.Row():
            with gr.Column(scale=1):
                # theme = gr.Textbox(label="Select theme")
                topic = gr.Textbox(label="Select Topic")
                submit2 = gr.Button("Submit", elem_id="submit2")
                
                with gr.Tab("Question"):
                    question_select = gr.Dropdown(label="Select Question", choices=[], interactive=True)
                    question_display = gr.Textbox(label="Question", interactive=False)
                   
                with gr.Tab("Test Cases"):
                    # testcases_state = gr.State()
                    testcases_state = gr.Markdown(label = 'testcases')
                    # testcases_md = gr.Markdown(label='Test cases')
                
                with gr.Tab("Output"):
                    outputs_md = gr.Markdown(label = "Output") # JSON output component
                
                with gr.Tab("Solution 🔒"):
                    gr.Textbox("This is a Sample solution")
                    
            with gr.Column(scale=1):
                code_input = gr.Code(label="Write your code here", language="python", lines=10, interactive=True)
                run_button = gr.Button("Run")

        # Connect buttons to functions
        submit2.click(
            fn=submit_second_page, 
            inputs=[topic], 
            outputs=[data_state, question_select]
        )
        
        question_select.change(
            fn=make_template_testcases, 
            inputs=[question_select, data_state], 
            outputs=[question_display, testcases_state, code_input]
        )
        print(question_select)
        run_button.click(
            fn=lambda code, question, data: make_template_outputs(code, question, data), 
            inputs=[code_input, question_select, data_state], 
            outputs=[outputs_md]  # Ensure this is JSON formatted
        )

    return page3, question_select

