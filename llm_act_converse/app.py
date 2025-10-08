import ollama
import random
import re
import os
import sys
from io import StringIO

def remove_language_identifier(code_content):
    code_lines = code_content.split('\n')
    if code_lines and code_lines[0].strip().lower() in ['python', 'py']:
        return '\n'.join(code_lines[1:])
    return code_content

def extract_code_from_response(llm_response):
    if '```' not in llm_response:
        return None
    
    parts = llm_response.split('```')
    code_content = parts[1].strip() if len(parts) > 1 else ""
    
    # Remove language identifier if present (e.g., "python" at the start)
    code_content = remove_language_identifier(code_content)
    
    return code_content

def save_code_to_file(code_content):
    # Generate a very long random number for filename
    random_number = random.randint(10**15, 10**20 - 1)  # 16-20 digit number
    
    # Create scripts directory if it doesn't exist
    scripts_dir = "scripts"
    os.makedirs(scripts_dir, exist_ok=True)
    
    # Create filename with scripts directory
    filename = os.path.join(scripts_dir, f"{random_number}.py")
    
    # Write the code content to the new file
    with open(filename, 'w') as f:
        f.write(code_content)
    
    return filename

def execute_code_file(filename):
    # Capture stdout during execution
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    # Execute the file
    execution_error = None
    try:
        exec(open(filename).read())
    except Exception as e:
        execution_error = str(e)
    finally:
        # Restore stdout
        sys.stdout = old_stdout
    
    # Get the captured output
    output = captured_output.getvalue()
    
    return output, execution_error

def print_code_generation_response(llm_response):
    # Print the LLM response indented for clarity
    print("\n  [Code Generation Response:]")
    for line in llm_response.split('\n'):
        print(f"  {line}")

def main():
    # Initialize conversation history
    messages = []
    
    # System prompt (only set once at the beginning)
    system_prompt = """
    You are a software engineer who is really good at writing Python code and nothing else. Given a simple request, you can turn that into
    Python code, surrounded by three backticks. Whatever the user asks, that code will be executed so just give them the code.
    Always make sure to generate code, if the question cannot be answered with code then tell the user and let them clarify.
    Do not assume that you can just give them the answer. You will probably be wrong unless the answer is in Python. 
    Failing to generate code is failure at the task.
    """
    
    print("Welcome to the conversational LLM action app!")
    print("Enter your prompts and I'll generate and execute code for you.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        # Skip empty inputs
        if not user_input:
            continue
        
        # Add user message to conversation history
        messages.append({'role': 'user', 'content': user_input})
        
        # Prepend system prompt to the first message for context
        if len(messages) == 1:
            messages[0]['content'] = system_prompt + "\n\n" + user_input
        
        # Send to Ollama (using codellama:7b model)
        response = ollama.chat(
            model='codellama:7b',
            messages=messages
        )
        
        llm_response = response['message']['content']
        
        # Store the LLM's code generation response separately
        messages.append({'role': 'code_generation', 'content': llm_response})
        
        # Variable to store the final result that will be shown to the user
        execution_result = ""
        
        # Extract code from the LLM response
        code_content = extract_code_from_response(llm_response)
        
        if code_content is not None:
            # Save the code to a file
            filename = save_code_to_file(code_content)
            
            # Print the entire LLM response (indented for clarity)
            print_code_generation_response(llm_response)
            
            # Print the filename (indented)
            print(f"\n  [Created file: {filename}]")
            
            # Say we're executing the file (indented)
            print("  [Executing that file...]\n")
            
            # Execute the file and capture output
            output, execution_error = execute_code_file(filename)
            
            # Print the output to the user (NOT indented - this is the final result)
            print("Result:")
            if output:
                print(output)
                execution_result = f"Code Output:\n{output}"
            elif execution_error:
                print(f"Error executing the file: {execution_error}")
                execution_result = f"Error executing the file: {execution_error}"

        else:
            # If no backticks found, just print the response (indented)
            print_code_generation_response(llm_response)
            print("\n  [No code block found in the response.]")
            execution_result = "No code block found in the response."
        
        # Add the final result to conversation history as 'assistant'
        messages.append({'role': 'assistant', 'content': execution_result})
        
        print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()

