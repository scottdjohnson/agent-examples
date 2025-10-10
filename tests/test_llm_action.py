"""Tests for llm_action module."""
import pytest
import os
from llm_action.app import process_prompt_to_code
from test_utils import llm_judge


def test_process_prompt_to_code(tmp_path):
    """Test the complete pipeline: prompt -> code generation -> save -> execute."""
    user_input = "Write a function that multiplies two numbers and print the result of 3 times 4"
    
    # Run the complete pipeline
    result = process_prompt_to_code(user_input, scripts_dir=str(tmp_path))
    
    # Define criteria for validation
    criteria = """
    The result should indicate a successful code generation and execution pipeline:
    - 'code' should contain valid Python code with a function definition
    - 'code' should be related to multiplying two numbers
    - 'filename' should be a valid file path ending in .py
    - 'executed' should be True (code ran successfully)
    - 'error' should be None (no errors occurred)
    - The code should be syntactically correct Python
    """
    
    # Basic assertions
    assert result is not None, "Result should not be None"
    assert isinstance(result, dict), "Result should be a dictionary"
    assert 'code' in result, "Result should have 'code' key"
    assert 'filename' in result, "Result should have 'filename' key"
    assert 'executed' in result, "Result should have 'executed' key"
    assert 'error' in result, "Result should have 'error' key"
    
    # Validate code was generated
    assert result['code'] is not None, "Code should be generated"
    assert isinstance(result['code'], str), "Code should be a string"
    assert len(result['code']) > 0, "Code should not be empty"
    
    # Validate file was created
    assert result['filename'] is not None, "Filename should be set"
    assert os.path.exists(result['filename']), f"File should exist: {result['filename']}"
    assert result['filename'].endswith('.py'), "Filename should end with .py"
    
    # Use LLM judge for semantic validation
    assert llm_judge(result, criteria), f"Pipeline validation failed. Result:\n{result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

