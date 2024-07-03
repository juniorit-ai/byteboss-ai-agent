# ByteBoss AI Agent User Manual

Welcome to the AI Agent User Manual. This document will guide you through the setup, usage, and key features of our AI coding assistant agent.

## Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Key Features](#key-features)
5. [File Structure](#file-structure)
6. [Troubleshooting](#troubleshooting)

## Introduction

The AI Agent is a powerful tool designed to assist developers in various coding tasks. It can analyze existing code, generate new code, update files, and provide shell commands when necessary. This agent is particularly useful for maintaining and expanding codebases, following TODO comments, and creating documentation.

## Setup

1. **Environment Setup**:
   - Ensure you have Python installed on your system.
   - Clone the repository containing the AI agent code.

2. **Dependencies**:
   - Install the required dependencies by running:
     ```sh
     pip install -r requirements.txt
     ```

3. **API Keys**:
   - Create a `.env` file in the `projects/your-project-folder` directory.
   - Add your API keys for the LLM providers you plan to use. For example:
     ```sh
     OPENAI_API_KEY=your_openai_api_key
     DEEPSEEK_API_KEY=your_deepseek_api_key
     ANTHROPIC_API_KEY=your_anthropic_api_key
     ```

4. **Configuration**:
   - Set the `LLM_PROVIDER` in the `projects/your-project-folder/user.conf.sh` file to choose between 'openai', 'anthropic', 'deepseek', or 'juniorit'.
   - Optionally, set `LOGS_DIR` to specify a directory for storing logs.

## Usage

1. **Projects Folder**:
   - `agent_self`: Update and develop the agent's own code.
   - `sample`: An empty sample project, which can be used as a template.

2. **Running the Agent**:
   - Execute the agent script under your project folder `projects/your-project-folder`:
     ```sh
     ./agent.sh
     ```

3. **Directory Structure**:
   - Place your reference code in the `projects/your-project-folder/references` directory.
   - The agent will generate or update code in the `projects/your-project-folder/src` directory.

4. **Ignoring Files**:
   - Create an `ignore-by-agent.txt` file in both `references` and `src` directories to specify files or patterns to be ignored by the agent.

5. **Prompts and TODOs**:
   - Add `.prompt.md` files in the `src` directory for specific instructions.
   - Use `TODO:` comments in your code files for tasks you want the agent to address.

6. **Web UI**:
   - To use the web interface, run:
     ```sh
     python webui.py
     ```
   - Access the UI through your web browser at the provided local URL (it is still in the development stage).

## Key Features

1. **Code Analysis**: The agent can analyze existing code in both reference and output directories.

2. **File Updates**: It can create new files or update existing ones based on instructions or TODO comments.

3. **Multiple LLM Support**: Supports various language models including OpenAI's GPT, Anthropic's Claude, DeepSeek, and JuniorIT.

4. **Image to Code Conversion**: Capable of interpreting images (PNG, JPG) and generating corresponding code.

5. **Shell Command Generation**: Can suggest and execute shell commands for setup and running the code.

6. **Error Handling**: Provides suggestions for fixing errors encountered during execution.

7. **Web Interface**: Offers a user-friendly web UI for easier interaction with the agent.

## File Structure Under `byteboss_agent`

- `main.py`: The entry point of the application.
- `agent.py`: Contains the core logic for the AI agent.
- `executor.py`: Handles file updates and command execution.
- `user.py`: Manages user interactions and confirmations.
- `llm_interface.py`: Defines the interface for language model interactions.
- `llm_openai.py` and `llm_anthropic.py`: Implement specific LLM providers.
- `webui.py`: Provides a web-based user interface.

## Troubleshooting

1. **API Key Issues**:
   - Ensure your API keys are correctly set in the `.env` file.
   - Check if you have sufficient credits or permissions for the chosen LLM provider.

2. **Dependency Errors**:
   - Make sure all required packages are installed using the provided pip command.
   - Check for any version conflicts and update packages if necessary.

3. **LLM Provider Errors**:
   - If encountering issues with a specific provider, try switching to an alternative in the `.env` file.

4. **Logging**:
   - Check the logs in the specified `LOGS_DIR` for detailed information on each run.

For further assistance or to report issues, please contact the development team or raise an issue in the project's repository.