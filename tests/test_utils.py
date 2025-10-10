"""Common utilities for testing agent examples."""
import ollama


def llm_judge(result, expected_criteria, model='qwen2.5:7b'):
    """Use LLM as a judge to validate if results meet criteria.
    
    Args:
        result: The actual result from the function
        expected_criteria: Description of what the result should contain
        model: The LLM model to use for judging (default: qwen2.5:7b)
        
    Returns:
        bool: True if LLM judges the result as valid
    """
    prompt = f"""You are a judge evaluating test results. 

Result to evaluate:
{result}

Expected criteria:
{expected_criteria}

Does the result meet the criteria? Respond with only "PASS" or "FAIL" followed by a brief explanation.
"""
    
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    judgment = response['message']['content'].strip()
    print(f"\nLLM Judge: {judgment}")
    
    return judgment.upper().startswith("PASS")

