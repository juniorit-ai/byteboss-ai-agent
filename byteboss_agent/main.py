import os
import json
from dotenv import load_dotenv
from user import User
from agent import Agent
from executor import Executor
from llm_openai import LLMOpenAI
from llm_anthropic import LLMAnthropic

def get_api_key_for_provider(provider):
    return os.getenv(f'{provider.upper()}_API_KEY')

def main():
    load_dotenv()
    
    if os.getenv('LOGS_DIR') :
        os.makedirs(os.getenv('LOGS_DIR'), exist_ok=True)

    llm_provider = os.getenv('LLM_PROVIDER', 'openai').lower()
    api_key = get_api_key_for_provider(llm_provider)
    if not api_key:
        if os.getenv('JUNIORIT_CONTAINER_TOKEN') is not None:
            api_key = os.getenv('JUNIORIT_CONTAINER_TOKEN')
            llm_provider = 'juniorit'
        else:
            print(f"API key for {llm_provider} is not set. Please check your .env file.")
            return
    
    code_references_dir = os.getenv('CODE_REFERENCES_DIR', '../code-references')
    code_prompts_dir = os.getenv('CODE_PROMPTS_DIR', '../code-prompts')
    code_output_dir = os.getenv('CODE_OUTPUT_DIR', '../code-output')
    if code_prompts_dir is None:
        code_prompts_dir = code_output_dir
        
    ignore_file = 'ignore-by-agent.txt'
    
    if llm_provider == 'openai':
        llm = LLMOpenAI(api_key, os.getenv('OPENAI_MODEL', 'gpt-4o-2024-05-13'))
    elif llm_provider == 'deepseek':
        llm = LLMOpenAI(api_key, os.getenv('DEEPSEEK_MODEL', 'deepseek-coder'), os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com'))
    elif llm_provider == 'octoai':
        llm = LLMOpenAI(api_key, os.getenv('OCTOAI_MODEL', 'meta-llama-3.1-70b-instruct'), os.getenv('OCTOAI_API_URL', 'https://text.octoai.run/v1'))
    elif llm_provider == 'juniorit':
        llm = LLMOpenAI(api_key, 'juniorit', 'https://juniorit.ai/rest/llm')
    elif llm_provider == 'anthropic':
        llm = LLMAnthropic(api_key, os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20240620'))
    else:
        print(f"Unsupported LLM provider: {llm_provider}")
        return
    
    context, image_urls = Agent.generate_context(code_references_dir, code_prompts_dir, code_output_dir, ignore_file)
    #print("Generated context for AI:\n", context)
    
    ai_output, messages = llm.get_ai_code_files(context, image_urls)
    #print("AI Output:\n", ai_output)
    
    json_data = json.loads(ai_output)
    
    if 'files' in json_data['agentOutput']:
        Executor.update_files_from_json(json_data, code_output_dir)
        print("git comments provided by AI:\n", json_data["agentOutput"]["gitComments"])
        # exit program, we only do once for image to code conversion
    else:
        for file in json_data["agentOutput"]["instruction"]:
            ai_output, messages = llm.get_ai_file_update(messages, file)
            json_data = json.loads(ai_output)
            if(json_data["agentOutput"]["file"]):
                Executor.update_file_from_json(json_data, code_output_dir)

        ai_output, messages = llm.get_ai_shell_commands(messages)
        json_data = json.loads(ai_output)
        
        # Install necessary packages
        if 'setup' in json_data['agentOutput'] and json_data['agentOutput']['setup']:
            setup_result = Executor.install_packages(json_data['agentOutput']['setup'])
            if setup_result is not True and llm_provider != 'juniorit':
                user_response = User.get_user_response("Command execution failed. Would you like the AI to check the error? (Yes/No, or you can provide information to help the AI fix it directly): ")
                if user_response.lower() in ('yes', 'y'):
                    error_message = setup_result
                elif len(user_response) < 5 or user_response.lower() in ('n', 'no'):
                    print("Exiting program.")
                    return
                else:
                    error_message = f"{user_response}\n\n{setup_result}"
                    
                ai_output = llm.get_ai_error_fix(messages, error_message)
                print("AI Retry Output:\n", ai_output)
                
                json_data = json.loads(ai_output)
                if "gitComments" in json_data["agentOutput"]:
                    print("git comments provided by AI:\n", json_data["agentOutput"]["gitComments"])

                if(json_data["agentOutput"]["files"]):
                    Executor.update_files_from_json(json_data, code_output_dir)
                
                if(json_data["agentOutput"]["setup"]):
                    Executor.install_packages(json_data['agentOutput']['setup'])

                if(json_data["agentOutput"]["commands"]):
                    Executor.install_packages(json_data['agentOutput']['commands'])
        
        # Run provided commands
        if 'commands' in json_data['agentOutput'] and json_data['agentOutput']['commands']:
            command_result = Executor.run_commands(json_data['agentOutput']['commands'])
            if command_result is not True and llm_provider != 'juniorit':
                user_response = User.get_user_response("Command execution failed. Would you like the AI to check the error? (Yes/No, or you can provide information to help the AI fix it directly): ")
                if user_response.lower() in ('yes', 'y'):
                    error_message = command_result
                elif len(user_response) < 5 or user_response.lower() in ('n', 'no'):
                    print("Exiting program.")
                    return
                else:
                    error_message = f"{user_response}\n\n{command_result}"
                    
                ai_output = llm.get_ai_error_fix(messages, error_message)
                print("AI Retry Output:\n", ai_output)
                
                json_data = json.loads(ai_output)
                if "gitComments" in json_data["agentOutput"]:
                    print("git comments provided by AI:\n", json_data["agentOutput"]["gitComments"])
    
                if(json_data["agentOutput"]["files"]):
                    Executor.update_files_from_json(json_data, code_output_dir)
                
                if(json_data["agentOutput"]["setup"]):
                    Executor.install_packages(json_data['agentOutput']['setup'])

                if(json_data["agentOutput"]["commands"]):
                    Executor.install_packages(json_data['agentOutput']['commands'])

if __name__ == '__main__':
    main()
