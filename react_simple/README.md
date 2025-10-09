# ReAct Simple Agent

A simple educational example of a ReAct (Reasoning + Acting) agent that can look up city information.

**Paper**: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

## Overview

This agent demonstrates the ReAct pattern where an LLM reasons about what actions to take, executes tools, observes results, and continues until it has enough information to answer the user's question.

## Features

The agent has access to three tools:

1. **geocode[city_name]**: Look up latitude/longitude coordinates for a city using the Open-Meteo geocoding API
2. **weather[latitude,longitude]**: Get current weather information using the weather.gov API
3. **time[timezone]**: Get the current time for a specific timezone

## How It Works

1. User asks a question about a city
2. The LLM receives a ReAct prompt with the question
3. The LLM thinks about what to do and chooses an action
4. The agent parses the action and executes the appropriate tool
5. The observation (tool result) is fed back to the LLM
6. Steps 3-5 repeat until the LLM provides a "Final Answer"

## ReAct Pattern

The agent follows this format:
```
Thought: [reasoning about what to do next]
Action: [tool_name[parameters]]
Observation: [tool result]
... (repeat as needed)
Thought: I now know the final answer
Final Answer: [complete response]
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running with the llama3.2 model:
```bash
ollama pull llama3.2:latest
```

## Usage

Run the agent:
```bash
python app.py
```

Example questions:
- "What's the weather in Seattle?"
- "What time is it in Tokyo?"
- "Tell me about the weather in New York City"
- "What are the coordinates of London?"


