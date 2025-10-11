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
Action: [tool_name[parameters]]

Do NOT add an observation at this point, it will be provided later.
If the user wants to continue, they will provide an the result of the action, you should form this as an observation:

Observation: [tool result will be provided]

In this case, continue again with a another thought and another action:

Thought: [I need to use another tool]
Action: [tool_name[parameters]]

This process continues until the final thought determines that the answer has been found, then return it to the user:

Thought: [Answer to the original question]
Action: Final[Answer to the original question]

Note that the above pattern may occur only once or multiple times. 
Do not create more than one thought at a time.

Begin!

User Question: {question}
"""

