import ollama
import re
from tools import execute_tool
from prompt import REACT_PROMPT


def parse_action(text):
    """Parse action from LLM response."""
    # Look for Action: tool_name(parameters)
    match = re.search(r'Action:\s*(\w+)\((.*?)\)', text, re.IGNORECASE)
    if match:
        tool_name = match.group(1)
        parameters = match.group(2).strip()
        return tool_name, parameters
    return None, None


def run_react_agent(question, max_iterations=5):
    """Run the ReAct agent with the given question."""
    conversation = REACT_PROMPT.format(question=question)
    
    print(f"\n{'='*60}\nQuestion: {question}\n{'='*60}\n")
    
    for iteration in range(max_iterations):
        print(f"--- Iteration {iteration + 1} ---\n")
        
        # Call LLM
        response = ollama.chat(
            model='qwen2.5:7b',
            messages=[{'role': 'user', 'content': conversation}]
        )
        
        llm_response = response['message']['content']
        print(f"LLM Response:\n********************\n{llm_response}\n********************\n")
        
        # Parse and execute Action: []
        tool_name, parameters = parse_action(llm_response)
        
        # Check if we have a Final action (end of loop)
        if tool_name == "Final":
            print(f"\n{'='*60}\nFINAL ANSWER: {parameters}\n{'='*60}\n")
            return parameters
        
        elif tool_name:
            result = execute_tool(tool_name, parameters)
            print(f"Result: {result}\n")
            
            # Add observation to conversation
            conversation += f"\n{llm_response}\nObservation: {result}\n"
        else:
            # No action found, add response and continue
            conversation += f"\n{llm_response}\n"
    
    return "Unable to complete the task within iteration limit."


def main():
    # Get user input
    user_question = input("Ask about a city (e.g., 'What's the weather in Seattle?'): ")
    
    # Run the ReAct agent
    run_react_agent(user_question)


if __name__ == "__main__":
    main()

