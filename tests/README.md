# Agent Examples Tests

Tests for agent example modules using LLM-as-a-Judge evaluation.

## Test Files

- **`test_prompt_example.py`**: Tests the basic prompt example
- **`test_utils.py`**: Common utilities including `llm_judge()` function

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running with required models:
```bash
ollama pull qwen2.5:7b
ollama pull codellama:7b
```

## Running Tests

Run all tests:
```bash
pytest -v
```

Run a specific test:
```bash
pytest test_prompt_example.py -v
```

## How It Works

Each test:
1. Calls the testable function with sample input
2. Defines expected criteria for valid output
3. Uses `llm_judge()` to evaluate if result meets criteria
4. LLM returns PASS/FAIL with explanation

This approach validates semantic correctness rather than exact matches.

