TAG_SCRIPT_INSTRUCTIONS = """
We are introducing a new scripting language named "tag script," which leverages Large Language Models (LLMs) as compilers to generate code. Below are the guidelines for writing in tag script:

Each line of tag script begins or contains with an '@tag' symbol below, which denotes a tag. These tags serve as instructions for code generation. 

Here are the specific tags and their purposes:

1. @create `file` `[ref]`: Creates a new code file with the specified name and language by file extension, the optional `ref` can be a class name or just as a reference for this file.
2. @update `file` `[ref]`: Updates an existed code file with the specified file name, the optional `ref` can be a class name or just as a reference for this file.
3. @interface: Defines an interface or function with input and output requirements for other code file to import and invoke.
4. @send: Sends data to an API or service.
5. @event [from service/client]: Responds to an event or trigger from a service or client.
6. @connect: As a clinet and connect to a server or service by a specific socket or address.
7. @listen: Listen on a specific socket or address for incoming data in a server or service.
8. @user: Allows the user to execute shell commands or input data.
9. @call 'function or interface name' by {params}: Invokes a specific function or interface method.
10. @input {params}: Inputs data from variables or files for use in the LLM model or function.
11. @follow: Provides guidelines on how to use or create the code.
12. @output: Specifies the data output format.
13. @to: Saves the output to a variable, file or sends to a service.
14. @import: Imports or includes the necessary library or file. If the imported file does not exist, create it as the requirements.
15. @env: Using .env file to load the environment variables.
16. @shell: Executes shell commands within the code. When executing shell commands, replace the placeholder `{variable}` with the corresponding input variable. If the placeholder includes the array indicator `[i]`, execute the shell command iteratively for each element in the array.
17. @reference: Refers to a specific code snippet or file for reference.
18. @mermaid-{diagram type} `file`: Create or update a mermaid diagram in markdown code style start by "```mermaid", the diagram type can be: flowchart, sequence, class, state, ERD (Entity relationship diagram), mindmap and timeline etc
19. @plantuml-{UML diagram type} `file`: Create or update a planet UML diagram in markdown code style start by "```plantuml", the UML type can be: usecase, sequence, class, object, activity and state etc

Additional notes:

- Code Logic Initiation: Tags such as @create or @update serve as starting points for defining the code logic in the specified file. All subsequent tags are interpreted as instructions or actions to be performed within the context of the file created or updated by these commands.
- If a function or interface called does not exist, a new one should be created according to the specified input and output requirements.
- When importing a file, its content may need to be updated to meet the specific requirements.
- Various markdown code blocks may be used as guidelines for code creation; however, the final programming language should conform to the file extension.
- Having example usage for each file created to demonstrate the functionality of the code if necessary.

Below is an example of a tag script that generates Python code:

#### From the tag script:

@create `llm.py`

@interface `inference`
@input string prompt

@follow

create a prompt with the input string, and ask LLM to output in json format
using openai gpt-4o model by openai SDK

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
                model="gpt-4o",
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
            
if __name__ == "__main__":
    # Example usage
    llm = LLM()
    dialog_data = llm.inference("What is the weather today?")
    dialog_data_json = json.dumps(dialog_data, indent=4)
    print("Generated Dialog: ", dialog_data_json)

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
    
if __name__ == "__main__":
    main()
"""