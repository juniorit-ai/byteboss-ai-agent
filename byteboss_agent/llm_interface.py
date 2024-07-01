from abc import ABC, abstractmethod

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
