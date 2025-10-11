# ReAct Simple Agent

A simple educational example of a ReAct (Reasoning + Acting) agent that can look up city information.

**Paper**: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

## Overview

This agent demonstrates the ReAct pattern where an LLM reasons about what actions to take, executes tools, observes results, and continues until it has enough information to answer the user's question.

## Features

The agent has access to three tools:

1. **geocode(city_name)**: Look up latitude/longitude coordinates for a city using Open-Meteo Geocoding API
   ```bash
   python -c "from tools import geocode; print(geocode('Seattle'))"
   ```

2. **weather(latitude,longitude)**: Get current weather information using weather.gov API
   ```bash
   python -c "from tools import weather; print(weather('47.6062,-122.3321'))"
   ```

3. **time(timezone)**: Get the current time for a specific timezone
   ```bash
   python -c "from tools import time; print(time('America/New_York'))"
   ```


## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running with the qwen2.5:7b:
```bash
ollama pull qwen2.5:7b
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


