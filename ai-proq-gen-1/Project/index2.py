import gradio as gr
import os
import json
import ast
from PythonQuestionMaker import QuestionMaker

def create_third_page(data_state):
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
        return new_data, gr.update(choices=[d['problem_statement'] for d in new_data])

    with gr.Column(visible=True) as page3:
        gr.Markdown("# Programming in Python")
        with gr.Row():
            with gr.Column(scale=1):
                theme = gr.Textbox(label="Select theme")
                topic = gr.Textbox(label="Select Topic")
                submit2 = gr.Button("Submit", elem_id="submit2")
                
                with gr.Tab("Question"):
                    question_select = gr.Dropdown(label="Select Question", choices=[], interactive=True)
                    question_display = gr.Textbox(label="Question", interactive=False)
                    
                with gr.Tab("Test Cases"):
                    with gr.Tabs():
                        with gr.Tab("Case 1"):
                            input_box1 = gr.Textbox(label="Input for Test Case 1", interactive=False)
                            output_box1 = gr.Textbox(label="Output for Test Case 1", interactive=False)
                        with gr.Tab("Case 2"):
                            input_box2 = gr.Textbox(label="Input for Test Case 2", interactive=False)
                            output_box2 = gr.Textbox(label="Output for Test Case 2", interactive=False)
                            
                with gr.Tab("Solution"):
                    gr.Textbox(label="Sample solution")
                    
            with gr.Column(scale=1):
                code_input = gr.Code(label="Write your code here", language="python", lines=10)
                run_button = gr.Button("Run")

        def update_question(selected_question, data):
            if data is None or not data:
                return "", "", "", "", "", ""
            selected_data = next(d for d in data if d['problem_statement'] == selected_question)
            function_template = selected_data['function_template'].replace("\\n", "\n")
            print(selected_data)
            return (selected_data["problem_statement"],
                    selected_data['test_cases'][0]['input'],
                    selected_data['test_cases'][1]['input'],
                    selected_data['test_cases'][0]['output'],
                    selected_data['test_cases'][1]['output'],
                    function_template)

        def run_code(code, selected_question, data):
            outputs = []
            try:
                if data is None or not data:
                    return ["No data available."] * 2
                selected_data = next(d for d in data if d['problem_statement'] == selected_question)
                function_name = selected_data["function_name"]
                
                # Prepare the global namespace for the execution
                exec_globals = {}
                exec(code, exec_globals)
                
                # Retrieve the function from the user's code
                func = exec_globals.get(function_name)
                
                if not func:
                    return [f"Function '{function_name}' not found."] * 2

                # Run all test cases
                for test_case in selected_data['test_cases']:
                    inputs = test_case["input"]
                    expected_output = int(test_case["output"])

                    # Execute the function with the test case inputs
                    result = func(*inputs)
                    output = f"Input: {test_case['input']}\nOutput: {result}, Expected: {expected_output}"
                    outputs.append(output)
            except Exception as e:
                outputs = [f"An error occurred: {str(e)}"] * 2
            
            return outputs

        question_select.change(fn=update_question, inputs=[question_select, data_state], outputs=[question_display, input_box1, input_box2, output_box1, output_box2, code_input])
        run_button.click(fn=run_code, inputs=[code_input, question_select, data_state], outputs=[output_box1, output_box2])
        submit2.click(fn=submit_second_page, inputs=[theme, topic], outputs=[data_state, question_select])
        
    return page3, question_select

with gr.Blocks(css=".small-button { padding: 5px 10px; font-size: 12px; }") as demo:
    data_state = gr.State([])  
    
    with gr.Column(visible=True) as page1:
        gr.Markdown("# Page 1: User Details")
        name = gr.Textbox(label="Name")
        roll_no = gr.Textbox(label="Roll Number")
        submit1 = gr.Button("Submit", elem_id="submit1")
        result1 = gr.Text()
        
    with gr.Column(visible=False) as page3:
        page3_content, question_select = create_third_page(data_state)
        
    def submit_first_page(name, roll_no):
        return f"Name: {name}, Roll Number: {roll_no}", gr.update(visible=False), gr.update(visible=True)

    submit1.click(fn=submit_first_page, inputs=[name, roll_no], outputs=[result1, page1, page3])
    
    data_state.change(fn=lambda new_data: gr.update(choices=[d['problem_statement'] for d in new_data]), inputs=data_state, outputs=question_select)

demo.launch(share = True)
