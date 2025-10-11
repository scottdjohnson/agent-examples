# Prompt Example App

A simple Python application that takes user input and sends it to Ollama for LLM processing.

## Prerequisites

- Python 3.x
- Ollama installed and running (see top-level README for setup)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure Ollama is running (see top-level README)

## Usage

Run the application:
```bash
python app.py
```

Enter your prompt when prompted, and the app will send it to Ollama and display the response.

## Changing Models

In `app.py`, you can change the model by modifying the `LLM` parameter. For example:
- `'llama3'`
- `'codellama'`
- `'mistral'`
- Any other model you have installed
