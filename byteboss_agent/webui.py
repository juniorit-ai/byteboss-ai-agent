import gradio as gr
import os
import subprocess
from PIL import Image

# Initialize default directories
reference_directory = "../code-references"
code_directory = "../code-output"

# Helper function to make path relative
def make_relative(path):
    return os.path.relpath(path, os.getcwd())

# Function to select directory and update global variables
def select_reference_directory():
    import tkinter as tk
    from tkinter import filedialog

    global reference_directory
    root = tk.Tk()
    root.withdraw()
    selected_dir = filedialog.askdirectory(initialdir=reference_directory)
    if selected_dir:
        reference_directory = selected_dir
    return make_relative(reference_directory)

def select_code_directory():
    import tkinter as tk
    from tkinter import filedialog

    global code_directory
    root = tk.Tk()
    root.withdraw()
    selected_dir = filedialog.askdirectory(initialdir=code_directory)
    if selected_dir:
        code_directory = selected_dir
    return make_relative(code_directory)

# Function to handle submission
def handle_submit(prompt):
    global reference_directory, code_directory
    
    # Run a shell command using the provided prompt
    command = f"echo {prompt}"  # Example shell command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    # Generate an image (For demonstration, we'll create a blank image)
    image_path = os.path.join(code_directory, "output.png")
    image = Image.new('RGB', (1920, 1080), color = (73, 109, 137))
    image.save(image_path)
    
    # Read command output
    command_output = stdout.decode() + "\n" + stderr.decode()
    
    return command_output, image_path

css = """
.prompt_text {
    flex-grow: 1;
}

.submit_button {
    flex-grow: 0;
    width: 100px !important;
    height: 60px !important;
    padding: 10px !important;
    align-self: center;
}
"""

# Gradio interface elements
with gr.Blocks(css=css) as webui:
    with gr.Tabs():
        with gr.TabItem("Main"):
            with gr.Row():
                prompt_text = gr.Textbox(lines=5, placeholder="Prompt for task", elem_classes=["prompt_text"])
                submit_button = gr.Button("Submit", elem_classes=["submit_button"])
            
            command_output = gr.Textbox(lines=5, label="Command Output")
            generated_image = gr.Image(label="Generated Image", type="filepath")
            
            submit_button.click(handle_submit, inputs=prompt_text, outputs=[command_output, generated_image])
        
        with gr.TabItem("Settings"):
            with gr.Row():
                gr.Markdown("**Reference Directory**")
                reference_text = gr.Textbox(value=make_relative(reference_directory), interactive=False)
                reference_button = gr.Button("Select")
                reference_button.click(select_reference_directory, outputs=reference_text)
            
            with gr.Row():
                gr.Markdown("**Code Output Directory**")
                code_text = gr.Textbox(value=make_relative(code_directory), interactive=False)
                code_button = gr.Button("Select")
                code_button.click(select_code_directory, outputs=code_text)

webui.launch()