import gradio as gr

def greet(name):
    return f"Hello {name}!"

def square(number):
    return number ** 2

with gr.Blocks() as demo:
    with gr.Tab("Greetings"):
        with gr.Row():
            name_input = gr.Textbox(label="Enter your name:")
            greet_button = gr.Button("Greet")
        greet_output = gr.Textbox(label="Greeting Output:")
        greet_button.click(fn=greet, inputs=name_input, outputs=greet_output)
    
    with gr.Tab("Math Operations"):
        with gr.Row():
            number_input = gr.Number(label="Enter a number:")
            square_button = gr.Button("Square")
        square_output = gr.Number(label="Squared Output:")
        square_button.click(fn=square, inputs=number_input, outputs=square_output)
    
    with gr.Tab("About"):
        gr.Markdown("### This is a simple Gradio app with multiple tabs. \n Use the tabs to navigate through different functionalities.")

demo.launch()
