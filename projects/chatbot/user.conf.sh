export LLM_PROVIDER=deepseek  # 'deepseek', 'openai', 'anthropic', 'octoai'

export OPENAI_MODEL=gpt-4o-2024-05-13
export ANTHROPIC_MODEL=claude-3-5-sonnet-20240620
export DEEPSEEK_MODEL=deepseek-coder # 'deepseek-coder', 'deepseek-chat'
export OCTOAI_MODEL=meta-llama-3.1-70b-instruct # meta-llama-3.1-405b-instruct, meta-llama-3.1-70b-instruct

export DEEPSEEK_API_URL=https://api.deepseek.com
export OCTOAI_API_URL=https://text.octoai.run/v1

export CODE_PROMPTS_DIR=$(pwd)/prompts
export CODE_REFERENCES_DIR=$(pwd)/references
export CODE_OUTPUT_DIR=$(pwd)/src
export LOGS_DIR=$(pwd)/logs