import gradio as gr
import ast
from run import update_question, run_code
from difflib import Differ
from proq_gen.generators.chroma import get_db_store
import json
from proq_gen.convert_to_json import data_to_json

# Initialize the global variable
no_tests = None
def diff_texts(text1, text2):
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]
def print_n_value(n_value):
    global no_tests
    no_tests = n_value  # Store the value in the global variable
    print(f"Value of n stored in no_tests: {no_tests}")
    return n_value  # Return the value if needed for further processing

def submit_second_page(theme, topic):
    db_store = get_db_store("python-questions")
    questions = db_store.similarity_search(topic)
    print(questions)

    questions_json = json.loads(data_to_json(questions))
    # print(questions_json)
    # return questions_json
    # questionMaker = QuestionMaker(topic, theme)
    # userQuestions = questionMaker.get_questions(5)
    # new_data = []
    # for i in range(len(userQuestions)):
    #     try:
    #         d = ast.literal_eval(userQuestions[i])
    #         new_data.append(d)
    #     except Exception as e:
    #         print(f"Failed to write question {i+1}: {e}")
    return questions_json, gr.update(choices=[d['question'] for d in questions_json])
def create_third_page(data_state):
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
                    n = gr.Textbox(label="No of test cases", interactive=False)
                    
                with gr.Tab("Test Cases"):
                    
                    with gr.Tabs():
                        with gr.Tab("Case 1"):
                            input_box1 = gr.Textbox(label="Input for Test Case 1", interactive=False)
                            output_box11 = gr.Textbox(label="Expected Output for Test Case 1", interactive=False)
                            output_box12 = gr.Textbox(label="Actual Output for Test Case 1", interactive=False)
                            diff_1 = gr.HighlightedText(label="Diff", combine_adjacent=True, show_legend=True, color_map={"+": "red", "-": "green"})

                        with gr.Tab("Case 2"):
                            input_box2 = gr.Textbox(label="Input for Test Case 2", interactive=False)
                            output_box21 = gr.Textbox(label="Expected Output for Test Case 2", interactive=False)
                            output_box22 = gr.Textbox(label="Actual Output for Test Case 2", interactive=False)
                            diff_2 = gr.HighlightedText(label="Diff", combine_adjacent=True, show_legend=True, color_map={"+": "red", "-": "green"})

                with gr.Tab("Solution 🔒"):
                    gr.Textbox("This is a Sample solution")
                    
            with gr.Column(scale=1):
                code_input = gr.Code(label="Write your code here", language="python", lines=10, interactive=True)
                run_button = gr.Button("Run")

        submit2.click(fn=submit_second_page, inputs=[theme, topic], outputs=[data_state, question_select])
        question_select.change(fn=update_question, inputs=[question_select, data_state], outputs=[question_display, n, input_box1, input_box2, output_box11, output_box21, code_input])
        run_button.click(fn=run_code, inputs=[code_input, question_select, data_state], outputs=[output_box12, output_box22, diff_1, diff_2])

    return page3, question_select
