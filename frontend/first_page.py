import gradio as gr
import os
import json
import ast
import requests
from difflib import Differ

def submit_first_page(name, roll_no):
    # Process the input data
    result_message = f"Name: {name}, Roll Number: {roll_no} submitted successfully."
    
    # Return the result message and change visibility of pages
    return result_message, gr.update(visible=False), gr.update(visible=True)

with gr.Blocks(css=".small-button { padding: 5px 10px; font-size: 12px; }") as demo:
    data_state = gr.State([])  
    
    with gr.Column(visible=True) as page1:
        gr.Markdown("# Page 1: User Details")
        name = gr.Textbox(label="Name")
        roll_no = gr.Textbox(label="Roll Number")
        submit1 = gr.Button("Submit", elem_id="submit1")
        result1 = gr.Text()

    with gr.Column(visible=False) as page3:
        # Delay the import of create_third_page until it's needed
        from second_page import create_third_page, submit_second_page
        page3_content, question_select = create_third_page(data_state)
        
    submit1.click(fn=submit_first_page, inputs=[name, roll_no], outputs=[result1, page1, page3])
    data_state.change(fn=lambda new_data: gr.update(choices=[d['question'] for d in new_data]), inputs=data_state, outputs=question_select)   

demo.launch(share=True)
