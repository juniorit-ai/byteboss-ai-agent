TAG_SCRIPT_INSTRUCTIONS = """
We are introducing a new scripting language named "tag script," which leverages Large Language Models (LLMs) as compilers to generate code. Below are the guidelines for writing in tag script:

Each line of tag script begins with an '@' symbol, which denotes a tag. These tags serve as instructions for code generation. Here are the specific tags and their purposes:

1. @create: Creates a new code file with the specified name and language by file extension.
2. @update: Updates an existed code file with the specified file name.
3. @interface: Defines an interface or function with input and output requirements for other code file to import and invoke.
4. @user: Allows the user to execute shell commands or input data.
5. @call 'function or interface name': Invokes a specific function or interface method.
6. @input: Inputs data from variables or files for use in the LLM model or function.
7. @follow: Provides guidelines on how to use or create the code.
8. @output: Specifies the data output format.
9. @to: Saves the output to a variable or file.
10. @import: Imports or includes the necessary library or file. If the imported file does not exist, create it as the requirements.
11. @shell: Executes shell commands within the code. When executing shell commands, replace the placeholder `{variable}` with the corresponding input variable. If the placeholder includes the array indicator `[i]`, execute the shell command iteratively for each element in the array.

Additional notes:

- Code Logic Initiation: Tags such as @create or @update serve as starting points for defining the code logic in the specified file. All subsequent tags are interpreted as instructions or actions to be performed within the context of the file created or updated by these commands.
- If a function or interface called does not exist, a new one should be created according to the specified input and output requirements.
- When importing a file, its content may need to be updated to meet the specific requirements.
- Various markdown code blocks may be used as guidelines for code creation; however, the final programming language should conform to the file extension.

Below is an example of a tag script that generates Python code:

#### From the tag script:

@create `llm.py`

@interface `inference`
@input prompt string

@follow

create a prompt with the input string, and ask LLM to output in json format
using openai GPT-4 model by openai SDK

@output
```json
{
    "dialog": [{"name": "string", "role": "string", "style": "string", "content": "string"}]
}

// dialog[i].name: the person's name in the dialog
// dialog[i].role: male. female, girl
// dialog[i].style: chat, angry, cheerful, excited, friendly, shouting, unfriendly, whispering, hopeful, sad or terrified`
// dialog[i].content: the conversation text content in the dialog
```
___

@create `main.py`

@import `llm.py`
@call `inference`
@input `textfile.txt`
@ouput json
@to `dialog_data`

#### To the Python code:

# file: llm.py

import os
from openai import OpenAI
import json

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def inference(self, prompt: str) -> dict:

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": \"\"\"You are a dialog generator. Generate a dialog based on the given prompt. Output should be in JSON format below:
```json
{
    "dialog": [{"name": "string", "role": "string", "style": "string", "content": "string"}]
}

// commnets for each field in dialog for reference when generating the dialog json data output:
// dialog[i].name: the person's name in the dialog
// dialog[i].role: male. female, girl
// dialog[i].style: chat, angry, cheerful, excited, friendly, shouting, unfriendly, whispering, hopeful, sad or terrified`
// dialog[i].content: the conversation text content in the dialog
```         
 \"\"\"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            # Parse the JSON response
            dialog_data = json.loads(response.choices[0].message.content)
            return dialog_data

        except Exception as e:
            print(f"Error generating dialog: {str(e)}")
            raise Exception("Invalid dialog structure in the generated response")

# file: main.py

from llm import LLM

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    text_file_path = "textfile.txt"
    prompt = read_text_file(text_file_path)

    llm = LLM()
    dialog_data = llm.inference(prompt)
    
    print(dialog_data)
    
"""