import os
import base64
from tag_script_instructions import TAG_SCRIPT_INSTRUCTIONS

def get_relative_path(root_path, full_path):
    # Convert root_path and full_path to absolute paths
    root_path = os.path.abspath(root_path)
    full_path = os.path.abspath(full_path)
    
    # Calculate the relative path
    relative_path = os.path.relpath(full_path, start=root_path)
    return relative_path

class Agent:
    EXTENSION_TO_LANGUAGE = {
        '.py': 'python',
        '.md': 'markdown',
        '.js': 'javascript',
        '.html': 'html',
        '.css': 'css',
        '.c': 'c',
        '.cpp': 'cpp',
        '.java': 'java',
        '.ts': 'typescript',
        '.dart': 'dart',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.kts': 'kotlin',
        '.go': 'go',
        '.rs': 'rust',
        '.php': 'php',
        '.rb': 'ruby',
        '.sh': 'bash',
        '.pl': 'perl',
        '.sql': 'sql',
        '.txt': 'text',
    }

    @staticmethod
    def load_ignore_list(ignore_file):
        ignore_list = set()
        if os.path.exists(ignore_file):
            with open(ignore_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        ignore_list.add(line)
        return ignore_list

    @staticmethod
    def should_ignore(file_path, ignore_list):
        for ignore_item in ignore_list:
            if ignore_item in file_path:
                return True
            if file_path.endswith(ignore_item):
                return True
        return False
    
    @staticmethod
    def read_image_as_base64(file_path):
        # Determine the MIME type based on the file extension
        if file_path.endswith('.png'):
            mime_type = 'image/png'
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            mime_type = 'image/jpeg'
        else:
            raise ValueError("Unsupported image format")

        # Read the file and encode it as base64
        with open(file_path, 'rb') as f:
            image_data = f.read()
            image_url = f'data:{mime_type};base64,{base64.b64encode(image_data).decode("utf-8")}'
            return image_url

    @staticmethod
    def read_files_in_directory(directory, ignore_list):
        file_contents = {}
        images = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if Agent.should_ignore(file_path, ignore_list):
                    continue
                if file_path.endswith('.prompt.png') or file_path.endswith('.prompt.jpg') or file_path.endswith('.prompt.jpeg'):
                    images.append(Agent.read_image_as_base64(file_path))
                    continue
                if os.path.splitext(file_path)[1] not in Agent.EXTENSION_TO_LANGUAGE:
                    continue
                if file_path.endswith('.prompt.done.md'):
                    continue
                if file_path.endswith('.tag.done.md'):
                    continue
                if file_path.endswith('ignore-by-agent.txt'):
                    continue
                
                with open(file_path, 'r') as f:
                    file_contents[file_path] = f.read()
        return file_contents, images

    @staticmethod
    def get_language_by_extension(file_path):
        _, ext = os.path.splitext(file_path)
        return Agent.EXTENSION_TO_LANGUAGE.get(ext, '')

    @staticmethod
    def generate_context(code_references_dir, code_output_dir, ignore_file):
        referenced_files_context = ''
        image_urls = []
        
        # Read reference files
        ignore_list = Agent.load_ignore_list(os.path.join(code_references_dir, ignore_file))
        reference_files, ref_image_urls = Agent.read_files_in_directory(code_references_dir, ignore_list)
        if reference_files:
            referenced_files_context += f'There are total {len(reference_files)} files for you to reference only (it is not allowed to update these files, also do not mention it in any document file)\n\n'
            for i, (file_path, content) in enumerate(reference_files.items(), start = 1):
                language = Agent.get_language_by_extension(file_path)
                referenced_files_context += f'File-{i} in {language}, path: {get_relative_path(code_references_dir, file_path)}\n\n(""\n{content}\n"")\n\n'
        
        if ref_image_urls:
            image_urls.extend(ref_image_urls)
        
        output_files_context = ''
        files_with_todo_context = ''
        
        T2DO = 'TO' + 'DO' # The TO DO keyword to search for in the output files, we just mask it here to avoid the system to process it
        
        # Read output files
        ignore_list = Agent.load_ignore_list(os.path.join(code_output_dir, ignore_file))
        output_files, out_image_urls = Agent.read_files_in_directory(code_output_dir, ignore_list)
        if output_files:
            non_todo_files = {fp: c for fp, c in output_files.items() if f'{T2DO}:' not in c and not fp.endswith('.prompt.md') and not fp.endswith('.tag.md')}
            todo_files = {fp: c for fp, c in output_files.items() if f'{T2DO}:' in c and not fp.endswith('.prompt.md') and not fp.endswith('.tag.md')}
            
            if non_todo_files:
                output_files_context += f'There are total {len(non_todo_files)} files for you to check (do not contain {T2DO} comments), you may need to update it if it is necessary\n\n'
                for i, (file_path, content) in enumerate(non_todo_files.items(), start=1):
                    language = Agent.get_language_by_extension(file_path)
                    output_files_context += f'File-{i} in {language}, path: {get_relative_path(code_output_dir, file_path)}\n\n(""\n{content}\n"")\n\n'
            
            if todo_files:
                files_with_todo_context += f'There are total {len(todo_files)} files which contain {T2DO}: comments, please follow the {T2DO} requirement to update these files and other related files if necessary\n\n'
                for i, (file_path, content) in enumerate(todo_files.items(), start=1):
                    language = Agent.get_language_by_extension(file_path)
                    files_with_todo_context += f'File-{i} in {language}, path: {get_relative_path(code_output_dir, file_path)}\n\n(""\n{content}\n"")\n\n'

        if out_image_urls:
            image_urls.extend(out_image_urls)
            
        prompt_files_message = ''
        prompt_files_context = ''
        
        # Combine all the *.prompt.md files content together and show it, just separate by line
        prompt_files = {fp: c for fp, c in output_files.items() if fp.endswith('.prompt.md')}
        if prompt_files:
            if not files_with_todo_context:
                prompt_files_message = 'Please complete the task as per the instructions below:'
            else:
                prompt_files_message = 'In Addition, please complete the task as per the instructions below:'
                
            for file_path, content in prompt_files.items():
                prompt_files_context += f'{content}\n\n'
            
        tag_files_message = ''
        tag_files_context = ''
        
        # Combine all the *.tag.md files content together and show it, just separate by line
        tag_files = {fp: c for fp, c in output_files.items() if fp.endswith('.tag.md')}
        if tag_files:
            if not files_with_todo_context and not prompt_files_context:
                tag_files_message = f'{TAG_SCRIPT_INSTRUCTIONS}\n\nPlease complete the code as per the below tag script content:'
            else:
                tag_files_message = 'In Addition, {TAG_SCRIPT_INSTRUCTIONS}\n\nPlease complete the code as per the below tag script content:'
                
            for file_path, content in tag_files.items():
                tag_files_context += f'{content}\n\n'
                
        if not files_with_todo_context and not prompt_files_context and not tag_files_context:
            raise Exception(f'You must have at least one markdown prompt file with the extension `.prompt.md`, `.tag.md` or a file containing `TODO:` comments in the directory {code_output_dir}.')
        
        if prompt_files_context:
            prompt_files_context = f'{prompt_files_message}\n\n(""\n{prompt_files_context.strip()}\n"")'
            
        if tag_files_context:
            tag_files_context = f'{tag_files_message}\n\n(""\n{tag_files_context.strip()}\n"")'
        
        context = referenced_files_context + output_files_context + files_with_todo_context + prompt_files_context + tag_files_context
        
        return context, image_urls
