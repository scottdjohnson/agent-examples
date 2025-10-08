import ollama
import random
import re
import os

def main():
    # Get user input
    user_input = input("Enter your prompt: ")

    # Create the system prompt with user input included
    PROMPT = f"""
    You are a software engineer who is really good at writing Python code. Given a simple request, you can turn that into
    Python code, surrounded by three backticks. Whatever the user asks, that code will be executed so just give them the code.

    {user_input}
    """

    # Send to Ollama (using codellama:7b model)
    response = ollama.chat(
        model='codellama:7b',
        messages=[
            {'role': 'user', 'content': PROMPT}
        ]
    )

    llm_response = response['message']['content']

    # Find the first set of three backticks and extract content
    if '```' in llm_response:
        parts = llm_response.split('```')
        code_content = parts[1].strip() if len(parts) > 1 else ""

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

        # Print the entire LLM response
        print("\nFull LLM Response:")
        print(llm_response)

        # Print the filename
        print(f"\nCreated file: {filename}")

        # Say we're executing the file
        print("Executing that file...")

        # Execute the file
        try:
            exec(open(filename).read())
        except Exception as e:
            print(f"Error executing the file: {e}")

    else:
        # If no backticks found, just print the response
        print("\nFull LLM Response:")
        print(llm_response)
        print("\nNo code block found in the response.")

if __name__ == "__main__":
    main()
