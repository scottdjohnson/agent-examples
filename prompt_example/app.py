import ollama

def main():
    # Get user input
    user_input = input("Enter your prompt: ")

    # Send to Ollama (using llama2 model - you can change this to any model you have installed)
    response = ollama.chat(
        model='codellama:7b',
        messages=[{'role': 'user', 'content': user_input}]
    )

    # Print the response
    print("\nResponse:")
    print(response['message']['content'])

if __name__ == "__main__":
    main()
