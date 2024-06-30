import os
import subprocess
from user import User

class Executor:
    @staticmethod
    def update_file_or_files_from_json(json_data, code_output_dir, is_single_file=True):
        if is_single_file:
            files = [json_data['agentOutput']['file']]
        else:
            files = json_data['agentOutput']['files']

        for file in files:
            if file['filepath'].endswith('.env'):
                continue
            
            if not file['filepath'].startswith(code_output_dir):
                file_path = os.path.join(code_output_dir, file['filepath'])
            else:
                file_path = file['filepath']

            code = file['code']
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(code)
            print(f'Updated file: {file_path}')

    # Usage for single file
    @staticmethod
    def update_file_from_json(json_data, code_output_dir):
        Executor.update_file_or_files_from_json(json_data, code_output_dir)

    # Usage for multiple files
    @staticmethod
    def update_files_from_json(json_data, code_output_dir):
         Executor.update_file_or_files_from_json(json_data, code_output_dir, is_single_file=False)

    @staticmethod
    def install_packages(setup_commands):
        if not User.confirm_action("The following setup commands will be executed:", setup_commands):
            return True
        
        error_messages = []
        for command in setup_commands:
            try:
                docker_container = os.getenv('DOCKER_CONTAINER', '').strip()
                if docker_container:
                    command = f'docker exec -it {docker_container} {command}'

                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
                print(f'Executed setup command: {command}')
                print(f'STDOUT: {result.stdout}')
                print(f'STDERR: {result.stderr}')
            except subprocess.CalledProcessError as e:
                error_message = f'Error executing setup command: {command}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}'
                print(error_message)
                error_messages.append(error_message)
        
        if error_messages:
            return "\n".join(error_messages)
        return True

    @staticmethod
    def run_commands(commands):
        if not User.confirm_action("The following commands will be executed:", commands):
            return True
        
        error_messages = []
        for command in commands:
            try:
                docker_container = os.getenv('DOCKER_CONTAINER', '').strip()
                if docker_container:
                    # COMPLETED_BY_AI: Run the command inside the specified Docker container
                    command = f'docker exec -it {docker_container} {command}'

                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
                print(f'Executed command: {command}')
                print(f'STDOUT: {result.stdout}')
                print(f'STDERR: {result.stderr}')
            except subprocess.CalledProcessError as e:
                error_message = f'Error executing command: {command}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}'
                print(error_message)
                error_messages.append(error_message)
        
        if error_messages:
            return "\n".join(error_messages)
        return True
