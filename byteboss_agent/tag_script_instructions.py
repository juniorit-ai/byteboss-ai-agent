TAG_SCRIPT_INSTRUCTIONS = """
We are introducing a new scripting language named "tag script," which leverages Large Language Models (LLMs) as compilers to generate code. Below are the guidelines for writing in tag script:

Each line of tag script begins with an '@' symbol, which denotes a tag. These tags serve as instructions for code generation. Here are the specific tags and their purposes:

1. @create: Creates a new code file with the specified name and language by file extension.
2. @update: Updates an existed code file with the specified file name.
3. @interface: Defines an interface with input and output requirements for other code file to import.
4. @user: Allows the user to execute shell commands or input data.
5. @call 'function or interface name': Invokes a specific function or interface method.
6. @input: Inputs data from variables or files for use in the LLM model or function.
7. @follow: Provides guidelines on how to use or create the code.
8. @output: Specifies the data output format.
9. @to: Saves the output to a variable or file.
10. @import: Imports or includes the necessary library or file. If the imported file does not exist, create it as the requirements.
11. @shell: Executes shell commands within the code.

Additional notes:

- Code Logic Initiation: Tags such as @create or @update serve as starting points for defining the code logic in the specified file. All subsequent tags are interpreted as instructions or actions to be performed within the context of the file created or updated by these commands.
- If a function or interface called does not exist, a new one should be created according to the specified input and output requirements.
- When importing a file, its content may need to be updated to meet the specific requirements.
- Various markdown code blocks may be used as guidelines for code creation; however, the final programming language should conform to the file extension.
"""