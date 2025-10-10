import ollama
import random
import os
import sys
from io import StringIO

LLM='codellama:7b'

def save_and_execute_code(code_content, scripts_dir="scripts"):
    # Save code to file
    random_number = random.randint(10**15, 10**20 - 1)
    os.makedirs(scripts_dir, exist_ok=True)
    filename = os.path.join(scripts_dir, f"{random_number}.py")
    with open(filename, 'w') as f:
        f.write(code_content)
    
    # Execute code and capture output
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    output = None
    error = None
    try:
        exec(open(filename).read())
        output = captured_output.getvalue()
    except Exception as e:
        error = str(e)
    finally:
        sys.stdout = old_stdout
    
    # Determine execution result message
    if output:
        execution_result = f"Code Output:\n{output}"
    elif error:
        execution_result = f"Error executing the file: {error}"
    else:
        execution_result = "Code executed successfully (no output)"
    
    return {
        'filename': filename,
        'output': output,
        'error': error,
        'execution_result': execution_result
    }


def process_conversation_turn(user_input, messages, model=LLM, scripts_dir="scripts"):
    system_prompt = """
    You are a software engineer who is really good at writing Python code and nothing else. Given a simple request, you can turn that into
    Python code, surrounded by three backticks. Whatever the user asks, that code will be executed so just give them the code.
    Always make sure to generate code, if the question cannot be answered with code then tell the user and let them clarify.
    Do not assume that you can just give them the answer. You will probably be wrong unless the answer is in Python. 
    Failing to generate code is failure at the task.
    """
    
    # Add user message to conversation history
    messages.append({'role': 'user', 'content': user_input})
    
    # Prepend system prompt to the first message for context
    if len(messages) == 1:
        messages[0]['content'] = system_prompt + "\n\n" + user_input
    
    # Send to Ollama
    response = ollama.chat(
        model=model,
        messages=messages
    )
    
    llm_response = response['message']['content']
    messages.append({'role': 'code_generation', 'content': llm_response})
    
    # Extract code from backticks
    code_content = None
    if '```' in llm_response:
        parts = llm_response.split('```')
        code_content = parts[1].strip() if len(parts) > 1 else ""
        # Remove language identifier if present
        lines = code_content.split('\n')
        if lines and lines[0].strip().lower() in ['python', 'py']:
            code_content = '\n'.join(lines[1:])
    
    result = {
        'code': code_content,
        'filename': None,
        'output': None,
        'error': None,
        'llm_response': llm_response
    }
    
    if code_content:
        exec_result = save_and_execute_code(code_content, scripts_dir)
        result['filename'] = exec_result['filename']
        result['output'] = exec_result['output']
        result['error'] = exec_result['error']
        execution_result = exec_result['execution_result']
    else:
        execution_result = "No code block found in the response."
        result['error'] = execution_result
    
    messages.append({'role': 'assistant', 'content': execution_result})
    
    return result


def main():
    messages = []
    
    print("Welcome to the conversational LLM action app!")
    print("Enter your prompts and I'll generate and execute code for you.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Process the conversation turn
        result = process_conversation_turn(user_input, messages)
        
        # Display the result
        if result['code']:
            print(f"\n  [Code Generation Response:]")
            for line in result['llm_response'].split('\n'):
                print(f"  {line}")
            
            print(f"\n  [Created file: {result['filename']}]")
            print("  [Executing that file...]\n")
            
            print("Result:")
            if result['output']:
                print(result['output'])
            elif result['error']:
                print(f"Error: {result['error']}")
        else:
            print(f"\n  [Response:]")
            for line in result['llm_response'].split('\n'):
                print(f"  {line}")
            print(f"\n  [{result['error']}]")
        
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()
