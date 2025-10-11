import ollama

LLM='codellama:7b'

def get_llm_response(user_input, model=LLM):
    """Send a prompt to the LLM and return the response.
    
    Args:
        user_input: The user's prompt text
        model: The Ollama model to use
        
    Returns:
        str: The LLM's response text
    """
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': user_input}]
    )
    return response['message']['content']


def main():
    # Get user input
    user_input = input("Enter your prompt: ")
    
    # Get LLM response
    response_text = get_llm_response(user_input)
    
    # Print the response
    print("\nResponse:")
    print(response_text)


if __name__ == "__main__":
    main()
