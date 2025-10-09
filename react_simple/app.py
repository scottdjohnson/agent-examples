import ollama
import re
from tools import execute_tool

# ReAct prompt template
REACT_PROMPT = """You are an assistant that can look up city information using tools.

You have access to these tools:
- geocode[city_name]: Get latitude/longitude for a city
- weather[latitude,longitude]: Get weather information for coordinates
- time[timezone]: Get current time for a timezone (e.g., America/New_York)

Given a user question, begin with this format:

User Question: [user question]

Respond with the following format with a thought and an action:

Thought: [your reasoning about what to do next to]
Action: [tool_name(parameters)]

Do NOT add an observation at this point, it will be provided later.
If the user wants to continue, they will provide an the result of the action, you should form this as an observation:

Observation: [tool result will be provided]

In this case, continue again with a another thought and another action:

Thought: [I need to use another tool]
Action: [tool_name(parameters)]

This process continues until the final thought determines that the answer has been found, then return it to the user:

Thought: [Answer to the original question]
Action: Final(Answer to the original question)

Note that the above pattern may occur only once or multiple times. 
Do not create more than one thought at a time.

Example:
User Question: What is the weather in Paris?
Thought: I need to find the coordinates of Paris first.
Action: geocode(Paris)

Observation: {{'latitude': 48.85341, 'longitude': 2.3488, 'name': 'Paris', 'country': 'France', 'timezone': 'Europe/Paris'}}

Thought: Now I have the coordinates, I can get the weather information.
Action: weather(48.85341,2.3488)

Observation: {{'period': 'Today', 'temperature': 65, 'temperatureUnit': 'F', 'shortForecast': 'Partly Cloudy'}}

Thought: I now have all the information to answer the question.
Action: Final(The weather in Paris today is partly cloudy with a temperature of 65°F.)

Begin!

User Question: {question}
"""


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
    prompt = REACT_PROMPT.format(question=question)
    conversation = prompt
    
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
        
        # Parse and execute action
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

