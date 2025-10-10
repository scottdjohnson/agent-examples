"""Tests for prompt_example module."""
import pytest
from prompt_example.app import get_llm_response
from test_utils import llm_judge


def test_get_llm_response():
    """Test that get_llm_response returns a valid response from the LLM."""
    user_input = "Write a Python function that adds two numbers"
    
    # Call the function
    result = get_llm_response(user_input)
    
    # Define criteria
    criteria = """
    - Should be a non-empty string
    - Should contain Python-related content (like 'def', 'function', or code)
    - Should be relevant to the request about adding two numbers
    - Should be at least 20 characters long
    """
    
    # Validate with LLM judge
    assert isinstance(result, str), f"Result should be a string, got {type(result)}"
    assert len(result) > 0, "Result should not be empty"
    assert llm_judge(result, criteria), f"LLM response validation failed. Result:\n{result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

