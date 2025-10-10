import ollama
import random
import re
import os

LLM='codellama:7b'

def generate_code_from_prompt(user_input, model=LLM):
    PROMPT = f"""
    You are a software engineer who is really good at writing Python code. Given a simple request, you can turn that into
    Python code, surrounded by three backticks. Make sure that the code is syntactically correct, well formatted and will execute.
    Whatever the user asks, that code will be executed so just give them the code.

    {user_input}
    """

    response = ollama.chat(
        model=model,
        messages=[
            {'role': 'user', 'content': PROMPT}
        ]
    )

    llm_response = response['message']['content']
    
    # Extract code from backticks
    if '```' in llm_response:
        parts = llm_response.split('```')
        code_content = parts[1].strip() if len(parts) > 1 else ""
        # Remove language identifier if present (e.g., "python" at the start)
        lines = code_content.split('\n')
        if lines and lines[0].strip().lower() in ['python', 'py']:
            code_content = '\n'.join(lines[1:])
        return code_content
    
    return None


def save_code_to_file(code_content, scripts_dir="scripts"):
    # Generate a very long random number for filename
    random_number = random.randint(10**15, 10**20 - 1)
    
    # Create scripts directory if it doesn't exist
    os.makedirs(scripts_dir, exist_ok=True)
    
    # Create filename with scripts directory
    filename = os.path.join(scripts_dir, f"{random_number}.py")
    
    # Write the code content to the new file
    with open(filename, 'w') as f:
        f.write(code_content)
    
    return filename


def execute_code_file(filename):
    try:
        exec(open(filename).read())
        return True, None
    except Exception as e:
        return False, str(e)


def process_prompt_to_code(user_input, model=LLM, scripts_dir="scripts"):
    result = {
        'code': None,
        'filename': None,
        'executed': False,
        'error': None
    }
    
    # Step 1: Generate code
    code = generate_code_from_prompt(user_input, model=model)
    result['code'] = code
    
    if code is None:
        result['error'] = "No code block found in LLM response"
        return result
    
    # Step 2: Save code to file
    filename = save_code_to_file(code, scripts_dir=scripts_dir)
    result['filename'] = filename
    
    # Step 3: Execute the code
    success, error = execute_code_file(filename)
    result['executed'] = success
    result['error'] = error
    
    return result


def main():
    # Get user input
    user_input = input("Enter your prompt: ")
    
    # Process the prompt through the full pipeline
    result = process_prompt_to_code(user_input)
    
    if result['code']:
        print(f"\nCreated file: {result['filename']}")
        print("Executing that file...")
        
        if not result['executed']:
            print(f"Error executing the file: {result['error']}")
    else:
        print(f"\n{result['error']}")


if __name__ == "__main__":
    main()
