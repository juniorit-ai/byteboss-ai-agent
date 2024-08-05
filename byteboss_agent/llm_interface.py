from abc import ABC, abstractmethod
import json

class LLMInterface(ABC):
    @abstractmethod
    def get_ai_response(self, messages):
        pass
    
    @abstractmethod
    def get_ai_code_files(self, context, image_urls):
        pass

    @abstractmethod
    def get_ai_file_update(self, messages, file):
        pass

    @abstractmethod
    def get_ai_shell_commands(self, messages):
        pass

    @abstractmethod
    def get_ai_error_fix(self, messages, error_message):
        pass

    """
    <|start|>
    file: src/hello.c
    <|code|>
    #include <stdio.h>
    int main() {
        printf("Hello, World!\n");
        return 0;
    }
    <|stop|>
    """

    def file_info_to_json(self, content):
        # Remove leading/trailing whitespace and split the content into lines
        lines = content.strip().split('\n')

        # Extract file path
        file_line = next((line for line in lines if line.strip().startswith('file:')), None)
        if not file_line:
            return "Error: File path not found"

        filepath = file_line.split('file:', 1)[1].strip()

        # Find the start of the code
        code_start = next((i for i, line in enumerate(lines) if '<|code|>' in line), -1)
        if code_start == -1:
            return "Error: Code start not found"

        # Extract code content
        code_lines = lines[code_start + 1:]

        # Find the end of the code (if <|stop|> exists)
        code_end = next((i for i, line in enumerate(code_lines) if '<|sto' in line), len(code_lines))

        # Join the code lines
        code = '\n'.join(code_lines[:code_end]).strip()

        # Create the JSON structure
        json_data = {
            "agentOutput": {
                "file": {
                    "filepath": filepath,
                    "code": code
                }
            }
        }

        # Convert to JSON string
        json_string = json.dumps(json_data, indent=2)
        return json_string