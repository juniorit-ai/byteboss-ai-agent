from anthropic import Anthropic
import os
import re
import json
from json_repair import repair_json
import yaml
from llm_interface import LLMInterface
from system_message import SYSTEM_MESSAGE, UPDATE_SUMMARY_GUIDELINES, UPDATE_FILE_GUIDELINES, IMAGE_TO_CODE_GUIDELINES, EXECUTE_COMMANDS_GUIDELINES, ERROR_FIX_GUIDELINES, UPDATE_FILE_GUIDELINES_TEXT, UPDATE_FILE_GUIDELINES_PARTIAL_TEXT

api_invoke_times = 0

logs_dir = os.getenv('LOGS_DIR')

# Define a custom representer for long strings
def str_presenter(dumper, data):
    if '\n' in data:  # check for newlines
        data = '\n'.join(line.rstrip() for line in data.splitlines()) # avoid tail space yaml format bug
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

# Add the custom representer to the YAML dumper
yaml.add_representer(str, str_presenter)

def remove_json_markdown_block_signs(markdown_string: str) -> str:
    # Regular expression to match the first JSON block
    json_block_regex = r'```json\s*\n([\s\S]*?)\n```'
    
    # Find the first JSON block
    match = re.search(json_block_regex, markdown_string)
    if match:
        return match.group(1)
    else:
        return markdown_string  # Return input if no JSON block is found

class LLMAnthropic(LLMInterface):
    client = None
    model = None
    
    def __init__(self, api_key,  model):
        self.client = Anthropic(api_key = api_key)
        self.model = model
        
    def get_ai_response(self, messages, is_file=False):
        global api_invoke_times 
        
        api_invoke_times = api_invoke_times + 1

        #allow_unicode=True fix \u2019 issue
        messages_str = yaml.dump(messages, allow_unicode=True, default_flow_style=False, width=4096)

        #save the prompt to a file
        if logs_dir is not None:
            with open(os.path.join(logs_dir, f"prompt_{api_invoke_times}.log"), "w") as f:
                f.write(messages_str)

        print(f"Sent to LLM {api_invoke_times}")

        #quit()
        
        max_tokens = 4096

        stop_sequences = None
        if is_file:
            stop_sequences = ['<|stop|>']
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=messages,
                stop_sequences = stop_sequences
            )
        except Exception as e:
            print(messages)
            print(f"Error: {e}")
            raise e

        print(f"Received from LLM {api_invoke_times}")
        
        if len(response.content) == 0:
            print(messages)
            print(response)
            raise Exception("No content from the model")
        
        #save the raw output to a file
        try:
            if logs_dir is not None:
                with open(os.path.join(logs_dir, f"output_raw_{api_invoke_times}.log"), "w") as f:
                    f.write(response.content[0].text)
        except Exception as e:
            print(response)
            print(f"Error: {e}")
            raise e

        if response.stop_reason == 'max_tokens':
            print(response.content[0].text)
            if is_file:
                print(f"Max completion tokens ({max_tokens}) limit reached, we will try to get the rest of the output.")
                return False, response.content[0].text, messages

            raise  Exception(f"Max completion tokens ({response.usage.output_tokens}) limit reached, please refine your prompt to make the output shorter.")

        if is_file:
            content = re.sub(r"<\|start-content\|>\n?", "", response.content[0].text)
            last_element = messages[-1]
            if last_element["role"] == "assistant":
                messages.pop()
                content = last_element['content'] + content
            messages.append({"role": "assistant", "content": content})
            assistant_message = self.file_info_to_json(content)
        else:
            assistant_message = remove_json_markdown_block_signs(response.content[0].text)
            assistant_message = repair_json(assistant_message)
            messages.append({"role": "assistant", "content": assistant_message})

        json_data = json.loads(assistant_message)
        json_data_str = yaml.dump(json_data, allow_unicode=True, default_flow_style=False, width=4096)

        #save the output to a file
        if logs_dir is not None:
            with open(os.path.join(logs_dir, f"output_{api_invoke_times}.log"), "w") as f:
                f.write(json_data_str)
        
        return assistant_message, messages


    def get_ai_code_files(self, context, image_urls=[]):

        prompt_str = f"{context}"
        
        if len(image_urls) > 0:
            prompt_str += f"\n\n{IMAGE_TO_CODE_GUIDELINES}"
        else:
            prompt_str += f"\n\n{UPDATE_SUMMARY_GUIDELINES}"
        
        prompt_str += f"\n\nThe output JSON format must be the same as the output of JSON.stringify() in JavaScript. Ensure all double quotes and new lines within the string values are escaped."
        
        
        messages = [
                    {"role": "user", "content": SYSTEM_MESSAGE},
                    {"role": "assistant", "content": "sure, I will escape all double quotes and new lines within the string in the json ouput just as JSON.stringify() in JavaScript does."}
                ]
        
        if len(image_urls) > 0:
            content = [{"type": "text", "text": prompt_str}]
            for image_url in image_urls:
                #image_url = f'data:{mime_type};base64,{base64.b64encode(image_data).decode("utf-8")}'
                media_type =image_url.split(";")[0].split(":")[1]
                data = image_url.split(",")[1]
                
                content.append(
                    {
                        "type": "image", 
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": data
                        }
                    }
                )
            
            messages.append({"role": "user", "content": content})
        else:
            messages.append({"role": "user", "content": prompt_str})
        

        return self.get_ai_response(messages)
    
    def get_ai_file_update(self, messages, file):
        action_type = file["action_type"]
        filepath = file["filepath"]
        summary = file["summary"]
        messages.append({"role": "user", "content": f"Please {action_type} file {filepath} as the summary {summary}, and refer to all the chat history.\n\n{UPDATE_FILE_GUIDELINES_TEXT}"})
        returned_values = self.get_ai_response(messages, True)
        number_of_values = len(returned_values) if isinstance(returned_values, tuple) else 1

        max_retries = 5

        while number_of_values == 3 and max_retries > 0:
            _, content, messages = returned_values
            content = re.sub(r"<\|start-content\|>\n?", "", content)
            last_element = messages[-1]
            messages.pop()
            if last_element["role"] == "user":
                messages.append({"role": "user", "content": f"Please {action_type} file {filepath} as the summary {summary}, and refer to all the chat history.\n\n{UPDATE_FILE_GUIDELINES_PARTIAL_TEXT}"})
                messages.append({"role": "assistant", "content": content.strip()})
            else:
                messages.append({"role": "assistant", "content": (last_element['content'] + content).strip()})
            returned_values = self.get_ai_response(messages, True)
            number_of_values = len(returned_values) if isinstance(returned_values, tuple) else 1
            max_retries -= 1

        if number_of_values == 3:
            raise Exception("Max retries reached, please refine your prompt to make the output shorter.")

        return returned_values

    def get_ai_shell_commands(self, messages):
        messages.append({"role": "user", "content": f"Please check and give all the shell commans may be used in the context.\n\n{EXECUTE_COMMANDS_GUIDELINES}"})
        return self.get_ai_response(messages)


    def get_ai_error_fix(self, messages, error_message):
        
        messages.append({"role": "user", "content": f"Please check the information below to fix any issue if have:\n\n{error_message}\n\n{ERROR_FIX_GUIDELINES}"})
        return self.get_ai_response(messages)