import ollama
import re

# Handle both package import and direct execution
try:
    from .tools import execute_tool
    from .prompt import REACT_PROMPT
except ImportError:
    from tools import execute_tool
    from prompt import REACT_PROMPT


def parse_action(text):
    """Parse action from LLM response:
    
        Action: tool_name[parameters] or Action: tool_name(parameters)
    """
    # Try square brackets first
    match = re.search(r'Action:\s*(\w+)\[(.*?)\]', text, re.IGNORECASE)
    if match:
        tool_name = match.group(1)
        parameters = match.group(2).strip()
        return tool_name, parameters
    
    # Try parentheses
    match = re.search(r'Action:\s*(\w+)\((.*?)\)', text, re.IGNORECASE)
    if match:
        tool_name = match.group(1)
        parameters = match.group(2).strip()
        return tool_name, parameters
    
    return None, None


def process_react_query(question, model='qwen2.5:7b', max_iterations=5):
    conversation = REACT_PROMPT.format(question=question)
    iterations = []
    
    for iteration in range(max_iterations):
        # Call LLM
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': conversation}]
        )
        
        llm_response = response['message']['content']
        tool_name, parameters = parse_action(llm_response)
        
        iteration_result = {
            'iteration': iteration + 1,
            'llm_response': llm_response,
            'tool_name': tool_name,
            'parameters': parameters,
            'tool_result': None
        }
        
        # Check if we have a Final action (end of loop)
        if tool_name == "Final":
            iterations.append(iteration_result)
            return {
                'answer': parameters,
                'iterations': iterations,
                'completed': True
            }
        
        elif tool_name:
            result = execute_tool(tool_name, parameters)
            iteration_result['tool_result'] = result
            conversation += f"\n{llm_response}\nObservation: {result}\n"
        else:
            conversation += f"\n{llm_response}\n"
        
        iterations.append(iteration_result)
    
    return {
        'answer': "Unable to complete the task within iteration limit.",
        'iterations': iterations,
        'completed': False
    }


def run_react_agent(question, max_iterations=5):
    print(f"\n{'='*60}\nQuestion: {question}\n{'='*60}\n")
    
    result = process_react_query(question, max_iterations=max_iterations)
    
    for iter_data in result['iterations']:
        print(f"--- Iteration {iter_data['iteration']} ---\n")
        print(f"LLM Response:\n********************\n{iter_data['llm_response']}\n********************\n")
        print(f"Tool name: {iter_data['tool_name']}, Parameters: {iter_data['parameters']}")
        
        if iter_data['tool_result']:
            print(f"Result: {iter_data['tool_result']}\n")
    
    if result['completed']:
        print(f"\n{'='*60}\nFINAL ANSWER: {result['answer']}\n{'='*60}\n")
    
    return result['answer']


def main():
    # Get user input
    user_question = input("Ask about a city (e.g., 'What's the weather in Seattle?'): ")
    
    # Run the ReAct agent
    run_react_agent(user_question)


if __name__ == "__main__":
    main()

